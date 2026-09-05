# Home Network Security Roadmap (Revised September 5, 2026)

> **Phase Artifacts Map:** See [docs/phases/PHASE-ARTIFACTS.md](phases/PHASE-ARTIFACTS.md).
>
> **Current live state:** [docs/phases/phase-2-checkpoint-2026-09-05.md](phases/phase-2-checkpoint-2026-09-05.md)  
> **Wazuh outage narrative:** [docs/phases/phase-2-baseline-2026-08-29.md](phases/phase-2-baseline-2026-08-29.md)

## Phase 1: Network Build — Stable Family Foundation (Completed ✅)
**Timeline:** June 2026  
**Status:** Complete

- Deployed TP-Link Omada SDN: FR205 (Multi-WAN) router + SG2008P v3.20 managed switch (K108-MSW-1) + 2× EAP225 v4 APs.
- VLAN segmentation active: Management / LAN-Secure (1), Trusted/Secure (10), IoT (20).
- 21 clients inventoried via Omada.
- Physical racks, StarTech PDU, patch panel, Cat6.
- NetBox Cloud foundation complete.

**Primary Artifacts:**  
[PHASE-ARTIFACTS.md § Phase 1](phases/PHASE-ARTIFACTS.md#phase-1-network-build-stable-family-foundation) · [phase-1-completion.md](phases/phase-1-completion.md) · [devices-summary.md](inventory/devices-summary.md)

## Phase 2: Self-Hosted Services Build (In Progress 🟡)
**Timeline:** July 2026 – ongoing  
**Status:** PVE live. 16 GB RAM confirmed. Wazuh recovered + HV agent enrolled. Portainer healthy. 3 TB Seagate USB mounted for media/backups.

- **Host:** Lenovo M715q Tiny, node `debian`, PVE 9.2.4, `192.168.0.176`.
- **RAM:** 2×8 GB DDR4 SO-DIMM. PVE/top ~14.6 GiB after 2026-09-05 reboot (Aug 29 7.2 GiB reading was one DIMM not visible to the kernel).
- **CT 100 wazuh:** 6G RAM / 81G disk / `192.168.0.178`. Agent `pve-debian` (003) live.
- **CT 101 portainer:** 2G RAM / **4G disk** / `192.168.0.200`.
- **USB:** Seagate Backup+ Desk 3TB exFAT at `/mnt/seagate3tb` (376G used). USB 2 port. Not for VM disks.

**Immediate Next Steps:**
1. Optional PVE Directory storage on `/mnt/seagate3tb/pve-backup` for vzdump
2. Grow CT 101 disk before any new Portainer stack
3. NetBox: hypervisor + CTs + USB disk
4. Small next apps: AdGuard → WireGuard/Tailscale (not media until USB 3 or a dedicated media CT)

## Phase 3: Open Source Routing & Expansion (Future 🔵)
- OPNsense on dedicated hardware.
- Hybrid NAS.
- Advanced privacy hardening & monitoring.

---

**Risk Note:** Keep FR205 as warm spare. Keep CT 100 disk well under 80% or vuln feeds will kill Wazuh again. One fstab line only for the Seagate UUID.  
**Project Board:** https://github.com/users/jacob-kraniak/projects/1

*Last updated: 2026-09-05 — RAM correction + USB media disk + CT memory split.*
