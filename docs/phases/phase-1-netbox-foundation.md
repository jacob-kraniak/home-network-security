# Phase 1: NetBox Foundation Bootstrap - COMPLETE (June 13-14, 2026)

**Status:** ✅ Core taxonomy, templates, power model, racks, and initial device (PDU) established in NetBox. This provides the structured CMDB foundation complementing the physical rack installation and equipment relocation documented in [phase-1-completion.md](./phase-1-completion.md).

**Related Physical Work:** Basement rack setup (enclosed 12U "Network Stack" + "Server Hosts" rack), Startech PDU installation and mounting, temporary extension cord power, yellow/black cabling noted (cleanup planned post-electrician). Dedicated 5-20 outlet pending from electrician. Omada router (ER605) config pending.

## Why NetBox?
NetBox (DCIM/IPAM) is now the authoritative source for:
- Accurate device inventory (physical + virtual)
- Rack elevations and visual layout
- Power distribution and circuit tracking
- Network connections, cabling, and interface mapping
- IPAM, VLANs, and service discovery
- Change history and audit (changelog)
- Tagging for categorization (IoT risk, ownership: Personal vs KWE, criticality)

This directly supports core project goals: IoT inventory/risk mitigation, VLAN segmentation planning, self-hosted monitoring (Wazuh), and rack build-out scalability. It will gradually supersede or integrate with static files in `docs/inventory/` (nmap xmls, summaries).

## Bootstrap Summary (from NetBox Change Log)

### Organizational
- **Site Groups**: `Personal`, `Work`
- **Sites**: `Kraniak Home` (primary; updated), `KWE-Office` (created/revised)
- **Location**: `basement` (under Kraniak Home)
- **Contacts**: `Jacob Kraniak` (created + updated), `Christine Kraniak` (created)
- **Contact Groups**: `family`, `vendors`

### Device Roles (tailored for home lab + IoT + vehicles)
`Hypervisor`, `Server`, `Firewall`, `Switch`, `NAS`, `Workstation`, `Vehicle-Gateway`, `IoT-Device`, `Smart-Camera`, `Sensor`, `Media-Device`, `Printer`, `Power Distribution Unit`

### Manufacturers
`Startech.com`, `TP-Link`, `Lenovo`, `Dell`, `Ubiquiti`, `Cisco`, `Netgear`, `MSI`, `Google`, `Ring`, `Microsoft`

### Device Types (with Templates for reuse)
- `RKPW081915` (Startech PDU) — Power Port Template (`Input`), Power Outlet Templates (`Outlet1` through `Outlet8`)
- `ER605` (TP-Link Omada) — Interface Templates (`WAN1`, `WAN2`, `LAN1`–`LAN4`, `Console`)
- `Archer A7` (TP-Link) — Interface Templates (`WAN`, `LAN1`–`LAN4`) [updated x2]
- `X380 Yoga` / `Thinkpad X380 Yoga` (Lenovo) [updated]
- `Generic IoT / Smart Device`
- `Generic Ring Device`
- `Generic Nest/IoT Device`

### Racks (basement, Kraniak Home)
- **Network Stack**: Enclosed 12U with Drawer. **Current**: Startech PDU mounted (top position). Status: Active. Ready for core networking gear (ER605, switch, patch panel).
- **Server Hosts**: Created empty. Planned for Proxmox hosts, NAS, compute hardware.

### Power Infrastructure (Initial Model)
- `Main Panel - 200A` (Power Panel, updated)
- `Main Power` (Power Feed, created)
- `Main Power Feed` (Power Panel, created)
- **Device**: `Startech PDU` (created with 8x Power Outlets + 1x Power Port `Input` instantiated from templates)
- PDU successfully mounted and visible in rack elevation view.

### Tags (for categorization, risk, ownership)
`Home-Lab`, `Proxmox`, `Bazzite`, `Wazuh`, `IoT`, `Camera`, `Sensor`, `Critical`, `Firewall`, `Switch`, `NAS`, `Tesla`, `Volvo`, `Workstation`, `KWE`
(Ready for broad application; align with IoT risk strategy and privacy-migration goals.)

**Changelog Scope**: ~100 entries (June 13 00:21 – June 14 02:57). Focused on foundational/reusable objects rather than individual device population. Full log available as attached PDF.

## Current State Snapshot (from Rack View Screenshot)
- **Rack**: Network Stack (dcim.rack:1)
- **Mounted**: Startech PDU (highlighted, upper U position ~11-12)
- **Empty**: Remaining 10U+ positions available (front/rear views shown)
- **Rack Details**: Site=Personal / Kraniak Home, Location=basement, Status=Active, Description="Enclosed 12U with Drawer", Serial number= (none), Role=(none)
- **Validation**: Device type + rack mounting workflow confirmed working. PDU power outlets ready for assignment.

**Temporary Notes** (from physical phase): Yellow/black cables current; Cisco switch placeholder; Omada router pending full config; clean power outlet needed.

## Identified Gaps & Recommended Phase 2 Actions

### 1. Missing Device Types (High Priority)
Create types for immediate/planned hardware so instances can inherit templates:
- Proxmox hypervisor / miniPC host (Dell OptiPlex or equivalent; include CPU/RAM/storage attrs if available)
- NAS (model-specific or generic storage device)
- Managed Switch (e.g. TP-Link TL-SG1016DE / Omada equivalent, or Cisco placeholder)
- Access Point (Omada EAP series if expanding)
- Any specific vehicle or other edge devices

