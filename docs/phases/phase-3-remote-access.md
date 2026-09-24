# Phase 3 — Remote Access

**Status:** 🔵 Planned  
**Created:** 2026-09-24  
**Does not close Phase 2.** RustDesk *server* on CT 101 is already the Phase 2 remote-access line.

Two tracks. They can run in parallel. They are not equal.

| Priority | Track | Exit in one line | Issue |
|----------|-------|------------------|-------|
| **P0** | Layer 3 path | Laptop reaches the datacenter from anywhere | [#34](https://github.com/jacob-kraniak/home-network-security/issues/34) |
| **P1** | RustDesk fleet | Real-time desktop session to each in-scope endpoint | [#35](https://github.com/jacob-kraniak/home-network-security/issues/35) |

P1 does not block P0. P1 is not a substitute for P0. A working RustDesk session to one PC is not “datacenter access.”

---

## Why these are Phase 3

| Path | Phase | What it is | What it is not |
|------|-------|------------|----------------|
| RustDesk server (`hbbs`/`hbbr` on CT 101) | 2 (live) | ID/relay for desktop sessions | Clients on every endpoint; off-LAN path |
| RustDesk **clients** on endpoints | **3 / P1** | Screen control of named desktops | Network path into the rack |
| Cloudflare Tunnel (#25) | Voice-agent track | Inbound HTTPS to one app | Laptop → datacenter |
| VPN / WireGuard / Tailscale | **3 / P0** | Encrypted path from Jacob's laptop to management LAN | WAN publish of admin UIs |

---

# P0 — Layer 3 network path

**Exit criterion:** Jacob can access the datacenter from anywhere on his laptop.

“Datacenter” here = the basement rack services host and the Omada management plane (PVE, CT 100 Wazuh, CT 101 Portainer / Omada / NetBox). Not a requirement to hairpin every IoT VLAN on day one.

## Product choice (undecided — pick one and document)

Any of these can meet the P0 exit if the test below passes. Do not run two inbound VPN products on the same WAN port without a written decision.

1. **Tailscale (or Headscale)** — fastest path to “laptop off-LAN sees VLAN 1 hosts.” Good default if OPNsense is still months out.
2. **WireGuard on a Phase 2 CT / the M715q** — self-hosted, no mesh vendor. Needs a stable inbound path (DDNS + one UDP port) or a bounce host.
3. **WireGuard on OPNsense** — correct long-term home if Phase 3 routing cutover is in the same window. Do not block the laptop exit on the OPNsense hardware buy.

Research already on file: [self-hosted-services-roadmap.md §4](../services/self-hosted-services-roadmap.md) and [#13](https://github.com/jacob-kraniak/home-network-security/issues/13). Those are not the exit test.

## Hard rules (P0)

- Do **not** WAN-publish PVE, Wazuh, Portainer, Omada, or NetBox to satisfy this gate.
- Do **not** treat “I can RustDesk a workstation” as P0 done.
- Tokens, keys, Tailscale auth URLs, and WAN IPs stay off this public repo.
- Split-tunnel vs full-tunnel is an operator choice; record it when chosen. Split-tunnel to management prefixes is enough for the exit.

## P0 exit requirements

- [ ] Product chosen and written here (one row, dated)
- [ ] Laptop client installed and used as the daily remote path
- [ ] Off-LAN acceptance test passed (cellular hotspot or other non-home network)
- [ ] From that session, at least **PVE** and **one CT 101 admin UI** load over the tunnel
- [ ] Those UIs remain unpublished on WAN
- [ ] Short dated checkpoint in `docs/phases/` (no keys, no WAN IPs)
- [ ] #34 closed or moved to a follow-on only after the test is recorded

**Not required for P0:** OPNsense live, site-to-site, family devices on the mesh, AdGuard, Plane.so, media stack, RustDesk fleet (#35).

## P0 acceptance test (copy into the checkpoint)

1. Leave home Wi-Fi. Use phone hotspot (or any foreign LAN).
2. Bring the tunnel/mesh up on the laptop.
3. Open PVE and one of: Portainer, Omada controller, NetBox.
4. Confirm the same services are not reachable from the hotspot *without* the tunnel.
5. Write the dated note. Stop.

---

# P1 — RustDesk fleet (parallel, lower priority)

**Exit criterion:** From Jacob's laptop, a real-time RustDesk session opens to each in-scope desktop endpoint.

The **server** is Phase 2 and already running on CT 101. This track is **clients + pointing them at that server**. Install work can happen on-LAN now, in parallel with P0. Off-LAN sessions should ride the P0 tunnel once it exists — do not WAN-publish `hbbs`/`hbbr` to get there first.

## In-scope first cohort

Desktop OS only. Named hosts, not “every IP in NetBox.”

- Jacob laptop (viewer; host optional)
- Christine laptop
- BazzitePC

Add other GUI hosts later by name in this list. **Out of scope:** IoT, APs, switches, ONT, phones-as-IoT, headless CTs (no useful desktop on Wazuh / Portainer / NetBox containers).

## Hard rules (P1)

- Clients point at the **on-prem** server, not `rustdesk.com`.
- Do **not** WAN-publish hbbs/hbbr.
- Do **not** put RustDesk IDs, passwords, or unattended keys in this public repo.
- Unattended access on family endpoints is an explicit decision per host (Christine's laptop especially). Default: attended unless written otherwise.
- P1 green on-LAN does not close #34.

## P1 exit requirements

- [ ] First-cohort clients installed and registered to the on-prem server
- [ ] On-LAN: Jacob's laptop opens a session to each first-cohort host
- [ ] Off-LAN: session works over the P0 path, **or** off-LAN is explicitly deferred until #34 is green
- [ ] hbbs/hbbr remain unpublished on WAN
- [ ] Dated note (hostnames only, no IDs)
- [ ] #35 closed or reduced to a follow-on list of extra GUI hosts

## Parallelism

Safe to do now, before P0: install clients, set the custom server, test on-LAN.
Wait for P0 (or accept “LAN-only”) before calling off-LAN RustDesk done.

---

## Related

- Phase 2 close: [phase-2-close-linkedin.md](phase-2-close-linkedin.md)
- Phase map: [PHASE-ARTIFACTS.md](PHASE-ARTIFACTS.md)
- Roadmap: [../ROADMAP.md](../ROADMAP.md)
- Server deploy (Phase 2): [#29](https://github.com/jacob-kraniak/home-network-security/issues/29)
- OPNsense track: [#9](https://github.com/jacob-kraniak/home-network-security/issues/9)
- Voice-agent tunnel (not these exits): [#25](https://github.com/jacob-kraniak/home-network-security/issues/25)
