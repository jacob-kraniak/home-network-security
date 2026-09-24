# Phase 3 — Remote Access

**Status:** 🔵 Planned  
**Created:** 2026-09-24  
**Does not close Phase 2.** RustDesk *server* on CT 101 is already the Phase 2 remote-access line.

| Priority | Track | Exit in one line | Issue | When |
|----------|-------|------------------|-------|------|
| **P0** | Layer 3 path | Laptop reaches the datacenter from anywhere | [#34](https://github.com/jacob-kraniak/home-network-security/issues/34) | First |
| **P0-next** | Datacenter RustDesk | Off-LAN session into the rack, then hop into each CT | [#36](https://github.com/jacob-kraniak/home-network-security/issues/36) | After P0 |
| **P1** | Family desktop fleet | Session to each named family desktop | [#35](https://github.com/jacob-kraniak/home-network-security/issues/35) | Parallel on-LAN; off-LAN after P0 |

P0-next is the natural outcome of P0. It is not a substitute for P0. Browser tabs and laptop SSH can exist; they are not the intended daily remote path into the stack.

---

## Why these are Phase 3

| Path | Phase | What it is | What it is not |
|------|-------|------------|----------------|
| RustDesk server (`hbbs`/`hbbr` on CT 101) | 2 (live) | ID/relay for desktop sessions | Clients; off-LAN path; per-CT GUI |
| VPN / WireGuard / Tailscale | **3 / P0** | Encrypted path from the laptop to management LAN | WAN publish of admin UIs |
| RustDesk → jump guest → CT shells | **3 / P0-next** | Desktop landing zone in the rack | XFCE on the Wazuh CT |
| RustDesk on family desktops | **3 / P1** | Screen control of named PCs | Network path into the rack |
| Cloudflare Tunnel (#25) | Voice-agent track | Inbound HTTPS to one app | Laptop → datacenter |

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

**Not required for P0:** OPNsense live, site-to-site, family devices on the mesh, AdGuard, Plane.so, media stack, RustDesk fleet (#35), jump guest (#36).

## P0 acceptance test (copy into the checkpoint)

1. Leave home Wi-Fi. Use phone hotspot (or any foreign LAN).
2. Bring the tunnel/mesh up on the laptop.
3. Open PVE and one of: Portainer, Omada controller, NetBox.
4. Confirm the same services are not reachable from the hotspot *without* the tunnel.
5. Write the dated note. Stop. Then #36 is unblocked.

---

# P0-next — RustDesk into the datacenter stack

**Depends on:** #34 green.  
**Exit criterion:** Off-LAN, Jacob lands a RustDesk session *in the rack* and from that session opens a shell on each current CT. Laptop SSH and PVE/noVNC may exist as break-glass. They are not the daily path.

## Constraint (do not skip)

CT 100 (Wazuh) and CT 101 (Portainer / Omada / NetBox / RustDesk *server*) are **headless**. RustDesk attaches to a desktop session. Putting XFCE on the SIEM CT is rejected.

**Pattern:** one small GUI guest on the M715q (“jump” / ops workstation) runs the RustDesk *client* against the on-prem server. After P0, the path is:

`laptop → L3 tunnel → RustDesk → jump guest → SSH (or equivalent) into CT 100, CT 101, later CTs`

That is the easy hop into each container. It is not RustDesk-inside-Wazuh.

## Jump guest rules

- New CT or small KVM VM. Do not install a desktop on the PVE host.
- ~1–2 GiB RAM unless measured otherwise. Host is already ~14.6 GiB with two 6G CTs.
- Desktop is enough to run RustDesk + a terminal + bookmarks. Not a media box.
- SSH from jump → each CT; keys stay off this public repo.
- Optional later: add a new GUI guest to the hop list by name. Do not retro-GUI CT 100.
- Do **not** WAN-publish hbbs/hbbr so this works before P0.

## P0-next exit requirements

- [ ] Jump guest live (desktop + on-prem RustDesk client)
- [ ] Off-LAN RustDesk to the jump works over the P0 path
- [ ] From that session, shells open to CT 100 and CT 101 without the laptop being the SSH client of record
- [ ] No desktop stack on CT 100; hbbs/hbbr unpublished on WAN
- [ ] Dated note + RAM impact
- [ ] #36 closed or reduced to “add next CT to the hop list”

---

# P1 — Family desktop fleet (parallel, lower priority)

**Exit criterion:** From Jacob's laptop, a real-time RustDesk session opens to each in-scope *family* desktop.

This is not the datacenter hop. Install on-LAN anytime. Off-LAN rides P0.

## In-scope first cohort

- Jacob laptop (viewer; host optional)
- Christine laptop
- BazzitePC

**Out of scope here:** IoT, APs, switches, ONT, headless CTs. Datacenter hop is #36.

## Hard rules (P1)

- Clients point at the **on-prem** server, not `rustdesk.com`.
- Do **not** WAN-publish hbbs/hbbr.
- Do **not** put RustDesk IDs, passwords, or unattended keys in this public repo.
- Unattended access on family endpoints is an explicit decision per host (Christine's laptop especially). Default: attended unless written otherwise.
- P1 green on-LAN does not close #34 or #36.

## P1 exit requirements

- [ ] First-cohort clients installed and registered to the on-prem server
- [ ] On-LAN: Jacob's laptop opens a session to each first-cohort host
- [ ] Off-LAN: session works over the P0 path, **or** off-LAN is explicitly deferred until #34 is green
- [ ] hbbs/hbbr remain unpublished on WAN
- [ ] Dated note (hostnames only, no IDs)
- [ ] #35 closed or reduced to extra GUI hosts

---

## Related

- Phase 2 close: [phase-2-close-linkedin.md](phase-2-close-linkedin.md)
- Phase map: [PHASE-ARTIFACTS.md](PHASE-ARTIFACTS.md)
- Roadmap: [../ROADMAP.md](../ROADMAP.md)
- Server deploy (Phase 2): [#29](https://github.com/jacob-kraniak/home-network-security/issues/29)
- OPNsense track: [#9](https://github.com/jacob-kraniak/home-network-security/issues/9)
- Voice-agent tunnel (not these exits): [#25](https://github.com/jacob-kraniak/home-network-security/issues/25)
