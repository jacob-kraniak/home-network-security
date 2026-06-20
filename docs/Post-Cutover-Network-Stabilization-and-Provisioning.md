# Post-Cutover Network Stabilization and Provisioning

**Last updated:** 2026-06-20  
**Site:** Kraniak Home (`192.168.0.0/24`)  
**Focus:** Network stability → VLAN segmentation → full Omada management

---

## Cutover Summary

| Item | Detail |
|------|--------|
| **Status** | Successfully completed |
| **Date / time** | 2026-06-20, ~11:45 AM ET |
| **Downtime** | < 30 minutes |
| **Primary gateway** | TP-Link **ER605** (`192.168.0.1`) |
| **ER605 LAN MAC** | `58:04:4f:37:b9:cb` |
| **Upstream** | Verizon FIOS ONT → ER605 WAN |
| **Speed verification** | **320 / 320 Mbps** (download / upload) on Verizon |

### What changed

- **Archer A7** stepped down as primary router; **ER605** is now the edge gateway and DHCP server for the flat LAN.
- **TL-SG1016DE** managed switch is in the path for rack/core switching (VLAN trunking planned).
- **EAP225** and other Omada gear remain in **PRECONFIGURED** state until full Omada Cloud adoption completes.
- Physical topology target: **ONT → ER605 → switch → clients / APs**.

### Rollback note

ER605 configuration is exportable from Omada / local UI. Keep Archer A7 available until WAP conversion and VLAN cutover are validated.

---

## Post-Cutover ARP Snapshot (P14s)

Reference capture taken from **Lenovo ThinkPad P14s** (`UHQPF4P7QM2`) after cutover stabilization.

| IP | MAC | Notes |
|----|-----|-------|
| `192.168.0.1` | `58:04:4f:37:b9:cb` | ER605 gateway (primary router) |
| `192.168.0.103` | *(see live ARP)* | Client online at cutover |
| `192.168.0.100` | *(see live ARP)* | Client online at cutover |
| `192.168.0.108` | *(see live ARP)* | Client online at cutover |
| `192.168.0.139` | *(see live ARP)* | Client online at cutover (e.g. Pixel-10) |

> **Maintenance:** Re-capture ARP after major changes (VLAN rollout, AP conversion, new reservations). Store sanitized exports under `docs/inventory/` if needed for diffing; keep raw captures local/gitignored per [GROK-WORKSPACE.md](../GROK-WORKSPACE.md).

```bash
# Quick reference commands (Linux)
ip neigh show dev <iface>
arp -an | grep 192.168.0
```

---

## Stabilization Checklist

Use this order before VLAN segmentation.

