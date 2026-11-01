# Proxmox CT Notes auto-updater

**Status:** drafted 2026-11-01. **Not run on the rack yet.** Jacob installs it on the PVE host himself.
**Script:** [`scripts/proxmox/pve-ct-notes.sh`](../../scripts/proxmox/pve-ct-notes.sh)
**Host:** PVE node `debian` `192.168.0.176` (Proxmox VE 9.2)
**Related:** [Services index](README.md) · [Wazuh Omada syslog](wazuh-omada-syslog.md)

A nightly cron job rewrites each LXC container's **Notes** (the `description` field shown on the CT's Summary page) as Markdown tables. A handwritten section below a `<!-- manual -->` marker is kept as is.

---

## What it writes

Each CT gets one key/value table:

| Row | Source |
|-----|--------|
| Status, Node | `pvesh get /nodes/<node>/lxc/<id>/status/current` |
| Hostname | CT config `hostname` |
| IP | `pvesh get /nodes/<node>/lxc/<id>/interfaces`. Skips `lo`, `docker*`, `br-*`, `veth*`, `cni*`, `podman*`, and `virbr*`. Falls back to `ip=` in the `netN` config lines. |
| OS | `PRETTY_NAME` from `/etc/os-release` inside the CT. Falls back to the config `ostype` when the CT is stopped. |
| RAM, Swap | used / max (percent) from `status/current`. A stopped CT shows the configured sizes. |
| Uptime | `status/current` |
| Last backup (seagate-backup) | Newest vzdump per vmid from `pvesh get /nodes/<node>/storage/seagate-backup/content --content backup` |
| Wazuh agent | Version from `pct exec <id> -- /var/ossec/bin/wazuh-control info`. Falls back to `dpkg-query` for `wazuh-agent`. Shows `<missing agent>` when neither is found. |
| Wazuh manager | Only on the manager CT (CT 100): version from `wazuh-control info` (`WAZUH_TYPE="server"`), or `dpkg-query wazuh-manager` |

A running CT that has `docker` or `podman` also gets a **Containers** table with one row per running container: name, image or version, status, and ports. The data comes from `docker ps --format` or `podman ps --format`.

## Behavior

