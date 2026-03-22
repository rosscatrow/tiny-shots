# Claude Instructions for tiny-shots

## Deployment

This site is live at **shots.catrow.net**, served via GitHub Pages from the `main` branch.

### After completing any task:

1. Commit and push your changes to the `claude/*` working branch
2. Merge those changes into `main` and push `main`:
   ```
   git checkout main
   git pull origin main
   git merge --no-ff <your-claude-branch> -m "Merge <branch-name> into main"
   git push -u origin main
   git checkout <your-claude-branch>
   ```
3. This triggers the GitHub Actions deployment to shots.catrow.net automatically.

**Always do this at the end of every session** so the live site reflects your work.
