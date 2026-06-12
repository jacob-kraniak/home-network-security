# Hardware & Project Inventory Summary

**Project:** Home Network Security / Privacy Migration / Basement Rack Build  
**Last Updated:** June 12, 2026  
**Purpose:** Master single-source inventory of all hardware (purchased, existing, planned) relevant to Phase 1 networking (ER605 + Omada), rack infrastructure, power, compute for self-hosted services (Proxmox/Wazuh/Jellyfin/etc.), and overall privacy/security goals. Includes cost tracking for project expenditure.

> **Note on Sensitivity:** This file contains only high-level, non-sensitive summaries (models, roles, status, costs). Live discovered devices with MAC addresses, hostnames, or IPs remain in local/gitignored `docs/inventory/*.xml` files (nmap, services, etc.). See `iot-devices.md` for IoT-specific risk tracking.

## Project Cost Tracker (Known Purchases to Date)

**Total Confirmed Project Spend: $117.43** (as of June 12, 2026)

Only direct purchases made specifically for this project are tracked here. Pre-existing personal hardware, racks, and stock cabling are noted as "Existing (pre-project)" with N/A cost.

| Date       | Item                                              | Order / Vendor                  | Cost (USD) | Cumulative | Delivery / Notes                          |
|------------|---------------------------------------------------|---------------------------------|------------|------------|-------------------------------------------|
| 2026-06-09 | TP-Link ER605 V2 Omada Gigabit VPN Router        | Amazon #111-0504065-9871411    | 49.99     | 49.99     | Delivered 2026-06-11 (front door/porch)  |
| 2026-06-11 | StarTech.com 8-Outlet Horizontal 1U Rack PDU (RKPW081915) | Amazon (separate order)       | 67.44     | **117.43** | Delivered 2026-06-11; surge protection, 6ft cord |

**Future / Planned Additions (will be added when purchased):**
- TP-Link TL-SG1016DE 16-port managed switch
- Dell OptiPlex 7060 Micro (or N100/N305-class mini-PC) for Proxmox
- 24-port Cat6 patch panel
- Additional Cat6 cabling, mounting hardware, cable management accessories
- Potential Omada EAP-series WAP

**Cost Notes:**
- Prices reflect actual Amazon subtotals/totals from order confirmations.
- Tax, shipping (usually $0), and any rewards/gift card usage noted in detailed logs (see `DECISIONS.md` and order screenshots in chat history).
- No estimates included in the running total until actual purchase.

## Hardware Inventory by Category

**Status Legend**  
🟢 **Acquired** — Purchased and received for this project  
🔵 **Planned** — Approved/roadmapped for future purchase  
⚪ **Existing / Repurposed** — Owned prior to project or moved from elsewhere  
🟡 **In Progress** — Partially deployed or configuring

### Rack Infrastructure (Physical)

| Device                  | Model / Specs                                      | Status | Acquired      | Cost   | Location                  | Role / Notes                                      |
|-------------------------|----------------------------------------------------|--------|---------------|--------|---------------------------|---------------------------------------------------|
| Large Enclosed Rack    | ~21" H cabinet-style (~12-15U equiv), 19" wide   | ⚪ Existing | Pre-project  | N/A   | Basement (cinder block wall area) | Future compute/storage (Proxmox host, NAS)       |
| Smaller Open Rack      | ~15.5" H open-frame (~8-9U equiv), 19" wide, shallow | ⚪ Existing | Pre-project  | N/A   | Basement (currently on bins)     | Primary Phase 1 target: networking, PDU, patch panel, mini-PC |

### Power Distribution

| Device                  | Model / Specs                                      | Status | Acquired      | Cost   | Location                  | Role / Notes                                      |
|-------------------------|----------------------------------------------------|--------|---------------|--------|---------------------------|---------------------------------------------------|
| Rack PDU               | StarTech.com 8 Outlet Horizontal 1U (RKPW081915), surge prot., 120V/15A, 6ft cord | 🟢 Acquired | 2026-06-11   | 67.44 | Smaller open rack (1U slot) | Centralized clean power + surge protection for all rack equipment. See `home-lab-rack-build.md` |

### Core Networking (Gateway, Switch, Termination)

| Device                  | Model / Specs                                      | Status | Acquired      | Cost   | Location                  | Role / Notes                                      |
|-------------------------|----------------------------------------------------|--------|---------------|--------|---------------------------|---------------------------------------------------|
| Primary Gateway / Router | TP-Link ER605 V2 Omada SDN Gigabit VPN Router (3x WAN + 1x USB WAN, load balance, VPN firewall, lightning protection) | 🟢 Acquired | 2026-06-11   | 49.99 | Smaller open rack / shelf (initial) | Phase 1 edge device. Multi-WAN stability, Omada SDN ready, basic segmentation/VPN. See `DECISIONS.md`, `RACK.md` |
| Managed Switch         | TP-Link TL-SG1016DE (16-port Gigabit, VLAN + Omada support) | 🔵 Planned | TBD          | TBD   | Smaller open rack        | VLAN segmentation, managed switching for trusted/IoT/guest/work networks |
| Patch Panel            | 24-port Cat6                                       | 🔵 Planned | TBD          | TBD   | Smaller open rack        | Organized cable terminations and labeling        |
| ISP ONT (FIOS)         | ISP-provided Optical Network Terminal              | ⚪ Existing (to relocate) | N/A       | N/A   | Move to rack area        | Will be relocated to basement rack per infrastructure criteria |

