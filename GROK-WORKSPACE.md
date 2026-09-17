# Grok Workspace Instructions - Home Network Security Project

## Project Overview
This repository documents the transition from consumer-grade networking to a secure, segmented, privacy-focused home network. It is part of the broader Privacy Migration project. **This repo is public.**

## Production Architecture (network June 2026 + services host Sep 2026)

**Segmented VLAN lab** — **ER605 V2** tags VLANs 1/10/20; Omada / OpenWRT terminate SSIDs and L2 distribution.

| VID | Name | SSID | Prefix |
|-----|------|------|--------|
| 1 | LAN-Secure / Management | K108-Home-Secure | 192.168.0.0/24 |
| 10 | Trusted / Secure | K108-Home-Secure | see NetBox / network-overview |
| 20 | IoT | K108-Home-IoT | see NetBox / network-overview |

**Core devices:** ER605-Gateway (primary), OpenWRT / EAP225s, TL-SG116E / SG2008P, BazzitePC  
**Proxmox Host (Phase 2, live):** Lenovo ThinkCentre M715q Tiny (S/N MJ067MNT) — PVE 9.2.4 node `debian`, **~14.6 GiB RAM (2×8 GB)**, KingSpec 512GB NVMe. CT 100 Wazuh (6G), CT 101 Portainer (6G / 100G) running Portainer + Omada 6.3 + RustDesk + **NetBox v4.7**. See [docs/phases/phase-2-checkpoint-2026-09-16.md](docs/phases/phase-2-checkpoint-2026-09-16.md).  
**Authoritative IPAM:** NetBox Cloud (private — not mirrored here) until local import is verified  
**Local NetBox (empty until import):** `http://192.168.0.200:8000` — VLAN 1 / mesh only  
**Public doc:** [docs/network-overview.md](docs/network-overview.md)

## Phase Artifacts Map (Canonical)
**See [docs/phases/PHASE-ARTIFACTS.md](docs/phases/PHASE-ARTIFACTS.md)** for phase ownership of docs and diagrams.

**Return-to-project entry point:** [docs/phases/phase-2-checkpoint-2026-09-16.md](docs/phases/phase-2-checkpoint-2026-09-16.md)  
**Wazuh outage narrative only:** [docs/phases/phase-2-baseline-2026-08-29.md](docs/phases/phase-2-baseline-2026-08-29.md)

## Core Goals
- Accurate inventory — **NetBox is source of truth for live IPs/MACs**
- VLAN segmentation — deployed
- Risk mitigation / transference for IoT
- Self-hosted monitoring (Wazuh live; more services Phase 2)
- Rack build-out; OPNsense/pfSense evaluation in Phase 3

## Key Project Artifacts & Locations

- **Network overview (public):** docs/network-overview.md
- **Master Roadmap:** docs/ROADMAP.md
- **Phase Artifacts Map:** docs/phases/PHASE-ARTIFACTS.md
- **Phase 2 live checkpoint:** docs/phases/phase-2-checkpoint-2026-09-16.md
- **Inventory:** docs/inventory/devices-summary.md, iot-devices.md
- **Hardware decisions:** docs/hardware/DECISIONS.md
- **Services research:** docs/services/

## Working Guidelines for Grok
- **Always maintain privacy:** sanitize MACs, WAN IPs, credentials. RFC1918 lab addresses in Phase 2 checkpoints are intentional.
- **NetBox holds live data** — this repo holds architecture, decisions, and redacted summaries. Cloud remains SoT until local import is verified.
- **Do not assume Aug 29 RAM (~7.2 GiB) is current.** Trust Sep 16 checkpoint + devices-summary for live facts. Primary gateway is ER605 V2 only.
- Update PHASE-ARTIFACTS.md when adding artifacts.
- Small diffs; no drive-by refactors.

## GitHub Project Integration
Main board: https://github.com/users/jacob-kraniak/projects/1

Last Updated: 2026-09-16 (NetBox local service active on CT 101)
