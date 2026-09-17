# Phase Artifacts & Documentation Map

**Canonical reference** for which documents, diagrams, configs, and inventories belong to each project phase.  
**Last Updated:** 2026-09-16  
**Authoritative Timeline:** GitHub Project Board + Issues (see bottom)

> **Usage:** When working on a phase, start here. Update this file whenever a new artifact is created or an existing one is promoted/demoted between phases.

---

## Phase 1: Network Build (Stable Family Foundation)

**Status:** ✅ **Completed** (June 2026)

Unchanged. See prior revision for the Phase 1 tables.

### Associated Artifacts / Documents

| Category | File / Location | Description |
|----------|-----------------|-------------|
| **Roadmap & Status** | [docs/ROADMAP.md](../ROADMAP.md) | High-level Phase 1 completion summary |
| | [docs/phases/phase-1-completion.md](phase-1-completion.md) | Physical rack install & relocation log |
| | [docs/phases/phase-1-netbox-foundation.md](phase-1-netbox-foundation.md) | NetBox bootstrap |
| | [docs/NetBox-Inventory-Progress.md](../NetBox-Inventory-Progress.md) | NetBox audit log |
| **Hardware** | [docs/hardware/DECISIONS.md](../hardware/DECISIONS.md) | Hardware decisions |
| | [docs/hardware/RACK.md](../hardware/RACK.md) | Rack layout |
| **Inventory** | [docs/inventory/devices-summary.md](../inventory/devices-summary.md) | Hardware table |
| | [docs/inventory/iot-devices.md](../inventory/iot-devices.md) | IoT inventory |
| **Diagrams** | [docs/diagrams/](../diagrams/) | Topology + rack |
| **Workspace** | [GROK-WORKSPACE.md](../../GROK-WORKSPACE.md) | Workspace instructions |

### Phase 1 Exit Criteria (Met)
- [x] Racks powered & organized
- [x] Omada SDN live with VLANs
- [x] NetBox foundation + core devices
- [x] Public docs updated & redacted
- [x] Project board Phase 1 issues closed

---

## Phase 2: Self-Hosted Services Build

**Status:** 🟡 **In Progress** (NetBox local on CT 101 2026-09-16; Omada on-prem 2026-09-14)  
**Goal:** Deploy Proxmox VE, stand up core self-hosted services, integrate with NetBox & monitoring, document everything.

### Associated Artifacts / Documents

| Category | File / Location | Description |
|----------|-----------------|-------------|
| **Roadmap & Status** | [docs/ROADMAP.md](../ROADMAP.md) | Phase 2 section |
| | [docs/phases/phase-2-checkpoint-2026-09-16.md](phase-2-checkpoint-2026-09-16.md) | **Current live checkpoint** (NetBox on CT 101) |
| | [docs/phases/phase-2-close-linkedin.md](phase-2-close-linkedin.md) | **Phase 2 close + LinkedIn publish gates** |
| | [docs/phases/netbox-cloud-to-local.md](netbox-cloud-to-local.md) | Cloud → local inventory import runbook |
| | [docs/phases/phase-2-checkpoint-2026-09-14.md](phase-2-checkpoint-2026-09-14.md) | Omada CBC → CT 101 |
| | [docs/phases/phase-2-checkpoint-2026-09-05.md](phase-2-checkpoint-2026-09-05.md) | RAM split, Seagate 3TB, prior CT limits |
| | [docs/phases/phase-2-baseline-2026-08-29.md](phase-2-baseline-2026-08-29.md) | Wazuh disk-full outage + repair narrative |
| | [docs/NetBox-Inventory-Progress.md](../NetBox-Inventory-Progress.md) | Phase 2 NetBox entries |
| **Services** | [docs/services/self-hosted-services-roadmap.md](../services/self-hosted-services-roadmap.md) | Planned apps |
| | [docs/services/document-digitization.md](../services/document-digitization.md) | Paperless-ngx |
| **Hardware** | [docs/inventory/devices-summary.md](../inventory/devices-summary.md) | M715q + Seagate USB + Omada kit |
| | [docs/hardware/DECISIONS.md](../hardware/DECISIONS.md) | Acquisition notes |

### Phase 2 Current State (2026-09-16)
- [x] M715q acquired; KingSpec NVMe boot
- [ ] SanDisk Z400 — still not visible
- [x] PVE 9.2.4 node `debian`
- [x] **16 GB RAM (2×8 GB)** visible after 2026-09-05 reboot
- [x] CT 100 Wazuh at 6G / 81G / `192.168.0.178`; agents 003–006
- [x] CT 101 Portainer + RustDesk + Omada 6.3 + **NetBox v4.7** / `192.168.0.200` (6G / 100G)
- [x] Seagate Backup+ Desk 3TB exFAT at `/mnt/seagate3tb`
- [x] Omada CBC 6.3.0.100 → local 6.3.0.45; cloud closed
- [x] NetBox Docker stack healthy (`v4.7-5.1.1`) on CT 101 — Cloud still SoT until import
- [ ] Import Cloud inventory into local NetBox; then flip SoT
- [ ] One restore path (vzdump / volume copy to Seagate)
- [ ] PVE Directory storage / vzdump onto the Seagate
- [ ] AdGuard / WireGuard / Plane.so — **Phase 3 unless already live**
- [ ] Wazuh noise reduction (`local_rules.xml` / group agent.conf)
- [ ] `pve-edk2-firmware` only if UEFI VMs needed

Close gates (including LinkedIn): [phase-2-close-linkedin.md](phase-2-close-linkedin.md).

### Phase 2 Exit Criteria (Target)
- [ ] Proxmox VE stable + backups documented
- [ ] Core services running with backups
- [ ] NetBox local holds Cloud inventory + hypervisor + CTs
- [ ] Docs & diagrams current; SoT flipped to local
- [ ] Project board Phase 2 issues closed or moved to Phase 3
- [ ] LinkedIn follow-up only after SoT flip (see close note)

---

## Phase 3: Open Source Routing & Expansion (Future)

**Status:** 🔵 Planned

---

## Related Links
- Project Board: https://github.com/users/jacob-kraniak/projects/1
- Current checkpoint: [phase-2-checkpoint-2026-09-16.md](phase-2-checkpoint-2026-09-16.md)
- Close / LinkedIn gates: [phase-2-close-linkedin.md](phase-2-close-linkedin.md)
- Cloud → local: [netbox-cloud-to-local.md](netbox-cloud-to-local.md)
- Prior checkpoint: [phase-2-checkpoint-2026-09-14.md](phase-2-checkpoint-2026-09-14.md)
- Wazuh repair baseline: [phase-2-baseline-2026-08-29.md](phase-2-baseline-2026-08-29.md)
- NetBox deploy issue: [#28](https://github.com/jacob-kraniak/home-network-security/issues/28)

*Keep this map current when adding artifacts.*
