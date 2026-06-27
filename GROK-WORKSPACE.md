# Grok Workspace Instructions - Home Network Security Project

## Project Overview
This repository documents the transition from consumer-grade networking to a secure, segmented, privacy-focused home network. It is part of the broader Privacy Migration project.

## Production Architecture (2026-06-20)

**Segmented VLAN lab** — ER605 tags VLANs 1/10/20; OpenWRT terminates via `br-lan.N` subinterfaces.

| VID | Name | SSID | Prefix |
|-----|------|------|--------|
| 1 | LAN-Secure | K108-Home-Secure | 192.168.0.0/24 |
| 10 | IoT | K108-Home-IoT | 192.168.10.0/24 |
| 20 | Guest | K108-Guest | 192.168.20.0/24 |

**Core devices:** ER605-Gateway, OpenWRT-AP, TL-SG116E-SWITCH-1, K108_WAP2_Office, BazzitePC  
**Authoritative IPAM:** [NetBox Cloud](https://arfv7221.cloud.netboxapp.com/) (private — not mirrored in this repo)  
**Public doc:** [docs/network-overview.md](docs/network-overview.md)

## Core Goals
- Accurate inventory of all devices (especially IoT) — **NetBox is source of truth**
- VLAN segmentation (LAN-Secure, IoT, Guest) — **deployed 2026-06-20**
- Risk Mitigation (isolation) and Risk Transference (replacement) for IoT
- Self-hosted monitoring (Wazuh, Home Assistant) — Phase 2
- Rack build-out; evaluate OPNsense/pfSense in Phase 3

## Key Project Artifacts & Locations

- **Network overview (public):** docs/network-overview.md
- **Master Roadmap:** docs/ROADMAP.md + [Privacy Migration board](https://github.com/users/jacob-kraniak/projects/1)
- **Current Inventory:**
  - docs/inventory/devices-summary.md (hardware, costs — no live IPs)
  - docs/inventory/iot-devices.md (validated against Omada JSON: 21 clients, smartHome 10 Kasa, camera 2, etc.)
  - docs/inventory/nmap/ (raw & sanitized scans — gitignored where sensitive)
- **NetBox audit log:** docs/NetBox-Inventory-Progress.md
- **Post-Cutover:** docs/Post-Cutover-Network-Stabilization-and-Provisioning.md
- **Diagrams:** docs/diagrams/ (public topology diagrams — next phase; updated with final EAP225, FR205, SG2008P v3.20, 21 clients)
- **Configs:** docs/configs/ (pfSense, Wazuh, firewall rules)
- **Hardware Plans:** docs/hardware/ (rack build, shopping lists, mini-PC specs; final deployed per Omada JSON June 2026: FR205 router, SG2008P v3.20 switch K108-MSW-1, 2x EAP225 APs, Dell OptiPlex 7060 Micro Proxmox; 21 clients with clientStat/clientTypeStat)
- **Self-Hosted Services Research & Roadmap:** docs/services/self-hosted-services-roadmap.md (Host OS, Proxmox, OPNsense, Wazuh, RustDesk, media servers, Home Assistant, camera migration, phased roadmap)
- **Document Digitization:** docs/services/document-digitization.md (Paperless-ngx based searchable archive - high priority)
- **Automation:** [netbox-nmap-scan](https://github.com/jacob-kraniak/netbox-nmap-scan)

## IoT Risk Strategy
- TP-Link Kasa (12x): VLAN 10 + HA integration (Mitigation)
- Ring (4x): VLAN 10 → Full replacement with Reolink/Frigate (Transference)
- Google Nest (6x+): VLAN 10 + local control → Zigbee/Z-Wave migration

## Working Guidelines for Grok
- **Always maintain privacy:** Sanitize MACs, IPs, and personal details in committed files.
- **NetBox holds live data** — this repo holds architecture, decisions, and redacted summaries.
- Raw scan data should be gitignored where possible.
- Follow existing folder structure.
- When handing off to Grok Build, provide full file content in markdown blocks (see Parallel Workflow below).
- Cross-reference privacy-migration-docs where relevant.
- Track progress against: Privacy Migration, Software Migrations, Cyber Education, Network Rack Build-out.

## Parallel Workflow: Grok Chat/Project Space vs. Grok Build

- **Grok Chat / project space** — ideation, research, planning.
- **Grok Build** — implementation: edits files, commits, issues, documentation.
- **Hand-off rule:** Present Build-bound content in copy-pasteable markdown blocks.

## GitHub Project Integration

Main Project Board: https://github.com/users/jacob-kraniak/projects/1 (Privacy Migration)

### Labels
- `track:network-rack`
- `track:privacy-migration`
- `track:cyber-education`
- `track:software-migration`
- `status:planning` / `status:in-progress`

Last Updated: 2026-06-20 (production VLAN architecture + NetBox documentation complete)
