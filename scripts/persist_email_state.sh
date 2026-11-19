#!/usr/bin/env bash
set -euo pipefail
branch=blakeypoo-watchdog-state
mkdir -p "$RUNNER_TEMP/blakeypoo-email-state"
cd "$RUNNER_TEMP/blakeypoo-email-state"
git init -q
git config user.name 'BlakeyPoo Watchdog'
git config user.email '248803217+nashdarden5@users.noreply.github.com'
git remote add origin "https://x-access-token:${GITHUB_TOKEN}@github.com/${GITHUB_REPOSITORY}.git"
git fetch -q origin "$branch"
git checkout -q -b "$branch" FETCH_HEAD
cp "$GITHUB_WORKSPACE/watchdog-email-state.json" watchdog-email-state.json
git add watchdog-email-state.json
if ! git diff --cached --quiet; then git commit -qm 'Persist delivered auction alert keys'; git push -q origin HEAD:"$branch"; fi
