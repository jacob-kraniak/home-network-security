# Grok Workspace Instructions - Home Network Security Project

## Project Overview
This repository documents the transition from consumer-grade networking to a secure, segmented, privacy-focused home network. It is part of the broader Privacy Migration project.

## Core Goals
- Accurate inventory of all devices (especially IoT)
- VLAN segmentation (Trusted, IoT, Guest, Work)
- Risk Mitigation (isolation) and Risk Transference (replacement) for IoT
- Self-hosted monitoring (Wazuh, Home Assistant)
- Rack build-out with pfSense/OPNsense

## Key Project Artifacts & Locations

- **Master Roadmap**: ../privacy-migration-docs (or link in GitHub Projects)
- **Current Inventory**:
  - docs/inventory/devices-summary.md
  - docs/inventory/iot-devices.md
  - docs/inventory/nmap/ (raw & sanitized scans)
- **Diagrams**: docs/diagrams/ (Home-Network-Diagram.drawio + VLAN versions)
- **Configs**: docs/configs/ (pfSense, Wazuh, firewall rules)
- **Risk Register**: docs/risk/ (IoT devices, mitigation plans)
- **Hardware Plans**: docs/hardware/ (rack build, shopping lists, mini-PC specs)

## IoT Risk Strategy
- TP-Link Kasa (12x): VLAN + HA integration (Mitigation)
- Ring (4x): VLAN now → Full replacement with Reolink/Frigate (Transference)
- Google Nest (6x+): VLAN + local control → Zigbee/Z-Wave migration

## Working Guidelines for Grok
- Always maintain privacy: Sanitize MACs, IPs, and personal details in committed files.
- Use redacted summaries alongside raw data (raw data should be gitignored where possible).
- Follow existing folder structure.
- When suggesting changes, provide full file content in markdown blocks.
- Cross-reference privacy-migration-docs where relevant.
- Track progress against the 4 parallel tracks: Privacy Migration, Software Migrations, Cybersecurity Education, Network Rack Build-out.

## GitHub Project Integration

Main Project Board: https://github.com/users/jacob-kraniak/projects/1 (Privacy Migration)

### How to Link Work:
1. Create Issues in this repo for specific tasks (Network Rack, IoT, Wazuh, etc.).
2. Add them to the main Project board:
   - Open the issue → Click "Projects" → Add to "Privacy Migration".
   - Or from the Project board, use "Add item" and search for issues from this repo.
3. Use these labels consistently:
   - `track:network-rack`
   - `track:privacy-migration`
   - `track:cyber-education`
   - `track:software-migration`
   - `status:planning` / `status:in-progress`

This ensures all network activities roll up into the master Privacy Migration roadmap.

Last Updated: 2026-06-04
