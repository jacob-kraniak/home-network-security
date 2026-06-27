# Self-Hosted Services Research & Roadmap Documentation

> **High-level phases**: See the top-level [docs/ROADMAP.md](../ROADMAP.md) for the revised project roadmap (Phase 1-3 overview). This file contains the detailed research and decision logs.

**Project:** Home Network Security & Self-Hosted Infrastructure  
**Status:** Open Decisions | Aligned with Project Planner Goals (Security, Privacy, Reliability, Scalability)  
**Date:** June 12, 2026  

These markdown blocks are structured for easy pasting into your Grok build workspace. They follow a consistent format: Decision Area, Options & Research Summary, Recommendation, Pros/Cons, Action Items/Roadmap, and Risks/Dependencies. This aligns with your emphasis on privacy migration, documentation, and iterative planning.

## Summary of Core Infrastructure Decisions (Condensed)

### 1. Host OS
**Recommendation:** Ubuntu Server LTS (24.04+)

### 2. Virtualization & App Platform
**Recommendation:** Proxmox VE + Docker Compose in LXC/VMs

### 3. Kubernetes
**Recommendation:** Skip for now (use only if scaling requires it)

### 4. External Access
**Recommendation:** DDNS + WireGuard/Tailscale VPN

### 5. Remote Access
**Recommendation:** Self-hosted RustDesk

### 6. Firewall/SDN
**Recommendation:** OPNsense

### 7. Security Monitoring
**Recommendation:** Wazuh SIEM/XDR

### 8. IT Asset Management (ITAM)
**Recommendation:** NetBox (primary) or Snipe-IT

---

## Detailed Decision Areas

### 1. Host OS (Linux Distro)

**Options:** Fedora Server, Ubuntu Server LTS, Arch Linux.

**Research Summary:**

- **Ubuntu Server LTS (e.g., 24.04+):** Dominant for servers/homelabs due to stability, huge ecosystem, excellent documentation, and long-term support (5+ years). Strong for Docker/Proxmox/Wazuh.
- **Fedora Server:** Cutting-edge packages, good for developers, Cockpit web UI. Shorter lifecycle (upgrades every ~6 months). Solid for homelabs but more maintenance.
- **Arch:** Highly customizable but rolling-release risks breakage on a server. Better for advanced desktop than production-like hosting.

**Recommendation:** Ubuntu Server LTS (24.04 or newer) as base for stability and ecosystem alignment with self-hosted tools.

**Pros/Cons:**

- **Ubuntu:** High stability/community; slightly older packages.
- **Fedora:** Newer tech; more frequent upgrades.
- **Arch:** Ultimate control; higher risk.

**Action Items:**

- Test Ubuntu Server in a VM first.
- Document install process + hardening (firewall, unattended-upgrades).

**Roadmap:** Base OS decision Q2 2026; full migration path.

**Risks:** Distro lock-in; mitigate with containerization.

### 2. Virtualization & App Host Platform

**Options:** Docker (containers), Proxmox VE (hypervisor + LXC), ESXi (VMware).

**Research Summary:**

Proxmox VE (Debian-based) is the 2026 homelab favorite: free, KVM VMs + LXC containers, built-in backups, ZFS/Ceph, SDN. Docker excels for app isolation (run inside Proxmox VM or LXC). ESXi has licensing/cost issues post-Broadcom changes.

**Recommendation:** Proxmox VE as primary platform + Docker Compose/Portainer for apps inside dedicated Linux VMs/LXCs.

**Pros/Cons:**

- **Proxmox:** Feature-rich, open-source, easy clustering; learning curve.
- **Pure Docker:** Lightweight, fast; lacks full VM isolation.
- **ESXi:** Mature but costly/restricted now.

**Action Items:**

- Install Proxmox on dedicated hardware.
- Migrate/test key services in LXC + Docker.

**Roadmap:** Proxmox POC → Production by end of Q3 2026.

**Risks:** Nested virtualization overhead (minimal on modern hardware).

### 3. Kubernetes for Distributed App Access

**Options:** Full K8s (k3s/microk8s), or simpler alternatives (Docker Swarm, plain Docker Compose).

**Research Summary:** Overkill for most homelabs unless running many microservices with high availability needs. k3s is lightweight but adds complexity.

**Recommendation:** Skip full Kubernetes for now. Use Docker Compose + Proxmox for most services. Re-evaluate if scaling to 10+ complex apps.

**Action Items:**

- Document current/future services inventory.
- Test k3s in isolated VM if needed for learning.

**Risks:** Complexity overhead vs. benefits.

### 4. DDNS / Static IP for External Access

**Options:** ISP Static IP, DDNS (No-IP, DuckDNS, etc.), Tailscale/WireGuard VPN.

**Research Summary:** DDNS handles dynamic IPs reliably for most use cases. Combine with VPN for security (avoid exposing ports). Static IP simplifies but costs extra and reduces privacy slightly.

**Recommendation:** DDNS + strict firewall + VPN (WireGuard/Tailscale) as primary. Avoid direct port exposure.

