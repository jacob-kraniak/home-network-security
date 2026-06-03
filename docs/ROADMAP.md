# Home Network Security Roadmap (Revised June 2026)

## Phase 1: Stable Family Foundation (Current)
- Deploy TP-Link Festa FR205 (Multi-WAN) + TL-SG1016DE managed switch.
- Initial VLAN segmentation (Main / Kids / Guest / IoT).
- Rack organization with existing accessories.
- **Reference**: [`/hardware`](../hardware/) and [`/diagrams`](../diagrams/network-phase1.png) (update diagram after install).

## Phase 2: Self-Hosted Services (Next)
- Install Proxmox on Dell OptiPlex 7060 Micro.
- Core containers: AdGuard Home, WireGuard, Vaultwarden, monitoring stack.
- Keep TP-Link as primary router initially for stability.
- **Reference**: Update [`/diagrams`](../diagrams/) with new Proxmox host connections.

## Phase 3: Open Source Routing & Expansion
- Migrate to OPNsense on dedicated hardware.
- Add hybrid NAS (Aoostar WTR Pro or equivalent).
- **Reference**: [`hardware/`](../hardware/) for future hardware matrix.

**Risk Note**: Always maintain FR205 as warm spare for quick rollback.