# Home Network Security Roadmap (Revised August 29, 2026)

> **Phase Artifacts Map:** See [docs/phases/PHASE-ARTIFACTS.md](phases/PHASE-ARTIFACTS.md) for the complete list of documents, diagrams, configs, and inventories that belong to each phase.
>
> **Live Phase 2 baseline:** [docs/phases/phase-2-baseline-2026-08-29.md](phases/phase-2-baseline-2026-08-29.md)

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
**Status:** Proxmox VE **live** on M715q. Portainer healthy. Wazuh 4.8.2 recovered 2026-08-29. Constrained by ~7 GiB host RAM.

- **Proxmox Host:** Lenovo ThinkCentre M715q Tiny (S/N MJ067MNT, type 10M3000PUS). Node name `debian`. PVE **9.2.4**, Debian 13, kernel `7.0.14-4-pve`.
- **CPU / RAM (live):** AMD PRO A12-9800E (4 cores). **~7.2 GiB RAM observed** — July docs that say 16GB do not match hardware.
- **Disk:** KingSpec 512GB NVMe as ext4 `/`. SanDisk Z400 256GB **not detected**. Storage is PVE `local` dir (no LVM-thin).
- **Guests:** CT 100 `wazuh` (`192.168.0.178`, 2C/4G/81G). CT 101 `docker` (`192.168.0.200`, 4C/8G-limit/4G) running Portainer only. No QEMU VMs.
- **Wazuh:** AIO was down 2026-08-09 → 2026-08-29 (rootfs 100% from vuln-feed `vd_updater`). Resized + started. UI/Discover work; API intermittent from CT swap.
- NetBox Cloud still authoritative; hypervisor + CTs not fully modeled.

**Primary Artifacts:**  
[phase-2-baseline-2026-08-29.md](phases/phase-2-baseline-2026-08-29.md) · [PHASE-ARTIFACTS.md § Phase 2](phases/PHASE-ARTIFACTS.md#phase-2-self-hosted-services-build) · [self-hosted-services-roadmap.md](services/self-hosted-services-roadmap.md) · [document-digitization.md](services/document-digitization.md) · [devices-summary.md](inventory/devices-summary.md) · [NetBox-Inventory-Progress.md](NetBox-Inventory-Progress.md)

**Immediate Next Steps:**
1. RAM decision (DIMM vs shrink CT 101 limit vs indexer heap) before more Wazuh agents
2. Recreate missing `/etc/pve/storage.cfg` if needed
3. Grow CT 101 disk before any new Portainer stack
4. NetBox: hypervisor + CT 100/101
5. Small next apps via Portainer: AdGuard → WireGuard/Tailscale (not media)

## Phase 3: Open Source Routing & Expansion (Future 🔵)
- OPNsense migration on dedicated hardware.
- Hybrid NAS (Aoostar WTR Pro or equivalent).
- Advanced privacy hardening & monitoring.

**Artifacts:** To be defined when Phase 2 nears completion. Placeholder references currently in ROADMAP and services roadmap.

---

**Risk Note:** Always maintain FR205 as warm spare for quick rollback. Wazuh CT disk must stay well under 80% or vuln feeds will kill the SIEM again.  
**Project Board:** https://github.com/users/jacob-kraniak/projects/1 (use `phase:1` / `phase:2` labels + issues for timeline tracking).

*Last updated: 2026-08-29 — live PVE/Portainer/Wazuh baseline after recovery.*