**Action Items:**

- Set up DuckDNS or similar with Proxmox/OPNsense.
- Prioritize VPN for all remote access.

**Risks:** DDNS downtime (rare); ISP policy changes.

### 5. RustDesk for Remote Access

**Options:** Self-hosted OSS vs. Cloud/Pro version.

**Research Summary:** Self-hosted (hbbs/hbbr) is free, private, and sufficient for individuals. Pro adds web console/central management (subscription). Excellent open-source TeamViewer alternative.

**Recommendation:** Self-host OSS version on Proxmox/Docker. Use VPN for extra security.

**Action Items:**

- Deploy RustDesk server.
- Test clients across devices.

**Roadmap:** Integrate with central auth if needed.

**Risks:** Maintenance; use official Docker images.

### 6. pfSense or Equivalent SDN Solution

**Options:** pfSense, OPNsense (fork), IPFire, OpenWrt, VyOS.

**Research Summary:** OPNsense often preferred in 2026 for modern kernel, active development, and community (pfSense seen as more commercial). Strong firewall, VPN, IDS features.

**Recommendation:** OPNsense on dedicated hardware/appliance for core routing/firewall/SDN.

**Action Items:**

- Hardware selection (Protectli or similar).
- Migrate from current router.

**Risks:** Learning curve; backup configs religiously.

### 7. Wazuh SIEM/XDR

**Recommendation:** Deploy as all-in-one on Ubuntu/Proxmox VM. Excellent for homelab security monitoring (logs, vulnerability detection, active response).

**Action Items:**

- Install via official script/Docker.
- Add agents to key hosts (Proxmox, services).
- Integrate alerts with Home Assistant/Notify.

**Risks:** Resource usage (monitor RAM/CPU); start small.

### 8. IT Asset Management (ITAM) / CMDB

**Options:** Snipe-IT, NetBox, GLPI, RackTables, custom Markdown/Obsidian + Dataview.

**Research Summary:**

Markdown tables (as currently used in `docs/inventory/devices-summary.md`) work for small setups but become difficult to maintain as hardware, accessories, warranties, licenses, and rack relationships grow. A dedicated self-hosted ITAM tool provides structured data, relationships (racks → devices → ports → cables), search, reporting, QR/barcode support, warranty tracking, and depreciation.

**Top Contenders:**

