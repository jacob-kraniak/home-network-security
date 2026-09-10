# Phase 2 Live Baseline — 2026-08-29

> **Superseded for live facts** by [phase-2-checkpoint-2026-09-05.md](phase-2-checkpoint-2026-09-05.md) (16 GB RAM confirmed, CT memory split 6G/2G, Seagate USB).  
> **Keep this file** for the Wazuh disk-full outage + repair narrative only.

**Captured:** 2026-08-29 evening (EDT)  
**Purpose:** Return-to-project snapshot after Proxmox / Portainer / Wazuh troubleshooting.  
**Supersedes:** July 10 paper state (“Proxmox install pending”, “16GB RAM”).

RFC1918 addresses only. Credentials, tokens, MACs, and WAN IPs stay out of this file. Live IPAM remains NetBox.

---

## Availability scorecard (end of session)

| Plane | Where | State |
|-------|-------|-------|
| Proxmox VE 9.2.4 | Node `debian` | **Stable.** ~20d uptime at capture. All PVE units active. No QEMU VMs. |
| Portainer CE | CT 101 `docker` | **Healthy.** `portainer-ce:latest` Up ~2 weeks. API HTTP 200 on :9000 and :9443. No other stacks. |
| Wazuh 4.8.2 AIO | CT 100 `wazuh` | **Up after repair.** Manager + indexer + dashboard active. Discover ingesting `wazuh-alerts-*`. API `:55000` returns 401 unauthenticated (expected). UI API still flakes under RAM pressure. |

---

## Hypervisor

| Field | Live value |
|-------|------------|
| Hardware | Lenovo ThinkCentre M715q Tiny (10M3000PUS / S/N MJ067MNT) |
| CPU | AMD PRO A12-9800E R7, 4C+8G (4 CPU cores). SVM/HVM enabled. |
| RAM observed | **~7.2 GiB total** (`maxmem` 7214469120). Docs that say 16GB are wrong or a second DIMM is missing. |
| Boot | `legacy-bios`. Firmware M11KT53A (2021). |
| OS / PVE | Debian 13 (trixie), kernel `7.0.14-4-pve`, `pve-manager` 9.2.4 |
| Node name | `debian` (never renamed after install) |
| Mgmt NIC | `vmbr0` on physical `enp2s0f0`, prefix `192.168.0.0/24`, GW `192.168.0.1` |
| Host address | `192.168.0.176/24` |
| Root disk | KingSpec NVMe `NE-512 2280` — `/dev/nvme0n1p1` ext4 ~462G, ~11% used |
| Swap | ~7G on `nvme0n1p5` |
| Second disk | **SanDisk Z400 256GB not present in `lsblk`** |
| PVE storage | `local` directory (`/var/lib/vz`), ~10% used. `/etc/pve/storage.cfg` missing; `pvesm` still lists `local` active. Guest disks are loop-mounted raw files. |
| Firmware package | `pve-edk2-firmware: not correctly installed` — blocks UEFI VMs. LXC-only is fine. |
| Failed host unit | `geoclue.service` only (ignore). |

Linux user `jacobk` cannot run `qm`/`pct`/`pvesh`. Enumerate guests as **root**.

---

## Guests

### CT 100 — `wazuh`

- Status: running, `onboot: 1`, unprivileged Ubuntu, `nesting=1`
- Resources: 2 cores, **4096 MiB**, swap 1024, rootfs **81G** (resized +50G on 2026-08-29 from 32G)
- Address: `192.168.0.178/24` on `vmbr0`
- UI: `https://192.168.0.178` (`:443`)
- Indexer bound **localhost only** (`[::ffff:127.0.0.1]:9200`)
- Manager API `:55000`, agents `:1514`, enrollment `:1515`

