#!/usr/bin/env bash
# pve-ct-notes.sh: rewrite each LXC container's Proxmox Notes (description) as Markdown tables.
#
# Runs on a Proxmox VE 9.x host as root (nightly cron). It reads data and writes nothing
# except the CT description field.
#   - Finds nodes with `pvesh get /nodes` and CTs per node with `pvesh get /nodes/<n>/lxc`
#     (falls back to `pct list` if pvesh fails), so new CTs and new cluster nodes are covered.
#   - CTs on this node: inside data (OS, Wazuh, Docker/Podman) comes from `pct exec` with a timeout.
#     CTs on other cluster nodes: API data only, written with `pvesh set`.
#   - Everything from the line `<!-- manual -->` to the end of the old notes is kept verbatim.
#     Old notes with no generated header and no marker are moved below a new marker, not lost.
#
# Usage: pve-ct-notes.sh [--dry-run] [--ct <vmid>]... [--local-only]
# Docs:  docs/services/proxmox-ct-notes.md
set -euo pipefail
shopt -u patsub_replacement 2>/dev/null || true   # bash 5.2: keep "&" literal in ${v//x/y}

BACKUP_STORAGE="${BACKUP_STORAGE:-seagate-backup}"
EXEC_TIMEOUT="${EXEC_TIMEOUT:-20}"
MANUAL_MARKER='<!-- manual -->'
AUTO_TAG='<!-- pve-ct-notes:auto'
MAX_DESC_BYTES=8000   # PVE caps the description at 8 KiB

DRY_RUN=0
LOCAL_ONLY=0
ONLY_CTS=()

usage() { awk 'NR > 1 && /^#/ { sub(/^# ?/, ""); print; next } NR > 1 { exit }' "$0"; }
log()   { printf '%s %s\n' "$(date '+%F %T')" "$*" >&2; }

while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run)    DRY_RUN=1 ;;
    --local-only) LOCAL_ONLY=1 ;;
    --ct)         shift; [[ "${1:-}" =~ ^[0-9]+$ ]] || { echo "--ct needs a numeric vmid" >&2; exit 2; }; ONLY_CTS+=("$1") ;;
    -h|--help)    usage; exit 0 ;;
    *)            echo "unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
  shift
done

for bin in pvesh pct jq timeout; do
  command -v "$bin" >/dev/null 2>&1 || { echo "missing required command: $bin" >&2; exit 1; }
done
[ "$(id -u)" -eq 0 ] || { echo "run as root (pct/pvesh need it)" >&2; exit 1; }

LOCAL_NODE="$(hostname -s)"
NOW="$(date '+%F %H:%M %Z')"

# ---------- helpers ----------