### 2. Device Instantiation & Rack Mounting (High Priority)
Only the PDU exists as a Device. Create and mount:
- `ER605` (role: Firewall or Gateway; assign to rack position e.g. U1 or U2; add interfaces from template; connect power port to one PDU outlet)
- `Archer A7` if still in use (or retire)
- Existing servers, NAS, workstations from `docs/inventory/` and roadmap (e.g. Dell miniPC for Phase 2 services)
- IoT devices using Generic types + appropriate tags (Camera, Sensor, IoT, Critical). Reference `iot-devices.md` and risk register. Bulk import recommended.
- Thinkpad X380 Yoga if tracking in DCIM

### 3. Power Connections & Circuits
- Map PDU `OutletX` → device power ports (once devices added)
- Document which circuit/breaker from Main Panel feeds the PDU Power Feed
- Add any sub-feeds or additional PDUs/power strips later
- Track utilization where possible

### 4. Cabling & Interface Connections
- Create Cable objects for key runs (even temporary ones noted in physical phase)
- Connect interfaces (e.g. ER605 LAN → switch, WAN → upstream/modem, console if used)
- Plan for structured cabling post-electrician (patch panel from Aaron already noted)
- Use NetBox to generate connection reports / topology views

### 5. IPAM, VLANs, Prefixes
- Add VLANs / IP Prefixes matching segmentation plan (Trusted/Main, IoT, Guest/Kids, Work)
- Seed key static IPs (gateway, servers, critical IoT) from sanitized nmap/services.xml data
- Document DHCP ranges vs statics on ER605
- Later: integrate or cross-ref with Wazuh agents, Proxmox networking

### 6. Virtualization & Services Modeling
- Once Proxmox host added as Device (Hypervisor role): create Cluster if multi-host, then Virtual Machines + VM Interfaces
- Map running services (Wazuh, Jellyfin, Home Assistant, etc.) to VMs or Devices
- Align with `docs/services/self-hosted-services-roadmap.md`

### 7. Tagging, Custom Fields & Metadata
- Apply relevant tags to all new and existing objects (e.g. Home-Lab + Proxmox to servers; IoT + Camera to Ring/Nest devices; KWE to work gear)
- Evaluate/add Custom Fields for: `purchase_date`, `cost_usd`, `warranty_end`, `owner` (Personal/KWE), `risk_level` (IoT mitigation plan), `notes`, sanitized `mac_address`
- Add Journal entries for key decisions (rack strategy, electrician, etc.)

### 8. Rack & Visualization Polish
- Populate Server Hosts rack plan (assign future positions)
- Upload rack images/labels (include the provided NetBox screenshot + physical photos already in assets/phase1/)
- Consider rack Role or Type for filtering
- Decide/document long-term rack strategy (Network Stack for edge + PDU; Server Hosts for compute; future expansion rack?)

### 9. Documentation & Integration Gaps (This Repo)
- Update `ROADMAP.md` to reflect Phase 1 completion, rack decisions, and NetBox adoption as primary inventory tool.
- Cross-reference this file from `phase-1-completion.md` and hardware/rack docs.
- Evolve `docs/inventory/devices-summary.md` and `iot-devices.md` to note "Source of truth: NetBox" or generate summaries from NetBox exports.
- Add NetBox-specific section or subdir (`docs/netbox/`) for model decisions, export workflows, plugin ideas, sync scripts.
- Update diagrams/ (draw.io) to incorporate or link NetBox rack elevations and planned topology.

## Alignment with Project Tracks
- **Privacy Migration / IoT Risk**: Tags + future custom fields support risk register and mitigation/transference tracking (VLAN now, replacement later for Ring/Nest).
- **Self-Hosted Services**: NetBox will track hosts/VMs/services as they come online in Phase 2.
- **Cyber Education / Certs**: Hands-on with production-grade DCIM tool (NetBox is industry standard); good for portfolio, homelab skills.
- **Network Rack Build-out**: Visual + relational model now exists; power and cabling next.

## Next Immediate Actions (Recommended)
1. **Documentation**: Add this file to repo; update ROADMAP.md and phase-1-completion.md with cross-links and NetBox mention.
2. **NetBox UI**: Create the missing Device Types (start with switch/NAS/Proxmox host).
3. **Core Device**: Add ER605 instance, mount in Network Stack rack, connect power, document interfaces/IP.
4. **Physical Follow-up**: Schedule electrician; complete Omada config; clean up temporary cables.
5. **Bulk Prep**: Export current NetBox data (or use CSV) and cross-check against `docs/inventory/` for gaps/duplicates.

**Screenshots**:
- NetBox Rack Elevation (Network Stack w/ PDU): See user-provided `screenshot.jpeg` (add to `assets/phase1/netbox-network-stack-rack-20260614.png` recommended)
- Physical rack photos: `assets/phase1/PXL_20260613_*.jpg` (already committed)
- Change Log: `Change Log _ NetBox.pdf` (attached to this conversation; 8 pages / 100 entries)

*Last updated: 2026-06-14*
*Author: Grok-assisted analysis of provided NetBox changelog + rack UI screenshot*
*Related Issues/Project Board*: Link this to Privacy Migration board under appropriate track (e.g. track:network-rack or new NetBox label)