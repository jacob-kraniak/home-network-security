# Phase Artifacts & Documentation Map

**Canonical reference** for which documents, diagrams, configs, and inventories belong to each project phase.  
**Last Updated:** 2026-07-10  
**Authoritative Timeline:** GitHub Project Board + Issues (see bottom)

> **Usage:** When working on a phase, start here. Update this file whenever a new artifact is created or an existing one is promoted/demoted between phases.

---

## Phase 1: Network Build (Stable Family Foundation)

**Status:** ✅ **Completed** (June 2026)  
**Goal:** Physical rack build-out, Omada SDN gateway + switching + APs, VLAN segmentation (1/10/20), NetBox foundation, basic inventory.

### Core Deliverables (Completed)
- Physical basement racks (Network Stack + Server Hosts)
- TP-Link Omada stack: FR205 / ER605 gateway, SG2008P / TL-SG116E switch, 2× EAP225 APs
- VLAN 1 (Management/LAN-Secure), 10 (Trusted/Secure), 20 (IoT) live
- StarTech PDU, patch panel, structured Cat6
- NetBox Cloud foundation (sites, racks, device types, power model, tags, initial devices)
- 21-client inventory baseline from Omada controller

### Associated Artifacts / Documents

| Category | File / Location | Description |
|----------|-----------------|-------------|
| **Roadmap & Status** | [docs/ROADMAP.md](../ROADMAP.md) | High-level Phase 1 completion summary |
| | [docs/phases/phase-1-completion.md](phase-1-completion.md) | Physical rack install & relocation log |
| | [docs/phases/phase-1-netbox-foundation.md](phase-1-netbox-foundation.md) | NetBox bootstrap details (taxonomy, racks, power) |
| | [docs/NetBox-Inventory-Progress.md](../NetBox-Inventory-Progress.md) | Ongoing NetBox audit log (Phase 1 sections) |
| **Hardware** | [docs/hardware/DECISIONS.md](../hardware/DECISIONS.md) | Final Omada hardware decisions + rationale |
| | [docs/hardware/RACK.md](../hardware/RACK.md) | Phase 1 rack layout |
| | [docs/hardware/home-lab-rack-build.md](../hardware/home-lab-rack-build.md) | Purchase log & physical install notes |
| | [docs/hardware/rack-measurements.md](../hardware/rack-measurements.md) | Physical measurements |
| | [docs/hardware/infrastructure-criteria.md](../hardware/infrastructure-criteria.md) | Selection criteria |
| **Inventory** | [docs/inventory/devices-summary.md](../inventory/devices-summary.md) | Public-safe hardware table (Phase 1 devices) |
| | [docs/inventory/iot-devices.md](../inventory/iot-devices.md) | IoT risk inventory (Kasa, Wyze, etc.) |
| | `docs/inventory/*.xml` (gitignored) | Raw nmap / Omada exports |
| **Diagrams** | [docs/diagrams/Future-State-Network-Diagram.drawio](../diagrams/Future-State-Network-Diagram.drawio) | Production topology |
| | [docs/diagrams/Rack-Layout-12U.drawio](../diagrams/Rack-Layout-12U.drawio) | Rack elevation |
| | [docs/diagrams/README.md](../diagrams/README.md) | Diagram conventions |
| **Network Overview** | [docs/network-overview.md](../network-overview.md) | Public sanitized architecture |
| | [docs/Post-Cutover-Network-Stabilization-and-Provisioning.md](../Post-Cutover-Network-Stabilization-and-Provisioning.md) | Cutover notes |
| **Assets** | `assets/phase1/` | Photos of rack install |
| **Workspace** | [GROK-WORKSPACE.md](../../GROK-WORKSPACE.md) | Phase 1 production architecture snapshot |

### Phase 1 Exit Criteria (Met)
- [x] Racks powered & organized
- [x] Omada SDN live with VLANs
- [x] NetBox foundation + core devices
- [x] Public docs updated & redacted
- [x] Project board Phase 1 issues closed

---

## Phase 2: Self-Hosted Services Build

**Status:** 🟡 **In Progress** (Host hardware acquired 2026-07-09/10)  
**Goal:** Deploy Proxmox VE on dedicated host, stand up core self-hosted services (Wazuh, AdGuard, WireGuard, Jellyfin, Immich, Home Assistant, Paperless-ngx, RustDesk, Vaultwarden, etc.), integrate with NetBox & monitoring, document everything.

