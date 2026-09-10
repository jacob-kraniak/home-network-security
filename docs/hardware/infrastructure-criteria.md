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

## Revised Core Infrastructure Strategy (Final State June 2026 / corrected September 2026)

- **Deployed TP-Link Omada SDN (Phase 1 Complete)**: **ER605 V2** gateway + SG2008P v3.20 switch (K108-MSW-1) + EAP225 APs providing centralized control with VLANs (vid 10 Secure "K108-Home-Secure", vid 20 IoT "K108-Home-IoT"). 21 clients (June Omada snapshot).
- **Exceptions**:
  - Ring Base Station (upstairs) — kept for family armed status light visibility.
  - Wireless devices connect via EAP225 WAPs on IoT/Secure SSIDs.
- **Compute (Phase 2, live):** Lenovo ThinkCentre M715q Tiny on PVE 9.2.4 (not Dell OptiPlex as hypervisor). See Phase 2 checkpoint.
- **APs:** TP-Link EAP225 (office live; other conversions tracked in inventory).

This design (Omada SDN + Proxmox) maximizes security/privacy with VLAN isolation and family stability. Links fixed to /docs subdirs.

**Final Device Stats (Phase 1):** 2 APs (EAP225), 1 switch (SG2008P v3.20), 1 gateway (**ER605 V2**); clients on vid10/20/1.
