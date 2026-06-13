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
(Images to be uploaded later to /assets/phase1/)

**Temporary Setup Notes:**
- Yellow/black cables are current runs (clean-up planned post-electrician).
- Cisco switch is placeholder/temporary.
- Omada router configuration pending.

### Next Immediate Steps
1. **Electrician**: Install dedicated 5-20 outlet behind the table (critical for clean PDU power).
2. Finish configuration of the new **Omada Router**.
3. Plan and install wiring for the temporary **Cisco Switch**.

### Rack Configuration Decision
Now that we have a better physical picture, deciding between:
1. **Large rack for Network + Server hosts** (save smaller rack for future expansion).
2. **Large rack for Network only**, smaller rack dedicated to Server hardware.

**Pros/Cons** to discuss:
- Option 1: Simpler cabling/power in one place; better for short-term.
- Option 2: Cleaner separation (security/isolation); easier long-term scaling with Wazuh/Proxmox/Jellyfin etc.

### Credits & Thanks
Huge thanks to Aaron Kraniak for the hands-on help, patch panel, and keystones — this phase would have taken much longer without it!

*Last updated: 2026-06-13*