# Hardware & Project Inventory Summary

**Project:** Home Network Security / Privacy Migration / Basement Rack Build  
**Last Updated:** June 20, 2026  
**Purpose:** Master single-source inventory of hardware (purchased, existing, planned). **Live host IPs/MACs are in private NetBox only** — see [network-overview.md](../network-overview.md).

> **Sensitivity:** This file contains models, roles, status, and costs only. DHCP tables, MACs, and exact IPs remain in [NetBox Cloud](https://arfv7221.cloud.netboxapp.com/) and local/gitignored scan files.

## Project Cost Tracker (Known Purchases to Date)

**Total Confirmed Project Spend: $277.43** (as of June 12, 2026)

| Date | Item | Cost (USD) | Notes |
|------|------|------------|-------|
| June 2026 | Both Network Racks | 60.00 | Facebook Marketplace pair |
| June 2026 | Steel and Wood Table | 100.00 | Basement workspace |
| 2026-06-09 | TP-Link ER605 V2 | 49.99 | Primary gateway |
| 2026-06-11 | StarTech 8-outlet 1U PDU | 67.44 | Rack power |

## Hardware Inventory by Category

**Status Legend:** 🟢 Acquired | 🔵 Planned | ⚪ Existing | 🟡 In Progress

### Core Networking

| Device | Model | Status | Role / Notes |
|--------|-------|--------|--------------|
| Primary Gateway | TP-Link ER605 V2 | 🟢 Active | Omada SDN; VLAN 1/10/20 tagging; cutover 2026-06-20 |
| VLAN Termination | OpenWRT-AP | 🟢 Active | `br-lan.1/.10/.20` subinterfaces |
| Managed Switch | TP-Link TL-SG116E v2 | 🟢 Active | 16-port Easy Smart; patch panel 1:1 |
| Distribution Switch | TP-Link TL-SG105 | 🟢 Active | Office branch switch |
| Patch Panel | 16-port (active runs) | 🟡 Active | PP# = switch port # |
| ISP ONT | Verizon FIOS ONT | ⚪ Existing | Upstream of ER605 WAN |
| Backup Switch | Cisco SG100-16 | ⚪ Existing | Secondary / spare |

### Wireless & Access Points

| Device | Model | Status | Role / Notes |
|--------|-------|--------|--------------|
| Office AP | TP-Link EAP225 v4 (K108_WAP2_Office) | 🟢 Active | Omada; LAN-Secure segment |
| Upstairs AP | TP-Link Archer A7 | 🟡 Planned | AP conversion pending |

### Compute & Services Hosts

| Device | Model | Status | Role / Notes |
|--------|-------|--------|--------------|
| BazzitePC | MSI B450M / Ryzen 5 / GTX 1070 | ⚪ Existing | Primary workstation; Wazuh/Podman testing |
| Raspberry Pi 3 | Pi 3 Model B | ⚪ Repurposed | Temp basement host (switch port 2) |
| Proxmox Host | Dell OptiPlex 7060 Micro (planned) | 🔵 Phase 2 | Wazuh, Jellyfin, HA, etc. |
| Dev Laptop | ThinkPad X380 Yoga (Kali) | ⚪ Existing | Security testing |
| Work Laptop | ThinkPad P14s Gen 4 | ⚪ Existing | Day job |

### Rack & Power

| Device | Status | Notes |
|--------|--------|-------|
| Large Enclosed Rack | 🟢 Acquired | Future Proxmox/NAS |
| Smaller Open Rack | 🟢 Acquired | Network stack (ER605, switch, PDU) |
| StarTech PDU | 🟢 Acquired | 8-outlet 1U |

## How to Maintain

1. New purchase → Cost Tracker + hardware row.
2. Live network changes → update **NetBox** via `netbox-nmap-scan` scripts; update this file for hardware/status only.
3. Cross-reference `DECISIONS.md`, `RACK.md`, `ROADMAP.md`.

**Related:** [network-overview.md](../network-overview.md) · [NetBox Inventory Progress](../NetBox-Inventory-Progress.md) · [ROADMAP.md](../ROADMAP.md)

---
*Public-safe hardware summary. NetBox is authoritative for IPAM.*
