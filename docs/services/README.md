# Services

This directory documents the planned self-hosted services and core infrastructure for the Home Network Security & Self-Hosted Infrastructure project.

All decisions prioritize **security, privacy, reliability, and scalability**. Documentation follows a consistent format (Decision Area, Research Summary, Recommendation, Pros/Cons, Action Items, Risks).

## Planned Applications & Infrastructure

| Service / Component | Description | Recommendation | Key Summary / Details | Roadmap Phase | Details Link |
|---------------------|-------------|----------------|-----------------------|---------------|--------------|
| Host OS | Base operating system for servers and services. | Ubuntu Server LTS (24.04+) | Dominant for homelabs: stability, huge ecosystem, 5+ year support. Strong for Docker/Proxmox/Wazuh. | Phase 1 (Q2 2026) | [self-hosted-services-roadmap.md](self-hosted-services-roadmap.md#1-host-os-linux-distro) |
| Virtualization & App Platform | Hypervisor and container platform for running services. | Proxmox VE + Docker Compose (in LXC/VMs) | Free KVM VMs + LXC, built-in backups/ZFS. Docker for app isolation. Skip full Kubernetes for now (overkill unless 10+ microservices). | Phase 1 (Q2 2026) | [self-hosted-services-roadmap.md](self-hosted-services-roadmap.md#2-virtualization--app-host-platform) |
| Firewall / SDN | Core routing, firewall, and software-defined networking. | OPNsense | Preferred over pfSense in 2026 for modern kernel and active development. Strong VPN/IDS features. Run on dedicated hardware. | Phase 1 | [self-hosted-services-roadmap.md](self-hosted-services-roadmap.md#6-pfsense-or-equivalent-sdn-solution) |
| Security Monitoring (SIEM/XDR) | Logging, vulnerability detection, and active response. | Wazuh (all-in-one on Ubuntu/Proxmox VM) | Excellent for homelab: logs, vuln scanning, agents on key hosts. Integrate with HA/Notify. | Phase 1 | [self-hosted-services-roadmap.md](self-hosted-services-roadmap.md#7-wazuh-siemxdr) |
| Remote Access | Secure remote desktop/control. | Self-hosted RustDesk (OSS) | Free/private alternative to TeamViewer. Run on Proxmox/Docker. Use with VPN. | Phase 2 | [self-hosted-services-roadmap.md](self-hosted-services-roadmap.md#5-rustdesk-for-remote-access) |
| External Access | Secure remote connectivity without exposing ports. | DDNS + WireGuard/Tailscale VPN | DDNS for dynamic IPs + strict firewall + VPN as primary. Avoid direct port exposure. | Phase 1 | [self-hosted-services-roadmap.md](self-hosted-services-roadmap.md#4-ddns--static-ip-for-external-access) |
| Media Server | Self-hosted media streaming (movies/TV). | Jellyfin (Plex as paid alternative) | Fully open-source, no subscriptions, privacy-focused. Strong transcoding/clients. | Phase 2 | [self-hosted-services-roadmap.md](self-hosted-services-roadmap.md#later-goals) |
| Photo/Video Backup | Local photo/video management and backup (ProtonDrive alternative). | Immich or PhotoPrism + Nextcloud/MinIO | Immich/PhotoPrism for photos; rsync + encrypted storage for general backup. | Phase 2 | [self-hosted-services-roadmap.md](self-hosted-services-roadmap.md#later-goals) |
| Home Automation | Smart home hub and automation. | Home Assistant (HA OS on dedicated hardware) | Local-only with add-ons (e.g., Frigate for cameras). Best integration on Green/mini-PC. | Phase 3 | [self-hosted-services-roadmap.md](self-hosted-services-roadmap.md#later-goals) |
| Camera / NVR | Video surveillance and AI detection (migrate from Ring). | Frigate + Scrypted (with RTSP) | AI/object detection + RTSP from Ring (or local cams). Integrate with Home Assistant. | Phase 3 | [self-hosted-services-roadmap.md](self-hosted-services-roadmap.md#later-goals) |
| Document Digitization | Searchable archive for physical documents (paperless system). | Paperless-ngx (with Tesseract OCR) | Core DMS for OCR/tagging/search. Deploy in Proxmox LXC + Docker. Consumption folder for scanning. Grok API for AI summaries. Access via Nginx + Auth + VPN. High-performance scanner (SMB/WiFi). | Phase 1 (high priority POC) | [document-digitization.md](document-digitization.md) |

## Notes
- **Kubernetes**: Explicitly skipped for now to avoid unnecessary complexity.
- **Infrastructure Foundation**: All services run on Ubuntu Server LTS under Proxmox, behind OPNsense, monitored by Wazuh, accessed securely via VPN.
- **Privacy Focus**: Everything is local-first. No unnecessary cloud dependencies. VPN for remote access.
- **Phased Approach**:
  - **Phase 1 (Q2 2026)**: Base OS + Proxmox + OPNsense + Wazuh + Document Digitization POC.
  - **Phase 2**: Core services (RustDesk, backups, media).
  - **Phase 3**: HA + cameras + advanced automation.
- Full research, pros/cons, action items, and risks are in the linked documents.

See [self-hosted-services-roadmap.md](self-hosted-services-roadmap.md) for complete details, research summaries, and overall roadmap.