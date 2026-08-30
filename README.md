# Home Network Security Buildout

Production segmented network using TP-Link Omada SDN (June 2026).  
**Phase 2 services host is live** — start here: [docs/phases/phase-2-baseline-2026-08-29.md](docs/phases/phase-2-baseline-2026-08-29.md) (2026-08-29).

## Architecture Overview

**Hardware Stack:**
- **Gateway**: TP-Link ER605 v2.30 (firmware 2.3.3) – 192.168.0.1
- **Core Switch**: TP-Link SG2008P v3.20 (K108-MSW-1)
  - Serial: Y25A081000375
  - MAC: 10:5a:95:3a:16:b4
  - IP: 192.168.0.146
  - Firmware: 3.20.24 Build 20260509 Rel.2353
  - Uptime (snapshot): 4day(s) 3h 31m 52s
- **Wireless**: 2× TP-Link EAP225 v4.0
  - Living Room (192.168.0.148, firmware 5.2.4)
  - Office (192.168.0.105, firmware 5.2.2)
- **Controller**: Omada Software on BazzitePC
- **Proxmox (Phase 2, live 2026-08-29):** Lenovo ThinkCentre M715q Tiny — PVE 9.2.4 node `debian` `192.168.0.176`. CT 100 Wazuh `192.168.0.178`. CT 101 Portainer `192.168.0.200`.

**VLAN Plan:**
- VLAN 1 (Management) – Infrastructure
- VLAN 10 (Trusted) – User devices / PCs
- VLAN 20 (IoT)
- VLAN 30 (Guest)
- VLAN 40 (Lab / Servers)

**Key Features:**
- 802.1Q trunking on AP ports (Native = Management, Tagged = 10/20/30/40)
- Centralized management & monitoring
- Foundation for Wazuh, Proxmox homelab, and further security tooling

## Architecture Overview (Final Buildout June 2026 per Omada JSON)

**Hardware Stack:**
- **Gateway/Router**: TP-Link FR205 (Multi-WAN, firmware matching Omada)
- **Core Switch**: TP-Link SG2008P v3.20 (K108-MSW-1)
  - Serial: Y25A081000375
  - MAC: 10:5a:95:3a:16:b4
  - IP: 192.168.0.146
  - Firmware: 3.20.24 Build 20260509 Rel.2353
  - VLAN capable, Omada integrated.
- **Wireless**: 2× TP-Link EAP225 v4.0
- **Controller**: Omada on BazzitePC
- **Services hypervisor:** Lenovo M715q Tiny (not the Dell OptiPlex 7060). See Phase 2 baseline.

**VLAN Plan (Active):**
- VLAN 1 (Management) – Infrastructure
- VLAN 10 (Trusted/Secure) – K108-Home-Secure SSID – User devices / PCs
- VLAN 20 (IoT) – K108-Home-IoT SSID
- (Guest 30, Lab 40 planned)

**Key Features:**
- 802.1Q trunking on AP ports (Native = Management, Tagged = 10/20/30/40)
- Centralized management & monitoring via Omada
- 21 clients (clientStat: 2 wired, 19 wireless, ipc:2 cameras; clientType: smartHome:10, camera:2, office:4, audioVideo:1, mobile:1, other:3)
- Foundation for Wazuh + Portainer on Proxmox (M715q). ~7 GiB host RAM is the Phase 2 constraint.

See `docs/` for switch port profiles, WLAN mappings, ACL examples, and NetBox export. See [docs/ROADMAP.md](docs/ROADMAP.md) for phases.

## Key Documents
- [Phase 2 live baseline (2026-08-29)](docs/phases/phase-2-baseline-2026-08-29.md) — **return here first**
- [Project Roadmap](docs/ROADMAP.md)
- [Phase Artifacts Map](docs/phases/PHASE-ARTIFACTS.md)
- [IoT Devices & Risk Plan](docs/inventory/iot-devices.md)
- [Grok Workspace Instructions](GROK-WORKSPACE.md)
- [Self-Hosted Services Research & Roadmap](docs/services/self-hosted-services-roadmap.md)
- [Document Digitization System](docs/services/document-digitization.md) (Paperless-ngx - high priority)
- [Hardware Decisions](docs/hardware/DECISIONS.md)
- [Rack & Physical Infrastructure](docs/hardware/RACK.md)
- Diagrams: `docs/diagrams/`

## Parallel Tracks
This repo supports the main Privacy Migration project. See [privacy-migration-docs](https://github.com/jacob-kraniak/privacy-migration-docs) for overarching roadmap.

## Repository Structure

```
.
├── README.md
├── GROK-WORKSPACE.md
├── .gitignore
└── docs/
    ├── inventory/     # Nmap XMLs, device lists, host inventories (see .gitignore)
    ├── diagrams/      # Draw.io / diagrams.net network topology diagrams
    ├── hardware/      # Rack measurements, infrastructure criteria, DECISIONS.md, RACK.md
    ├── phases/        # Phase map + completion logs + Phase 2 live baseline
    ├── services/      # Self-hosted services roadmap, document digitization
    └── ROADMAP.md     # High-level project roadmap (phases)
```

### docs/inventory/

Intended for:

- Nmap scan outputs (XML)
- Device inventories and asset lists
- Discovered hosts, services, etc.

**Note on sensitivity:** Files matching `*.xml` (and other patterns) are ignored by `.gitignore` because they typically contain real MAC addresses, hostnames, and live network details. Keep raw scans local-only. Use summarized or anonymized lists (e.g. `devices.md`) if versioning is desired.

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
2. Read [docs/phases/phase-2-baseline-2026-08-29.md](docs/phases/phase-2-baseline-2026-08-29.md) before touching the M715q
3. Place your own Nmap XMLs or inventories into `docs/inventory/` — they will be ignored by default
4. Review `.gitignore` before any `git add -f` of sensitive data

## Security Notes

- This is a **private** repository.
- Even so, avoid committing live credentials, full packet captures, or unredacted device details unless necessary.
- Regularly audit committed files for accidental secrets.

Initial structure created 2026. Phase 2 baseline added 2026-08-29.
