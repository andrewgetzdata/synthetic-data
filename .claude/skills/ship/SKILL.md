---
name: ship
description: Stage, commit, push, and open a PR for the current work. Creates a branch if on main, pushes to existing branch if not, and creates or updates the PR.
argument-hint: [optional commit message]
user-invocable: true
---

Ship the current work: stage changes, commit, push, and ensure a PR exists.

## Procedure

### 1. Assess the current state

Run these in parallel:
- `git status` (no `-uall`) — check for staged/unstaged/untracked changes
- `git branch --show-current` — get current branch name
- `git log --oneline -5` — recent commit style reference
- `git diff --stat` — summary of changes

If there are no changes to ship, inform the user and stop.

### 2. Create a branch if needed

If the current branch is `main` or `master`:
1. Infer a branch name from the changes (use `feat/`, `fix/`, `refactor/`, etc. prefix per conventional commits)
2. Ask the user to confirm the branch name before creating it
3. `git checkout -b <branch-name>`

If already on a feature branch, continue on it.

### 3. Stage and commit

1. Review the diff (`git diff` and `git diff --cached`) to understand what changed
2. Stage relevant files by name — do NOT use `git add -A` or `git add .`
   - Skip files that look like secrets (`.env`, credentials, tokens)
   - If unsure about a file, ask the user
3. Write a conventional commit message (`feat:`, `fix:`, `refactor:`, etc.)
   - If the user provided a commit message argument, use that instead
   - Keep it concise (1-2 sentences), focus on the "why"
   - End with: `Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>`
4. Commit using a HEREDOC for the message

### 4. Push

1. Check if the branch has a remote tracking branch: `git rev-parse --abbrev-ref @{upstream} 2>/dev/null`
2. If no upstream: `git push -u origin <branch-name>`
3. If upstream exists: `git push`

### 5. Create or find PR

1. Check if a PR already exists for this branch: `gh pr view --json url,title 2>/dev/null`
2. If no PR exists:
   - Analyze all commits on the branch vs the base branch (`git log main..HEAD`)
   - Create a PR with `gh pr create`:
     - Title: short, under 70 chars
     - Body format:
       ```
       ## Summary
       <1-3 bullet points>

       ## Test plan
       - [ ] <testing steps>

       🤖 Generated with [Claude Code](https://claude.com/claude-code)
       ```
   - Use a HEREDOC for the body
3. If PR already exists, report the existing PR URL

### 6. Report

Print the PR URL so the user can review it.
