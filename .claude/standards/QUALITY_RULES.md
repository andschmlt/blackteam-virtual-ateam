
## Rule R50: Attachment Verification (P0)

**ALWAYS verify attachments are uploaded when requested:**
- ClickUp: GET task after upload, verify `attachments` array is not empty
- Email: Confirm file exists + size before marking sent
- Any system: Verify upload response before confirming

**Checklist:**
- [ ] File exists
- [ ] File not empty
- [ ] Upload HTTP 200
- [ ] Attachment visible in target system

**If verification fails:** STOP, REPORT, RETRY, ESCALATE

See: `/home/andre/AS-Virtual_Team_System_v2/whiteteam/rules/R50_ATTACHMENT_VERIFICATION.md`