- [x] ER605 online as gateway (`192.168.0.1`)
- [x] Internet throughput verified (320/320 Mbps)
- [x] Core clients receiving DHCP and reaching gateway
- [ ] **ER605 + EAP225 adopted in Omada Cloud** (move from PRECONFIGURED → Online)
- [ ] **DHCP reservations** on ER605 for critical MACs (servers, APs, infra)
- [ ] **Archer A7 converted to Access Point mode** (see below)
- [ ] **NetBox topology updated** (ONT → ER605, cables, interface statuses) — see [NetBox-Inventory-Progress.md](./NetBox-Inventory-Progress.md)
- [ ] VLAN design applied on ER605 + switch trunk ports
- [ ] Re-run inventory sync from [netbox-nmap-scan](https://github.com/jacob-kraniak/netbox-nmap-scan) after topology settles

---

## Archer A7 → Access Point Conversion

**Goal:** Repurpose Archer A7 as a downstream WAP only — no routing, no DHCP.

### Prerequisites

- ER605 stable as sole gateway
- Known static IP plan for AP management (recommend a reserved address on Main/LAN until VLAN 99 Mgmt exists)

### Steps

1. **Document current settings** (SSID names, passwords, channel) before changes.
2. **Assign static IP** on Archer (e.g. `192.168.0.105` or reserved address — align with DHCP plan and NetBox).
3. **Disable DHCP** on Archer A7 entirely.
4. **Enable AP / Access Point mode** (firmware: disable NAT/router features; wireless remains active).
5. **Physical cabling:** Connect Archer **WAN/LAN uplink** to a **switch port** on the trusted/Main network (not ONT directly).
6. **Validate:**
   - Wireless clients receive IP from ER605 DHCP
   - Default gateway for Wi-Fi clients is `192.168.0.1` (ER605)
   - Archer management UI reachable only on its static IP
7. **NetBox:** Update device role to WAP, status `active`, cable from switch → Archer LAN, retire old router/gateway associations.

### Post-conversion

- Consider replacing or supplementing with **Omada EAP225** once cloud adoption is complete.
- Archer may remain as backup WAP or guest SSID bridge during transition.

---

## VLAN Provisioning Plan

Target segmentation once flat LAN is stable on ER605.

| VLAN ID | Name | Purpose | ER605 interface | Notes |
|---------|------|---------|-----------------|-------|
| **1** | (default) | Flat LAN / transition | LAN until migrated | Retire after VLANs live |
| **10** | Main | Trusted family devices, workstations, servers | LAN + DHCP | Default trusted network |
| **20** | IoT | Smart home, cameras, sensors, appliances | Separate SSID / subnet | Align with IoT risk register |
| **30** | Guest | Isolated guest Wi-Fi | Guest SSID / subnet | No access to Main/IoT |
| **40** | Lab | Security lab, hypervisor mgmt, testing | Optional wired-only | P14s / Proxmox / Wazuh |
| **99** | Mgmt | Switch, AP, ER605 management | Management VLAN | Restrict access from other VLANs |

### Implementation sequence

1. Define subnets in ER605 (e.g. `192.168.10.0/24`, `192.168.20.0/24`, …) — finalize addressing before cutover.
2. Create VLANs on **TL-SG1016DE**; set trunk ports to ER605 and APs.
3. Map **EAP225** SSIDs to VLANs (Main / IoT / Guest).
4. Add **firewall rules** on ER605: IoT → Internet only; Guest → Internet only; block Guest/IoT → Main.
5. Seed **NetBox VLAN + prefix** objects to match live config.
6. Migrate DHCP scopes per VLAN; move reservations from flat LAN table.

Cross-reference: [phase-1-netbox-foundation.md](./phases/phase-1-netbox-foundation.md) (IPAM section), [iot-devices.md](./inventory/iot-devices.md).

---

## Omada Cloud Adoption

Devices expected in Omada SDN:

| Device | Role | Target state |
|--------|------|--------------|
| ER605-Router | Gateway | Online (cloud-managed) |
| TL-SG1016DE | Switch | Online |
| EAP225-Ceiling-AP | Access Point | Online |

### Adoption steps

1. Confirm ER605 has internet and correct time/NTP.
2. Log into **Omada Cloud** (or local controller if used).
3. For each device in **PRECONFIGURED**:
   - Verify serial/MAC matches hardware label.
   - Adopt → wait for **Online** status.
   - Apply firmware updates if prompted (maintenance window).
4. Group devices under site **Kraniak Home** (or equivalent).
5. Export / screenshot running config after adoption for rollback reference.
6. Update NetBox device status and comments with adoption date + firmware version.

---

## DHCP Reservations (ER605)

Create reservations for infrastructure and devices that must not float.

| Priority | Device | MAC | Suggested IP | Notes |
|----------|--------|-----|--------------|-------|
| Critical | ER605 (gateway) | `58:04:4f:37:b9:cb` | `192.168.0.1` | Static by definition |
| Critical | EAP225-Ceiling-AP | *(from NetBox)* | `192.168.0.105` | Verify post-adoption |
| Critical | Archer A7 (AP mode) | `B4:8C:24:D0:FD:60` | TBD reserved | After AP conversion |
| High | Bazzite-PC | *(from NetBox)* | `192.168.0.45` | Workstation / Wazuh testing |
| High | Verizon-ONT | N/A | N/A | L2 — document in NetBox only |

Full client list: sync from Archer/ER605 DHCP tables into NetBox via `netbox-nmap-scan` (`sync_dhcp_clients.py`). See inventory progress doc.

---

## NetBox Update Checklist (Post-Cutover)

- [ ] Set **ER605-Router** status `active`; primary IP `192.168.0.1/32` on LAN interface
- [ ] Cable: **Verizon-ONT** → **ER605 WAN1** (or documented WAN port)
- [ ] Cable: **ER605 LAN** → **TL-SG1016DE** uplink
- [ ] Update **Archer A7** role to WAP; remove gateway designation
- [ ] Mark **TL-SG105** / legacy switch paths if still in use (backup / interim)
- [ ] Add **VLAN** and **prefix** objects when ER605 VLANs go live
- [ ] Refresh tags (`env:home-lab`, `network-device:router`, `status:active`) via `rebuild_tags.py`
- [ ] Journal entry: cutover date, speed test result, rollback pointer

Detailed audit log: [NetBox-Inventory-Progress.md](./NetBox-Inventory-Progress.md)

---

## Pending / Next Actions

1. **Finalize & push** remaining local docs/changes to `main` on [home-network-security](https://github.com/jacob-kraniak/home-network-security).
2. **Convert Archer A7** to Access Point mode (static IP, DHCP off, uplink to switch).
3. **Adopt ER605 + EAP225** fully in Omada Cloud (PRECONFIGURED → Online).
4. **Create DHCP reservations** on ER605 for critical MACs.
5. **Proceed to VLAN config** on ER605 + switch trunking once stable.
6. **Update NetBox** with new topology (ONT → ER605, cables, statuses).

---

## Related Documentation

- [NetBox Inventory Progress](./NetBox-Inventory-Progress.md)
- [Phase 1 Completion](./phases/phase-1-completion.md)
- [NetBox Foundation](./phases/phase-1-netbox-foundation.md)
- [Devices Summary](./inventory/devices-summary.md)
- [Hardware Decisions](./hardware/DECISIONS.md)
- [Roadmap](./ROADMAP.md)
- Automation repo: [netbox-nmap-scan](https://github.com/jacob-kraniak/netbox-nmap-scan)
