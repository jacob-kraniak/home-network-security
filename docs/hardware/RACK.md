# Rack & Physical Infrastructure (Updated July 10, 2026)

## Phase 1 Layout (Completed)
- Router/Gateway: TP-Link FR205 (Multi-WAN) + SG2008P v3.20 managed switch (K108-MSW-1, serial Y25A081000375, MAC 10:5a:95:3a:16:b4, IP 192.168.0.146, fw 3.20.24) + 24-port patch panel on 1U shelf.
- APs (wall-mounted but part of infrastructure): 2x TP-Link EAP225 v4 (K108_WAP1_LivingRoom "58:04:4f:dc:ce:72", K108_WAP2_Office "5c:e9:31:6c:b5:44").
- PDU: StarTech 8-Outlet.
- Cabling: Monoprice Cat6; color-code by VLAN (vid10 Secure, vid20 IoT, Management).
- Per final Omada data: 2 APs (EAP225), 1 switch (SG2008P v3.20), gateway (FR205); clients 21 (2 wired incl. BazzitePC on vid1, 19 wireless on K108-Home-Secure/IoT).

## Phase 2 Additions (In Progress — Host Acquired)
- **Proxmox Host**: Lenovo ThinkCentre M715q Tiny (S/N MJ067MNT, type 10M3000PUS) — free employer surplus, onsite 2026-07-09/10.
  - Specs: AMD Ryzen PRO APU (quad-core), 16GB DDR4, KingSpec 512GB NVMe Gen3x4 boot, SanDisk Z400 256GB 2.5" SATA mounted for potential RAID1.
  - Dual DisplayPort (no HDMI; use active DP→HDMI adapter if needed for local monitor).
  - Form factor: ~1L Tiny — ideal for shelf/VESA/rack shelf mount in Server Hosts rack or open rack.
  - Planned: Install Proxmox VE, run Wazuh + containers/services. External Seagate 3TB for bulk data.
- Integrate services (Proxmox clients/services on wired LAN-Secure).

**References**:
- See [../diagrams](../diagrams/) for visual layout (Future-State-Network-Diagram.drawio, Rack-Layout-12U.drawio reflect actual EAP225/MSW-1/FR205).
- Full hardware details: [DECISIONS.md](DECISIONS.md)
- Root status: [../../README.md](../../README.md#project-status-update-june-2026) (21 clients, deviceStat 2 APs + switch + gateway)
- Controller data (final): JSON in project notes (exact macs, ips 192.168.0/10/20, rssi, traffic, vid for all 21 clients e.g. Wyze d0:3f:27:2b:2b:53 "Baby Cam", HS220 50:91:e3:48:b3:2b, Lenovo bc:df:58:b3:b2:c0, BazzitePC e0:d5:5e:e3:98:97, etc.)
