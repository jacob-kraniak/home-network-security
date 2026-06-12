# Home Network Security Roadmap (Revised June 12, 2026)

## Phase 1: Stable Family Foundation (Current - In Progress)
- Deploy **TP-Link ER605 V2** Omada SDN Gigabit VPN Router (Multi-WAN / load balance / VPN firewall; purchased June 9, delivered June 11, 2026 for $49.99) + TL-SG1016DE managed switch (planned).
- StarTech 8-outlet 1U horizontal rackmount PDU also acquired (delivered June 11, 2026; $67.44) for clean power in small open rack.
- Initial VLAN segmentation (Main/Trusted, Kids/Guest, IoT, Work) and basic firewall rules on ER605.
- Rack organization and mounting of new networking gear in basement smaller open rack.
- **Reference**: [`/hardware`](../hardware/) (DECISIONS.md, RACK.md, home-lab-rack-build.md for full inventory/purchase details) and update diagrams in [`/diagrams`](../diagrams/).
- **Status**: Router and PDU received and ready for physical install/config. Phase 1 hardware foundation complete on procurement side.

## Phase 2: Self-Hosted Services (Next)
- Install Proxmox on Dell OptiPlex 7060 Micro (or equivalent miniPC).
- Core services/containers: AdGuard Home (or Pi-hole), WireGuard VPN, Vaultwarden, Wazuh monitoring/SIEM, Jellyfin/Plex media, Home Assistant, document archive (Paperless-ngx).
- Retain TP-Link ER605 V2 as primary edge router initially for network stability during transition (Omada SDN ready for expansion).
- **Reference**: Update [`/diagrams`](../diagrams/) with Proxmox host placement and service connections. See `docs/services/` for research roadmaps.

## Phase 3: Open Source Routing & Expansion (Future)
- Evaluate migration of routing/firewall to OPNsense (or pfSense) on dedicated hardware for full open-source control and advanced features.
- Add hybrid NAS/storage solution (e.g. Aoostar or custom).
- Expand rack utilization (large enclosed rack for compute/storage).
- **Reference**: [`hardware/`](../hardware/) for hardware matrix and future purchases.

**Risk / Rollback Note**: ER605 V2 supports easy configuration backup/export for quick restore or rollback if issues arise during any phase. Maintain fallback options and test failover where multi-WAN is configured.

**Recent Inventory Updates**: Logged TP-Link ER605 V2 and StarTech PDU purchases with full order details, costs, delivery info, and intended roles. See hardware/ docs for complete tracking. This keeps project inventory accurate and auditable against the Privacy Migration goals.