want_ct() {   # is this vmid selected by --ct (or no filter)?
  [ ${#ONLY_CTS[@]} -eq 0 ] && return 0
  local c; for c in "${ONLY_CTS[@]}"; do [ "$c" = "$1" ] && return 0; done
  return 1
}

human_bytes() {   # bytes -> "1.5 GiB"
  awk -v b="${1:-0}" 'BEGIN{ split("B KiB MiB GiB TiB",u," "); i=1; while (b>=1024 && i<5){b/=1024;i++}
    if (i==1) printf "%d %s", b, u[i]; else printf "%.1f %s", b, u[i] }'
}

usage_cell() {    # used max -> "1.0 GiB / 4.0 GiB (25%)"
  local used="${1:-0}" max="${2:-0}"
  if [ "$max" -gt 0 ] 2>/dev/null; then
    printf '%s / %s (%d%%)' "$(human_bytes "$used")" "$(human_bytes "$max")" $(( used * 100 / max ))
  else
    printf '%s / none' "$(human_bytes "$used")"
  fi
}

human_uptime() {
  local s="${1:-0}"; [ "$s" -gt 0 ] 2>/dev/null || { printf -- '-'; return; }
  printf '%dd %dh %dm' $(( s/86400 )) $(( s%86400/3600 )) $(( s%3600/60 ))
}

cell() {   # make a value safe for one Markdown table cell
  local v="${1:-}"
  v="${v//$'\r'/}"; v="${v//$'\n'/ }"; v="${v//|/\\|}"
  v="${v//</&lt;}"; v="${v//>/&gt;}"
  printf '%s' "${v:--}"
}

ct_exec() {   # ct_exec <vmid> <cmd...>; stdout of the command, empty on failure/timeout
  local id="$1"; shift
  timeout -k 5 "$EXEC_TIMEOUT" pct exec "$id" -- "$@" </dev/null 2>/dev/null || true
}

# ---------- discovery ----------

list_nodes() {
  if [ "$LOCAL_ONLY" -eq 0 ] && out="$(pvesh get /nodes --output-format json 2>/dev/null)"; then
    jq -r '.[] | select(.status == "online") | .node' <<<"$out"
  else
    echo "$LOCAL_NODE"
  fi
}

list_cts() {   # list_cts <node> -> vmids
  local node="$1" out
  if out="$(pvesh get "/nodes/$node/lxc" --output-format json 2>/dev/null)"; then
    jq -r '.[].vmid' <<<"$out" | sort -n
  elif [ "$node" = "$LOCAL_NODE" ]; then
    pct list | awk 'NR>1 {print $1}'
  fi
}

declare -A LAST_BACKUP=()
NO_BACKUP_TEXT='none found'
load_backups() {   # newest vzdump per vmid on $BACKUP_STORAGE for <node>
  local node="$1" out
  LAST_BACKUP=(); NO_BACKUP_TEXT='none found'
  out="$(pvesh get "/nodes/$node/storage/$BACKUP_STORAGE/content" --content backup --output-format json 2>/dev/null)" || {
    NO_BACKUP_TEXT="n/a (storage not readable on $node)"
    log "node $node: storage $BACKUP_STORAGE not readable; backup column will say n/a"; return 0; }
  while IFS=$'\t' read -r vmid ctime; do
    [ -n "$vmid" ] && LAST_BACKUP[$vmid]="$(date -d "@$ctime" '+%F %H:%M')"
  done < <(jq -r 'group_by(.vmid)[] | max_by(.ctime) | "\(.vmid)\t\(.ctime)"' <<<"$out")
}

# ---------- per-CT data ----------

ct_ip() {   # from the guest interface API, then the config
  local node="$1" id="$2" cfg="$3" ips
  ips="$(pvesh get "/nodes/$node/lxc/$id/interfaces" --output-format json 2>/dev/null \
        | jq -r '[.[] | select(.name | test("^(lo|docker|br-|veth|cni|podman|virbr)") | not) | (.inet // empty) | sub("/.*"; "")] | join(", ")' 2>/dev/null || true)"
  if [ -z "$ips" ]; then
    ips="$(jq -r '[to_entries[] | select(.key | test("^net[0-9]+$")) | .value | capture("ip=(?<ip>[^,/]+)").ip] | join(", ")' <<<"$cfg" 2>/dev/null || true)"
  fi
  printf '%s' "$ips"
}

# shellcheck disable=SC2016  # ${Version} is a dpkg-query format, not a shell expansion
wazuh_info() {   # prints "<type>\t<version>"; type = agent|server|none
  local id="$1" info ver type
  info="$(ct_exec "$id" /var/ossec/bin/wazuh-control info)"
  ver="$(sed -n 's/^WAZUH_VERSION="\{0,1\}v\{0,1\}\([^"]*\)"\{0,1\}$/\1/p' <<<"$info")"
  type="$(sed -n 's/^WAZUH_TYPE="\{0,1\}\([^"]*\)"\{0,1\}$/\1/p' <<<"$info")"
  if [ -z "$ver" ]; then
    ver="$(ct_exec "$id" dpkg-query -W -f='${Version}' wazuh-manager)"; [ -n "$ver" ] && type=server
  fi
  if [ -z "$ver" ]; then
    ver="$(ct_exec "$id" dpkg-query -W -f='${Version}' wazuh-agent)"; [ -n "$ver" ] && type=agent
  fi
  [ -z "$ver" ] && type=none
  printf '%s\t%s' "${type:-agent}" "$ver"
}

container_rows() {   # Markdown rows for running docker/podman containers, with a heading
  local id="$1" engine out
  for engine in docker podman; do
    out="$(ct_exec "$id" sh -c "command -v $engine >/dev/null 2>&1 && $engine ps --format '{{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'")"
    [ -z "$out" ] && continue
    printf '\n#### Containers (%s, running)\n\n| Name | Image / version | Status | Ports |\n|------|-----------------|--------|-------|\n' "$engine"
    sort <<<"$out" | while IFS=$'\t' read -r name image status ports; do
      ports="${ports//, /<br>}"
      printf '| %s | %s | %s | %s |\n' "$(cell "$name")" "$(cell "$image")" "$(cell "$status")" "$(cell "$ports" | sed 's/&lt;br&gt;/<br>/g')"
    done
  done
}

render_notes() {   # render_notes <node> <vmid> <cfg-json> <status-json>
  local node="$1" id="$2" cfg="$3" st="$4"
  local status name ostype os ip local_ct=0 wz wtype wver agent_cell
  status="$(jq -r '.status // "unknown"' <<<"$st")"
  name="$(jq -r '.hostname // empty' <<<"$cfg")"; [ -z "$name" ] && name="$(jq -r '.name // empty' <<<"$st")"
  ostype="$(jq -r '.ostype // empty' <<<"$cfg")"
  [ "$node" = "$LOCAL_NODE" ] && local_ct=1

  os="$ostype (from config)"; agent_cell='n/a (stopped)'
  if [ "$status" = running ] && [ "$local_ct" -eq 1 ]; then
    local pretty
    # shellcheck disable=SC2016  # expands inside the CT, not here
    pretty="$(ct_exec "$id" sh -c '. /etc/os-release 2>/dev/null && echo "$PRETTY_NAME"')"
    [ -n "$pretty" ] && os="$pretty"
    wz="$(wazuh_info "$id")"; wtype="${wz%%$'\t'*}"; wver="${wz#*$'\t'}"
    case "$wtype" in
      none)   agent_cell='<missing agent>' ;;
      server) agent_cell='n/a (this CT is the Wazuh manager)' ;;
      *)      agent_cell="$wver" ;;
    esac
  elif [ "$status" = running ]; then
    agent_cell='n/a (CT on another node; run the script there)'
  fi
  ip="$(ct_ip "$node" "$id" "$cfg")"

  printf '%s generated %s by pve-ct-notes.sh; everything above the manual marker is rewritten nightly -->\n' "$AUTO_TAG" "$NOW"
  printf '### CT %s · %s\n\n' "$id" "$(cell "$name")"
  printf '| Field | Value |\n|-------|-------|\n'
  printf '| Status | %s |\n' "$(cell "$status")"
  printf '| Node | %s |\n' "$(cell "$node")"
  printf '| Hostname | %s |\n' "$(cell "$name")"
  printf '| IP | %s |\n' "$(cell "$ip")"
  printf '| OS | %s |\n' "$(cell "$os")"
  if [ "$status" = running ]; then
    printf '| RAM | %s |\n'  "$(usage_cell "$(jq -r '.mem // 0' <<<"$st")"  "$(jq -r '.maxmem // 0' <<<"$st")")"
    printf '| Swap | %s |\n' "$(usage_cell "$(jq -r '.swap // 0' <<<"$st")" "$(jq -r '.maxswap // 0' <<<"$st")")"
  else
    printf '| RAM | - / %s MiB (configured) |\n'  "$(jq -r '.memory // "?"' <<<"$cfg")"
    printf '| Swap | - / %s MiB (configured) |\n' "$(jq -r '.swap // "?"' <<<"$cfg")"
  fi
  printf '| Uptime | %s |\n' "$(human_uptime "$(jq -r '.uptime // 0' <<<"$st")")"
  printf '| Last backup (%s) | %s |\n' "$BACKUP_STORAGE" "$(cell "${LAST_BACKUP[$id]:-$NO_BACKUP_TEXT}")"
  printf '| Wazuh agent | %s |\n' "$(cell "$agent_cell")"
  if [ "${wtype:-}" = server ]; then
    printf '| Wazuh manager | %s |\n' "$(cell "$wver")"
  fi

  if [ "$status" = running ] && [ "$local_ct" -eq 1 ]; then
    container_rows "$id"
  fi
}

manual_section() {   # print the manual marker plus what follows it (or the old handwritten notes)
  local old="$1"
  if grep -qF -- "$MANUAL_MARKER" <<<"$old"; then
    awk -v m="$MANUAL_MARKER" 'found || index($0, m) { found=1; print }' <<<"$old"
  elif [ -n "$old" ] && ! grep -qF -- "$AUTO_TAG" <<<"$old"; then
    printf '%s\n%s\n' "$MANUAL_MARKER" "$old"   # first run: keep existing handwritten notes
  else
    printf '%s\n' "$MANUAL_MARKER"
  fi
}

# ---------- main ----------

rc=0; seen=0
mapfile -t NODES < <(list_nodes)
for node in "${NODES[@]}"; do
  [ -z "$node" ] && continue
  load_backups "$node"
  mapfile -t CTS < <(list_cts "$node")
  for id in "${CTS[@]}"; do
    [ -z "$id" ] && continue
    want_ct "$id" || continue
    seen=$((seen + 1))
    cfg="$(pvesh get "/nodes/$node/lxc/$id/config" --output-format json 2>/dev/null)" || { log "CT $id: cannot read config; skipped"; rc=1; continue; }
    st="$(pvesh get "/nodes/$node/lxc/$id/status/current" --output-format json 2>/dev/null)" || st='{}'
    old="$(jq -r '.description // ""' <<<"$cfg")"
    new="$(render_notes "$node" "$id" "$cfg" "$st")"$'\n\n'"$(manual_section "$old")"

    if [ "$(printf '%s' "$new" | wc -c)" -gt "$MAX_DESC_BYTES" ]; then
      log "CT $id: notes would be over $MAX_DESC_BYTES bytes; not written"; rc=1; continue
    fi

    if [ "$DRY_RUN" -eq 1 ]; then
      printf '===== CT %s on %s: new notes =====\n%s\n' "$id" "$node" "$new"
      printf '===== CT %s: diff (old -> new) =====\n' "$id"
      diff -u --label "CT $id current" --label "CT $id new" <(printf '%s\n' "$old") <(printf '%s\n' "$new") || true
      continue
    fi

    if [ "$node" = "$LOCAL_NODE" ]; then
      pct set "$id" --description "$new" >/dev/null || { log "CT $id: pct set failed (locked by a backup?)"; rc=1; continue; }
    else
      pvesh set "/nodes/$node/lxc/$id/config" --description "$new" >/dev/null || { log "CT $id on $node: pvesh set failed"; rc=1; continue; }
    fi
    log "CT $id on $node: notes updated"
  done
done

if [ ${#ONLY_CTS[@]} -gt 0 ] && [ "$seen" -eq 0 ]; then
  log "no matching CT found for --ct ${ONLY_CTS[*]}"; rc=1
fi
exit "$rc"
