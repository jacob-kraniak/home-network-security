# Self-Hosted Services Research & Roadmap Documentation

**Project:** Home Network Security & Self-Hosted Infrastructure  
**Status:** Open Decisions | Aligned with Project Planner Goals (Security, Privacy, Reliability, Scalability)  
**Date:** June 2026  

These markdown blocks are structured for easy pasting into your Grok build workspace. They follow a consistent format: Decision Area, Options & Research Summary, Recommendation, Pros/Cons, Action Items/Roadmap, and Risks/Dependencies. This aligns with your emphasis on privacy migration, documentation, and iterative planning.

## Summary of Core Infrastructure Decisions

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

## Detailed Sections

### 1. Host OS (Linux Distro)
**Recommendation:** Ubuntu Server LTS (24.04+)

## 2. Virtualization & App Host Platform
**Recommendation:** Proxmox VE + Docker Compose in LXC/VMs

## 3. Kubernetes for Distributed App Access
**Recommendation:** Skip for now (use only if scaling requires it)

## 4. External Access
**Recommendation:** DDNS + WireGuard/Tailscale VPN

## 5. Remote Access
**Recommendation:** Self-hosted RustDesk

## 6. Firewall/SDN
**Recommendation:** OPNsense

## 7. Security Monitoring
**Recommendation:** Wazuh SIEM/XDR

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
**Recommendation:** Paperless-ngx as the core tool for OCR, tagging, and full-text search. Deploy in Proxmox LXC/Docker with consumption folder for easy scanning. Backups via ZFS + encrypted offsite.

See dedicated page: [docs/services/document-digitization.md](document-digitization.md) for full Decision Area, Research, Pros/Cons, Action Items, and integration details (local-first, privacy-focused, integrates with Proxmox, Wazuh, Home Assistant).

## Overall Roadmap Integration

**Phase 1 (Q2 2026):** Base OS + Proxmox + OPNsense + Wazuh + Document Digitization POC.

**Phase 2:** Core services (RustDesk, backups, media, full digitization import).

**Phase 3:** HA + cameras + advanced automation.

---

**Changelog / Version Notes:**
- 2026-06-03: Added condensed core decisions summary. Promoted Document Digitization project from project-ideas into active services documentation with dedicated page. Updated GitHub issues.

**Next Steps:** Expand issues in GitHub Project Board and track decisions. Keep everything documented, privacy-aligned, and actionable.