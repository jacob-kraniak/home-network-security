# Grok Workspace Instructions - Home Network Security Project

## Project Overview
This repository documents the transition from consumer-grade networking to a secure, segmented, privacy-focused home network. It is part of the broader Privacy Migration project.

## Production Architecture (2026-06-20 + July 2026 Host)

**Segmented VLAN lab** — ER605/FR205 tags VLANs 1/10/20; OpenWRT/Omada terminates via subinterfaces / Omada SSIDs.

| VID | Name | SSID | Prefix |
|-----|------|------|--------|
| 1 | LAN-Secure / Management | K108-Home-Secure | 192.168.0.0/24 |
| 10 | Trusted / Secure | K108-Home-Secure | 192.168.10.0/24 (or per final) |
| 20 | IoT | K108-Home-IoT | 192.168.20.0/24 |

**Core devices:** ER605/FR205-Gateway, OpenWRT-AP / EAP225s, TL-SG116E / SG2008P, K108_WAP2_Office, BazzitePC  
**Proxmox Host (Phase 2):** Lenovo ThinkCentre M715q Tiny (S/N MJ067MNT) — free employer surplus, KingSpec 512GB NVMe + SanDisk Z400 256GB 2.5"  
**Authoritative IPAM:** [NetBox Cloud](https://arfv7221.cloud.netboxapp.com/) (private — not mirrored in this repo)  
**Public doc:** [docs/network-overview.md](docs/network-overview.md)

## Phase Artifacts Map (NEW — Canonical)
**See [docs/phases/PHASE-ARTIFACTS.md](docs/phases/PHASE-ARTIFACTS.md)** for the definitive list of documents, diagrams, configs, and inventories that belong to:
- **Phase 1: Network Build** (Completed)
- **Phase 2: Self-Hosted Services Build** (In Progress)
- **Phase 3: Open Source Routing & Expansion** (Future)

Always consult (and update) that file when adding or reclassifying documentation.

## Core Goals
- Accurate inventory of all devices (especially IoT) — **NetBox is source of truth**
- VLAN segmentation (LAN-Secure, IoT, Guest) — **deployed 2026-06-20**
- Risk Mitigation (isolation) and Risk Transference (replacement) for IoT
- Self-hosted monitoring (Wazuh, Home Assistant) — Phase 2
- Rack build-out; evaluate OPNsense/pfSense in Phase 3

## Key Project Artifacts & Locations

- **Network overview (public):** docs/network-overview.md
- **Master Roadmap:** docs/ROADMAP.md + [Privacy Migration board](https://github.com/users/jacob-kraniak/projects/1)
- **Phase Artifacts Map:** docs/phases/PHASE-ARTIFACTS.md ← **start here for phase ownership**
- **Current Inventory:**
  - docs/inventory/devices-summary.md (hardware, costs — no live IPs)
  - docs/inventory/iot-devices.md (validated against Omada JSON)
  - docs/inventory/nmap/ (raw & sanitized scans — gitignored where sensitive)
- **NetBox audit log:** docs/NetBox-Inventory-Progress.md
- **Post-Cutover:** docs/Post-Cutover-Network-Stabilization-and-Provisioning.md
- **Diagrams:** docs/diagrams/
- **Configs:** docs/configs/ (to be populated in Phase 2)
- **Hardware Plans:** docs/hardware/
- **Self-Hosted Services Research & Roadmap:** docs/services/self-hosted-services-roadmap.md
- **Document Digitization:** docs/services/document-digitization.md
- **Automation:** [netbox-nmap-scan](https://github.com/jacob-kraniak/netbox-nmap-scan)

## Working Guidelines for Grok
- **Always maintain privacy:** Sanitize MACs, IPs, and personal details in committed files.
- **NetBox holds live data** — this repo holds architecture, decisions, and redacted summaries.
- Raw scan data should be gitignored where possible.
- Follow existing folder structure.
- When handing off to Grok Build, provide full file content in markdown blocks.
- Cross-reference privacy-migration-docs where relevant.
- Track progress against: Privacy Migration, Software Migrations, Cyber Education, Network Rack Build-out.
- **Phase ownership:** Use PHASE-ARTIFACTS.md to decide which docs belong to which phase. Update it when creating new artifacts.

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

Last Updated: 2026-07-10 (Phase Artifacts map created; M715q Proxmox host inventoried)
