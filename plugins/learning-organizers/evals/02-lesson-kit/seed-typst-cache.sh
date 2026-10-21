#!/bin/bash
# Scaffold, identical in every case (test_suite.py checks). Runs as the operator,
# before the agent, with HOME = the run's sandbox home and cwd = the run's cwd.
# 1. The eval sandbox blocks packages.typst.org and starts from an empty home, so
#    organizer.py's renders cannot fetch cetz 0.5.2 and fletcher 0.5.8. Seed the
#    sandbox's own Typst package cache from the operator's copy, found where
#    organizer.py looks (cc-intelligent-ui's vendored packages) or in the
#    operator's Typst cache.
# 2. When the case has an inputs/ folder, copy its contents into cwd: the files
#    the user "already has" (they exist before the run, so `files` never lists them).
set -eu
case_dir=$(cd "$(dirname "$0")" && pwd)
real_home=$(eval echo "~$(id -un)")
dest="$HOME/Library/Caches/typst/packages"
seeded=""
for src in "$real_home"/.claude/plugins/cache/*/cc-intelligent-ui/*/render/packages \
           "$real_home/Library/Caches/typst/packages"; do
  if [ -d "$src/preview/cetz/0.5.2" ] && [ -d "$src/preview/fletcher/0.5.8" ]; then
    mkdir -p "$dest/preview"
    cp -R "$src/preview/." "$dest/preview/"
    seeded=1
    break
  fi
done
if [ -z "$seeded" ]; then
  echo "seed-typst-cache: no cetz 0.5.2 + fletcher 0.5.8 under $real_home (install cc-intelligent-ui, or render one organizer once with network)" >&2
  exit 1
fi
if [ -d "$case_dir/inputs" ]; then
  cp -R "$case_dir/inputs/." .
fi
