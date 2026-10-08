# Network telemetry → Wazuh: detection plan (2026-10-08)

> **Status:** Plan only. Nothing deployed. Builds on [wazuh-omada-syslog.md](wazuh-omada-syslog.md).

## Goal

Enough telemetry in Wazuh (`192.168.0.178`) to write rules for:

1. Brute-force attempts from unknown MAC addresses
2. Unknown IPs appearing on VLANs 1 / 10 / 20
3. Outbound traffic to untrusted destinations

## What existing data covers

| Detection | Covered today by | Gap |
|-----------|------------------|-----|
| 1. Brute force, unknown MAC | ER605 DHCP leases (MAC↔IP) once the decoder works; known-MAC CDB list | Omada logs no client auth failures; EAP225 v4 cannot see Wi-Fi PSK guessing or deauth. Failures only appear on the target host. |
| 2. Unknown IP | DHCP leases + `srcip` from `omada-ap-traffic` vs a known-IP CDB list | Static-IP wired hosts never lease; AP traffic covers Wi-Fi only. |
| 3. Untrusted outbound | `dstip` / `dstport` from `omada-ap-traffic` vs a bad-IP CDB list | No wired flows, no domain names; ER605 exports no firewall/NAT session logs. |

## Planned additions (in order)

1. **Fix the ER605 DHCP decoder first** (`omada-er605`, `omada-er605-dhcp`, test rule 100500). Everything else correlates on leases.
2. **Known-MAC / known-IP CDB lists generated from NetBox** (on-prem SoT at `192.168.0.200:8000`). Rules alert on any lease or `srcip` not on the list.
3. **Wazuh agents (or forwarded auth logs) on targets**: Proxmox `.176`, Omada controller / NetBox CT 101, SSH hosts. Built-in failed-login rules, correlated to the DHCP lease for the source MAC.
4. **Pi-hole DNS query logging (Phase 2)**: Pi-hole handed out as the resolver on every VLAN via DHCP, query log shipped to Wazuh. Covers bad-domain detection.
5. **Suricata or Zeek on a mirrored port** between the ER605 and the LAN switch, `eve.json` read by a Wazuh agent. Covers wired traffic, outbound flows, and static-IP hosts.

## DNS resolver decision: Pi-hole (2026-10-08)

Pi-hole is the chosen resolver for DNS query logging and moves up to **Phase 2**. AdGuard Home is dropped from the roadmap.

Rationale:

- **Proven locally:** successful Raspberry Pi proof of concept last year.
- **Lightweight:** fits the M715q Proxmox host as a small LXC at **1 vCPU / 512 MiB RAM / 4 GB disk** (Pi-hole docs: 512 MB RAM, 2 GB min / 4 GB recommended disk).
- **Wazuh fit:** query logs give Wazuh the per-client domain data needed for detection rules.

## Prerequisites and constraints

- **Port mirroring:** confirm the Omada switch model supports it before planning step 5.
- **Capture NIC:** the M715q has a single Ethernet port; a mirror feed needs a second NIC (e.g., USB 3 gigabit) passed to the sensor guest.
- **Host RAM:** M715q config RAM is already ~12 GiB of ~14.58 GiB (see [Compute Sizing](self-hosted-services-roadmap.md#compute-sizing--hardware-acquisition-2026-10-01)). Pi-hole takes ~0.5 GiB of that headroom (~2.1 GiB left); a Suricata sensor would use the rest.
- **CT 100 disk:** keep under 80%; Suricata and DNS logs raise Wazuh index volume.
- **Wazuh 5.0** removes the built-in 514 listener; plan rsyslog + agent before upgrading.

## Open decisions

- Sensor choice: Suricata (signature alerts) vs Zeek (connection/DNS logs) vs both.
- Sensor host: M715q now vs Host B.
