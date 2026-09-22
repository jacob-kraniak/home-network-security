# Network Overview — Production State (2026-06-20, services note 2026-09-21)

**Site:** Kraniak Home  
**Authoritative IPAM:** on-prem NetBox at `http://192.168.0.200:8000` (CT 101) — SoT as of 2026-09-21 ([#28](https://github.com/jacob-kraniak/home-network-security/issues/28))  
**NetBox Cloud:** archive / reference only — pending reconcile toward on-prem (not authoritative)  
**Automation:** [netbox-nmap-scan](https://github.com/jacob-kraniak/netbox-nmap-scan)

This document is a **redacted, public-safe** summary. Exact host IPs, full MAC addresses, serial numbers, and DHCP client tables are maintained only in NetBox.

---

## Architecture

```
                    ┌─────────────────┐
   ISP ────────────►│  ER605-Gateway  │  VLAN tagging (1 / 10 / 20 / 30 / 40)
                    │   (Omada SDN)   │
                    └────────┬────────┘
                             │ LAN3 trunk
                    ┌───────┴────────┐
                    │   OpenWRT-AP    │
                    │  br-lan.1       │  LAN-Secure
                    │  br-lan.10      │  IoT
                    │  br-lan.20      │  Guest
                    └───────┬────────┘
                             │
                    ┌───────┴────────┐
                    │ TL-SG116E       │  16-port Easy Smart
                    │ SWITCH-1        │  patch panel 1:1
                    └───────┬────────┘
                             │
              ┌─────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
         Trusted clients  IoT / Guest    Lab / mgmt hosts
         (VLAN 10)        (20 / 30)      (40 / 1)
```

**Design notes:**
- ER605 performs **802.1Q VLAN tagging**; Omada Controller is on-prem (CT 101).
- SSIDs / L2 distribution via Omada-managed switch + APs (OpenWRT may still terminate some subinterfaces historically).
- Management hosts (Proxmox, CTs, controller) live on VLAN 1 (`192.168.0.0/24`).

---

## VLANs & Prefixes

**Omada SoT (2026-09-15 screenshot / Lab Watch cross-check):** gateway = `.1` on each `/24`.

| VID | Omada name | Purpose | Gateway / prefix | Typical SSID |
|-----|------------|---------|------------------|--------------|
| 1 | Management (Default) | Infrastructure / management | `192.168.0.1/24` (`192.168.0.0/24`) | (wired / mgmt) |
| 10 | Trusted | Trusted clients / secure WLAN | `192.168.10.1/24` (`192.168.10.0/24`) | K108-Home-Secure |
| 20 | IoT | Smart home / IoT devices | `192.168.20.1/24` (`192.168.20.0/24`) | K108-Home-IoT |
| 30 | Guest | Visitor network | `192.168.30.1/24` (`192.168.30.0/24`) | K108-Guest (as provisioned) |
| 40 | Lab | Lab / experiment segment | `192.168.40.1/24` (`192.168.40.0/24`) | (as provisioned) |

> **Supersedes** the June 2026 public table that incorrectly mapped VLAN 10→IoT and VLAN 20→Guest. Treat **Omada as live VLAN/network SoT**. On-prem NetBox is IPAM SoT; Cloud archive may lag and is not authoritative.

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

*Last updated: 2026-09-21 (on-prem NetBox IPAM SoT; Cloud archive pending reconcile).*
