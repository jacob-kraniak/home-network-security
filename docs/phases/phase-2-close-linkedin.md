# Phase 2 Close + LinkedIn Follow-Up

**Status:** Planned — do not mark Phase 2 complete or publish until the gates below are checked.  
**Created:** 2026-09-16  
**Depends on:** [netbox-cloud-to-local.md](netbox-cloud-to-local.md), [phase-2-checkpoint-2026-09-16.md](phase-2-checkpoint-2026-09-16.md)

This is the close definition for Phase 2 and the public-article gate. AdGuard, WireGuard/Tailscale as a product, Plane.so, media, and OPNsense stay **Phase 3** unless already live.

Phase 3 remote-access exit (laptop → datacenter from anywhere): [phase-3-remote-access.md](phase-3-remote-access.md) · [#34](https://github.com/jacob-kraniak/home-network-security/issues/34).

---

## Phase 2 scope (what “done” means)

| Layer | Live target |
|-------|-------------|
| Hypervisor | PVE 9.2.4 on the M715q |
| SIEM | Wazuh 4.8.2 on CT 100 |
| App host | Portainer on CT 101 |
| Network controller | Omada 6.3 on-prem (cloud closed) |
| Remote access | RustDesk on CT 101 (**desktop only** — not off-LAN VPN) |
| IPAM/DCIM | NetBox v4.7 on CT 101 (**on-prem SoT**); Cloud archive reconcile still open |

Wazuh agents to cite internally: `003` pve-debian, `004` ct101-portainer, `005` bazzite, `006` Christines_Laptop. Public wording: hypervisor + Portainer CT + two workstation endpoints. Do not count disconnected Kali `002` as coverage.

---

## Exit requirements (repo + board)

- [ ] Cloud → local NetBox import complete; device / prefix / VLAN / tag counts match within an agreed delta ([netbox-cloud-to-local.md](netbox-cloud-to-local.md))
- [ ] Local NetBox contains Phase 2 objects: M715q, CT 100, CT 101, Omada controller, four SDN devices (ER605, MSW-1, two EAPs)
- [x] SoT flipped (2026-09-21 Jacob GO): Cloud is archive; on-prem is authoritative in `GROK-WORKSPACE.md`, `network-overview.md`, `NetBox-Inventory-Progress.md`
- [ ] One restore path written (vzdump of CT 100/101 and/or NetBox volume copy to the Seagate). “Core services running with backups” is an existing Phase 2 exit line
- [ ] Checkpoint `phase-2-complete` (or dated close note) + `PHASE-ARTIFACTS.md` / `ROADMAP.md` set Phase 2 ✅
- [ ] #28 closed after import; leftover Phase 2 issues closed or relabeled `phase:3`; #23 closed or explicitly deferred
- [ ] No WAN publish of PVE / Wazuh / Portainer / Omada / NetBox

**Explicitly not required to close Phase 2:** SanDisk Z400, Proxbox, Diode/Orb, Wazuh `local_rules` polish, power/cable completeness, AdGuard, mesh VPN product, Plane.so.

---

## LinkedIn article — publish gates

SoT has moved to on-prem (2026-09-21). Do **not** publish until Cloud→local reconcile is honest in the narrative (platform up; archive pending reconcile OK to state).

### Must include
- Consumer SDN → local Omada controller
- Surplus PC → Proxmox services host
- On-prem SIEM + inventory + remote access as containers on one Tiny
- One operational lesson: disk-full killed Wazuh; CT 101 was grown *before* NetBox
- Honest scope: Phase 2 is the services host, not a SOC and not a router replacement (OPNsense stays later)

### Must omit (public repo + LinkedIn)
- RFC1918 addresses, Cloud instance URL, serials, MACs, agent IDs, tokens, screenshots of live IPs
- Inflated agent or device counts
- “Finished homelab security” framing

### Suggested angle
*From cloud controllers to a one-box services host* — follow-up to the Privacy Migration series.

### After publish
Link the article from `ROADMAP.md` or a short Phase 2 completion note. Keep the article URL only; do not paste the full post into this repo.

---

*Add a dated row here when import finishes and when the article goes live.*
