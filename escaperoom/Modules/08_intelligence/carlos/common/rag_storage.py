from __future__ import annotations

import atexit
import logging
import os
import shutil
import signal
import threading
from pathlib import Path
from typing import Optional

from common.env_utils import is_gcp
from common.gcs_utils import download_prefix, upload_directory

logger = logging.getLogger(__name__)

_syncer = None  # type: Optional["RagSyncer"]


def _ensure_writable(path: Path) -> None:
    """
    Best-effort: make sure the directory tree is writable by the current user.
    """
    try:
        if path.is_file():
            path.chmod(0o644)
            return
        for p in path.rglob("*"):
            if p.is_dir():
                p.chmod(0o755)
            else:
                p.chmod(0o644)
        path.chmod(0o755)
    except Exception:
        # Non-fatal; proceed even if chmod fails.
        pass


class RagSyncer:
    """
    Best-effort async uploader for RAG data to GCS.
    Triggered after writes; de-dupes concurrent uploads.
    """

    def __init__(self, bucket: str, prefix: str, local_path: Path) -> None:
        self.bucket = bucket
        self.prefix = prefix
        self.local_path = local_path
        self._lock = threading.Lock()
        self._inflight = False

    def trigger(self) -> None:
        if not self.bucket:
            return
        with self._lock:
            if self._inflight:
                return
            self._inflight = True

        def _run():
            try:
                upload_directory(self.bucket, self.prefix, str(self.local_path))
            except Exception as e:
                logger.warning("[rag] Async upload failed: %s", e)
            finally:
                with self._lock:
                    self._inflight = False

        threading.Thread(target=_run, daemon=True).start()

    def sync_now(self) -> None:
        try:
            upload_directory(self.bucket, self.prefix, str(self.local_path))
        except Exception as e:
            logger.warning("[rag] Sync failed: %s", e)


def _env_flag(name: str, default: Optional[str] = None) -> str:
    val = os.getenv(name)
    return val if val is not None else (default or "")


def prepare_rag_storage() -> Path:
    """
    Resolve and prepare the local directory used by Chroma.

    If RAG_STORAGE=gcs and bucket/prefix are provided, download the latest
    snapshot from GCS into the local directory (default: /tmp/chroma_db on GCP,
    ./chroma_db locally). Registers an atexit + SIGTERM handler to upload
    changes back to GCS on shutdown. Async uploads are triggered on writes.
    """
    global _syncer

    storage_mode = _env_flag("RAG_STORAGE", "local").lower()
    bucket = _env_flag("RAG_GCS_BUCKET")
    prefix = _env_flag("RAG_GCS_PREFIX", "chroma_db")

    default_local = "/tmp/chroma_db" if is_gcp() else "./chroma_db"
    requested_path = Path(_env_flag("RAG_LOCAL_PATH", default_local)).resolve()
    fallback_path = Path("/tmp/chroma_db")

    local_path = requested_path
    try:
        local_path.mkdir(parents=True, exist_ok=True)
        # Basic writability probe
        probe = local_path / ".rag_write_probe"
        probe.touch(exist_ok=True)
        probe.unlink(missing_ok=True)
    except Exception as e:
        logger.warning(
            "[rag] Local RAG path %s not writable (%s); falling back to %s",
            requested_path,
            e,
            fallback_path,
        )
        local_path = fallback_path
        local_path.mkdir(parents=True, exist_ok=True)
    _ensure_writable(local_path)

    if storage_mode != "gcs" or not bucket:
        if storage_mode == "gcs" and not bucket:
            logger.warning("[rag] RAG_STORAGE=gcs but RAG_GCS_BUCKET not set; falling back to local path %s", local_path)
        else:
            logger.info("[rag] Using local RAG storage at %s", local_path)
        _syncer = None
        logger.info("[rag] RAG writes will use %s", local_path)
        return local_path

    try:
        logger.info("[rag] Syncing RAG from GCS gs://%s/%s -> %s", bucket, prefix, local_path)
        # Start fresh to avoid stale files
        if local_path.exists():
            for child in local_path.iterdir():
                if child.is_file():
                    child.unlink()
                else:
                    shutil.rmtree(child)
        download_prefix(bucket, prefix, str(local_path))
        _ensure_writable(local_path)
    except Exception as e:
        logger.warning("[rag] Failed to download RAG from GCS (%s); continuing with local path %s", e, local_path)

    _syncer = RagSyncer(bucket=bucket, prefix=prefix, local_path=local_path)
    logger.info("[rag] RAG writes will use %s (syncing to gs://%s/%s)", local_path, bucket, prefix)

    def _sync():
        if _syncer:
            _syncer.sync_now()

    atexit.register(_sync)

    def _handle_signal(signum, frame):
        _sync()
        raise SystemExit(0)

    try:
        signal.signal(signal.SIGTERM, _handle_signal)
    except Exception:
        # Not fatal if we can't register (e.g., on some platforms)
        pass

    return local_path


def trigger_rag_sync() -> None:
    """
    Trigger an async upload if GCS sync is configured.
    """
    if _syncer:
        _syncer.trigger()


def sync_rag_now() -> None:
    """
    Force a synchronous upload if GCS sync is configured.
    """
    if _syncer:
        _syncer.sync_now()
