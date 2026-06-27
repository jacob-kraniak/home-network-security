# Diagrams

This directory contains `.drawio` (diagrams.net / draw.io) files documenting the home network security project architecture and physical layout.

## Available Diagrams

| Diagram | Description | Open / Edit in draw.io | GitHub View |
|---------|-------------|------------------------|-------------|
| Future-State-Network-Diagram.drawio | Future-State Home Network Topology. Shows physical layers (Upstairs Living Room, Basement Racks, Home Office), centralized core networking (including moved FIOS ONT), VLAN strategy (color-coded: Green/Trusted, Red/IoT, Yellow/Guest, Blue/Work), cable paths, and logical flows. Includes notes on Starlink failover and Wazuh monitoring. **Updated to reflect dual-rack setup.** | [Open in draw.io](https://app.diagrams.net/#Hjacob-kraniak%2Fhome-network-security%2Fmain%2Fdocs%2Fdiagrams%2FFuture-State-Network-Diagram.drawio#%7B%22pageId%22%3A%22VYEXW0rNY10q_rIyr2fQ%22%7D) | [View on GitHub](https://github.com/jacob-kraniak/home-network-security/blob/main/docs/diagrams/Future-State-Network-Diagram.drawio) |
| Rack-Layout-12U.drawio | Basement Rack Physical Layout. **Revised for two separate racks**: Large enclosed 21" (~12-15U) cabinet-style and smaller open-frame ~15.5" (~8-9U). Use for planning gear allocation and U-spacing. | [Open in draw.io](https://app.diagrams.net/#Hjacob-kraniak%2Fhome-network-security%2Fmain%2Fdocs%2Fdiagrams%2FRack-Layout-12U.drawio#%7B%22pageId%22%3A%22rack-12u-revised%22%7D) | [View on GitHub](https://github.com/jacob-kraniak/home-network-security/blob/main/docs/diagrams/Rack-Layout-12U.drawio) |

## How to Edit

1. Click an "Open in draw.io" link above. ...

## Related Documentation

- [infrastructure-criteria.md](../hardware/infrastructure-criteria.md) — Server hardware decisions and revised core infrastructure strategy (updated for final Omada buildout: FR205, SG2008P v3.20, 2x EAP225, 21 clients per JSON).
- [DECISIONS.md](../hardware/DECISIONS.md) — Hardware decisions log (final deployed).
- [RACK.md](../hardware/RACK.md) — Rack & physical infrastructure (Phase 1 completed with Omada names).
- [rack-measurements.md](../hardware/rack-measurements.md) — Measurement tasks completed for final layout.
- [ROADMAP.md](../ROADMAP.md) — High-level project roadmap (Phase 1 complete per Omada JSON: 2 APs EAP225, switch SG2008P v3.20, FR205, client stats).
- Main project: [README.md](../../README.md) and [GROK-WORKSPACE.md](../../GROK-WORKSPACE.md)

**Note**: Living documents. Updated June 6, 2026 with confirmed rack measurements and final client/device stats from Omada JSON. Open diagrams in draw.io to adjust physical scales, add second rack representation, and reallocate gear (FR205 + SG2008P v3.20 + 2x EAP225).