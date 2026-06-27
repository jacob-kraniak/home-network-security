# Home Network Security Roadmap (Revised June 20, 2026)

# Home Network Security Roadmap (Revised June 2026)

## Phase 1: Stable Family Foundation (Completed)
- Deployed TP-Link Omada SDN: FR205 (Multi-WAN) router + TL-SG1016DE managed switch (K108-MSW-1) + 2x EAP225 v4 APs (K108_WAP1_LivingRoom, K108_WAP2_Office).
- VLAN segmentation active: K108-Home-Secure (vid 10), K108-Home-IoT (vid 20), Management.
- 21 clients (2 wired including BazzitePC desktop, 19 wireless): smartHome:10 (TP-Link Kasa), camera:2 (Wyze v3 "Baby Cam" +), office:4 (Lenovo Smart Clock, etc.), with full clientStat/clientTypeStat per Omada controller JSON.
- Rack organization with PDU, Cat6.
- Dell OptiPlex 7060 Micro (i7-8700T, 32GB, 1TB NVMe) deployed as Proxmox services host (BazzitePC/compute).
- **Reference**: [docs/hardware/DECISIONS.md](../hardware/DECISIONS.md), [docs/hardware/RACK.md](../hardware/RACK.md), [docs/diagrams](../diagrams/) (Future-State-Network-Diagram.drawio, Rack-Layout-12U.drawio with actual EAP225/MSW-1/FR205).

## Phase 2: Self-Hosted Services (In Progress)
- Proxmox on Dell OptiPlex 7060 Micro active (BazzitePC/compute).
- Core containers/services: AdGuard Home, WireGuard, Vaultwarden, monitoring (Wazuh), media (Jellyfin), photo (Immich), HA, document (Paperless-ngx).
- TP-Link Omada as primary for stability (FR205 warm spare for rollback).
- **Reference**: Update [docs/diagrams](../diagrams/) with Proxmox host, services connections. See [docs/services/self-hosted-services-roadmap.md](../services/self-hosted-services-roadmap.md) and [document-digitization.md](../services/document-digitization.md).

## Phase 3: Open Source Routing & Expansion (Future)
- Migrate routing to OPNsense on dedicated hardware.
- Add hybrid NAS (Aoostar WTR Pro or equivalent).
- **Reference**: [docs/hardware](../hardware/) for future hardware matrix (e.g. OPNsense appliance).

**Risk Note**: Always maintain FR205 as warm spare for quick rollback. All updates use /docs structure; links in root README fixed to point under /docs.

**Final Buildout Stats (June 2026 per provided Omada JSON)**: 21 clients (2 wired/19 wireless), deviceStat: 2 APs (EAP225), 1 switch (TL-SG1016DE), 1 gateway (FR205); clientType: smartHome 10, camera 2, office 4, audioVideo 1, mobile 1, other 3. See full client list in project notes (Kasa HS220/HS105, Wyze "Baby Cam" d0:3f:27:2b:2b:53, Lenovo Clock bc:df:58:b3:b2:c0, BazzitePC e0:d5:5e:e3:98:97, Digital Frame, etc. on IoT/Secure SSIDs with rssi, traffic, vid 10/20/1).

*Last updated: 2026-06-06 — Phase 1 complete per JSON final state; docs updated with actual hardware/client stats.*
