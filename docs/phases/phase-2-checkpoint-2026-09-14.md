# Phase 2 Checkpoint — 2026-09-14

**Captured:** 2026-09-14 evening (EDT)  
**Supersedes for live facts:** [phase-2-checkpoint-2026-09-05.md](phase-2-checkpoint-2026-09-05.md)  
Keep Aug 29 / Sep 5 files for Wazuh outage and RAM/USB narrative.

RFC1918 only. No WAN IPs, tokens, or Omada passwords.

---

## Milestone

**Omada Software Controller is on-prem** in Portainer on CT 101. Cloud-Based Controller export was restored locally; devices migrated via inform `192.168.0.200`. Cloud account closed. Site **Kraniak-Home** telemetry (DHCP, device connect) is visible on the local UI.

SSID / VLAN / DHCP on the ER605 stayed up through the flip. Brief management disconnect while devices adopted.

---

## Omada on CT 101

| Field | Value |
|-------|-------|
| Host | CT 101 `portainer` `192.168.0.200` |
| Stack | Portainer Compose project `omada_controller` |
| Image | `mbentley/omada-controller:6.3` (running **6.3.0.45**) |
| Cloud source | Omada Essential CBC **6.3.0.100** (closed after migrate) |
| UI | `https://192.168.0.200:8043` (self-signed) |
| HTTP | `8088` |
| Portal | `8843` |
| Device ports | `29810/udp`, `29811–29817/tcp`, `27001/udp` |
| Volumes | `omada_controller_omada-data`, `omada_controller_omada-logs` |
| Container mem | `2g` (`-Xmx1024m` JVM) |
| Controller Hostname/IP | **Manual `192.168.0.200`** — do not use Auto Refresh (picks Docker `172.19.0.2`) |
| Cloud Access | Disabled |
| Site | Kraniak-Home |

Software Controller 6.3 has **no Copy Inform URL** (that is CBC-only). Cloud migrate accepted bare IP `192.168.0.200`.

---

## Adopted devices (Kraniak-Home)

| Name | Role | MAC | Typical IP |
|------|------|-----|------------|
| K108-ER605-Gateway | Gateway | 58:04:4f:37:b9:cb | 192.168.0.1 |
| K108-MSW-1 | Switch | 10:5a:95:3a:16:b4 | 192.168.0.102 |
| K108_WAP1_LivingRoom | AP | 58:04:4f:dc:ce:72 | 192.168.0.101 |
| K108_WAP2_Office | AP | 5c:e9:31:6c:b5:44 | 192.168.0.100 |

Connected events in site logs ~21:08–21:15 EDT 2026-09-14. Gateway also handing leases on VLAN 10 / 20 / 30 / 40 as before.

---

## Also on CT 101 (unchanged this night)

- Portainer CE
- RustDesk `hbbs`/`hbbr` (key lives in volume `rustdesk_rustdesk-data`)

CT 101 rootfs was grown earlier in Phase 2 (do not treat Sep 5 “4G disk” as current).

---

## Wazuh / agents (carry-forward)

Still 4.8.2. Agents: `000` manager, `003` pve-debian, `004` ct101-portainer, `005` bazzite, `006` Christines_Laptop. Groups: `containers`, `hypervisor`, `endpoints_Linux`, `endpoints_Windows`.

---

## Still open

1. Wazuh `local_rules.xml` + group `agent.conf` (rootcheck off on LXC; SCA not a pager).
2. Optional Omada syslog → Wazuh `:514` **after** alert noise is down.
3. PVE Directory / vzdump on `/mnt/seagate3tb/pve-backup`.
4. NetBox: hypervisor + CTs + Omada controller + four SDN devices.
5. Plane.so still not deployed.
6. Do not enable Omada Cloud Access unless there is a specific need.

---

*Checkpoint written 2026-09-14 from local Omada 6.3 UI + site event export (WAN IPs stripped).*
