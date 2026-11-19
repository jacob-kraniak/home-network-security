#!/usr/bin/env bash
# lab-status-push.sh — run lab-status-collect.py and POST its JSON to the
# Grok Bot "Lab status ingest" webhook. Runs on Proxmox debian (.176) as root.
# Approved 2026-10-16; drafted 2026-11-17 (feat/omada-wazuh-realtime).
#
# Secrets: /root/secrets/labwatch-push.env (root-owned, chmod 600). Jacob creates it:
#   LABWATCH_PUSH_URL='https://...'        # Lab status ingest webhook URL
#   LABWATCH_PUSH_KEY='...'                # its key/secret
#   # optional:
#   # LABWATCH_PUSH_AUTH_HEADER='Authorization'
#   # LABWATCH_PUSH_AUTH_SCHEME='Bearer'   # set '' to send the raw key
#
# Usage: lab-status-push.sh [--dry-run]
#   --dry-run  run the collector and validate the JSON, print size and target host; no POST.
# The key never goes on a command line or to stdout/stderr: curl reads the header from stdin.
set -euo pipefail
umask 077

ENV_FILE="${LABWATCH_PUSH_ENV:-/root/secrets/labwatch-push.env}"
COLLECT="${LAB_STATUS_COLLECT:-/usr/local/bin/lab-status-collect.py}"
OUT="${LAB_STATUS_OUT:-/var/lib/lab-watch/lab-status.json}"
DRY_RUN=0

case "${1-}" in
  --dry-run) DRY_RUN=1 ;;
  "") ;;
  *) echo "usage: $0 [--dry-run]" >&2; exit 2 ;;
esac

log() { printf '%s lab-status-push: %s\n' "$(date -Is)" "$*" >&2; }

# --- refuse unsafe secrets file -------------------------------------------
if [[ ! -f "$ENV_FILE" ]]; then
  log "missing $ENV_FILE"; exit 1
fi
mode="$(stat -c '%a' "$ENV_FILE")"
owner="$(stat -c '%U' "$ENV_FILE")"
if [[ "$mode" != "600" ]]; then
  log "refusing: $ENV_FILE is mode $mode, must be 600 (chmod 600 $ENV_FILE)"; exit 1
fi
if [[ "$owner" != "$(id -un)" ]]; then
  log "refusing: $ENV_FILE is owned by $owner, expected $(id -un)"; exit 1
fi

set +x
# shellcheck disable=SC1090
. "$ENV_FILE"
: "${LABWATCH_PUSH_URL:?LABWATCH_PUSH_URL not set in $ENV_FILE}"
: "${LABWATCH_PUSH_KEY:?LABWATCH_PUSH_KEY not set in $ENV_FILE}"
AUTH_HEADER="${LABWATCH_PUSH_AUTH_HEADER:-Authorization}"
AUTH_SCHEME="${LABWATCH_PUSH_AUTH_SCHEME-Bearer}"

case "$LABWATCH_PUSH_URL" in
  https://*) ;;
  *) log "refusing: LABWATCH_PUSH_URL must be https"; exit 1 ;;
esac
target_host="$(printf '%s' "$LABWATCH_PUSH_URL" | sed -E 's#^https://([^/:]+).*#\1#')"

# --- collect ---------------------------------------------------------------
"$COLLECT" >&2
if [[ ! -s "$OUT" ]]; then
  log "collector produced no $OUT"; exit 1
fi
python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); assert "collected_at" in d' "$OUT" \
  || { log "$OUT is not valid collector JSON"; exit 1; }
bytes="$(wc -c <"$OUT")"

if (( DRY_RUN )); then
  log "dry run: $OUT ok (${bytes} bytes); would POST to host ${target_host}; nothing sent"
  exit 0
fi

# --- push ------------------------------------------------------------------
if [[ -n "$AUTH_SCHEME" ]]; then
  auth_line="${AUTH_HEADER}: ${AUTH_SCHEME} ${LABWATCH_PUSH_KEY}"
else
  auth_line="${AUTH_HEADER}: ${LABWATCH_PUSH_KEY}"
fi

status="$(
  printf '%s\n' "$auth_line" | curl --silent --show-error \
    --max-time 30 --retry 3 --retry-delay 5 --retry-connrefused \
    --header @- \
    --header 'Content-Type: application/json' \
    --data-binary @"$OUT" \
    --output /dev/null --write-out '%{http_code}' \
    "$LABWATCH_PUSH_URL"
)" || { log "curl failed posting to ${target_host}"; exit 1; }
unset auth_line LABWATCH_PUSH_KEY

if [[ "$status" =~ ^2[0-9][0-9]$ ]]; then
  log "pushed ${bytes} bytes to ${target_host} (HTTP ${status})"
else
  log "push to ${target_host} returned HTTP ${status}"; exit 1
fi
