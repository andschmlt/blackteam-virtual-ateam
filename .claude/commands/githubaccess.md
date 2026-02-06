# GitHub Access Command

Add a user as a collaborator to a GitHub repository.

## Phase 0: RAG Context Loading

**Load repository registry from RAG.**

```python
from AS-Virtual_Team_System_v2.rag.rag_client import VTeamRAG
rag = VTeamRAG()
context = rag.query("github repository access collaborator", top_k=3)
```

---

## Usage
/githubaccess [REPO_URL] [USERNAME]

## Arguments
- **REPO_URL**: Full GitHub repository URL (e.g., https://github.com/ParadiseMediaOrg/BI-AI_Agents_REPO)
- **USERNAME**: GitHub username to add as collaborator

## Instructions
When this command is invoked:

1. Extract the owner/repo from the URL by removing "https://github.com/"
2. Run this command to add the user:
   ```bash
   gh api repos/{owner}/{repo}/collaborators/{username} -X PUT -f permission=push
   ```
3. If successful, inform the user and provide the invitation link:
   https://github.com/{owner}/{repo}/invitations

## Example
User: /githubaccess https://github.com/ParadiseMediaOrg/BI-AI_Agents_REPO johndoe

Action: Run `gh api repos/ParadiseMediaOrg/BI-AI_Agents_REPO/collaborators/johndoe -X PUT -f permission=push`

Response: "Done! **johndoe** has been added to ParadiseMediaOrg/BI-AI_Agents_REPO with write access. Invitation link: https://github.com/ParadiseMediaOrg/BI-AI_Agents_REPO/invitations"
