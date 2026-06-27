# IoT Device Inventory & Risk Treatment Plan

## TP-Link Kasa
- **Devices**: 9x Smart Light Switches, 3x Smart Plugs (Total: 12)
- **Risk Level**: Medium-High (Cloud telemetry, firmware updates)
- **Current Treatment**: VLAN Isolation + Home Assistant local control
- **Target**: Risk Mitigation (short-term) → Matter/Thread replacement (long-term)

## Ring Ecosystem
- **Devices**: Doorbell Camera, Floodlight Cam, Security Base Station (Ethernet) + Keypad
- **Risk Level**: High (Video cloud storage, known privacy issues)
- **Current Treatment**: Immediate strict IoT VLAN + limited local access via Scrypted/Frigate
- **Target**: Risk Transference — Replace with local PoE cameras + Frigate NVR

## Google Nest
- **Devices**: Home Hub, Smart Thermostat, Lenovo Smart Clock, Home Speaker (1st Gen), Home Mini, Nest Mini (gen 3)
- **Risk Level**: High (Always-listening microphones, heavy data collection)
- **Current Treatment**: VLAN Isolation + Home Assistant integration where possible
- **Target**: Risk Transference — Migrate to local Zigbee/Z-Wave + Home Assistant Assist voice

## Overall IoT Strategy
- All devices → Dedicated IoT VLAN with egress-only firewall rules
- Central control via self-hosted Home Assistant (Proxmox VM)
- Long-term goal: Minimize cloud dependency for privacy

**Status (Final June 2026)**: Inventory complete and validated against Omada controller (21 clients total). clientTypeStat matches: smartHome 10 (TP-Link Kasa e.g. HS220/HS105 on vid20 IoT), camera 2 (Wyze v3 "Baby Cam" d0:3f:27:2b:2b:53 +), office 4 (Lenovo Smart Clock bc:df:58:b3:b2:c0 +), with full details (ips, rssi, traffic, vid 10/20). VLANs implemented (K108-Home-IoT vid20, Secure vid10). See root README and docs/ROADMAP.md for clientStat/JSON data. Rack buildout complete (FR205 + TL-SG1016DE + 2x EAP225).
