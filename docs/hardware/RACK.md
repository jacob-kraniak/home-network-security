# Rack & Physical Infrastructure (Updated June 12, 2026)

## Phase 1 Layout (Hardware Acquired / In Progress)

- **Gateway/Router**: TP-Link ER605 V2 Omada SDN Integrated Gigabit VPN Router (purchased June 9, 2026; delivered June 11, 2026; $49.99). Primary multi-WAN gateway with load balancing, VPN, firewall, and Omada SDN support. Compact form factor suitable for shelf or initial rack placement.

- **Switch**: TP-Link TL-SG1016DE (planned; 16-port Gigabit managed switch with VLAN/Omada SDN support for segmentation).

- **PDU**: StarTech.com 8 Outlet Horizontal 1U Rack Mount PDU Power Strip (model RKPW081915) - Surge Protection, 120V/15A, 6ft Power Cord (purchased & delivered June 11, 2026; $67.44). Ready for 1U horizontal mounting.

- **Patch Panel**: 24-port Cat6 (planned for organized terminations).

- **Cabling**: Monoprice Cat6 or existing stock (planned for color-coded VLAN runs: Trusted/Main, IoT, Guest, Work).

## Phase 2 Additions (Planned)

- Mount Dell OptiPlex 7060 Micro (or equivalent miniPC) on additional shelf space or in large enclosed rack.
- Cable management accessories, labels, and velcro for professional organization.
- Cooling considerations (fans, airflow) especially if using enclosed rack section.

**Current Status (Post June 11 Delivery)**:
- Both ER605 V2 router and StarTech PDU have been received (packages left near front door/porch).
- **Immediate Actions**: Mount PDU in 1U slot of smaller open rack (~8-9U). Position ER605 for easy port access (WAN1/2/3, LAN, USB). Connect to power via PDU once mounted. Basic config and connectivity test.
- Integrates with existing home network; supports future Omada WAP and centralized management.
- Aligns with overall privacy migration (VLANs, monitoring via Wazuh on Bazzite/Proxmox) and home lab goals.

**References**:
- See [`../diagrams/`](../diagrams/) for visual layout, topology diagrams (update post-install).
- Hardware decisions, purchase logs & rationale: [DECISIONS.md](DECISIONS.md)
- Detailed rack build, measurements & acquired equipment inventory: [home-lab-rack-build.md](home-lab-rack-build.md)
- Project board: https://github.com/users/jacob-kraniak/projects/1