# Home Document Digitization and Searchable Archive System

**Project:** Home Network Security & Self-Hosted Infrastructure  
**Status:** Planning | High Priority  
**Date:** June 2026  
**Related:** [Self-Hosted Services Roadmap](../services/self-hosted-services-roadmap.md)

## Overview
Goal: Eliminate paper clutter by creating a fully local, privacy-respecting, full-text searchable digital archive for documents (receipts, manuals, contracts, photos of documents, tax records, etc.). Replace reliance on cloud services (Google Drive, Dropbox, Evernote) with a self-hosted solution that supports OCR, tagging, and easy retrieval.

This project supports the broader goals of **Security, Privacy, Reliability, and Scalability**.

## Recommended Stack (2026)
- **Primary Tool:** Paperless-ngx (core document management)
  - OCR via Tesseract (excellent for printed + good handwriting support)
  - Automatic tagging, correspondent detection, and full-text search
  - Consumption folder (hotfolder) for easy import from scanners/phones
  - REST API for integrations (e.g., Home Assistant)
- **Frontend/Dashboard:** Paperless-ngx web UI + integration into a central Homepage or Nextcloud dashboard.
- **Storage Backend:** Local ZFS/Btrfs volume (via Proxmox) with snapshots. Optional MinIO for S3-compatible object storage and offsite encrypted backups.
- **Scanning/Input:**
  - Mobile: Open-source apps like "Open Scanner" or "Document Scanner" apps that save directly to SMB/NFS share.
  - Hardware: Dedicated document scanner (e.g., Fujitsu ScanSnap or Brother) feeding the consumption folder.
- **Backup & Redundancy:** Automated rsync to external drive + encrypted remote (e.g., via rclone to a private location).
- **Search Enhancement:** Paperless-ngx built-in search is strong; future integration with a local search engine if needed (e.g., via Meilisearch).
- **Optional Additions:** Gotenberg (for advanced PDF rendering), Tika (for more file types).

## Decision Area: Document Management Platform
**Options & Research Summary:**
- Paperless-ngx: Current community favorite for homelabs. Actively maintained, Docker-first, powerful automation, great OCR, and privacy-focused (no cloud).
- Mayan EDMS: More enterprise-oriented, heavier resource use.
- Docspell: Lightweight alternative with strong OCR and tagging.
- Nextcloud + full-text search / OnlyOffice: Good for general files but weaker dedicated document workflow and OCR compared to Paperless.
- Plain filesystem + Recoll or ripgrep: Too manual for large archives.

**Recommendation:** Paperless-ngx as the core system. Deploy in a dedicated LXC container or Docker Compose stack on Proxmox.

**Pros/Cons:**
- **Pros:** Excellent search and organization, local-only, active development, easy consumption workflow, API for automation, free and open source.
- **Cons:** Initial setup for consumption/hotfolder and scanning workflow; requires some maintenance for updates and backups; OCR quality depends on document quality.

**Action Items / Roadmap:**
- Deploy Paperless-ngx on Proxmox (LXC preferred for resource efficiency).
- Configure consumption directory with proper permissions (SMB share for easy phone/scanner access).
- Set up automated backups (ZFS snapshots + offsite encrypted copy).
- Test import workflow with sample documents (receipts, manuals).
- Integrate notifications (e.g., new documents added → Home Assistant).
- High priority: POC and initial import of critical documents in Q2 2026. Full production archive by end of Q3 2026.

**Risks/Dependencies:**
- Dependency on Proxmox storage stability.
- Scanning effort for existing paper (start with high-value documents).
- Handwriting OCR limitations (mitigate with good lighting/scanners).
- Data migration if switching tools later (Paperless has export options).

## Integration with Existing Infrastructure
- **Virtualization:** Run in Proxmox LXC (lightweight) or as a Docker stack inside a dedicated services VM.
- **Networking:** Accessible only via internal VLAN (Trusted or Work) + WireGuard VPN for remote access. No direct public exposure.
- **Security/Monitoring:** Wazuh agent for logging and vulnerability scanning. Regular updates via Unattended-upgrades or Proxmox.
- **Backup:** Leverage existing backup strategy (ZFS + external + offsite).
- **Search/Access:** Link from central dashboard (e.g., Homepage or Heimdall). Future: Voice search via Home Assistant.
- **Privacy:** Everything stays local. Documents never leave the network unless explicitly backed up encrypted.

## Current Status & Next Steps
- **Status:** Research complete. Awaiting hardware finalization and Proxmox deployment.
- **Related Issues:** See GitHub Project Board (Document Digitization System - high priority).
- **Version History:**
  - 2026-06-03: Initial dedicated page created and linked from main roadmap. Recommended stack finalized around Paperless-ngx.

This system will significantly reduce physical storage needs while providing fast, reliable, private access to important documents.