# Home Network Security Buildout

Production segmented network using TP-Link Omada SDN (June 2026).

## Architecture Overview

**Hardware Stack:**
- **Gateway**: TP-Link ER605 v2.30 (firmware 2.3.3) – 192.168.0.1
- **Core Switch**: TP-Link SG2008P v3.20 (firmware 3.20.24) – 192.168.0.146
- **Wireless**: 2× TP-Link EAP225 v4.0
  - Living Room (192.168.0.148, firmware 5.2.4)
  - Office (192.168.0.105, firmware 5.2.2)
- **Controller**: Omada Software on BazzitePC

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
- **Gateway/Router**: TP-Link FR205 (Multi-WAN, firmware matching Omada) – public IP 173.56.71.104
- **Core Switch**: TP-Link SG2008P v3.20 (K108-MSW-1)
  - Serial: Y25A081000375
  - MAC: 10:5a:95:3a:16:b4
  - IP: 192.168.0.146
  - Firmware: 3.20.24 Build 20260509 Rel.2353
  - Uptime: 4day(s) 3h 31m 52s (as of data)
  - VLAN capable, Omada integrated.
- **Wireless**: 2× TP-Link EAP225 v4.0 (Living Room "58:04:4f:dc:ce:72" fw 5.2.2, Office "5c:e9:31:6c:b5:44" fw 5.2.4)
- **Controller**: Omada on BazzitePC / Dell OptiPlex

**VLAN Plan (Active):**
- VLAN 1 (Management) – Infrastructure
- VLAN 10 (Trusted/Secure) – K108-Home-Secure SSID – User devices / PCs
- VLAN 20 (IoT) – K108-Home-IoT SSID
- (Guest 30, Lab 40 planned)

**Key Features:**
- 802.1Q trunking on AP ports (Native = Management, Tagged = 10/20/30/40)
- Centralized management & monitoring via Omada
- 21 clients (clientStat: 2 wired, 19 wireless, ipc:2 cameras; clientType: smartHome:10, camera:2, office:4, audioVideo:1, mobile:1, other:3)
- Foundation for Wazuh, Proxmox homelab, and further security tooling. Dell OptiPlex 7060 Micro (i7-8700T 32GB) as Proxmox services host (BazzitePC client).

See `docs/` for switch port profiles, WLAN mappings, ACL examples, and NetBox export. See [docs/ROADMAP.md](docs/ROADMAP.md) for phases.

## Key Documents
- [Project Status Update](README.md#project-status-update-june-2026) (this file)
- [Project Roadmap](docs/ROADMAP.md)
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
├── .gitignore
└── docs/
    ├── inventory/     # Nmap XMLs, device lists, host inventories (see .gitignore)
    ├── diagrams/      # Draw.io / diagrams.net network topology diagrams
    ├── hardware/      # Rack measurements, infrastructure criteria, DECISIONS.md, RACK.md
    ├── services/      # Self-hosted services roadmap, document digitization (Paperless-ngx) + table of planned apps in services/README.md
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
2. Place your own Nmap XMLs or inventories into `docs/inventory/` — they will be ignored by default
3. Add diagrams to `docs/diagrams/`
4. Review `.gitignore` before any `git add -f` of sensitive data

## Security Notes

- This is a **private** repository.
- Even so, avoid committing live credentials, full packet captures, or unredacted device details unless necessary.
- Regularly audit committed files for accidental secrets.

Initial structure created 2026.
