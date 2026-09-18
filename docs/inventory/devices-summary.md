# Hardware & Project Inventory Summary

**Project:** Home Network Security / Privacy Migration / Basement Rack Build  
**Last Updated:** September 16, 2026  
**Purpose:** Hardware inventory (purchased, existing, planned). Live IPs stay in NetBox except RFC1918 lab notes in Phase 2 checkpoints.

## Project Cost Tracker (Known Purchases to Date)

**Total Confirmed Project Spend: $277.43** (as of June 12, 2026) + $0 for Proxmox host (employer surplus)

| Date | Item | Cost (USD) | Notes |
|------|------|------------|-------|
| June 2026 | Both Network Racks | 60.00 | Facebook Marketplace pair |
| June 2026 | Steel and Wood Table | 100.00 | Basement workspace |
| 2026-06-09 | TP-Link ER605 V2 | 49.99 | Primary gateway |
| 2026-06-11 | StarTech 8-outlet 1U PDU | 67.44 | Rack power |
| 2026-07-09/10 | Lenovo ThinkCentre M715q Tiny (Proxmox host) | 0.00 | Free employer surplus (S/N MJ067MNT); KingSpec 512GB NVMe; SanDisk Z400 planned — still not detected |

## Hardware Inventory by Category

**Status Legend:** 🟢 Acquired | 🔵 Planned | ⚪ Existing | 🟡 In Progress

### Core Networking

| Device | Model | Status | Role / Notes |
|--------|-------|--------|--------------|
| Primary Gateway | TP-Link ER605 V2 (K108-ER605-Gateway) | 🟢 Active | On-prem Omada 6.3 (CT 101). VLAN 1/10/20 (+30/40). `192.168.0.1` |
| Omada Controller | `mbentley/omada-controller:6.3` on CT 101 | 🟢 Active | `https://192.168.0.200:8043`. Cloud CBC closed 2026-09-14 |
| NetBox (local) | `netboxcommunity/netbox:v4.7-5.1.1` on CT 101 | 🟢 Active service | `http://192.168.0.200:8000`. Empty until Cloud import. Cloud still IPAM SoT. |
| VLAN Termination | OpenWRT-AP | 🟢 Active | `br-lan.1/.10/.20` |
| Managed Switch | K108-MSW-1 | 🟢 Active | Omada-managed; `192.168.0.102` |
| Distribution Switch | TP-Link TL-SG105 | 🟢 Active | Office branch |
| Patch Panel | 16-port | 🟡 Active | PP# = switch port # |
| ISP ONT | Verizon FIOS ONT | ⚪ Existing | Upstream of ER605 WAN |
| Backup Switch | Cisco SG100-16 | ⚪ Existing | Spare |

### Wireless & Access Points

| Device | Model | Status | Role / Notes |
|--------|-------|--------|--------------|
| Living Room AP | K108_WAP1_LivingRoom | 🟢 Active | Omada; `192.168.0.101` |
| Office AP | K108_WAP2_Office (EAP225 class) | 🟢 Active | Omada; `192.168.0.100` |
| Upstairs AP | TP-Link Archer A7 | 🟡 Planned | AP conversion pending |

### Compute & Services Hosts

| Device | Model | Status | Role / Notes |
|--------|-------|--------|--------------|
| BazzitePC | MSI B450M / Ryzen 5 / GTX 1070 | ⚪ Existing | Primary workstation; Wazuh agent 005 |
| Raspberry Pi 3 | Pi 3 Model B | ⚪ Repurposed | Temp basement host |
| **Proxmox Host** | **Lenovo ThinkCentre M715q Tiny (10M3000PUS / S/N MJ067MNT)** | 🟢 **Live PVE 9.2.4** | AMD PRO A12-9800E (4C). **RAM: 2×8 GB DDR4 SO-DIMM (~14.6 GiB).** KingSpec 512GB NVMe. Node `debian`. CT 100 Wazuh 6G; CT 101 Portainer 6G/100G + Omada + RustDesk + NetBox. |
| Dev Laptop | ThinkPad X380 Yoga (Kali) | ⚪ Existing | Security testing; agent 002 |
| Spouse laptop | Windows 10 22H2 (Christines_Laptop) | ⚪ Existing | Wazuh agent 006; `192.168.10.101` |
| Work Laptop | ThinkPad P14s Gen 4 | ⚪ Existing | Day job |

### Storage

| Device | Model | Status | Role / Notes |
|--------|-------|--------|--------------|
| External HDD | Seagate Backup+ Desk 3TB (S/N NA5KMDT1) | 🟢 **Mounted 2026-09-05** | USB `/dev/sda`, exFAT `sda2` UUID `531C-AD38` at `/mnt/seagate3tb`. USB 2. Backup/media only — not PVE VM disks. |

### Rack & Power

| Device | Status | Notes |
|--------|--------|-------|
| Large Enclosed Rack | 🟢 Acquired | Future Proxmox/NAS |
| Smaller Open Rack | 🟢 Acquired | Network stack |
| StarTech PDU | 🟢 Acquired | 8-outlet 1U |

**Related:** [ROADMAP.md](../ROADMAP.md) · [phase-2-checkpoint-2026-09-16.md](../phases/phase-2-checkpoint-2026-09-16.md) · [phase-2-checkpoint-2026-09-14.md](../phases/phase-2-checkpoint-2026-09-14.md)

---
*Public-safe hardware summary. NetBox Cloud remains authoritative for IPAM until local import.*
