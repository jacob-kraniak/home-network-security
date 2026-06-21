# Home Network Security Roadmap (Revised June 20, 2026)

## Phase 1.5: ER605 Cutover + VLAN Segmentation — ✅ COMPLETE (2026-06-20)

- **Cutover:** ER605 is primary gateway. Completed ~11:45 AM ET; Verizon speed verified at 320/320 Mbps.
- **VLANs deployed:** VID 1 LAN-Secure, VID 10 IoT, VID 20 Guest — prefixes `192.168.0/10/20.0/24`.
- **Architecture:** ER605 VLAN tagging → OpenWRT subinterfaces → TL-SG116E distribution.
- **WiFi SSIDs:** K108-Home-Secure, K108-Home-IoT, K108-Guest.
- **NetBox documentation:** Production inventory synced; public repo redacted. See [network-overview.md](network-overview.md), [NetBox-Inventory-Progress.md](NetBox-Inventory-Progress.md).
- **Remaining operational items:**
  1. Omada Cloud full adoption (ER605, EAP225, TL-SG116E)
  2. DHCP reservations for critical infrastructure MACs
  3. Dedicated electrician outlet for rack PDU ([#20](https://github.com/jacob-kraniak/home-network-security/issues/20))

## Phase 1: Stable Family Foundation + Rack Relocation + NetBox Bootstrap — ✅ COMPLETE

- Physical rack + ER605 + PDU installed in basement.
- NetBox CMDB bootstrap (~52 devices, taxonomy, tags, racks).
- See [phase-1-completion.md](phases/phase-1-completion.md), [phase-1-netbox-foundation.md](phases/phase-1-netbox-foundation.md).

## Phase 2: Self-Hosted Services & Automation (Next)

- **Proxmox** on Dell OptiPlex / mini-PC; model in NetBox as Hypervisor.
- **Wazuh** SIEM/XDR deployment ([#10](https://github.com/jacob-kraniak/home-network-security/issues/10)).
- **Automated NetBox sync** — scheduled DHCP/nmap refresh from [netbox-nmap-scan](https://github.com/jacob-kraniak/netbox-nmap-scan).
- **Public topology diagrams** — sanitized draw.io from NetBox export.
- Core services: AdGuard, WireGuard, Vaultwarden, Jellyfin, Home Assistant, Paperless-ngx.
- NetBox Phase 2: power modeling ([#19](https://github.com/jacob-kraniak/home-network-security/issues/19)), virtualization objects, bulk IoT risk tags.
- Reference: [self-hosted-services-roadmap.md](services/self-hosted-services-roadmap.md)

## Phase 3: Open Source Routing & Expansion (Future)

- Evaluate OPNsense/pfSense migration from ER605 edge.
- Camera migration (Reolink/Frigate), Zigbee for Nest.
- NetBox plugins/webhooks for Proxmox/Wazuh integration.

**Risk / Rollback:** ER605 config exportable. All changes tracked in NetBox changelog.

*Last updated: 2026-06-20* — NetBox production documentation complete; Phase 2 (Proxmox/Wazuh) next.
