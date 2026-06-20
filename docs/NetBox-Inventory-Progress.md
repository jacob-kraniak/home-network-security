# NetBox Inventory Progress

**Last updated:** 2026-06-20  
**NetBox instance:** [NetBox Cloud](https://arfv7221.cloud.netboxapp.com/)  
**Primary site:** Kraniak Home  
**Automation repo:** [netbox-nmap-scan](https://github.com/jacob-kraniak/netbox-nmap-scan)

This document tracks CMDB population and audit activity complementing the physical cutover documented in [Post-Cutover-Network-Stabilization-and-Provisioning.md](./Post-Cutover-Network-Stabilization-and-Provisioning.md).

---

## Current Snapshot

| Metric | Value (approx.) |
|--------|-----------------|
| Devices | ~52 |
| IPs in `192.168.0.0/24` | ~42 |
| Tag schema | `key:value` (e.g. `env:home-lab`, `vlan:lan`, `device-class:iot`) |
| Legacy flat tags | Removed / migrated |
| Device custom fields | `device_key`, `model_number`, `scantime` |

### Core infrastructure (post-cutover target state)

| Device | Role | Type | IP | Status / notes |
|--------|------|------|-----|----------------|
| Verizon-ONT | Network | Nokia FIOS ONT | — | Upstream of ER605; serial documented |
| ER605-Router | router / Firewall | ER605 | `192.168.0.1` | **Primary gateway** after 2026-06-20 cutover |
| TL-SG1016DE | Switch | *(planned type)* | TBD | Managed Omada switch — populate in NetBox |
| TL-SG105 | Switch | TL-SG105 | — | Active distribution switch |
| Archer A7 | router → **WAP** | Archer A7 | `192.168.0.1` → migrate | Convert to AP; update role/cables |
| EAP225-Ceiling-AP | WAP | EAP225 | `192.168.0.105` | Omada adoption pending |
| Startech PDU | PDU | RKPW081915 | — | Rack-mounted |

---

## Taxonomy Additions (2026-06)

### Manufacturers created

| Manufacturer | Notes |
|--------------|-------|
| Nokia | FIOS ONT |
| Akimart | Digital photo frame |

### Roles created

| Role | Slug | Used for |
|------|------|----------|
| IoT-Security | `iot-security` | Ring base station |
| HVAC | `hvac` | Nest Thermostat |
| Display | `display` | Nest Hub, Lenovo Smart Clock |
| Network | `network` | ONT, Cisco backup switch |

### Device types created (walk-through + appliances)

| Type | Manufacturer | Assigned devices |
|------|--------------|------------------|
| Ring Base Station | Ring | Ring-Base-Station |
| Nest Thermostat | Google | Nest-Thermostat |
| SG100-16 | Cisco | Cisco-SG100-16-Switch (backup) |
| FIOS ONT | Nokia | Verizon-ONT |
| Nest Hub | Google | Living-Room-Display |
| Smart Clock | Lenovo | Bedroom-Clock |
| ZN-DP1002 | Akimart | Digital-Frame-Frameo |
| Smart Oven | LG | LG_Smart_Oven2 |
| Smart Dryer | LG | LG_Smart_Dryer2 |
| Smart Washer | LG | LG_Smart_Laundry2 |

---

## Inventory Audit Log

Chronological summary of significant NetBox automation and manual corrections.

### 2026-06-13 — Phase 1 foundation bootstrap

- Sites, racks, PDU, taxonomy templates (ER605, Archer A7, generics).
- ~100 changelog entries. See [phase-1-netbox-foundation.md](./phases/phase-1-netbox-foundation.md).

### 2026-06-14 — 18 → 52 devices

- Router enrichment (Archer A7 WAN/LAN MACs, EAP225).
- DHCP client import from Archer A7 (~41 clients).
- Device alignment via ARP/OUI (`align_devices.py`).
- Topology documentation and cable modeling started.

### 2026-06-19 — Tag schema migration

- Rebuilt tags to `key:value` schema (`rebuild_tags.py`).
- Legacy flat tags removed; descriptions migrated.
- DHCP sync updated for renamed devices (Nest-Thermostat, Kasa-HS103-Plug, Living-Room-Display).

### 2026-06-19 — Physical walk-through sync

Applied `sync_walkthrough.py` — physically verified inventory:

| Action | Device |
|--------|--------|
| Created | Ring-Base-Station, Cisco-SG100-16-Switch, Bedroom-Clock, Digital-Frame-Frameo |
| Renamed | Nest-Thermostat-5A16 → Nest-Thermostat; Unknown-113 → Living-Room-Display; Kasa-HS103-199 → Kasa-HS103-Plug |
| Enriched | Verizon-ONT (Nokia serial), Archer A7 (serial + LAN MAC `B4:8C:24:D0:FD:60`) |

### 2026-06-19 — Taxonomy refinement

- Created walk-through-specific **roles** and **device types** (no more generic IoT reuse for verified hardware).
- All seven walk-through devices assigned correct role/type pairs.

### 2026-06-19 — LG appliances

- Created LG Smart Oven / Dryer / Washer device types from inventory comments (vendor **LG Innotek** in scan data).
- Assigned to `LG_Smart_Oven2`, `LG_Smart_Dryer2`, `LG_Smart_Laundry2`.

### 2026-06-19 — Duplicate merges

| Merge | Result |
|-------|--------|
| `android-153` + `Digital-Frame-Frameo` | Single device **Digital-Frame-Frameo** (`wlan0` `.153`) — Frameo photo frame |
| `UHQPF4P7QM2-196` + `UHQPF4P7QM2-71` | Single device **UHQPF4P7QM2** — `eth0` wired `.196`, `wlan0` wireless `.71` (P14s) |

### 2026-06-20 — Post-cutover (pending NetBox updates)

- [ ] ER605 confirmed primary gateway in NetBox (role, IP, cables)
- [ ] ONT → ER605 WAN cable documented
- [ ] ER605 → TL-SG1016DE cable documented
- [ ] Archer A7 demoted from router to WAP in NetBox
- [ ] VLAN / prefix objects for VLANs 10, 20, 30, 40, 99
- [ ] Omada adoption metadata (firmware, cloud status) on ER605 / EAP225

---

## Automation Scripts (`netbox-nmap-scan`)

| Script | Purpose |
|--------|---------|
| `sync_dhcp_clients.py` | Archer/ER605 DHCP list → devices, MACs, IPs |
| `sync_device_networks.py` | ARP bindings, interface MAC alignment |
| `sync_walkthrough.py` | Physical walk-through YAML → NetBox |
| `align_devices.py` | OUI-based IP alignment + primary IPs |
| `rebuild_tags.py` | `key:value` tag schema enforcement |
| `import_iot_scan.py` | Incremental `iot_scan.xml` → comments/tags |
| `setup_lg_appliance_types.py` | LG appliance device types |
| `lg_appliance_types.py` | LG type definitions (shared module) |

### Multi-interface DHCP bindings

`sync_dhcp_clients.py` maps multiple DHCP hostnames to one device:

| DHCP hostname | NetBox device | Interface |
|---------------|---------------|-----------|
| `UHQPF4P7QM2-196` | `UHQPF4P7QM2` | `eth0` |
| `UHQPF4P7QM2-71` | `UHQPF4P7QM2` | `wlan0` |

Primary IPv4 is set from `eth0` when defined in `PRIMARY_INTERFACES`.

---

## Tag Schema Reference

Representative tags applied via `rebuild_tags.py`:

```
env:home-lab
vlan:lan
status:active
device-class:iot | workstation | appliance | infrastructure | camera
asset-criticality:Low | Medium | High | Critical
vendor:tp-link | google | lg | lenovo | ...
network-device:router | switch | wap | ont
scan:autoscan
```

---

## Gaps & Phase 2 Priorities

Aligned with [phase-1-netbox-foundation.md](./phases/phase-1-netbox-foundation.md):

1. **Cutover topology** — cables and interface connections for ONT → ER605 → switch path.
2. **TL-SG1016DE** — create device type + instance; trunk interfaces.
3. **VLAN/IPAM** — prefixes per VLAN plan in post-cutover doc.
4. **Virtualization** — Proxmox cluster/VMs once host is live.
5. **Bulk IoT** — continue nmap import; resolve `Unknown-*` DHCP names.
6. **Custom fields** — populate `model_number` from walk-through and scan data.

---

## Related Documentation

- [Post-Cutover Network Stabilization](./Post-Cutover-Network-Stabilization-and-Provisioning.md)
- [Phase 1 NetBox Foundation](./phases/phase-1-netbox-foundation.md)
- [IoT Devices](./inventory/iot-devices.md)
- [Devices Summary](./inventory/devices-summary.md)
