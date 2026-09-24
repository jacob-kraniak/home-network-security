# Phase 3 — Remote Network Access

**Status:** 🔵 Planned  
**Created:** 2026-09-24  
**Issue:** [#34](https://github.com/jacob-kraniak/home-network-security/issues/34)  
**Does not close Phase 2.** RustDesk on CT 101 is desktop control only.

Phase 2 close already parks “WireGuard/Tailscale as a product” in Phase 3. This file is the missing **exit definition**.

---

## Why this is Phase 3

| Path | Phase | What it is | What it is not |
|------|-------|------------|----------------|
| RustDesk (`hbbs`/`hbbr` on CT 101) | 2 (live) | Screen/session to a desktop | A network path into the rack |
| Cloudflare Tunnel (#25) | Voice-agent track | Inbound HTTPS to one app | Laptop → datacenter |
| VPN / WireGuard / Tailscale | **3** | Encrypted path from Jacob's laptop to management LAN | WAN publish of admin UIs |

**Exit criterion:** Jacob can access the datacenter from anywhere on his laptop.

“Datacenter” here = the basement rack services host and the Omada management plane (PVE, CT 100 Wazuh, CT 101 Portainer / Omada / NetBox). Not a requirement to hairpin every IoT VLAN on day one.

---

## Product choice (undecided — pick one and document)

Any of these can meet the exit if the test below passes. Do not run two inbound VPN products on the same WAN port without a written decision.

1. **Tailscale (or Headscale)** — fastest path to “laptop off-LAN sees VLAN 1 hosts.” Good default if OPNsense is still months out.
2. **WireGuard on a Phase 2 CT / the M715q** — self-hosted, no mesh vendor. Needs a stable inbound path (DDNS + one UDP port) or a bounce host.
3. **WireGuard on OPNsense** — correct long-term home if Phase 3 routing cutover is in the same window. Do not block the laptop exit on the OPNsense hardware buy.

Research already on file: [self-hosted-services-roadmap.md §4](../services/self-hosted-services-roadmap.md) and [#13](https://github.com/jacob-kraniak/home-network-security/issues/13). Those are not the exit test.

---

## Hard rules

- Do **not** WAN-publish PVE, Wazuh, Portainer, Omada, or NetBox to satisfy this gate.
- Do **not** treat “I can RustDesk a workstation” as done.
- Tokens, keys, Tailscale auth URLs, and WAN IPs stay off this public repo.
- Split-tunnel vs full-tunnel is an operator choice; record it when chosen. Split-tunnel to management prefixes is enough for the exit.

---

## Exit requirements

- [ ] Product chosen and written here (one row, dated)
- [ ] Laptop client installed and used as the daily remote path
- [ ] Off-LAN acceptance test passed (cellular hotspot or other non-home network)
- [ ] From that session, at least **PVE** and **one CT 101 admin UI** load over the tunnel
- [ ] Those UIs remain unpublished on WAN
- [ ] Short dated checkpoint in `docs/phases/` (no keys, no WAN IPs)
- [ ] #34 closed or moved to a follow-on only after the test is recorded

**Not required for this exit:** OPNsense live, site-to-site to another site, family devices on the mesh, AdGuard, Plane.so, media stack.

---

## Acceptance test (copy into the checkpoint)

1. Leave home Wi-Fi. Use phone hotspot (or any foreign LAN).
2. Bring the tunnel/mesh up on the laptop.
3. Open PVE and one of: Portainer, Omada controller, NetBox.
4. Confirm the same services are not reachable from the hotspot *without* the tunnel.
5. Write the dated note. Stop.

---

## Related

- Phase 2 close: [phase-2-close-linkedin.md](phase-2-close-linkedin.md)
- Phase map: [PHASE-ARTIFACTS.md](PHASE-ARTIFACTS.md)
- Roadmap: [../ROADMAP.md](../ROADMAP.md)
- OPNsense track: [#9](https://github.com/jacob-kraniak/home-network-security/issues/9)
- Voice-agent tunnel (not this exit): [#25](https://github.com/jacob-kraniak/home-network-security/issues/25)
