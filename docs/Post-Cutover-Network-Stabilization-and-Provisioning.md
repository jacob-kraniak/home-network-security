# Post-Cutover Network Stabilization and Provisioning

**Last updated:** 2026-09-15  
**Site:** Kraniak Home  
**Public summary:** [network-overview.md](network-overview.md)  
**Focus:** Stability → VLAN segmentation → Omada management → Phase 2 services

---

## Cutover Summary

| Item | Detail |
|------|--------|
| **Status** | Successfully completed |
| **Date / time** | 2026-06-20, ~11:45 AM ET |
| **Downtime** | < 30 minutes |
| **Primary gateway** | TP-Link **ER605-Gateway** |
| **Upstream** | Verizon FIOS ONT → ER605 WAN |
| **Speed verification** | **320 / 320 Mbps** |

### What changed

- **Archer A7** stepped down as primary router; **ER605** is edge gateway and DHCP server.
- **VLAN segmentation deployed** (June cutover used early naming). **Current Omada SoT (2026-09-15):** Management (1), Trusted (10), IoT (20), Guest (30), Lab (40) — see table below.
- **NetBox inventory** synced to production state (~52 devices). Public repo redacted.
- Physical topology: **ONT → ER605 → OpenWRT → TL-SG116E → clients / APs**.

---

## Stabilization Checklist

- [x] ER605 online as gateway
- [x] Internet throughput verified (320/320 Mbps)
- [x] Core clients receiving DHCP
- [x] **VLAN design applied** (VID 1/10/20/30/40 — Omada SoT 2026-09-15)
- [x] **NetBox topology updated** — see [NetBox-Inventory-Progress.md](NetBox-Inventory-Progress.md)
- [x] OpenWRT-AP + subinterfaces documented in NetBox
- [ ] **ER605 + EAP225 + TL-SG116E adopted in Omada Cloud** (PRECONFIGURED → Online)
- [ ] **DHCP reservations** for critical infrastructure MACs
- [ ] **Archer A7 converted to Access Point mode**
- [ ] Re-run inventory sync after Omada adoption settles

---

## VLAN Plan (current Omada SoT — 2026-09-15)

| VID | Omada name | Gateway / prefix | Typical SSID |
|-----|------------|------------------|--------------|
| 1 | Management (Default) | 192.168.0.1/24 | (mgmt / wired) |
| 10 | Trusted | 192.168.10.1/24 | K108-Home-Secure |
| 20 | IoT | 192.168.20.1/24 | K108-Home-IoT |
| 30 | Guest | 192.168.30.1/24 | K108-Guest (as provisioned) |
| 40 | Lab | 192.168.40.1/24 | (as provisioned) |

> June 2026 cutover notes below this file historically labeled VID 10 as IoT and VID 20 as Guest. That mapping is **obsolete** — do not use it for new work.

Firewall rules between segments: configure per IoT risk register.

---

## Archer A7 → Access Point Conversion

**Goal:** Repurpose Archer A7 as downstream WAP only.

### Prerequisites

- ER605 stable as sole gateway
- Reserved management IP on LAN-Secure (see NetBox)

### Steps (summary)

1. Disable DHCP and routing on Archer A7.
2. Set static management IP on LAN-Secure.
3. Connect LAN port to switch infrastructure.
4. Update NetBox role to WAP; remove stale router cables.

---

## Omada Cloud Adoption

Adopt in order: ER605 → TL-SG116E → EAP225 (K108_WAP2_Office). Export ER605 config before major changes.

---

## Related Documentation

- [Network Overview](network-overview.md)
- [NetBox Inventory Progress](NetBox-Inventory-Progress.md)
- [Devices Summary](inventory/devices-summary.md)
- [Roadmap](ROADMAP.md)
- [Automation repo](https://github.com/jacob-kraniak/netbox-nmap-scan)