- **Discovery:** the script lists nodes with `pvesh get /nodes` (online nodes only) and CTs with `pvesh get /nodes/<node>/lxc`. If `pvesh` fails, it falls back to `pct list`. New CTs, and new nodes if a cluster forms, are picked up on the next run without any change to the script.
- **Writes:** the only write is the description field. On this node it uses `pct set <id> --description`. For a CT on another cluster node it uses `pvesh set /nodes/<node>/lxc/<id>/config --description`.
- **Inside the CT:** the script only runs read commands through `pct exec`: `cat /etc/os-release`, `wazuh-control info`, `dpkg-query`, and `docker ps` or `podman ps`. Each call has a timeout (`EXEC_TIMEOUT`, default 20 s).
- **Stopped CTs:** shown as `stopped`, filled from config only, with no `pct exec`.
- **CTs on other nodes:** `pct exec` only works on the local node, so these get API data only, and the Wazuh column says to run the script on that node. See [Cluster](#cluster-later).
- **Manual section:** everything from the line `<!-- manual -->` to the end of the old notes is kept verbatim (trailing blank lines are trimmed). On the first run, existing notes with no marker and no generated header move below a new marker, so nothing is lost.
- **Size limit:** PVE caps the description at 8 KiB. If new notes would go over 8000 bytes, that CT is skipped and an error is logged.
- **Exit code:** non-zero if any CT failed, for example `pct set` on a CT locked by a running backup. The other CTs are still updated.

Options: `--dry-run` prints the new notes and a `diff -u` against the current notes without writing. `--ct <vmid>` limits the run to one CT and can be repeated. `--local-only` skips other nodes. Environment overrides: `BACKUP_STORAGE` (default `seagate-backup`) and `EXEC_TIMEOUT`.

`<missing agent>` is written as `&lt;missing agent&gt;` so the Markdown renderer shows it instead of dropping it as an HTML tag.

---

## Install (on the PVE host, as root, by Jacob)

```bash
# 0. Requirement: jq. Check first; install only if it's missing.
command -v jq || apt install jq

# 1. Save the current notes so you can roll back.
mkdir -p /root/ct-notes-backup
for id in $(pct list | awk 'NR>1 {print $1}'); do
  pvesh get /nodes/$(hostname -s)/lxc/$id/config --output-format json | jq -r '.description // ""' > /root/ct-notes-backup/$id.md
done

# 2. Copy the script from this repo (scripts/proxmox/pve-ct-notes.sh).
install -o root -g root -m 0755 pve-ct-notes.sh /usr/local/sbin/pve-ct-notes.sh

# 3. Dry run: writes nothing. Check the tables and the diff.
/usr/local/sbin/pve-ct-notes.sh --dry-run --ct 101 | less
/usr/local/sbin/pve-ct-notes.sh --dry-run | less

# 4. One real run on one CT, then look at its Summary > Notes in the PVE UI.
/usr/local/sbin/pve-ct-notes.sh --ct 101

# 5. Nightly cron at 03:15.
cat > /etc/cron.d/pve-ct-notes <<'CRON'
# Rewrite LXC Notes nightly. See home-network-security docs/services/proxmox-ct-notes.md
15 3 * * * root /usr/local/sbin/pve-ct-notes.sh >> /var/log/pve-ct-notes.log 2>&1
CRON
```

**Cron timing:**

- 03:15 stays clear of the Sunday 04:00 NetBox restart, so Sunday notes don't catch the NetBox containers mid-restart.
- Also check the vzdump schedule (Datacenter → Backup). If a backup to `seagate-backup` is running on a CT at 03:15, that CT is locked and `pct set` fails for it until the next night. If that happens, move the cron line to a time outside the backup window.

---

## Sample output (EXAMPLE data, not real output)

The sample below comes from a `--dry-run` against **mocked** `pvesh` and `pct` commands, on a test machine, not the rack. The mock is based on the known setup: CT 100 Wazuh at `192.168.0.178`, CT 101 Portainer at `192.168.0.200` running Pi-hole, the Omada controller, the 5-container NetBox stack, RustDesk `hbbs` and `hbbr`, and Portainer.

**Invented values:** the OS strings, versions, image tags, RAM, uptime, backup dates, and ports. CT 100's manager version will be whatever 4.14.x it is running after today's upgrade.

### CT 100 (Wazuh manager)

```markdown
<!-- pve-ct-notes:auto generated 2026-11-02 03:15 EST by pve-ct-notes.sh; everything above the manual marker is rewritten nightly -->
### CT 100 · wazuh

| Field | Value |
|-------|-------|
| Status | running |
| Node | debian |
| Hostname | wazuh |
| IP | 192.168.0.178 |
| OS | Ubuntu 22.04.5 LTS |
| RAM | 5.2 GiB / 8.0 GiB (64%) |
| Swap | 100.0 MiB / 512.0 MiB (19%) |
| Uptime | 3d 5h 16m |
| Last backup (seagate-backup) | 2026-11-01 02:00 |
| Wazuh agent | n/a (this CT is the Wazuh manager) |
| Wazuh manager | 4.14.0 |

<!-- manual -->
```

### CT 101 (Docker host, with an existing handwritten note moved below the marker)

```markdown
<!-- pve-ct-notes:auto generated 2026-11-02 03:15 EST by pve-ct-notes.sh; everything above the manual marker is rewritten nightly -->
### CT 101 · portainer

| Field | Value |
|-------|-------|
| Status | running |
| Node | debian |
| Hostname | portainer |
| IP | 192.168.0.200 |
| OS | Debian GNU/Linux 12 (bookworm) |
| RAM | 2.8 GiB / 6.0 GiB (46%) |
| Swap | 0 B / 512.0 MiB (0%) |
| Uptime | 14d 1h 2m |
| Last backup (seagate-backup) | 2026-11-01 03:00 |
| Wazuh agent | &lt;missing agent&gt; |

#### Containers (docker, running)

| Name | Image / version | Status | Ports |
|------|-----------------|--------|-------|
| hbbr | rustdesk/rustdesk-server:1.1.14 | Up 2 weeks | - |
| hbbs | rustdesk/rustdesk-server:1.1.14 | Up 2 weeks | - |
| netbox | netboxcommunity/netbox:v4.4 | Up 2 days (healthy) | 0.0.0.0:8000-&gt;8080/tcp |
| netbox-housekeeping | netboxcommunity/netbox:v4.4 | Up 2 days | - |
| netbox-postgres | postgres:17-alpine | Up 2 days | 5432/tcp |
| netbox-redis | valkey/valkey:8.1-alpine | Up 2 days | 6379/tcp |
| netbox-worker | netboxcommunity/netbox:v4.4 | Up 2 days | - |
| omada-controller | mbentley/omada-controller:6.3 | Up 2 weeks | - |
| pihole | pihole/pihole:2025.08.0 | Up 2 weeks (healthy) | 0.0.0.0:53-&gt;53/tcp<br>0.0.0.0:53-&gt;53/udp<br>0.0.0.0:8081-&gt;80/tcp |
| portainer | portainer/portainer-ce:2.33.1 | Up 2 weeks | 0.0.0.0:9443-&gt;9443/tcp |

<!-- manual -->
Handwritten: CT101 hosts the Docker stacks.
NetBox restarts Sundays 04:00 via cron.
```

---

## Cluster (later)

If a second node joins, pick one setup:

- **Recommended:** install the script and cron line on **each** node and add `--local-only`. Every CT then gets full data (OS, Wazuh, containers) from its own node.
- **Simpler:** install it on **one** node without `--local-only`. CTs on other nodes then get API data only, written with `pvesh set`.

Don't mix the two setups. If you do, a node running without `--local-only` overwrites the other nodes' full notes with API-only notes.

## Rollback

```bash
rm /etc/cron.d/pve-ct-notes /usr/local/sbin/pve-ct-notes.sh
# Optional: put back the notes saved in install step 1
for f in /root/ct-notes-backup/*.md; do id=$(basename "$f" .md); pct set "$id" --description "$(cat "$f")"; done
```

Removing the cron job leaves each CT's last generated notes in place. They just stop updating.

## Caveats

- QEMU VMs are not covered, only LXC CTs.
- The notes show container names, images, and published ports. Anyone with read access to the CT in the PVE UI can see them.
- Docker inside an unprivileged CT needs the usual nesting setup. If `docker ps` fails or times out, the Containers table is left out for that run.
