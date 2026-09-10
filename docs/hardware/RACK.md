# Rack & Physical Infrastructure (Updated September 9, 2026)

## Phase 1 Layout (Completed)
- Router/Gateway: TP-Link **ER605 V2** + SG2008P v3.20 managed switch (K108-MSW-1, serial Y25A081000375, MAC 10:5a:95:3a:16:b4, IP 192.168.0.146, fw 3.20.24) + 24-port patch panel on 1U shelf.
- APs (wall-mounted but part of infrastructure): TP-Link EAP225 coverage (office live; see inventory for planned conversions).
- PDU: StarTech 8-Outlet.
- Cabling: Monoprice Cat6; color-code by VLAN (vid10 Secure, vid20 IoT, Management).
- Per Omada snapshot: 2 APs (EAP225), 1 switch (SG2008P v3.20), gateway (ER605 V2); clients 21 (2 wired incl. BazzitePC on vid1, 19 wireless on K108-Home-Secure/IoT).

## Phase 2 Additions (In Progress — Host Live)
- **Proxmox Host**: Lenovo ThinkCentre M715q Tiny (S/N MJ067MNT, type 10M3000PUS) — free employer surplus, onsite 2026-07-09/10; **live PVE 9.2.4** as of 2026-08-29 / checkpoint 2026-09-05.
  - Specs: AMD PRO A12-9800E (4C), **2×8 GB DDR4 (~14.6 GiB visible)**, KingSpec 512GB NVMe boot. SanDisk Z400 still not detected.
  - Dual DisplayPort (no HDMI; use active DP→HDMI adapter if needed).
  - Form factor: ~1L Tiny — shelf/VESA/rack shelf mount.
  - Guests: CT 100 Wazuh, CT 101 Portainer. External Seagate 3TB mounted for media/backups.
- See [phase-2-checkpoint-2026-09-05.md](../phases/phase-2-checkpoint-2026-09-05.md) for live limits.

**References**:
- Diagrams: [../diagrams](../diagrams/) (update rack labels to ER605 V2)
- Hardware details: [DECISIONS.md](DECISIONS.md)
- Root status: [../../README.md](../../README.md)
