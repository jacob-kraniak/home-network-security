# Phase Artifacts & Documentation Map

**Canonical reference** for which documents, diagrams, configs, and inventories belong to each project phase.  
**Last Updated:** 2026-09-05  
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

**Status:** 🟡 **In Progress** (PVE live; 16 GB RAM confirmed 2026-09-05; Wazuh + Portainer + HV agent)  
**Goal:** Deploy Proxmox VE, stand up core self-hosted services, integrate with NetBox & monitoring, document everything.

### Associated Artifacts / Documents

| Category | File / Location | Description |
|----------|-----------------|-------------|
| **Roadmap & Status** | [docs/ROADMAP.md](../ROADMAP.md) | Phase 2 section |
| | [docs/phases/phase-2-checkpoint-2026-09-05.md](phase-2-checkpoint-2026-09-05.md) | **Current live checkpoint** (RAM split, Seagate 3TB, CT limits) |
| | [docs/phases/phase-2-baseline-2026-08-29.md](phase-2-baseline-2026-08-29.md) | Wazuh disk-full outage + repair narrative |
| | [docs/NetBox-Inventory-Progress.md](../NetBox-Inventory-Progress.md) | Phase 2 NetBox entries |
| **Services** | [docs/services/self-hosted-services-roadmap.md](../services/self-hosted-services-roadmap.md) | Planned apps |
| | [docs/services/document-digitization.md](../services/document-digitization.md) | Paperless-ngx |
| **Hardware** | [docs/inventory/devices-summary.md](../inventory/devices-summary.md) | M715q + Seagate USB |
| | [docs/hardware/DECISIONS.md](../hardware/DECISIONS.md) | Acquisition notes |

### Phase 2 Current State (2026-09-05)
- [x] M715q acquired; KingSpec NVMe boot
- [ ] SanDisk Z400 — still not visible
- [x] PVE 9.2.4 node `debian`
- [x] **16 GB RAM (2×8 GB)** visible after 2026-09-05 reboot
- [x] CT 100 Wazuh at 6G / 81G / `192.168.0.178`; HV agent `pve-debian` (003)
- [x] CT 101 Portainer at 2G / 4G disk / `192.168.0.200`
- [x] Seagate Backup+ Desk 3TB exFAT at `/mnt/seagate3tb`
- [ ] PVE Directory storage / vzdump onto the Seagate
- [ ] NetBox hypervisor + CTs + USB disk
- [ ] AdGuard / WireGuard / remaining apps
- [ ] Grow CT 101 disk before media stacks
- [ ] `pve-edk2-firmware` only if UEFI VMs needed

### Phase 2 Exit Criteria (Target)
- [ ] Proxmox VE stable + backups documented
- [ ] Core services running with backups
- [ ] NetBox reflects hypervisor + CTs + power + cables
- [ ] Docs & diagrams current
- [ ] Project board Phase 2 issues closed or moved to Phase 3

---

## Phase 3: Open Source Routing & Expansion (Future)

**Status:** 🔵 Planned

---

## Related Links
- Project Board: https://github.com/users/jacob-kraniak/projects/1
- Current checkpoint: [phase-2-checkpoint-2026-09-05.md](phase-2-checkpoint-2026-09-05.md)
- Wazuh repair baseline: [phase-2-baseline-2026-08-29.md](phase-2-baseline-2026-08-29.md)

*Keep this map current when adding artifacts.*
