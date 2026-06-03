# Self-Hosted Services Research & Roadmap Documentation

**Project:** Home Network Security & Self-Hosted Infrastructure  
**Status:** Open Decisions | Aligned with Project Planner Goals (Security, Privacy, Reliability, Scalability)  
**Date:** June 2026  

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

**Phase 1 (Q2 2026):** Base OS + Proxmox + OPNsense + Wazuh + Document Digitization POC.

**Phase 2:** Core services (RustDesk, backups, media, full digitization import).

**Phase 3:** HA + cameras + advanced automation.

---

**Changelog / Version Notes:**
- 2026-06-03: Added condensed core decisions summary (Block 1). Promoted Document Digitization project from /project-ideas into active services documentation with dedicated page using Paperless-ngx stack. Updated GitHub issues for board. Maintained consistent formatting and privacy focus.
- 2026-06-03 (refinement): Incorporated exact user-provided content for Status, Recommended Stack (including Grok API, Nginx+Auth+VPN), and Action Items into document-digitization.md and linked section in roadmap.

**Next Steps for Workspace:** Expand issues in GitHub Project Board and track decisions. Let me know which area to deep-dive or generate configs for next. This keeps everything documented, privacy-aligned, and actionable per your guidelines.