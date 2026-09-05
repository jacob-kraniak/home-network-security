# Phase 2 Checkpoint — 2026-09-05

**Captured:** 2026-09-05 afternoon (EDT)  
**Supersedes for live facts:** [phase-2-baseline-2026-08-29.md](phase-2-baseline-2026-08-29.md) (keep that file for the Wazuh outage narrative).

RFC1918 only. No credentials. Media folder names exist on the USB disk; this file does not inventory titles.

---

## Scorecard

| Plane | State |
|-------|-------|
| PVE 9.2.4 node `debian` | Stable after a reboot ~16:02. Load fell from ~1.0–1.8 (swap pressure) to ~0.3. |
| Host RAM | **2×8 GB DDR4 SO-DIMM physically confirmed.** `top` / PVE UI: **14932 MiB (~14.6 GiB)** total, ~10 GiB available after boot. Aug 29 `maxmem` ~7.2 GiB was the kernel seeing one stick only; reboot made the second stick visible. |
| CT 100 `wazuh` | `memory: 6144` `swap: 1024`. `free` inside CT: 6.0G total, ~2.4G used, ~3.6G available. |
| CT 101 `portainer` (was hostname `docker`) | `memory: 2048` `swap: 512`. Disk still **4G** — do not pull media stacks yet. |
| Wazuh agents | Manager `000`; HV agent `pve-debian` **003** enrolled 2026-08-29 and shipping alerts. CT 101 agent not required for this checkpoint. |
| External disk | Seagate Backup+ Desk **3.00 TB / 2.73 TiB** on USB as `/dev/sda`, mounted, visible in PVE Disks. |

---

## Memory map (applied)

| Consumer | Limit |
|----------|-------|
| Host / PVE | leftover ~2 GiB+ (not a CT) |
| CT 100 Wazuh | **6 GiB** |
| CT 101 Portainer | **2 GiB** |
| Unassigned | ~6 GiB of the 14.6 GiB host |

No DIMM purchase needed for Wazuh + Portainer + a small next app.

---

## Seagate Backup+ Desk

| Field | Value |
|-------|-------|
| Model | Seagate Backup+ Desk (`idVendor=0bc2`, `idProduct=a0a4`) |
| Serial | NA5KMDT1 |
| Bus | USB `2-4.2` **high-speed (USB 2)**, UAS. Not SuperSpeed. |
| Node | `/dev/sda` GPT |
| `sda1` | ~200M EFI System Partition (empty FSTYPE in lsblk) — leave it |
| `sda2` | 2.7T **exFAT** label `Seagate 3TB` UUID `531C-AD38` |
| Mount | `/mnt/seagate3tb` |
| Capacity at mount | 2.8T size, **376G used**, 2.4T avail (14%) |
| Content | Existing media library (`Movies`, `TV Shows`, `Videos`, plus a few DVD-rip folders). Do not format. |
| fstab | **One** line only: `UUID=531C-AD38 /mnt/seagate3tb exfat uid=1000,gid=1000,umask=002,nofail,x-systemd.device-timeout=15 0 0` |

A duplicate fstab line caused a stacked mount; it was removed. `findmnt` must show **one** row.

**Use:** media bind-mount later; file-level / `vzdump` directory backups.  
**Do not use:** PVE VM/CT raw disks (exFAT + USB 2).

Optional next: `mkdir /mnt/seagate3tb/pve-backup` and a PVE Directory storage pointed there (`vzdump` only).

---

## Host disk reminder

- NVMe KingSpec `NE-512 2280` serial `9K60519000031` — `/` now **~22%** used (was ~11% on Aug 29).
- SanDisk Z400 still not in the disk list.

---

## Still open

1. CT 101 4G rootfs before any Compose stack beyond Portainer.
2. Watch CT 100 `df` — vuln-feed can refill.
3. USB 3 port if this disk will stream media from the M715q.
4. NetBox: hypervisor + CTs + this USB disk.
5. `pve-edk2-firmware` only if UEFI VMs are needed.
6. RustDesk is running on the **hypervisor** as `jacobk` (seen in `top`). Decide if that stays on the host or moves to CT 101.

---

*Checkpoint written 2026-09-05 from PVE UI + host CLI on node `debian`.*