**Outage (closed):**
- Indexer + manager dead since **2026-08-09 10:06 UTC** (same boot as the 20-day host uptime).
- Root cause: CT rootfs **100% full**. `/var/ossec/queue/vd_updater` was **21G**; `/var/ossec/queue/vd` **5.2G**. Vuln-feed write failed (`Failed writing received data to disk`).
- Indexer `Result: resources` (never started that boot). Manager `wazuh-control` exit 1. Stale `/var/ossec/var/start-script-lock`.
- Dashboard stayed up and looped `ECONNREFUSED 127.0.0.1:9200`.
- After resize, units started. Disk after recovery: **~9.5G used / 81G (13%)** — updater cache dropped.
- First UI error after login (`2001 Unexpected end of JSON input`) is the known corrupt `wazuh-registry.json` after disk-full. Deleting that file + dashboard restart restored Discover.

**Remaining Wazuh issues:**
- CT RAM: ~2.4G used / 4.0G, ~63Mi free, **swap ~552Mi**. Explains intermittent API.
- Unprivileged LXC cannot raise `nofile` to 458752 (`Operation not permitted`). Non-fatal; manager still runs.
- Discover noise: agent `000` rootcheck on `/dev/lxc/proc/*` (expected on unprivileged LXC).
- No agents enrolled besides the manager. No historical alerts from the 20-day gap (indexer data was ~4M before repair).
- Single-node: `wazuh-clusterd` / `maild` not running is normal.

### CT 101 — `docker`

- Status: running, `onboot: 1`, unprivileged Debian, `nesting=1,keyctl=1`, guest firewall on `net0`
- Resources: 4 cores, memory **limit 8192 MiB** (host only has ~7 GiB), swap 2048, rootfs **4G**
- Address: `192.168.0.200/24` on `vmbr0`
- Disk at capture: 3.9G, **1.4G used, 2.3G free (38%)**
- Docker: 1 image, 1 container — `portainer` created ~6 weeks earlier, Up ~2 weeks
- URLs: `https://192.168.0.200:9443`, `http://192.168.0.200:9000`

Do not pull Immich/Jellyfin/Paperless onto a 4G rootfs.

---

## Corrections vs July 10 docs

| July 10 claim | Live 2026-08-29 |
|---------------|-----------------|
| Proxmox install pending | Installed; PVE 9.2.4; guests onboot |
| 16GB RAM | ~8GB class / 7.2 GiB observed |
| SanDisk Z400 mounted for RAID1 | Not in `lsblk` |
| First services order AdGuard → VPN → Wazuh | Wazuh + Portainer already deployed; AdGuard/VPN not present |
| Dell OptiPlex 7060 as Proxmox host (README) | **M715q is the live hypervisor.** OptiPlex/BazzitePC is not this node. |
| Wazuh issue still `status:planning` | Deployed 4.8.2 AIO; recovered 2026-08-29 |

---

## Do not do on return (until decided)

- Do not treat empty `qm`/`pct` output as “no guests” unless running as root.
- Do not install a second Wazuh or Portainer.
- Do not give CT 100 more than 4G RAM without cutting CT 101’s 8G *limit* or adding a DIMM.
- Do not create UEFI VMs until `pve-edk2-firmware` is fixed (or stay on LXC).
- Do not enroll a pile of Wazuh agents while the CT is swapping.

---

## Next session order

1. Confirm units still `active` (host + both CTs). Re-check `df` on CT 100 (`vd_updater` can refill).
2. RAM decision: add SODIMM, or drop CT 101 memory limit to ~1G, or shrink indexer heap (`/etc/wazuh-indexer/jvm.options`) after reading current `-Xms/-Xmx`.
3. Recreate `/etc/pve/storage.cfg` if the UI storage view is broken.
4. Resize or replace CT 101 disk before any new Compose stack.
5. One Wazuh agent (PVE host or CT 101), then stop.
6. Sync NetBox: hypervisor + CT 100/101 + interfaces.
7. Rename node `debian` → something durable (optional; needs care on a live node).

Recommended small next deploy through Portainer remains **AdGuard** then **WireGuard/Tailscale**, not media.

---

## Related issues

- #10 Wazuh SIEM/XDR Deployment
- #23 Phase 2 Artifacts Map
- #28 NetBox on Proxmox (still planning; NetBox Cloud remains SoT)

*Baseline written 2026-08-29 from live CLI snapshots on node `debian`.*
