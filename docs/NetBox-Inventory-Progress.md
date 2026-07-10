# NetBox Inventory Progress

**Last updated:** 2026-07-10  
**NetBox instance:** [NetBox Cloud](https://arfv7221.cloud.netboxapp.com/) (private)  
**Primary site:** Kraniak Home  
**Automation repo:** [netbox-nmap-scan](https://github.com/jacob-kraniak/netbox-nmap-scan)  
**Public summary:** [network-overview.md](network-overview.md)

---

## Current Snapshot

| Metric | Value (approx.) |
|--------|-----------------|
| Devices | ~53 (+1 Proxmox host) |
| VLANs | 3 active (1, 10, 20) |
| Prefixes | 3 (`192.168.0/10/20.0/24`) |
| Tag schema | `key:value` |
| Public repo | Redacted — NetBox is authoritative IPAM |

### Core infrastructure (production)

| Device | Role | Segment | Status |
|--------|------|---------|--------|
| Verizon-ONT | Network / ONT | — | Documented; WAN handoff to ER605 |
| ER605-Gateway | Gateway / firewall | LAN-Secure | Primary router; VLAN tagging on LAN3 |
| OpenWRT-AP | WAP / VLAN termination | 1/10/20 | Subinterfaces `br-lan.1/.10/.20` |
| TL-SG116E-SWITCH-1 | Switch | LAN-Secure | Active; patch panel 1:1 |
| K108_WAP2_Office | WAP (EAP225) | LAN-Secure | Omada office AP |
| PATCH-PANEL | Infrastructure | — | PP# = switch port # |
| Startech PDU | PDU | — | Rack-mounted |
| **Lenovo-M715q-Proxmox** | Hypervisor | LAN-Secure (planned) | **NEW 2026-07-10** — Free employer M715q Tiny (S/N MJ067MNT, type 10M3000PUS). 16GB RAM. KingSpec 512GB NVMe boot + SanDisk Z400 256GB 2.5" for potential RAID1. Dual DP. To be racked in Server Hosts rack. |

---

## 2026-07-10 — Proxmox Host Acquired ✅

- Free Lenovo ThinkCentre M715q Tiny (retired employer asset) received and inventoried.
- Serial: MJ067MNT
- Machine Type: 10M3000PUS (M715q)
- Support: https://pcsupport.lenovo.com/us/en/products/desktops-and-all-in-ones/thinkcentre-m-series-desktops/m715q/10m3/10m3000pus/mj067mnt
- Storage: KingSpec 512GB NVMe Gen3x4 installed; SanDisk Z400 256GB 2.5" SATA mounted in bay (potential RAID1 mirror).
- RAM: 16GB DDR4 (upgrade path to 32GB available).
- Role: Primary Proxmox VE host for containers/VMs (Wazuh, Jellyfin, HA, etc.).
- **Action required in NetBox**: Create Device Type (Lenovo M715q Tiny), Device instance (role: Hypervisor / Server), assign to Server Hosts rack, add interfaces (DP, Ethernet, USB), power port, custom fields (serial, acquisition_date=2026-07-10, cost=0, notes=employer surplus).
- Public docs updated in devices-summary.md, DECISIONS.md, RACK.md, ROADMAP.md.

---

## 2026-06-20 — Production inventory complete ✅

NetBox documentation milestone reached. Public repo updated with redacted summaries.

| Item | Status |
|------|--------|
| ER605-Gateway primary gateway | ✅ |
| ONT → ER605 WAN cable | ✅ |
| ER605 LAN3 → OpenWRT trunk | ✅ |
| OpenWRT → TL-SG116E uplink | ✅ |
| VLANs 1/10/20 (LAN-Secure, IoT, Guest) | ✅ active |
| Prefixes per VLAN | ✅ |
| OpenWRT-AP device + subinterfaces | ✅ |
| K108_WAP2_Office (EAP225) | ✅ |
| DHCP client sync (~42 hosts) | ✅ |
| DESCRIPTIVE-ROLE naming convention | ✅ |
| SSID objects (K108-Home-*) | ✅ |

**Automation scripts added/updated:** `sync_network_inventory.py`, `vlan_specs.py`, `sync_naming_inventory.py`

---

## Inventory Audit Log (prior)

### 2026-06-13 — Phase 1 foundation bootstrap
- Sites, racks, PDU, taxonomy templates. See [phase-1-netbox-foundation.md](phases/phase-1-netbox-foundation.md).

### 2026-06-14 — 18 → 52 devices
- DHCP import, ARP alignment, topology cables started.

### 2026-06-19 — Tag schema + walk-through
- `rebuild_tags.py`; physical walk-through sync; LG appliance types.

---

## Automation Scripts (`netbox-nmap-scan`)

| Script | Purpose |
|--------|---------|
| `sync_network_inventory.py` | VLANs, prefixes, OpenWRT, ER605 topology |
| `sync_dhcp_clients.py` | DHCP list → devices, MACs, IPs |
| `sync_naming_inventory.py` | Naming convention + SSID metadata |
| `sync_home_rack.py` | Rack placement + cables |
| `sync_walkthrough.py` | Physical walk-through → NetBox |
| `rebuild_tags.py` | `key:value` tag schema |

---

## Remaining Gaps (Phase 2)

1. **Power modeling** — PDU outlet → device connections ([#19](https://github.com/jacob-kraniak/home-network-security/issues/19))
2. **Proxmox / virtualization** — cluster + VM objects once host live (**host hardware now acquired — next**)
3. **Automated sync** — scheduled NetBox refresh from DHCP/nmap
4. **Public diagrams** — sanitized topology draw.io from NetBox export
5. **Omada Cloud adoption** — move PRECONFIGURED APs to managed state

---

## Related Documentation

- [Network Overview](network-overview.md)
- [Post-Cutover Stabilization](Post-Cutover-Network-Stabilization-and-Provisioning.md)
- [Devices Summary](inventory/devices-summary.md)
- [Roadmap](ROADMAP.md)
