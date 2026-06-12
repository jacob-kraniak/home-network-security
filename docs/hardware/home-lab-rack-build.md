# Home Lab Basement Rack Build

## Overview
Project for organizing and mounting home lab equipment (Bazzite/Podman/Wazuh + Proxmox/Jellyfin home lab, miniPC container host, Omada WAP, core networking gear) in the basement. Aligns with privacy migration, network segmentation (VLANs: Trusted/Main, IoT, Guest, Work), self-hosted monitoring (Wazuh), and cybersecurity home infrastructure goals.

**Last Updated:** June 12, 2026

## Rack Inventory & Measurements (Confirmed)

### Large Enclosed Rack
- **Type**: Fully enclosed on all sides (cabinet-style)
- **Height**: 21 inches (~12-15U equivalent, based on standard 1.75" per U)
- **Width**: 19" rack-mount standard
- **Depth**: To be confirmed (suitable for deeper servers/gear)
- **Status**: Available in basement, stacked or positioned near cinder block wall
- **Notes**: Good for core servers (Proxmox host), storage, or protected/sensitive equipment. Future expansion space.

### Smaller Open Rack
- **Type**: Open-frame / 2-post style
- **Height**: ~15.5 inches (~8-9U equivalent)
- **Width**: 19" rack-mount standard
- **Depth**: Shallow (~12-18" estimated)
- **Status**: Confirmed via photos; currently on storage bins
- **Notes**: Ideal for networking gear (router, switch, patch panel, WAP), PDU, miniPC, and cable management. Primary target for current Phase 1 deployments.

## Recently Acquired / Purchased Equipment (Delivered June 11, 2026)

### TP-Link ER605 V2 Omada Gigabit VPN Router
- **Purchase Details**:
  - Amazon Order #111-0504065-9871411 (placed June 9, 2026)
  - Item(s) Subtotal: $49.99 | Shipping & Handling: $0.00 | Estimated tax: $4.37 | Grand Total: $54.36
  - Payment: Prime Visa ending in 9182 (Get 5% Back + rewards on select items) charged to this card; Amazon gift card balance also used.
  - Delivery: Left near front door or porch at 108 Uncas Street, Ronkonkoma, NY 11779, United States. Eligible for return/replace through July 11, 2026.
  - Supplied by: Amazon.com (Sold by: Other)
- **Key Specs & Features**: Wired Gigabit VPN Router, Up to 3 WAN Ethernet Ports + 1 USB WAN, VPN Firewall SMB Router, Omada SDN Integrated, Load Balance, Lightning Protection.
- **Intended Role in Project**: Primary gateway/router for stable family internet with multi-WAN failover/load balancing. Core of Phase 1 networking. Omada SDN ready for centralized management (pairs well with future Omada WAPs). Supports VPN, firewall rules, and basic segmentation to advance privacy and security goals. Compact desktop form; will be shelf or bracket mounted in/near small open rack initially.

### StarTech.com 8 Outlet Horizontal 1U Rack Mount PDU Power Strip
- **Model / Part**: RKPW081915
- **Purchase Details**:
  - Delivered June 11, 2026 (separate Amazon order from router)
  - Cost: $67.44
  - Return/replace eligible through July 11, 2026.
  - Supplied by: Amazon.com (Sold by: Other)
- **Key Specs & Features**: 8 Outlets, Horizontal 1U rack-mount form factor, Surge Protection, 120V/15A rating, includes 6ft Power Cord. Designed specifically for network/server racks.
- **Intended Role in Project**: Centralized power distribution and surge protection for all equipment in the rack (ER605, TL-SG1016DE switch, miniPC/Proxmox host, Omada WAP, patch panel, etc.). Eliminates power strip clutter, improves organization, safety, and reliability in the basement rack build. Mounts cleanly in 1U horizontal space of the smaller open rack.

**Notes on Purchases**: Both items arrived June 11, 2026 per Amazon delivery notifications and order summaries. Inventory updated in project docs (DECISIONS.md, RACK.md) with full order details for tracking, warranty, and reference.

## Next Steps
1. **Rack Preparation & Layout Finalization**: Measure/confirm usable space, power outlet locations/circuit capacity near rack area. Install any needed mounting rails, shelves, or brackets for open rack. Optimize positioning (proximity to cable entry point from upper floor if applicable, ventilation, accessibility).
2. **Physical Installation of New Gear**:
   - Secure StarTech PDU horizontally in a 1U slot (top or eye-level recommended for easy outlet access).
   - Position TP-Link ER605 V2 for convenient access to all ports (WANs, LANs, USB, reset). Connect primary WAN (and secondary if available) and LAN uplink to planned switch.
   - Power all devices through the new PDU once mounted.
3. **Configuration & Integration**:
   - Initial ER605 setup: Update firmware, configure WANs (DHCP/static or multi-WAN rules), basic firewall, VPN if needed, LAN DHCP. Adopt into Omada SDN if/when controller is deployed.
   - VLAN prep: Plan initial segmentation (even if basic ACLs initially) aligned with privacy migration.
   - Update network topology diagrams in `docs/diagrams/` post physical install and config.
4. **Monitoring & Validation**: Once stable, add ER605 (if SNMP/compatible) or downstream devices to Wazuh monitoring (via Bazzite/Proxmox). Run updated nmap scans and update `docs/inventory/` assets. Validate against risk register and security goals.
5. **Expansion Prep**: Source TL-SG1016DE switch, plan Dell OptiPlex 7060 Micro or other miniPC mounting, cable management kit, any additional 1U/2U shelves or organizers.
6. **Documentation**: Keep this file, RACK.md, and DECISIONS.md updated with photos, configs, issues encountered, and lessons learned. Link updates to GitHub Project board (Privacy Migration).

## References
- Full project context: [README.md](../README.md) and [GROK-WORKSPACE.md](../GROK-WORKSPACE.md)
- Rack layout & Phase 1 details: [RACK.md](RACK.md)
- Hardware decisions & purchase tracking: [DECISIONS.md](DECISIONS.md)
- Rack measurements & planned actions: [rack-measurements.md](rack-measurements.md)
- Infrastructure criteria: [infrastructure-criteria.md](infrastructure-criteria.md)
- GitHub repo: https://github.com/jacob-kraniak/home-network-security
- Project Board: https://github.com/users/jacob-kraniak/projects/1 (add related issues/tasks here)