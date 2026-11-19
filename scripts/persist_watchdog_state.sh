#!/usr/bin/env bash
set -euo pipefail
branch=blakeypoo-watchdog-state
mkdir -p "$RUNNER_TEMP/blakeypoo-state"
cd "$RUNNER_TEMP/blakeypoo-state"
git init -q
git config user.name 'BlakeyPoo Watchdog'
git config user.email '248803217+nashdarden5@users.noreply.github.com'
git remote add origin "https://x-access-token:${GITHUB_TOKEN}@github.com/${GITHUB_REPOSITORY}.git"
if git fetch -q origin "$branch"; then git checkout -q -b "$branch" FETCH_HEAD; else git checkout -q --orphan "$branch"; fi
cp "$GITHUB_WORKSPACE/watchdog-state.json" watchdog-state.json
git add watchdog-state.json
if ! git diff --cached --quiet; then git commit -qm 'Persist auction observation history'; git push -q origin HEAD:"$branch"; fi
