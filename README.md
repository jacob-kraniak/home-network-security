# home-network-security

Home network security documentation, inventories, diagrams, and configurations.

## Overview

This repository is for tracking and versioning the security posture, scans, diagrams, and configs of a home lab / residential network.

**Related projects:**
- [privacy-migration-docs](https://github.com/jacob-kraniak/privacy-migration-docs) — privacy and data migration documentation

## Project Status Update (June 12, 2026)

### Current Phase: Foundation Networking + Initial Compute
- **Phase 1 (In Progress)**: TP-Link ER605 V2 Omada hardware deployed for stable family internet with basic security + VLAN prep. StarTech rack PDU acquired.  
  See [hardware](docs/hardware/) and the new **[Hardware & Project Inventory Summary](docs/inventory/devices-summary.md)** (master list + cost tracker) for full details.
- **Phase 2 (Next)**: Deploy **Dell OptiPlex 7060 Micro** (or N100-class mini-PC) as first Proxmox services host.  
  See [diagrams](docs/diagrams/) for updated network topology.
- **Phase 3**: Migrate routing to OPNsense + expand storage.

**Core Principles**: Balance security/privacy with family stability. Prefer open source where low-risk; retain TP-Link Omada for warranty, SDN features, and fast recovery.

See [docs/ROADMAP.md](docs/ROADMAP.md) for detailed phases and [hardware](docs/hardware/) for decisions.

## Key Documents
- [Project Status Update](README.md#project-status-update-june-12-2026) (this file)
- [Project Roadmap](docs/ROADMAP.md)
- **[Hardware & Project Inventory Summary](docs/inventory/devices-summary.md)** — **New master hardware list, status tracking, and project cost tracker** (purchased + existing + planned)
- [IoT Devices & Risk Plan](docs/inventory/iot-devices.md)
- [Grok Workspace Instructions](GROK-WORKSPACE.md)
- [Self-Hosted Services Research & Roadmap](docs/services/self-hosted-services-roadmap.md)
- [Document Digitization System](docs/services/document-digitization.md) (Paperless-ngx - high priority)
- [Hardware Decisions](docs/hardware/DECISIONS.md)
- [Rack & Physical Infrastructure](docs/hardware/RACK.md)
- [Rack Build Overview](docs/hardware/home-lab-rack-build.md)
- Diagrams: `docs/diagrams/`

## Parallel Tracks
This repo supports the main Privacy Migration project. See [privacy-migration-docs](https://github.com/jacob-kraniak/privacy-migration-docs) for overarching roadmap.

## Repository Structure

```
.
├── README.md
├── .gitignore
└── docs/
    ├── inventory/     # Master devices-summary.md + Nmap XMLs, device lists, host inventories (see .gitignore for sensitive files)
    ├── diagrams/      # Draw.io / diagrams.net network topology diagrams
    ├── hardware/      # Rack measurements, infrastructure criteria, DECISIONS.md, RACK.md, home-lab-rack-build.md
    ├── services/      # Self-hosted services roadmap, document digitization (Paperless-ngx) + table of planned apps in services/README.md
    └── ROADMAP.md     # High-level project roadmap (phases)
```

### docs/inventory/

Intended for:
- **devices-summary.md** — Master summarized hardware inventory + project cost tracker (newly created)
- Nmap scan outputs (XML) — raw & sanitized
- Device inventories and asset lists
- Discovered hosts, services, etc.

**Note on sensitivity:** Files matching `*.xml` (and other patterns) are ignored by `.gitignore` because they typically contain real MAC addresses, hostnames, and live network details. Keep raw scans local-only. Use summarized or anonymized lists (e.g. `devices-summary.md`) if versioning is desired.

### docs/diagrams/

- Network diagrams in `.drawio` format (editable with diagrams.net / Draw.io)
- `.gitignore` also excludes Draw.io backup files

### docs/configs/

Placeholder for future configuration management:
- pfSense / OPNsense exports and rules
- Wazuh / OSSEC agent configs and policies
- Other security tooling configs

## Getting Started

1. Clone the repo (private — access restricted)
2. Place your own Nmap XMLs or inventories into `docs/inventory/` — they will be ignored by default
3. Add diagrams to `docs/diagrams/`
4. Review `.gitignore` before any `git add -f` of sensitive data

## Security Notes

- This is a **private** repository.
- Even so, avoid committing live credentials, full packet captures, or unredacted device details unless necessary.
- Regularly audit committed files for accidental secrets.

Initial structure created 2026. Updated June 2026 with ER605 V2 + StarTech PDU inventory and cost tracking.