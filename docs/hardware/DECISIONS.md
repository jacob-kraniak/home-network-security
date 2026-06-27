# Hardware Decisions Log (Updated June 2026 - Final Buildout per Omada JSON)

## Deployed Hardware (Final Buildout - June 2026)
- **Router/Gateway (Phase 1)**: TP-Link FR205 (Multi-WAN) - deployed as core router (public IP 173.56.71.104, handling WAN for Omada SDN).
- **Core Switch**: TP-Link SG2008P v3.20 (K108-MSW-1)
  - Serial Number: Y25A081000375
  - MAC Address: 10:5a:95:3a:16:b4
  - IP Address: 192.168.0.146
  - Firmware: 3.20.24 Build 20260509 Rel.2353
  - Uptime (as of data): 4day(s) 3h 31m 52s
  - VLAN capable, Omada integrated.
- **APs**: 2x TP-Link EAP225 v4 (K108_WAP1_LivingRoom "58:04:4f:dc:ce:72", K108_WAP2_Office "5c:e9:31:6c:b5:44") - deployed, EAP225 US v4.0, 2 APs in deviceStat, running 5.2.2 firmware, providing K108-Home-Secure (vid10) and K108-Home-IoT (vid20) SSIDs. Channel/radio details per JSON (e.g., 2.4G ch11 40MHz, 5G ch48 80MHz).
- **Compute/Services Host (Phase 2)**: Dell OptiPlex 7060 Micro (i7-8700T, 32GB RAM, 1TB NVMe) as primary Proxmox host - deployed (associated with "BazzitePC" wired client e0:d5:5e:e3:98:97 or compute; model B450m DSH3 noted in client data). 1 wired desktop/compute client.
- **Clients/Inventory (from Omada controller)**: 21 total (2 wired, 19 wireless; clientStat: ipc:2 camera, noData:19, wired:2, wireless:19). clientTypeStat: audioVideo:1, camera:2 (WyzeCam v3 "Baby Cam" d0:3f:27:2b:2b:53 +), mobile:1, office:4 (Lenovo Smart Clock bc:df:58:b3:b2:c0 "Bedroom Clock", BazzitePC, etc.), other:3, smartHome:10 (TP-Link Kasa HS220/HS105 e.g. 50:91:e3:48:b3:2b "DIMM1-Dining-Room", "1A-5D-BE-06-32-C6" etc. on IoT). Full list in controller JSON (names, IPs on vid 10/20/1, rssi, traffic, etc.).

## Rationale (Updated for Final State)
- TP-Link Omada (FR205 + SG2008P v3.20 + 2x EAP225) chosen and deployed for vendor warranty, simple UI, fast recovery, Multi-WAN, VLAN (vid10 Secure, vid20 IoT), and family network priority (Phase 1 complete per JSON deviceStat: 2 APs, 1 switch, 1 gateway).
- Refurb OptiPlex Micro selected/deployed for Proxmox (reliability, low power ~15-40W, upgradability); BazzitePC client confirms compute active.
- 21 clients across categories confirm smartHome/IoT isolation on vid20, office/compute on Secure/Management.
- Single NIC on services host acceptable (downstream from router/switch).

**Links**:
- Related inventory/measurements: [rack-measurements.md](rack-measurements.md)
- Rack layout: [RACK.md](RACK.md) (in this directory)
- Diagrams: [`../diagrams/`](../diagrams/)
- Root status: [README.md](../../README.md#project-status-update-june-2026)
- Controller data (final state): project notes / JSON (2 EAP225, SG2008P v3.20, FR205, 21 clients with exact mac/ip/vid/rssi/traffic)