- **Snipe-IT** (https://snipeitapp.com): Excellent traditional hardware asset management. Strong on check-in/check-out, people assignment, accessories, licenses, consumables, QR codes, and reporting. Docker Compose friendly. Very popular in homelabs and small IT teams. PHP + MySQL/MariaDB stack.

- **NetBox** (https://netbox.dev): Modern DCIM + IPAM + asset management. Outstanding for physical infrastructure (racks, devices, interfaces, cables, power distribution, VLANs). Has growing plugin ecosystem. Python/Django, excellent API, Docker support. Often preferred when you have physical racks + networking focus.

- **GLPI**: Feature-rich (assets + helpdesk + agent-based auto-inventory). More ITIL-oriented but heavier resource footprint.

- **RackTables**: Lightweight older tool focused on rack/DC management. Simpler but less actively developed.

- **Lightweight/Custom**: Keep using/enhancing `devices-summary.md` + Obsidian Dataview/Kanban (you already use Obsidian heavily). Or a simple self-hosted database frontend (e.g., Baserow, NocoDB, or Datasette). Lower overhead but less structured relationships and reporting.

**Recommendation:**

**Primary recommendation: NetBox**

Given your active basement rack build (large enclosed + smaller open rack), physical networking gear (ER605, future OPNsense, Omada, patch panels, cabling), and desire for structured relationships between racks, devices, and connections, **NetBox** is the stronger long-term fit. It excels at modeling exactly what you're building.

**Strong alternative: Snipe-IT** if your primary pain point is hardware tracking, warranties, accessories, and simple check-in/out rather than deep rack/cable/port modeling. Snipe-IT has a gentler learning curve for pure asset management.

You could even run both (NetBox for infrastructure modeling + Snipe-IT for consumables/licenses), but start with one.

**Pros of NetBox (Recommended):**
- Native rack elevation views and device positioning
- Excellent modeling of connections (interfaces, cables, power)
- Strong API + plugins (many homelab users extend it)
- Privacy-friendly self-hosted (no cloud dependency)
- Aligns well with future OPNsense + network documentation goals

**Cons of NetBox:**
- Steeper initial learning curve than Snipe-IT for non-networking assets
- Requires more initial modeling effort

**Pros of Snipe-IT:**
- Very intuitive for hardware, accessories, and people assignment
- Great reporting, depreciation, and warranty tracking
- Easier QR code / barcode workflows
- Slightly lighter for pure asset tracking

**Action Items:**

- Deploy a test instance of NetBox (Docker Compose recommended) on Proxmox.
- Import current hardware from `docs/inventory/devices-summary.md` (racks, ER605, PDU, table, planned devices).
- Evaluate rack elevation views and device type templates.
- Decide between NetBox vs Snipe-IT after 1-2 weeks of testing.
- If choosing one, plan migration path from Markdown tables and update `devices-summary.md` to point to the live ITAM as source of truth.

**Roadmap:**
- POC/test instance in late Q2 / early Q3 2026 (alongside rack physical install).
- Production deployment once rack hardware is mounted and initial devices are racked.
- Integrate with Wazuh (asset inventory as source) and future documentation systems.

**Risks/Dependencies:**
- Initial data modeling effort required.
- Database (PostgreSQL for NetBox) adds another service to maintain.
- Avoid over-modeling early; start minimal (racks + key devices) and expand.

## Later Goals

### 5. Plex/Jellyfin Media Server

**Recommendation:** Jellyfin (fully open-source, no subscriptions, privacy-focused). Strong transcoding, clients. Plex for polish/ecosystem if willing to pay.

### 6. Photo/Video Backup (ProtonDrive Alternative)

**Recommendation:** Immich or PhotoPrism for photos. Nextcloud or plain S3-compatible (MinIO) for sync/backup. Use rsync + encrypted storage.

### 7. Home Assistant

**Recommendation:** HA OS on dedicated hardware (Green or mini-PC) for best integration. Local-only focus with add-ons (Frigate for cameras).

### 8. Ring Cameras → Open-Source RTSP

**Recommendation:** Frigate + Scrypted for AI/object detection + RTSP exposure from Ring (or migrate to local cams). Integrate with Home Assistant.

## 9. Home Document Digitization and Searchable Archive System (New High-Priority Project)

**Status:** Promoted from project-ideas to active self-hosted service.

**Recommended Stack:**
- Paperless-ngx (core DMS)
- Tesseract OCR
- Proxmox LXC + Docker
- High-performance scanner (SMB/WiFi)
- Grok API for AI summaries
- Nginx + Auth + VPN access

See dedicated page: [docs/services/document-digitization.md](document-digitization.md) for full well-structured details (Decision Area, Research Summary, Recommendation, Pros/Cons, Action Items, Risks, integration).

**Action Items:**
- Acquire scanner
- Deploy Paperless-ngx test instance
- Configure consumption folder and automation

**Roadmap:** High priority - include in Phase 1. POC in Q2 2026.

## Overall Roadmap Integration

**Phase 1 (Completed June 2026)**: TP-Link Omada SDN (FR205 + SG2008P v3.20 K108-MSW-1 + 2x EAP225 APs) + base Proxmox on Dell OptiPlex 7060 Micro (BazzitePC/compute). 21 clients (2 wired, 19 wireless; smartHome 10 Kasa, camera 2 Wyze, office 4 incl. Lenovo Clock + BazzitePC desktop, vid 10/20/1 SSIDs). Per final controller JSON data. Document Digitization POC started. Wazuh/monitoring integrated.

**Phase 2 (In Progress)**: Expand self-hosted services on Proxmox (AdGuard, WireGuard, Vaultwarden, Jellyfin, Immich, HA, Paperless-ngx, RustDesk). Keep TP-Link Omada primary (FR205 warm spare).

**Phase 3 (Future)**: OPNsense migration + hybrid NAS (Aoostar WTR Pro). Full open-source routing.

**Final Buildout Stats (from Omada JSON)**: clientStat total 21 (wired 2, wireless 19, ipc 2, noData 19); clientType smartHome 10, camera 2, office 4, audioVideo 1, mobile 1, other 3; devices: 2 APs (EAP225 v4 fw5.2.2), 1 switch (SG2008P v3.20), 1 gateway (FR205); APs on 192.168.0.x, clients on 192.168.10/20/0 with rssi/traffic/vid details (e.g. Wyze d0:3f:27:2b:2b:53 Baby Cam on IoT, HS220 on IoT, BazzitePC e0:d5:5e:e3:98:97 wired Management, Lenovo bc:df:58:b3:b2:c0 Bedroom Clock on Secure).

See [docs/ROADMAP.md](../ROADMAP.md) for high-level phases.

---

**Changelog / Version Notes:**
- 2026-06-03: Added condensed core decisions summary (Block 1). Promoted Document Digitization project from /project-ideas into active services documentation with dedicated page using Paperless-ngx stack. Updated GitHub issues for board. Maintained consistent formatting and privacy focus.
- 2026-06-03 (refinement): Incorporated exact user-provided content for Status, Recommended Stack (including Grok API, Nginx+Auth+VPN), and Action Items into document-digitization.md and linked section in roadmap.
- 2026-06-06 (final buildout): Updated all references per Omada controller JSON (21 clients, 2 EAP225 APs, SG2008P v3.20 switch, FR205 router, vid/SSID details, clientTypeStat). Marked Phase 1 complete; Phase 2 Dell Proxmox deployed. Fixed links to /docs subdirs in root README and related docs. No duplication.

**Next Steps for Workspace:** Expand issues in GitHub Project Board and track decisions. Let me know which area to deep-dive or generate configs for next. This keeps everything documented, privacy-aligned, and actionable per your guidelines.