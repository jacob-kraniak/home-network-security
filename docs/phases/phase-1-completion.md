# Phase 1: Initial Rack Installation and Equipment Relocation - COMPLETE (June 2026)

**Status:** ✅ Completed with support from Aaron Kraniak (Kingdom Integrations). Aaron provided a brand-new TrueCable patch panel and collection of keystones.

### Key Accomplishments
1. Cut the CAT6 line from the office to the router, allowing pull-back into the basement.
2. Created just enough room to pull the fiber line through the floor hole.
3. Re-terminated CAT6 and moved all equipment to the rack.
4. Installed hardware in placeholder positions (PDU and drawer positions will likely remain; shelf may shift once managed switch arrives).
5. Ran temporary extension cord to the PDU.
6. Confirmed network stability after powering everything back on.

**Photos:**

![Rack Interior - PDU & Equipment](https://github.com/jacob-kraniak/home-network-security/blob/main/assets/phase1/PXL_20260613_162004808.jpg)

![Full Rack View with Cisco & Router](https://github.com/jacob-kraniak/home-network-security/blob/main/assets/phase1/PXL_20260613_193632285.jpg)

**Temporary Setup Notes:**
- Yellow/black cables are current runs (clean-up planned post-electrician).
- Cisco switch is placeholder/temporary.
- Omada router configuration pending.

### Next Immediate Steps
1. **Electrician**: Install dedicated 5-20 outlet behind the table (critical for clean PDU power).
2. Finish configuration of the new **Omada Router**.
3. Plan and install wiring for the temporary **Cisco Switch**.

### Rack Configuration
Physical work resulted in **two dedicated racks** in the basement:
- **Network Stack** (enclosed 12U with drawer): Hosts the Startech PDU + planned core networking (ER605 Omada router/gateway, managed switch, patch panel). See NetBox rack elevation view.
- **Server Hosts** (separate rack): Reserved for compute (Proxmox hypervisors, NAS, future expansion).

This aligns with long-term separation for security/isolation and easier scaling of Wazuh/Proxmox/Jellyfin etc. (Option 2 from earlier discussion, executed).

### Parallel Documentation Work: NetBox Bootstrap
In parallel with physical relocation, foundational objects were created in **NetBox** (DCIM/IPAM tool) to establish a structured, visual, relational inventory and CMDB for the home lab. This included:
- Sites, Location (basement), Contacts/Groups
- Custom Device Roles (Hypervisor, Server, Firewall/Gateway, IoT-Device, Power Distribution Unit, etc.)
- Manufacturers and Device Types (with reusable Interface/Power templates for ER605, Archer A7, PDU, generics for IoT)
- Racks (Network Stack + Server Hosts) with elevation views
- Power modeling (Main Panel 200A, feeds, PDU with 8 outlets + input)
- Tags for categorization (Home-Lab, Proxmox, Wazuh, IoT, Critical, Tesla, KWE, etc.)
- Initial Device: Startech PDU mounted in Network Stack rack

**See detailed summary, current state, identified gaps, and Phase 2 population plan**: [phase-1-netbox-foundation.md](./phase-1-netbox-foundation.md)

NetBox changelog (100 entries June 13-14) and rack UI screenshot provided for reference. This positions the project for queryable inventory, power/cable management, change tracking, and future automation/sync with Proxmox/Wazuh.

### Credits & Thanks
Huge thanks to Aaron Kraniak for the hands-on help, patch panel, and keystones — this phase would have taken much longer without it!

*Last updated: 2026-06-14* (added NetBox bootstrap cross-reference and rack config clarification)