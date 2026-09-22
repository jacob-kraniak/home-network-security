# Home Network Security Buildout

Production segmented home network (Omada SDN, June 2026) plus Phase 2 self-hosted services on Proxmox.

**Start here for live state:** [docs/phases/phase-2-checkpoint-2026-09-16.md](docs/phases/phase-2-checkpoint-2026-09-16.md) (2026-09-16).  
**Wazuh outage narrative (historical):** [docs/phases/phase-2-baseline-2026-08-29.md](docs/phases/phase-2-baseline-2026-08-29.md).

This repository is **public**. Keep credentials, WAN IPs, full MACs, and unredacted scans out of commits. NetBox is authoritative for IPAM: **on-prem** (local CT 101 / `http://192.168.0.200:8000`) is SoT; Cloud is archive pending reconcile ([#28](https://github.com/jacob-kraniak/home-network-security/issues/28)).

## Architecture Overview (live)

**Hardware stack**
- **Gateway:** TP-Link ER605 V2 (Omada SDN)
- **Core switch:** TP-Link SG2008P v3.20 (K108-MSW-1)
- **Wireless:** Omada EAP225 coverage (office + living room)
- **Controller:** Omada 6.3 on CT 101 (`https://192.168.0.200:8043`)
- **Proxmox (Phase 2, live):** Lenovo ThinkCentre M715q Tiny — PVE 9.2.4 node `debian` `192.168.0.176`
  - **RAM:** 2×8 GB DDR4 SO-DIMM (~14.6 GiB visible after 2026-09-05 reboot)
  - CT 100 Wazuh `192.168.0.178` (6 GiB)
  - CT 101 Portainer `192.168.0.200` (6 GiB / 100G) — Portainer + Omada + RustDesk + **NetBox v4.7** (`http://192.168.0.200:8000`)

**VLAN plan (active — Omada SoT 2026-09-15)**
- VLAN 1 — Management (Default) — `192.168.0.1/24`
- VLAN 10 — Trusted — `192.168.10.1/24` (K108-Home-Secure)
- VLAN 20 — IoT — `192.168.20.1/24` (K108-Home-IoT)
- VLAN 30 — Guest — `192.168.30.1/24`
- VLAN 40 — Lab — `192.168.40.1/24`
- Details: [docs/network-overview.md](docs/network-overview.md)

**Design notes**
- 802.1Q tagging at the ER605; L2 distribution via managed switch + patch panel
- Foundation for Wazuh + Portainer + NetBox on the M715q; AdGuard / WireGuard next

## Key Documents

- [Phase 2 checkpoint (2026-09-16)](docs/phases/phase-2-checkpoint-2026-09-16.md) — **return here first**
- [Phase Artifacts Map](docs/phases/PHASE-ARTIFACTS.md)
- [Project Roadmap](docs/ROADMAP.md)
- [Network overview (public-safe)](docs/network-overview.md)
- [Hardware inventory summary](docs/inventory/devices-summary.md)
- [Hardware decisions](docs/hardware/DECISIONS.md)
- [IoT devices & risk plan](docs/inventory/iot-devices.md)
- [Grok workspace instructions](GROK-WORKSPACE.md)
- [Self-hosted services roadmap](docs/services/self-hosted-services-roadmap.md)
- Diagrams: `docs/diagrams/`

## Parallel Tracks

This repo supports the Privacy Migration project. See [privacy-migration-docs](https://github.com/jacob-kraniak/privacy-migration-docs) for the overarching roadmap. Project board: https://github.com/users/jacob-kraniak/projects/1

## Repository Structure

```
.
├── README.md
├── GROK-WORKSPACE.md
├── .gitignore
└── docs/
    ├── inventory/     # Summaries (raw nmap XML gitignored)
    ├── diagrams/      # Draw.io topology / rack
    ├── hardware/      # DECISIONS.md, RACK.md, criteria
    ├── phases/        # Phase map + checkpoints + baselines
    ├── services/      # Self-hosted services research
    ├── configs/       # Placeholder for future exports
    ├── network-overview.md
    └── ROADMAP.md
```

## Getting Started

1. Clone the repo
2. Read [docs/phases/phase-2-checkpoint-2026-09-16.md](docs/phases/phase-2-checkpoint-2026-09-16.md) before changing the M715q
3. Keep raw scans and secrets local; review `.gitignore` before any forced adds
4. Prefer on-prem NetBox for live IPs/MACs — this repo holds architecture and redacted summaries. No live sync from bots without Jacob yes.

## Security Notes

- Public docs only: RFC1918 lab addresses used intentionally in Phase 2 checkpoints; no credentials or WAN IPs
- Do not commit full packet captures or unredacted device dumps
- Audit diffs for accidental secrets before commit
- Do not WAN-publish admin UIs (PVE, Wazuh, Portainer, Omada, NetBox)

*Last reconciled: 2026-09-21 (on-prem NetBox IPAM SoT; Cloud archive pending reconcile).*
