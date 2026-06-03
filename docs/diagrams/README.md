# Diagrams

This directory contains `.drawio` (diagrams.net / draw.io) files documenting the home network security project architecture and physical layout.

## Available Diagrams

| Diagram | Description | Open / Edit in draw.io | GitHub View |
|---------|-------------|------------------------|-------------|
| Future-State-Network-Diagram.drawio | Future-State Home Network Topology. Shows physical layers (Upstairs Living Room, Basement Rack, Home Office), centralized core networking (including moved FIOS ONT), VLAN strategy (color-coded: Green/Trusted, Red/IoT, Yellow/Guest, Blue/Work), cable paths, and logical flows. Includes notes on Starlink failover and Wazuh monitoring. | [Open in draw.io](https://raw.githubusercontent.com/jacob-kraniak/home-network-security/main/docs/diagrams/Future-State-Network-Diagram.drawio) | [View on GitHub](https://github.com/jacob-kraniak/home-network-security/blob/main/docs/diagrams/Future-State-Network-Diagram.drawio) |
| Rack-Layout-12U.drawio | 12U Basement Rack Physical Elevation (Future State). Detailed front-view rack layout with U1–U12 positions, incoming fiber/CAT6 from floor hole, centralized components (ONT in U3, firewall, switch, Proxmox, UPS, PDU, etc.), legend distinguishing planned vs. current/temporary hardware, and cable management notes. | [Open in draw.io](https://raw.githubusercontent.com/jacob-kraniak/home-network-security/main/docs/diagrams/Rack-Layout-12U.drawio) | [View on GitHub](https://github.com/jacob-kraniak/home-network-security/blob/main/docs/diagrams/Rack-Layout-12U.drawio) |

## How to Edit

1. Click an "Open in draw.io" (raw) link above — it will load directly into the online editor.
2. Or download the `.drawio` file and open it in the desktop app or https://app.diagrams.net.
3. Diagrams are designed with layers (e.g., Current State vs. Target Future State, Cable Paths). Use the Layers panel in draw.io to toggle visibility.
4. Feel free to add icons from the built-in libraries (search for "server", "router", "switch", "rack", "UPS", etc.) and refine shapes/positions.

## Related Documentation

- [infrastructure-criteria.md](../hardware/infrastructure-criteria.md) — Server hardware decisions and revised core infrastructure strategy.
- [rack-measurements.md](../hardware/rack-measurements.md) — Measurement tasks for finalizing the physical layout.
- Main project: [README.md](../../README.md) and [GROK-WORKSPACE.md](../../GROK-WORKSPACE.md)

**Note**: These are living documents. Update the diagrams and this README as the network build progresses.
