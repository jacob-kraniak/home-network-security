# Grok Workspace Instructions - Home Network Security Project

## Project Overview
This repository documents the transition from consumer-grade networking to a secure, segmented, privacy-focused home network. It is part of the broader Privacy Migration project.

## Production Architecture (2026-06-20 network + 2026-08-29 services host)

**Segmented VLAN lab** — ER605/FR205 tags VLANs 1/10/20; OpenWRT/Omada terminates via subinterfaces / Omada SSIDs.

| VID | Name | SSID | Prefix |
|-----|------|------|--------|
| 1 | LAN-Secure / Management | K108-Home-Secure | 192.168.0.0/24 |
| 10 | Trusted / Secure | K108-Home-Secure | 192.168.10.0/24 (or per final) |
| 20 | IoT | K108-Home-IoT | 192.168.20.0/24 |

**Core devices:** ER605/FR205-Gateway, OpenWRT-AP / EAP225s, TL-SG116E / SG2008P, K108_WAP2_Office, BazzitePC  
**Proxmox Host (Phase 2, live):** Lenovo ThinkCentre M715q Tiny (S/N MJ067MNT) — PVE 9.2.4 node `debian`, ~7.2 GiB RAM, KingSpec 512GB NVMe. CT 100 Wazuh, CT 101 Portainer. See [docs/phases/phase-2-baseline-2026-08-29.md](docs/phases/phase-2-baseline-2026-08-29.md).  
**Authoritative IPAM:** [NetBox Cloud](https://arfv7221.cloud.netboxapp.com/) (private — not mirrored in this repo)  
**Public doc:** [docs/network-overview.md](docs/network-overview.md)

## Phase Artifacts Map (Canonical)
**See [docs/phases/PHASE-ARTIFACTS.md](docs/phases/PHASE-ARTIFACTS.md)** for the definitive list of documents, diagrams, configs, and inventories that belong to:
- **Phase 1: Network Build** (Completed)
- **Phase 2: Self-Hosted Services Build** (In Progress — PVE + Wazuh + Portainer live)
- **Phase 3: Open Source Routing & Expansion** (Future)

Always consult (and update) that file when adding or reclassifying documentation.

**Return-to-project entry point:** [docs/phases/phase-2-baseline-2026-08-29.md](docs/phases/phase-2-baseline-2026-08-29.md)

## Core Goals
- Accurate inventory of all devices (especially IoT) — **NetBox is source of truth**
- VLAN segmentation (LAN-Secure, IoT, Guest) — **deployed 2026-06-20**
- Risk Mitigation (isolation) and Risk Transference (replacement) for IoT
- Self-hosted monitoring (Wazuh, Home Assistant) — Phase 2 (Wazuh live, RAM-constrained)
- Rack build-out; evaluate OPNsense/pfSense in Phase 3

## Key Project Artifacts & Locations

- **Network overview (public):** docs/network-overview.md
- **Master Roadmap:** docs/ROADMAP.md + [Privacy Migration board](https://github.com/users/jacob-kraniak/projects/1)
- **Phase Artifacts Map:** docs/phases/PHASE-ARTIFACTS.md ← **start here for phase ownership**
- **Phase 2 live baseline:** docs/phases/phase-2-baseline-2026-08-29.md
- **Current Inventory:**
  - docs/inventory/devices-summary.md (hardware, costs — no live IPs except where noted)
  - docs/inventory/iot-devices.md (validated against Omada JSON)
  - docs/inventory/nmap/ (raw & sanitized scans — gitignored where sensitive)
- **NetBox audit log:** docs/NetBox-Inventory-Progress.md
- **Post-Cutover:** docs/Post-Cutover-Network-Stabilization-and-Provisioning.md
- **Diagrams:** docs/diagrams/
- **Configs:** docs/configs/ (still a placeholder)
- **Hardware Plans:** docs/hardware/
- **Self-Hosted Services Research & Roadmap:** docs/services/self-hosted-services-roadmap.md
- **Document Digitization:** docs/services/document-digitization.md
- **Automation:** [netbox-nmap-scan](https://github.com/jacob-kraniak/netbox-nmap-scan)

## Working Guidelines for Grok
- **Always maintain privacy:** Sanitize MACs, WAN IPs, and credentials in committed files. RFC1918 lab addresses used in the Phase 2 baseline are intentional.
- **NetBox holds live data** — this repo holds architecture, decisions, and redacted summaries.
- Raw scan data should be gitignored where possible.
- Follow existing folder structure.
- When handing off to Grok Build, provide full file content in markdown blocks.
- Cross-reference privacy-migration-docs where relevant.
- Track progress against: Privacy Migration, Software Migrations, Cyber Education, Network Rack Build-out.
- **Phase ownership:** Use PHASE-ARTIFACTS.md to decide which docs belong to which phase. Update it when creating new artifacts.
- **Do not assume July 10 “install pending” text is current.** Trust phase-2-baseline-2026-08-29.md over older ROADMAP bullets.

## Parallel Workflow: Grok Chat/Project Space vs. Grok Build

- **Grok Chat / project space** — ideation, research, planning.
- **Grok Build** — implementation: edits files, commits, issues, documentation.
- **Hand-off rule:** Present Build-bound content in copy-pasteable markdown blocks.

## GitHub Project Integration

Main Project Board: https://github.com/users/jacob-kraniak/projects/1 (Privacy Migration)

### Labels
- `track:network-rack` (Phase 1)
- `track:privacy-migration`
- `track:self-hosted-services` (Phase 2)
- `phase:1` / `phase:2` / `phase:3`
- `status:planning` / `status:in-progress` / `status:done`

Last Updated: 2026-08-29 (Phase 2 live baseline after Wazuh recovery)
