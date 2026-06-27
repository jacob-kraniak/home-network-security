# Home Network Security Buildout

Production segmented network using TP-Link Omada SDN (June 2026).

## Architecture Overview

**Hardware Stack:**
- **Gateway**: TP-Link ER605 v2.30 (firmware 2.3.3) – 192.168.0.1
- **Core Switch**: TP-Link SG2008P v3.20 (firmware 3.20.24) – 192.168.0.146
- **Wireless**: 2× TP-Link EAP225 v4.0
  - Living Room (192.168.0.148, firmware 5.2.4)
  - Office (192.168.0.105, firmware 5.2.2)
- **Controller**: Omada Software on BazzitePC

**VLAN Plan:**
- VLAN 1 (Management) – Infrastructure
- VLAN 10 (Trusted) – User devices / PCs
- VLAN 20 (IoT)
- VLAN 30 (Guest)
- VLAN 40 (Lab / Servers)

**Key Features:**
- 802.1Q trunking on AP ports (Native = Management, Tagged = 10/20/30/40)
- Centralized management & monitoring
- Foundation for Wazuh, Proxmox homelab, and further security tooling

See `docs/` for switch port profiles, WLAN mappings, ACL examples, and NetBox export.