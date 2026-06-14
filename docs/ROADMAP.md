# Home Network Security Roadmap (Revised June 14, 2026)

## Phase 1: Stable Family Foundation + Rack Relocation + NetBox Bootstrap - ✅ COMPLETE
- **Physical**: TP-Link ER605 V2 Omada SDN router + Startech 8-outlet 1U PDU acquired and installed in basement. CAT6/fiber relocation, equipment moved to rack with help from Aaron Kraniak (patch panel + keystones). Temporary power/cabling; dedicated outlet pending electrician. Network stability confirmed.
- **Rack Config**: Two racks established in basement:
  - **Network Stack** (enclosed 12U w/ drawer): PDU mounted + space for ER605, switch, patch panel.
  - **Server Hosts**: Empty, reserved for Proxmox/NAS/compute.
- **Documentation & CMDB**: Parallel bootstrap of **NetBox** as primary structured inventory tool (DCIM/IPAM). Created sites/locations/contacts, custom roles (incl. Power Distribution Unit, IoT-Device, Hypervisor), manufacturers, device types with interface/power templates (ER605, Archer A7, PDU, IoT generics), racks, power panels/feeds/outlets, and comprehensive tags (Home-Lab, Proxmox, Wazuh, IoT, Critical, KWE, Tesla, etc.). Initial device (Startech PDU) created and rack-mounted. Full changelog + rack elevation screenshot captured.
- **See**: [phase-1-completion.md](phases/phase-1-completion.md) and new [phase-1-netbox-foundation.md](phases/phase-1-netbox-foundation.md) for details, gaps, and Phase 2 plan.
- **VLAN/Segmentation**: Basic plan defined (Trusted, IoT, Guest, Work); implementation on ER605 pending full config.
- **Status**: Hardware foundation and NetBox model complete. Next: electrician, Omada config, core device population in NetBox, cabling/power connections.

## Phase 2: Self-Hosted Services & NetBox Population (Next)
- Install Proxmox on Dell OptiPlex / miniPC host; add as Device in NetBox (Hypervisor role).
- Core services: AdGuard/Pi-hole, WireGuard, Vaultwarden, Wazuh (SIEM/XDR), Jellyfin/Plex, Home Assistant, Paperless-ngx document archive.
- **NetBox Phase 2 Priorities** (see phase-1-netbox-foundation.md):
  - Create missing Device Types (Proxmox host, NAS, managed switch, APs).
  - Instantiate & mount core devices (ER605 first, then others); apply tags.
  - Model power connections (PDU outlets → devices), circuits from Main Panel.
  - Add Cables & interface connections (start with temporary runs; plan structured).
  - Seed IPAM/VLANs/Prefixes from sanitized inventory data.
  - Begin virtualization modeling (Clusters, VMs) once Proxmox live.
  - Bulk IoT device entry with risk tags; cross-ref risk register.
- Retain ER605 as edge initially; evaluate OPNsense/pfSense migration later (Phase 3).
- Update diagrams/ and inventory/ summaries to align with NetBox as source of truth.
- **Reference**: `docs/services/self-hosted-services-roadmap.md`, hardware/ docs, privacy-migration board.

## Phase 3: Open Source Routing & Expansion (Future)
- Migrate routing/firewall to OPNsense (or pfSense) on dedicated hardware for full control.
- Expand rack (additional large rack?), hybrid NAS, more IoT replacements (Reolink/Frigate for Ring, Zigbee for Nest).
- Full NetBox utilization: advanced queries, exports, potential plugins/webhooks for Proxmox/Wazuh integration, custom fields for costs/warranty/risk.
- Align with ongoing privacy migration, cyber certs, and homelab automation (MCP, GitHub Actions, Obsidian).

**Risk / Rollback**: ER605 config exportable for quick restore. Maintain fallback options during transitions. All changes tracked in NetBox changelog.

**Recent Updates (June 13-14)**: Physical rack relocation complete + NetBox foundation bootstrap (taxonomy, power, racks, PDU). See phases/ docs and attached changelog/screenshots for full audit trail. Inventory tracked against Privacy Migration goals.

*Last updated: 2026-06-14* (Phase 1 marked complete; NetBox integration added; rack decisions clarified)