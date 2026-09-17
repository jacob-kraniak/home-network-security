# Home Network Security Roadmap (Revised September 16, 2026)

> **Phase Artifacts Map:** See [docs/phases/PHASE-ARTIFACTS.md](phases/PHASE-ARTIFACTS.md).
>
> **Current live state:** [docs/phases/phase-2-checkpoint-2026-09-16.md](phases/phase-2-checkpoint-2026-09-16.md)  
> **Prior checkpoints:** [2026-09-14](phases/phase-2-checkpoint-2026-09-14.md) (Omada on-prem) · [2026-09-05](phases/phase-2-checkpoint-2026-09-05.md)  
> **Wazuh outage narrative:** [docs/phases/phase-2-baseline-2026-08-29.md](phases/phase-2-baseline-2026-08-29.md)

## Phase 1: Network Build — Stable Family Foundation (Completed ✅)
**Timeline:** June 2026  
**Status:** Complete

- Deployed TP-Link Omada SDN: **ER605 V2** gateway + managed switch (K108-MSW-1) + EAP coverage (Living Room + Office).
- VLAN segmentation active: Management / LAN-Secure (1), Trusted/Secure (10), IoT (20), plus 30/40 as provisioned.
- Physical racks, StarTech PDU, patch panel, Cat6.
- NetBox Cloud foundation complete.
- **2026-09-14:** Controller moved off Omada Cloud onto CT 101. Hardware unchanged; management is local.

**Primary Artifacts:**  
[PHASE-ARTIFACTS.md § Phase 1](phases/PHASE-ARTIFACTS.md#phase-1-network-build-stable-family-foundation) · [phase-1-completion.md](phases/phase-1-completion.md) · [devices-summary.md](inventory/devices-summary.md)

## Phase 2: Self-Hosted Services Build (In Progress 🟡)
**Timeline:** July 2026 – ongoing  
**Status:** PVE live. Wazuh + Portainer + RustDesk + Omada 6.3 + **NetBox v4.7** on CT 101. 3 TB Seagate USB mounted.

- **Host:** Lenovo M715q Tiny, node `debian`, PVE 9.2.4, `192.168.0.176`.
- **RAM:** 2×8 GB DDR4 SO-DIMM (~14.6 GiB).
- **CT 100 wazuh:** 6G RAM / 81G disk / `192.168.0.178`. Agents 003–006.
- **CT 101 portainer:** 6G / 100G / `192.168.0.200`. Portainer + RustDesk + Omada 6.3 + NetBox.
- **Omada:** `mbentley/omada-controller:6.3` (6.3.0.45). Inform / Controller Hostname **`192.168.0.200`**. Cloud CBC closed.
- **NetBox:** `netboxcommunity/netbox:v4.7-5.1.1` at `http://192.168.0.200:8000`. Local UI healthy; **Cloud still SoT** until import. Issue [#28](https://github.com/jacob-kraniak/home-network-security/issues/28).
- **USB:** Seagate Backup+ Desk 3TB exFAT at `/mnt/seagate3tb`.

**Immediate Next Steps:**
1. Import Cloud inventory into local NetBox; dual-run; flip SoT only after counts match
2. Wazuh tuning (group `agent.conf` + `local_rules.xml`)
3. Optional PVE Directory storage on `/mnt/seagate3tb/pve-backup`
4. Model hypervisor + CTs + USB + Omada controller in NetBox
5. Small next apps: AdGuard → WireGuard/Tailscale; Plane.so
6. Omada syslog → Wazuh only after SIEM noise is down

## Phase 3: Open Source Routing & Expansion (Future 🔵)
- OPNsense on dedicated hardware.
- Hybrid NAS.
- Advanced privacy hardening & monitoring.

---

**Risk Note:** Keep CT 100 disk well under 80% or vuln feeds will kill Wazuh again. Omada Controller Hostname must stay `192.168.0.200` (not Docker `172.19.0.2`). One fstab line only for the Seagate UUID. Do not WAN-publish NetBox `:8000`.  
**Project Board:** https://github.com/users/jacob-kraniak/projects/1

*Last updated: 2026-09-16 — NetBox v4.7 active on CT 101.*
