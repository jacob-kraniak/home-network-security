# Grok Workspace Instructions - Home Network Security Project

## Project Overview
This repository documents the transition from consumer-grade networking to a secure, segmented, privacy-focused home network. It is part of the broader Privacy Migration project.

## Core Goals
- Accurate inventory of all devices (especially IoT)
- VLAN segmentation (Trusted, IoT, Guest, Work)
- Risk Mitigation (isolation) and Risk Transference (replacement) for IoT
- Self-hosted monitoring (Wazuh, Home Assistant)
- Rack build-out with pfSense/OPNsense

## Key Project Artifacts & Locations

- **Master Roadmap**: ../privacy-migration-docs (or link in GitHub Projects)
- **Current Inventory**:
  - docs/inventory/devices-summary.md
  - docs/inventory/iot-devices.md
  - docs/inventory/nmap/ (raw & sanitized scans)
- **Diagrams**: docs/diagrams/ (Home-Network-Diagram.drawio + VLAN versions)
- **Configs**: docs/configs/ (pfSense, Wazuh, firewall rules)
- **Risk Register**: docs/risk/ (IoT devices, mitigation plans)
- **Hardware Plans**: docs/hardware/ (rack build, shopping lists, mini-PC specs)
- **Self-Hosted Services Research & Roadmap**: docs/services/self-hosted-services-roadmap.md (Host OS, Proxmox, OPNsense, Wazuh, RustDesk, media servers, Home Assistant, camera migration, phased roadmap)
- **Document Digitization**: docs/services/document-digitization.md (Paperless-ngx based searchable archive - high priority)

## IoT Risk Strategy
- TP-Link Kasa (12x): VLAN + HA integration (Mitigation)
- Ring (4x): VLAN now → Full replacement with Reolink/Frigate (Transference)
- Google Nest (6x+): VLAN + local control → Zigbee/Z-Wave migration

## Working Guidelines for Grok
- Always maintain privacy: Sanitize MACs, IPs, and personal details in committed files.
- Use redacted summaries alongside raw data (raw data should be gitignored where possible).
- Follow existing folder structure.
- When suggesting changes (especially when handing off from Grok Chat to Grok Build), provide full file content in markdown blocks. See the "Parallel Workflow" section below for the required hand-off format.
- Cross-reference privacy-migration-docs where relevant.
- Track progress against the 4 parallel tracks: Privacy Migration, Software Migrations, Cybersecurity Education, Network Rack Build-out.

## Parallel Workflow: Grok Chat/Project Space vs. Grok Build

- **Grok Chat / project space** is used for ideation, research, brainstorming, and high-level planning. This is where ideas are explored, options are researched, and decisions are drafted.
- **Grok Build** is the implementation layer. It directly edits files in the GitHub repository, creates commits, opens issues, updates documentation, and executes concrete changes in the codebase.
- **Clear separation of concerns**: Use Grok Chat for thinking and drafting. Use Grok Build to turn those drafts into actual repository changes.
- **Hand-off rule**: Grok Chat should **always** present any input, instructions, or content destined for Grok Build in a cleanly formatted markdown block (using triple backticks with `markdown` or plain ```) that can be easily copied and pasted. This ensures a smooth, reliable hand-off between the two environments.

Example hand-off block (to be pasted into Grok Build):

```markdown
## Task for Grok Build

**Objective:** [Brief description]

**Files to create/update:**
- `path/to/file.md` (or full content if small)
- ...

**Instructions:**
1. ...
2. ...

**Context / Research Summary:**
[Key findings from chat/ideation]

**Acceptance Criteria:**
- ...
```

This workflow keeps research fluid in chat while ensuring precise, auditable implementation in the repo.

## GitHub Project Integration

Main Project Board: https://github.com/users/jacob-kraniak/projects/1 (Privacy Migration)

### How to Link Work:
1. Create Issues in this repo for specific tasks (Network Rack, IoT, Wazuh, etc.).
2. Add them to the main Project board:
   - Open the issue → Click "Projects" → Add to "Privacy Migration".
   - Or from the Project board, use "Add item" and search for issues from this repo.
3. Use these labels consistently:
   - `track:network-rack`
   - `track:privacy-migration`
   - `track:cyber-education`
   - `track:software-migration`
   - `status:planning` / `status:in-progress`

This ensures all network activities roll up into the master Privacy Migration roadmap.

Last Updated: 2026-06-05 (revised with parallel workflow)
