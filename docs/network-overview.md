# Network Overview — Production State (2026-06-20)

**Site:** Kraniak Home  
**Authoritative IPAM:** [NetBox Cloud](https://arfv7221.cloud.netboxapp.com/) (private)  
**Automation:** [netbox-nmap-scan](https://github.com/jacob-kraniak/netbox-nmap-scan)

This document is a **redacted, public-safe** summary. Exact host IPs, full MAC addresses, serial numbers, and DHCP client tables are maintained only in NetBox.

---

## Architecture

```
                    ┌─────────────────┐
   ISP ────────────►│  ER605-Gateway  │  VLAN tagging (1 / 10 / 20)
                    │   (Omada SDN)   │
                    └────────┬────────┘
                             │ LAN3 trunk
                    ┌────────▼────────┐
                    │   OpenWRT-AP    │
                    │  br-lan.1       │  LAN-Secure
                    │  br-lan.10      │  IoT
                    │  br-lan.20      │  Guest
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ TL-SG116E       │  16-port Easy Smart
                    │ SWITCH-1        │  patch panel 1:1
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
        K108_WAP2_Office  BazzitePC    IoT clients (~40+)
        (EAP225 office)   (workstation)
```

**Design notes:**
- ER605 performs **802.1Q VLAN tagging** on the uplink trunk.
- OpenWRT terminates VLANs via **subinterfaces** (`br-lan.N`).
- Basement switch provides L2 distribution; management IPs are on LAN-Secure.

---

## VLANs & Prefixes

| VID | NetBox name | Purpose | Prefix | SSID |
|-----|-------------|---------|--------|------|
| 1 | LAN-Secure | Trusted LAN / infrastructure | `192.168.0.0/24` | K108-Home-Secure |
| 10 | IoT | Smart home / IoT devices | `192.168.10.0/24` | K108-Home-IoT |
| 20 | Guest | Visitor network | `192.168.20.0/24` | K108-Guest |

All three VLANs are **active** in NetBox (group: `Kranak-Home-VLANs`).

---

## Core Infrastructure (NetBox)

| Device | Role | Notes |
|--------|------|-------|
| Verizon-ONT | Upstream handoff | FIOS optical terminal → ER605 WAN |
| ER605-Gateway | Primary gateway | Omada SDN; DHCP + VLAN tagging |
| OpenWRT-AP | VLAN termination | Subinterfaces on `br-lan` bridge |
| TL-SG116E-SWITCH-1 | Managed switch | In-band mgmt on LAN-Secure |
| K108_WAP2_Office | Omada WAP | EAP225 v4; office coverage |
| PATCH-PANEL | Termination | Port # = switch port # (1:1) |
| CISCO-SG100-16-SWITCH-2 | Backup switch | Secondary / spare |
| RASPBERRY-PI-3 | Temp host | Basement rack (port 2) |

**Key clients** (names only — see NetBox for IPs/MACs): BazzitePC, Pixel-10, Google/Nest IoT fleet, Kasa switches, Ring cameras, LG appliances, Tesla.

---

## Redaction Policy (public repo)

| In NetBox (private) | In this repo (public) |
|---------------------|----------------------|
| Full IPv4/MAC per host | Device role + VLAN segment only |
| DHCP client table | Aggregate counts (~52 devices) |
| WAN public IP | "ISP handoff" reference only |
| Personal hostnames | Sanitized or omitted |

Raw nmap XML and ARP captures remain **local / gitignored** per [GROK-WORKSPACE.md](../GROK-WORKSPACE.md).

---

## Sync Scripts

| Script | Purpose |
|--------|---------|
| `sync_network_inventory.py` | VLANs, prefixes, OpenWRT, ER605 topology |
| `sync_dhcp_clients.py` | DHCP inventory → devices/IPs |
| `sync_naming_inventory.py` | Naming convention + metadata |
| `sync_home_rack.py` | Rack placement + cables |

---

## Related Docs

- [NetBox Inventory Progress](NetBox-Inventory-Progress.md)
- [Post-Cutover Stabilization](Post-Cutover-Network-Stabilization-and-Provisioning.md)
- [Devices Summary](inventory/devices-summary.md)
- [Roadmap](ROADMAP.md)

*Last updated: 2026-06-20*
