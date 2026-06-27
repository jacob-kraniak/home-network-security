## Server Hardware Decision - Rack Server vs Mini-PC

### Assessment
- Full rack-mount servers (Dell PowerEdge etc.): **Overkill** for current needs (Wazuh, Home Assistant, Frigate, light VMs).
- Primary Concern: Power consumption (150-300W idle vs 15-40W on modern mini-PCs).
- Noise, heat, and electricity cost make them suboptimal for always-on home use.

### Recommended Path
**Primary Host**: Low-power mini-PC or SFF PC for Proxmox (N100/N305/AMD equivalents).
- Reuse existing 2.5" SSDs where possible.
- Dell SAS HDDs: Consider only if building a separate storage node (e.g., TrueNAS) with spin-down.

**When Rack Server Might Make Sense**:
- Heavy storage needs (10+ drives)
- Advanced homelab / certification practice (future education track)
- If acquired very cheap with low-power CPUs (rare)

**Current Direction**: Prioritize efficiency. Use rack space for networking gear, UPS, and clean cable management first.

Status: Decision documented 2026-06-03

## Revised Core Infrastructure Strategy (Final State June 2026)

- **Deployed TP-Link Omada SDN (Phase 1 Complete)**: FR205 Multi-WAN router + TL-SG1016DE switch (K108-MSW-1) + 2x EAP225 v4 APs (K108_WAP1_LivingRoom, K108_WAP2_Office) providing centralized control with VLANs (vid 10 Secure "K108-Home-Secure", vid 20 IoT "K108-Home-IoT"). 21 clients (clientStat/clientTypeStat per JSON: smartHome 10 TP-Link Kasa, camera 2 Wyze etc., office 4 incl. BazzitePC desktop/Lenovo Clock, 2 wired/19 wireless).
- **Exceptions**:
  - Ring Base Station (upstairs) — kept for family armed status light visibility (as before).
  - Wireless devices (Kasa 10+, Nest incl. Lenovo Clock, phones, cameras) connect via EAP225 WAPs on IoT/Secure SSIDs.
- **Compute (Phase 2)**: Dell OptiPlex 7060 Micro (i7-8700T, 32GB RAM, 1TB NVMe) deployed as Proxmox services host (BazzitePC or associated; wired client e0:d5:5e:e3:98:97 on Management vid1). Future: OPNsense on dedicated + Aoostar WTR Pro hybrid NAS (Phase 3).
- **Repurposed/Current**: TP-Link EAP225 APs (no Archer A7 in final; previous assumptions updated). FR205 retained as primary/warm spare.

This design (Omada SDN + Proxmox) maximizes security/privacy with VLAN isolation, family stability (TP-Link warranty/recovery), and single pane (Omada controller + Proxmox). 21 clients confirm success (see JSON data for full list: HS220, Wyze "Baby Cam", Lenovo Clock, Digital Frame, BazzitePC, etc.). Links fixed to /docs subdirs.

**Final Device Stats**: 2 APs (EAP225, fw 5.2.2), 1 switch (TL-SG1016DE), 1 gateway (FR205); clients on vid10/20/1 with rssi/signal/traffic details.
