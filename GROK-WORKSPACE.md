# Grok Workspace Instructions - Home Network Security Project

## Project Overview
This repository documents the transition from consumer-grade networking to a secure, segmented, privacy-focused home network. It is part of the broader Privacy Migration project. **This repo is public.**

## Production Architecture (network June 2026 + services host Sep 2026)

**Segmented VLAN lab** — **ER605 V2** tags VLANs 1/10/20/30/40; Omada terminates SSIDs and L2 distribution (Controller on CT 101).

| VID | Omada name | SSID | Gateway / prefix |
|-----|------------|------|------------------|
| 1 | Management (Default) | (mgmt) | 192.168.0.1/24 |
| 10 | Trusted | K108-Home-Secure | 192.168.10.1/24 |
| 20 | IoT | K108-Home-IoT | 192.168.20.1/24 |
| 30 | Guest | (as provisioned) | 192.168.30.1/24 |
| 40 | Lab | (as provisioned) | 192.168.40.1/24 |

**Core devices:** ER605-Gateway (primary), OpenWRT / EAP225s, TL-SG116E / SG2008P, BazzitePC  
**Proxmox Host (Phase 2, live):** Lenovo ThinkCentre M715q Tiny (S/N MJ067MNT) — PVE 9.2.4 node `debian`, **~14.6 GiB RAM (2×8 GB)**, KingSpec 512GB NVMe. CT 100 Wazuh (6G), CT 101 Portainer (6G / 100G) running Portainer + Omada 6.3 + RustDesk + **NetBox v4.7**. See [docs/phases/phase-2-checkpoint-2026-09-16.md](docs/phases/phase-2-checkpoint-2026-09-16.md).  
**Authoritative IPAM:** on-prem NetBox at `http://192.168.0.200:8000` (CT 101). Cloud is archive / reference pending reconcile ([#28](https://github.com/jacob-kraniak/home-network-security/issues/28)).  
**Local NetBox (SoT):** `http://192.168.0.200:8000` — VLAN 1 / mesh only; Cloud archive pending reconcile  
**Public doc:** [docs/network-overview.md](docs/network-overview.md)

## Phase Artifacts Map (Canonical)
**See [docs/phases/PHASE-ARTIFACTS.md](docs/phases/PHASE-ARTIFACTS.md)** for phase ownership of docs and diagrams.

**Return-to-project entry point:** [docs/phases/phase-2-checkpoint-2026-09-16.md](docs/phases/phase-2-checkpoint-2026-09-16.md)  
**Wazuh outage narrative only:** [docs/phases/phase-2-baseline-2026-08-29.md](docs/phases/phase-2-baseline-2026-08-29.md)  
**Phase 3 remote access:** [docs/phases/phase-3-remote-access.md](docs/phases/phase-3-remote-access.md) — **P0** laptop → datacenter off-LAN ([#34](https://github.com/jacob-kraniak/home-network-security/issues/34)); **P1** RustDesk clients on named desktops ([#35](https://github.com/jacob-kraniak/home-network-security/issues/35)). P1 does not satisfy P0.

## Core Goals
- Accurate inventory — **on-prem NetBox is source of truth for live IPs/MACs**
- VLAN segmentation — deployed
- Risk mitigation / transference for IoT
- Self-hosted monitoring (Wazuh live; more services Phase 2)
- Rack build-out; OPNsense/pfSense evaluation in Phase 3
- Off-LAN network path to the rack in Phase 3 (VPN / WireGuard / Tailscale) — P0
- RustDesk sessions to named desktop endpoints — Phase 3 P1, parallel, lower priority

## Key Project Artifacts & Locations

- **Network overview (public):** docs/network-overview.md
- **Master Roadmap:** docs/ROADMAP.md
- **Phase Artifacts Map:** docs/phases/PHASE-ARTIFACTS.md
- **Phase 2 live checkpoint:** docs/phases/phase-2-checkpoint-2026-09-16.md
- **Phase 3 remote access:** docs/phases/phase-3-remote-access.md
- **Inventory:** docs/inventory/devices-summary.md, iot-devices.md
- **Hardware decisions:** docs/hardware/DECISIONS.md
- **Services research:** docs/services/

## Working Guidelines for Grok
- **Always maintain privacy:** sanitize MACs, WAN IPs, credentials. RFC1918 lab addresses in Phase 2 checkpoints are intentional.
- **On-prem NetBox holds live IPAM SoT** — this repo holds architecture, decisions, and redacted summaries. Cloud is archive pending reconcile (Jacob GO 2026-09-21). No live sync from bots without Jacob yes.
- **Do not assume Aug 29 RAM (~7.2 GiB) is current.** Trust Sep 16 checkpoint + devices-summary for live facts. Primary gateway is ER605 V2 only.
- **RustDesk server ≠ Phase 3 P0.** P0 is the L3 path. P1 is clients on named desktops. Do not WAN-publish hbbs/hbbr or admin UIs.
- Update PHASE-ARTIFACTS.md when adding artifacts.
- Small diffs; no drive-by refactors.

## GitHub Project Integration
Main board: https://github.com/users/jacob-kraniak/projects/1

Last Updated: 2026-09-24 (Phase 3 P0 L3 + P1 RustDesk fleet)