### Core Deliverables (Target)
- Proxmox VE host online (Lenovo M715q Tiny)
- Containerized / VM services running
- NetBox fully populated with hypervisor + VMs + interfaces + power
- Local management display + backup strategy
- Service-specific docs, configs, and runbooks
- Updated diagrams & inventory

### Associated Artifacts / Documents

| Category | File / Location | Description |
|----------|-----------------|-------------|
| **Roadmap & Status** | [docs/ROADMAP.md](../ROADMAP.md) | Phase 2 section (host status, next steps) |
| | [docs/phases/PHASE-ARTIFACTS.md](PHASE-ARTIFACTS.md) | This file |
| | [docs/NetBox-Inventory-Progress.md](../NetBox-Inventory-Progress.md) | Phase 2 NetBox entries (Proxmox host, future VMs) |
| **Services Research** | [docs/services/self-hosted-services-roadmap.md](../services/self-hosted-services-roadmap.md) | Core decisions (Proxmox, Wazuh, OPNsense later, etc.) |
| | [docs/services/document-digitization.md](../services/document-digitization.md) | Paperless-ngx stack (high priority) |
| | [docs/services/README.md](../services/README.md) | Services index |
| **Hardware (Phase 2 Host)** | [docs/inventory/devices-summary.md](../inventory/devices-summary.md) | Lenovo M715q entry (KingSpec NVMe + SanDisk Z400) |
| | [docs/hardware/DECISIONS.md](../hardware/DECISIONS.md) | M715q acquisition & rationale |
| | [docs/hardware/RACK.md](../hardware/RACK.md) | Phase 2 host placement notes |
| **Configs (Future)** | `docs/configs/` | Proxmox, Wazuh, Docker Compose, firewall rules, etc. (to be populated) |
| **Diagrams (Future)** | `docs/diagrams/` | Updated with Proxmox host, service topology, VLANs |
| **Inventory** | NetBox Cloud | Authoritative for VMs, IPs, interfaces once live |

### Phase 2 Entry / Current State (2026-07-10)
- [x] Free Lenovo ThinkCentre M715q Tiny acquired (S/N MJ067MNT)
- [x] KingSpec 512GB NVMe installed
- [x] SanDisk Z400 256GB 2.5" mounted for potential RAID1
- [ ] BIOS prep (SVM, C6, Secure Boot, etc.)
- [ ] Proxmox VE install
- [ ] NetBox device + rack placement
- [ ] Local DP monitor / adapter decision
- [ ] First services (Wazuh, AdGuard, WireGuard recommended order)

### Phase 2 Exit Criteria (Target)
- [ ] Proxmox VE stable + updated
- [ ] Core services running with backups
- [ ] NetBox reflects hypervisor + VMs + power + cables
- [ ] All Phase 2 docs & diagrams current
- [ ] Project board Phase 2 issues closed or moved to Phase 3

---

## Phase 3: Open Source Routing & Expansion (Future)

**Status:** 🔵 Planned  
**Goal:** OPNsense migration, hybrid NAS, advanced monitoring, further privacy hardening.

Artifacts will be defined when Phase 2 nears completion. Placeholder references currently live in ROADMAP.md and services roadmap.

---

## How to Maintain This Map

1. **New document created** → Add row to the correct phase table above.
2. **Document moves phases** → Update both tables + commit message.
3. **Major milestone** → Update ROADMAP.md status + this file’s checklists.
4. **GitHub Issues / Project Board** → Every Phase 1/2 deliverable should have a corresponding issue linked to the Privacy Migration board (https://github.com/users/jacob-kraniak/projects/1).

### Recommended Labels
- `track:network-rack` (mostly Phase 1)
- `track:privacy-migration`
- `track:self-hosted-services` (Phase 2)
- `phase:1` / `phase:2` / `phase:3`
- `status:planning` / `status:in-progress` / `status:done`

---

## Related Links
- Project Board: https://github.com/users/jacob-kraniak/projects/1
- NetBox Cloud: https://arfv7221.cloud.netboxapp.com/ (private)
- GROK-WORKSPACE.md (top-level instructions)
- Privacy Migration overarching docs (separate repo)

*This file is the single source of truth for “which docs belong to which phase.” Keep it current.*
