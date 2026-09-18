# Phase 2 Checkpoint — 2026-09-16

**Captured:** 2026-09-16 evening (EDT)  
**Supersedes for live facts:** [phase-2-checkpoint-2026-09-14.md](phase-2-checkpoint-2026-09-14.md)  
Keep Sep 14 for Omada on-prem, Sep 5 for RAM/USB, Aug 29 for the Wazuh outage narrative.

RFC1918 only. No tokens, passwords, or WAN IPs.

---

## Milestone

**NetBox Community is an active container service on CT 101.** Empty local instance is healthy; **NetBox Cloud remains authoritative IPAM** until inventory is imported and counts match.

Placement decision: grow CT 101 (no CT 102). Same Docker/Portainer control plane as Omada and RustDesk.

---

## CT 101 (resized 2026-09-15)

| Field | Value |
|-------|-------|
| Hostname | `portainer` |
| IP | `192.168.0.200/24` gw `192.168.0.1` via `vmbr0` |
| Cores | 4 (`nesting=1`, `keyctl=1`) |
| Memory | 6144 MiB + 1024 MiB swap |
| Rootfs | `local:101/vm-101-disk-0.raw` **100G** |
| Type | unprivileged Debian, `onboot=1`, tag `docker` |

Inside the guest at deploy time: ~1.9 GiB used of 6 GiB, ~3.9 GiB used of 99 GiB.

---

## NetBox stack on CT 101

| Field | Value |
|-------|-------|
| Path | `/opt/stacks/netbox` (`netbox-community/netbox-docker` branch `release`) |
| Image | `netboxcommunity/netbox:v4.7-5.1.1` |
| App | NetBox Community **v4.7.0** |
| DB | `postgres:18-alpine` |
| Cache / queue | `valkey/valkey:9.1-alpine` × 2 |
| UI | `http://192.168.0.200:8000` (VLAN 1 / mesh only — no WAN publish) |
| Compose publish | `8000:8080` |
| Volumes | `netbox_netbox-postgres`, `netbox_netbox-redis-data`, `netbox_netbox-redis-cache-data`, media/reports/scripts |
| Container limits | netbox 768M, worker 512M, postgres 512M, each Valkey 128M |

All five containers `running (healthy)` 2026-09-16. Local admin login confirmed (`jacob-admin`). Local IPAM widgets are empty (0 sites / prefixes / VLANs) — expected before Cloud import.

Do not port-forward `:8000`. Do not `compose down -v`.

---

## Also on CT 101 (unchanged this night)

- Portainer CE `:9443` / `:9000`
- Omada Controller 6.3.0.45 `:8043` — Controller Hostname stays `192.168.0.200`
- RustDesk `hbbs`/`hbbr`

---

## Still open

1. Import Cloud inventory via API / `netbox-nmap-scan`; dual-run; flip SoT only after device/prefix/VLAN counts match.
2. Model hypervisor + CT 100/101 + Omada controller in NetBox (issue #28 remainder).
3. Scheduled DHCP/nmap sync against the **local** API.
4. Optional Proxbox later — not on this pass.
5. Wazuh noise reduction; PVE Directory/vzdump on the Seagate; no Omada Cloud Access.

---

*Checkpoint written 2026-09-16 from CT 101 `docker compose ps` + local UI. Secrets stay on the guest.*
