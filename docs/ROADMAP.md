# Home Network Security Roadmap (Revised September 24, 2026)

> **Phase Artifacts Map:** See [docs/phases/PHASE-ARTIFACTS.md](phases/PHASE-ARTIFACTS.md).
>
> **Current live state:** [docs/phases/phase-2-checkpoint-2026-09-16.md](phases/phase-2-checkpoint-2026-09-16.md)  
> **Prior checkpoints:** [2026-09-14](phases/phase-2-checkpoint-2026-09-14.md) (Omada on-prem) · [2026-09-05](phases/phase-2-checkpoint-2026-09-05.md)  
> **Wazuh outage narrative:** [docs/phases/phase-2-baseline-2026-08-29.md](phases/phase-2-baseline-2026-08-29.md)
>
> **Phase 3 remote access:** [docs/phases/phase-3-remote-access.md](phases/phase-3-remote-access.md) · P0 [#34](https://github.com/jacob-kraniak/home-network-security/issues/34) · P0-next [#36](https://github.com/jacob-kraniak/home-network-security/issues/36) · P1 [#35](https://github.com/jacob-kraniak/home-network-security/issues/35)

## Phase 1: Network Build — Stable Family Foundation (Completed ✅)
**Timeline:** June 2026  
**Status:** Complete

- Deployed TP-Link Omada SDN: **ER605 V2** gateway + managed switch (K108-MSW-1) + EAP coverage (Living Room + Office).
- VLAN segmentation active (Omada SoT 2026-09-15): Management (1) `192.168.0.1/24`, Trusted (10) `192.168.10.1/24`, IoT (20) `192.168.20.1/24`, Guest (30) `192.168.30.1/24`, Lab (40) `192.168.40.1/24`.
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
- **NetBox:** `netboxcommunity/netbox:v4.7-5.1.1` at `http://192.168.0.200:8000`. Local UI healthy; Cloud archive pending reconcile. Issue [#28](https://github.com/jacob-kraniak/home-network-security/issues/28) closed as platform deploy; import still open in docs.
- **USB:** Seagate Backup+ Desk 3TB exFAT at `/mnt/seagate3tb`.
- **Remote desktop:** RustDesk *server* on CT 101 is the Phase 2 line. Family clients = Phase 3 P1 ([#35](https://github.com/jacob-kraniak/home-network-security/issues/35)). Datacenter hop = Phase 3 P0-next after L3 ([#36](https://github.com/jacob-kraniak/home-network-security/issues/36)).

**Immediate Next Steps (still Phase 2):**
1. Import Cloud inventory into local NetBox; dual-run; keep on-prem as SoT; document count deltas
2. Wazuh tuning (group `agent.conf` + `local_rules.xml`)
3. Optional PVE Directory storage on `/mnt/seagate3tb/pve-backup`
4. Model hypervisor + CTs + USB + Omada controller in NetBox
5. One restore path written (vzdump / volume copy)
6. Omada syslog → Wazuh only after SIEM noise is down

AdGuard, WireGuard/Tailscale, Plane.so, RustDesk clients / jump guest — **Phase 3** unless already live. See [phase-3-remote-access.md](phases/phase-3-remote-access.md).

## Phase 3: Open Source Routing & Expansion (Future 🔵)
- **P0 Remote network access:** VPN / WireGuard / Tailscale so the laptop reaches the datacenter from anywhere. [#34](https://github.com/jacob-kraniak/home-network-security/issues/34).
- **P0-next Datacenter RustDesk (after P0):** jump guest on the M715q; off-LAN RustDesk into the rack; hop into each CT from that desktop. Not XFCE on Wazuh. [#36](https://github.com/jacob-kraniak/home-network-security/issues/36).
- **P1 Family RustDesk fleet (parallel, lower priority):** Jacob laptop, Christine laptop, BazzitePC. [#35](https://github.com/jacob-kraniak/home-network-security/issues/35).
- OPNsense on dedicated hardware.
- Hybrid NAS.
- Advanced privacy hardening & monitoring.

See [phase-3-remote-access.md](phases/phase-3-remote-access.md).

---

**Risk Note:** Keep CT 100 disk well under 80% or vuln feeds will kill Wazuh again. Omada Controller Hostname must stay `192.168.0.200` (not Docker `172.19.0.2`). One fstab line only for the Seagate UUID. Do not WAN-publish NetBox `:8000`. Host RAM is tight (~14.6 GiB, two 6G CTs) — size the jump guest small.  
**Project Board:** https://github.com/users/jacob-kraniak/projects/1

*Last updated: 2026-09-24 — P0 L3, then P0-next datacenter RustDesk jump.*
