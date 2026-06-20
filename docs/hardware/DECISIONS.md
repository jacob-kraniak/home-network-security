# Hardware Decisions Log (Updated June 20, 2026)

## Completed Purchases (June 2026)

- **Router (Phase 1)**: TP-Link ER605 V2 Wired Gigabit Omada SDN VPN Router 
  - **Details**: Up to 3 WAN Ethernet Ports + 1 USB WAN, VPN Firewall SMB Router, Omada SDN Integrated, Load Balance, Lightning Protection. 
  - **Order**: Amazon Order #111-0504065-9871411 placed June 9, 2026; Delivered June 11, 2026 (left near front door/porch at 108 Uncas St, Ronkonkoma, NY 11779).
  - **Cost**: Item subtotal $49.99; Estimated tax $4.37; Grand Total $54.36. Paid with Prime Visa ending in 9182 (additional rewards) + Amazon gift card balance.
  - **Rationale**: Selected for full Omada SDN integration, multi-WAN load balancing for family internet stability, built-in VPN/firewall, and lightning protection. Strong match for home/SMB use case and future Omada WAP/AP integration in the privacy migration and home lab rack project. (Note: Supersedes earlier FR205 consideration for better SDN/controller features.)

- **PDU (Phase 1 Rack Power)**: StarTech.com 8 Outlet Horizontal 1U Rack Mount PDU Power Strip 
  - **Model**: RKPW081915
  - **Details**: Surge Protection - 120V/15A - w/ 6ft Power Cord. Designed for Network Server Racks.
  - **Order**: Separate Amazon order; Delivered June 11, 2026. Return/replace eligible through July 11, 2026.
  - **Cost**: $67.44
  - **Rationale**: Exact match for planned 1U horizontal PDU in smaller open rack layout. Provides organized surge-protected power for rack gear (router, switch, compute, WAP, etc.), reducing cable clutter and improving reliability/safety in basement setup.

- **Managed Switch (Phase 1)**: TP-Link TL-SG1016DE 16-port Gigabit managed switch with VLAN and Omada SDN support. 
  - **Status**: Onsite; integrated in cutover path. Omada Cloud adoption pending.
  - **Rationale**: Omada-compatible for centralized management and VLAN segmentation (trusted, IoT, guest, work networks). Enables clean rollout per network migration plan.

## Cutover Decision (June 20, 2026)

- **ER605 promoted to primary gateway** replacing Archer A7 as edge router/DHCP server.
  - **Cutover window**: ~11:45 AM ET; <30 min downtime.
  - **Verified**: 320/320 Mbps on Verizon FIOS.
  - **Gateway**: `192.168.0.1` (ER605 LAN MAC `58:04:4f:37:b9:cb`).
  - **Rollback**: ER605 config exportable; Archer A7 retained for AP conversion fallback.
  - **Documentation**: [Post-Cutover-Network-Stabilization-and-Provisioning.md](../Post-Cutover-Network-Stabilization-and-Provisioning.md)

## Planned / Approved (Future Phases)

- **Compute (Phase 2)**: Dell OptiPlex 7060 Micro (Renewed, i7-8700T, 32GB RAM, 1TB NVMe SSD) as primary Proxmox host for self-hosted services (Wazuh, Jellyfin, etc.).
- Patch panel and cabling accessories.

## Rationale Summary
- **TP-Link Omada ecosystem** chosen for balance of features, warranty/support, simple management UI, fast recovery/rollback options (important for family network), and centralized SDN control (controller can later run self-hosted on Proxmox).
- **Rack infrastructure** (PDU, measurements, layout) prioritized for clean, scalable basement installation supporting both current TP-Link gear and future open-source routing/compute.
- Refurb enterprise-grade mini PC selected for low power draw, reliability, and expandability.

**Cross-References**:
- Rack layout & Phase details: [RACK.md](RACK.md)
- Rack build overview & acquired gear: [home-lab-rack-build.md](home-lab-rack-build.md)
- Measurements: [rack-measurements.md](rack-measurements.md)
- Infrastructure criteria: [infrastructure-criteria.md](infrastructure-criteria.md)
- Project README & inventory notes: [../README.md](../README.md)
- GROK-WORKSPACE.md for workflow guidelines.
