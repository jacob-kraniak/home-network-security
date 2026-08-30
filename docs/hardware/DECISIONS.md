# Hardware Decisions Log (Updated August 29, 2026)

## Deployed Hardware (Final Buildout - June 2026 + July/August Proxmox Host)
- **Router/Gateway (Phase 1)**: TP-Link FR205 (Multi-WAN) - deployed as core router (handling WAN for Omada SDN).
- **Core Switch**: TP-Link SG2008P v3.20 (K108-MSW-1)
  - Serial Number: Y25A081000375
  - MAC Address: 10:5a:95:3a:16:b4
  - IP Address: 192.168.0.146
  - Firmware: 3.20.24 Build 20260509 Rel.2353
  - VLAN capable, Omada integrated.
- **APs**: 2x TP-Link EAP225 v4 (K108_WAP1_LivingRoom, K108_WAP2_Office) - deployed, providing K108-Home-Secure (vid10) and K108-Home-IoT (vid20) SSIDs.
- **Compute/Services Host (Phase 2)**: **Lenovo ThinkCentre M715q Tiny** (type 10M3000PUS, S/N MJ067MNT) — acquired free 2026-07-09/10 as retired employer surplus. **Live 2026-08-29:** PVE 9.2.4 node `debian`. CPU **AMD PRO A12-9800E R7 (4C+8G)**, not a generic “Ryzen PRO 16GB” story. **RAM observed ~7.2 GiB.** KingSpec 512GB NVMe is the only disk the OS sees. SanDisk Z400 256GB 2.5" **not detected** — RAID1 plan is on hold. Dual DisplayPort. Replaces previously planned Dell OptiPlex 7060 Micro as the hypervisor. Support page: https://pcsupport.lenovo.com/us/en/products/desktops-and-all-in-ones/thinkcentre-m-series-desktops/m715q/10m3/10m3000pus/mj067mnt.
- **Phase 2 guests (live):** CT 100 Wazuh AIO 4.8.2; CT 101 Debian + Portainer. Details in [phase-2-baseline-2026-08-29.md](../phases/phase-2-baseline-2026-08-29.md).
- **Clients/Inventory (from Omada controller, June snapshot):** 21 total (2 wired, 19 wireless). Full list belongs in NetBox / controller JSON, not this log.

## Rationale (Updated for Final State + Free Proxmox Host)
- TP-Link Omada (FR205 + SG2008P v3.20 + 2x EAP225) chosen and deployed for vendor warranty, simple UI, fast recovery, Multi-WAN, VLAN (vid10 Secure, vid20 IoT), and family network priority (Phase 1 complete).
- **Lenovo M715q Tiny selected/acquired free** for Proxmox (familiar employer hardware, low power, Tiny form factor). Cost $0 vs planned refurb purchase.
- **Constraint recorded 2026-08-29:** this APU + ~8GB class RAM is enough for PVE + Wazuh AIO + Portainer only if Wazuh stays at 4G and no heavy media stacks share the box. Plan additional RAM or a second host before Jellyfin/Immich/HA.
- 21 clients across categories confirm smartHome/IoT isolation on vid20, office/compute on Secure/Management.
- Single NIC on services host acceptable (downstream from router/switch).

**Links**:
- Related inventory/measurements: [rack-measurements.md](rack-measurements.md)
- Rack layout: [RACK.md](RACK.md) (in this directory)
- Phase 2 live baseline: [`../phases/phase-2-baseline-2026-08-29.md`](../phases/phase-2-baseline-2026-08-29.md)
- Diagrams: [`../diagrams/`](../diagrams/)
- Root status: [README.md](../../README.md)
