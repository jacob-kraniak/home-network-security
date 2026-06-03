# Home Document Digitization and Searchable Archive System

**Project:** Home Network Security & Self-Hosted Infrastructure  
**Status:** Promoted from project-ideas to active self-hosted service.  
**Date:** June 2026  
**Related:** [Self-Hosted Services Roadmap](../services/self-hosted-services-roadmap.md)

## Overview
Goal: Eliminate paper clutter by creating a fully local, privacy-respecting, full-text searchable digital archive for documents (receipts, manuals, contracts, photos of documents, tax records, etc.). Replace reliance on cloud services (Google Drive, Dropbox, Evernote) with a self-hosted solution that supports OCR, tagging, and easy retrieval.

This project supports the broader goals of **Security, Privacy, Reliability, and Scalability**.

## Recommended Stack
- Paperless-ngx (core DMS)
- Tesseract OCR
- Proxmox LXC + Docker
- High-performance scanner (SMB/WiFi)
- Grok API for AI summaries
- Nginx + Auth + VPN access

**Details:** Paperless-ngx as primary for document management, OCR with Tesseract, automatic tagging, full-text search, consumption folder (hotfolder) for easy import. Deploy in Proxmox LXC + Docker. Storage on local ZFS with snapshots + optional MinIO for backups. Access via Nginx reverse proxy with auth and VPN only (no direct exposure). Use Grok API for AI-powered summaries and search enhancements.

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

**Action Items:**
- Acquire scanner
- Deploy Paperless-ngx test instance
- Configure consumption folder and automation

**Roadmap:** High priority - POC in Q2 2026, production by Q3. Integrate with Phase 1 of self-hosted services.

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