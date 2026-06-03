## Server Hardware Decision - Rack Server vs Mini-PC

### Assessment
- Full rack-mount servers (Dell PowerEdge etc.): **Overkill** for current needs (Wazuh, Home Assistant, Frigate, light VMs).
- Primary Concern: Power consumption (150-300W idle vs 15-40W on modern mini-PCs).
- Noise, heat, and electricity cost make them suboptimal for always-on home use.

### Recommended Path
**Primary Host**: Low-power mini-PC or SFF PC for Proxmox (N100/N305/AMD equivalents).
- Reuse existing 2.5" SSDs where possible.
- Dell SAS HDDs: Consider only if building a separate storage node (e.g., TrueNAS) with spin-down.

**When Rack Server Might Make Sense**:
- Heavy storage needs (10+ drives)
- Advanced homelab / certification practice (future education track)
- If acquired very cheap with low-power CPUs (rare)

**Current Direction**: Prioritize efficiency. Use rack space for networking gear, UPS, and clean cable management first.

Status: Decision documented 2026-06-03