### Wireless & Access Points

| Device                  | Model / Specs                                      | Status | Acquired      | Cost   | Location                  | Role / Notes                                      |
|-------------------------|----------------------------------------------------|--------|---------------|--------|---------------------------|---------------------------------------------------|
| Repurposed AP          | TP-Link Archer A7 (AP mode only)                   | ⚪ Existing / Repurposed | Pre-project | N/A   | Strategic location (TBD) | Dedicated access point to reduce IoT/main mixing. See `infrastructure-criteria.md` |
| Omada WAP / EAP        | TBD (Omada SDN compatible EAP series)              | 🔵 Planned | TBD          | TBD   | Rack / ceiling mount     | Future expansion of Omada centralized management |

### Compute & Services Hosts

| Device                  | Model / Specs                                      | Status | Acquired      | Cost   | Location                  | Role / Notes                                      |
|-------------------------|----------------------------------------------------|--------|---------------|--------|---------------------------|---------------------------------------------------|
| Primary Daily Driver (Bazzite) | MSI B450M DS3H, Ryzen 5 2600X, 16GB DDR4, GTX 1070, Bazzite Linux (immutable) | ⚪ Existing | Feb 2024    | N/A (personal) | Desk / home office       | Current Wazuh/Podman testing + daily use. May partially integrate or remain separate |
| Primary Proxmox Host   | Dell OptiPlex 7060 Micro (or N100/N305-class mini-PC), i7-8700T or equiv, 32GB RAM, 1TB NVMe (renewed or new) | 🔵 Planned (Phase 2) | TBD       | ~200-400 (est.) | Large enclosed or small rack | Low-power always-on host for Wazuh, Jellyfin, Home Assistant, AdGuard, WireGuard, document archive, etc. Preferred over full rack servers for efficiency |
| Dev / Testing          | Lenovo ThinkPad X380 Yoga (Kali Linux)             | ⚪ Existing | ~2018?      | N/A   | Portable                 | Security testing, lab work                       |
| Work Laptop            | Lenovo ThinkPad P14s Gen 4 (i7-1370P, 32GB, RTX A500, Win11) | ⚪ Existing | 202?        | N/A   | Not rack-mounted         | Day job + occasional lab access                  |

### Cabling, Accessories & Misc (Planned / Stock)

| Device                  | Model / Specs                                      | Status | Acquired      | Cost   | Location                  | Role / Notes                                      |
|-------------------------|----------------------------------------------------|--------|---------------|--------|---------------------------|---------------------------------------------------|
| Ethernet Cabling       | Monoprice Cat6 (or existing stock)                 | 🔵 Planned / Partial Existing | TBD     | TBD   | Rack runs                | Color-coded by VLAN where possible (Trusted/Main, IoT, Guest, Work) |
| Cable Management       | Velcro, ties, labels, organizers                   | 🔵 Planned | TBD          | TBD   | Rack                     | Professional appearance and maintainability      |
| Mounting Hardware      | Rails, shelves, brackets (as needed for open rack) | 🔵 Planned | TBD          | TBD   | Rack                     | Secure mounting of non-1U gear                   |

## How to Maintain This Inventory
1. When a new purchase is made → Add row to Cost Tracker table + corresponding hardware row (update Status to 🟢 Acquired, fill Cost).
2. When status changes (e.g., installed, configured) → Update Status column and add note with date.
3. Cross-reference major changes in `DECISIONS.md`, `RACK.md`, `home-lab-rack-build.md`, and `ROADMAP.md`.
4. For detailed live network scans → Keep raw XMLs local-only (gitignored); add sanitized summaries here only if useful.
5. Link related GitHub issues to the Privacy Migration project board (`track:network-rack` label).

**Related Documentation**
- [Home Lab Rack Build Details & Install Steps](hardware/home-lab-rack-build.md)
- [Rack Layout & Phase 1](hardware/RACK.md)
- [Hardware Decisions & Rationale](hardware/DECISIONS.md)
- [Infrastructure Criteria & Power Strategy](hardware/infrastructure-criteria.md)
- [Rack Measurements](hardware/rack-measurements.md)
- [IoT Devices & Risk Treatment](inventory/iot-devices.md)
- [Project Roadmap](ROADMAP.md)
- [Main README](../README.md) and [GROK-WORKSPACE.md](../GROK-WORKSPACE.md)

**Diagrams:** See `docs/diagrams/` (update after physical rack install and ER605 configuration).

---
*This file fulfills the "Current Inventory: docs/inventory/devices-summary.md" reference in the project workspace instructions.*