# Hardware Decisions Log (June 2026)

## Approved Purchases
- **Router (Phase 1)**: TP-Link Festa FR205 — Multi-WAN for stability and family use.
- **Switch**: TP-Link TL-SG1016DE — VLAN support.
- **Compute (Phase 2)**: Dell OptiPlex 7060 Micro (Renewed, i7-8700T, 32GB RAM, 1TB NVMe) as primary Proxmox host.

## Rationale
- TP-Link chosen for vendor warranty, simple UI, and fast recovery (family network priority).
- Refurb enterprise Micro PC selected for reliability, low power, and upgradability.
- Single NIC acceptable for services host (downstream from router).

**Links**:
- Related inventory/measurements: [rack-measurements.md](rack-measurements.md)
- Rack layout: [RACK.md](RACK.md) (in this directory)
- Diagrams: [`../diagrams/`](../diagrams/)