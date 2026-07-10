# Home Network Security Roadmap (Revised July 10, 2026)

> **Phase Artifacts Map:** See [docs/phases/PHASE-ARTIFACTS.md](phases/PHASE-ARTIFACTS.md) for the complete list of documents, diagrams, configs, and inventories that belong to each phase.

## Phase 1: Network Build — Stable Family Foundation (Completed ✅)
**Timeline:** June 2026  
**Status:** Complete

- Deployed TP-Link Omada SDN: FR205 (Multi-WAN) router + SG2008P v3.20 managed switch (K108-MSW-1) + 2× EAP225 v4 APs.
- VLAN segmentation active: Management / LAN-Secure (1), Trusted/Secure (10), IoT (20).
- 21 clients inventoried via Omada.
- Physical racks (Network Stack + Server Hosts), StarTech PDU, patch panel, Cat6.
- NetBox Cloud foundation complete.

**Primary Artifacts:**  
[PHASE-ARTIFACTS.md § Phase 1](phases/PHASE-ARTIFACTS.md#phase-1-network-build-stable-family-foundation) · [phase-1-completion.md](phases/phase-1-completion.md) · [phase-1-netbox-foundation.md](phases/phase-1-netbox-foundation.md) · [DECISIONS.md](hardware/DECISIONS.md) · [RACK.md](hardware/RACK.md) · [devices-summary.md](inventory/devices-summary.md) · diagrams in `docs/diagrams/`

## Phase 2: Self-Hosted Services Build (In Progress 🟡)
**Timeline:** July 2026 – ongoing  
**Status:** Host hardware acquired; Proxmox install pending

- **Proxmox Host:** Free Lenovo ThinkCentre M715q Tiny (S/N MJ067MNT, type 10M3000PUS) acquired 2026-07-09/10. 16GB RAM, KingSpec 512GB NVMe boot, SanDisk Z400 256GB 2.5" for potential RAID1. Dual DisplayPort.
- Planned services: Wazuh, AdGuard Home, WireGuard/Tailscale, Vaultwarden, Jellyfin, Immich, Home Assistant, Paperless-ngx, RustDesk, etc.
- NetBox population for hypervisor + VMs + power.
- Local management display decision (DP or active adapter).

**Primary Artifacts:**  
[PHASE-ARTIFACTS.md § Phase 2](phases/PHASE-ARTIFACTS.md#phase-2-self-hosted-services-build) · [self-hosted-services-roadmap.md](services/self-hosted-services-roadmap.md) · [document-digitization.md](services/document-digitization.md) · updated [devices-summary.md](inventory/devices-summary.md) · [NetBox-Inventory-Progress.md](NetBox-Inventory-Progress.md) · future `docs/configs/`

**Immediate Next Steps:**
1. BIOS prep (SVM, C6, Secure Boot)
2. Proxmox VE install on KingSpec NVMe
3. NetBox device + rack placement
4. First services (recommended order: AdGuard → WireGuard → Wazuh)

## Phase 3: Open Source Routing & Expansion (Future 🔵)
- OPNsense migration on dedicated hardware.
- Hybrid NAS (Aoostar WTR Pro or equivalent).
- Advanced privacy hardening & monitoring.

**Artifacts:** To be defined when Phase 2 nears completion. Placeholder references currently in ROADMAP and services roadmap.

---

**Risk Note:** Always maintain FR205 as warm spare for quick rollback.  
**Project Board:** https://github.com/users/jacob-kraniak/projects/1 (use `phase:1` / `phase:2` labels + issues for timeline tracking).

*Last updated: 2026-07-10 — Phase artifacts map created; M715q Proxmox host inventoried; Phase 2 hardware ready.*
