#!/usr/bin/env bash
# Build + deploy + verify + notify evemisslab.com in one gated step.
#   1. python build.py                 -> fresh dist/, English at root, /zh
#   2. npx wrangler pages deploy dist   -> pushes into the existing `evemisslab`
#      Pages project (NOT a Worker - see README/build.py for why)
#   3. smoke test                      -> confirms the live domain is
#      actually responding (/ and /zh/) before telling anyone it worked
#   4. scripts/notify_beacon.py        -> tells the Continuous Discovery
#      Beacon (beacon.evemiss.com) this build is real and live. Non-fatal if
#      it fails or BEACON_SUBMIT_TOKEN_EVEMISSLAB isn't set: this site's own
#      deploy must never depend on the Beacon being reachable.
set -euo pipefail

python build.py
npx wrangler pages deploy dist --project-name evemisslab

echo "== smoke test =="
for path in / /zh/; do
  code=$(curl -sL -o /dev/null -w '%{http_code}' "https://evemisslab.com$path")
  if [ "$code" -lt 200 ] || [ "$code" -ge 300 ]; then
    echo "FATAL: $path returned HTTP $code"
    exit 1
  fi
  echo "$path -> $code"
done

python scripts/notify_beacon.py || echo "[warn] Beacon notification failed - deploy itself succeeded, this is non-fatal"
