# Pi-hole DNS resolver (deployed 2026-10-14)

> **Status:** Live on the Trusted VLAN (10). Other VLANs still use gateway DNS.
> Step 4 of the [network telemetry plan](wazuh-network-telemetry-plan.md). Wazuh ingestion not started.

## Deployment

| Item | Value |
|------|-------|
| Host | CT 101 Docker host `192.168.0.200` (same host as Omada controller, NetBox, RustDesk) |
| Managed by | Portainer stack `pi-hole` (`https://192.168.0.200:9443`), compose at `/data/compose/4` |
| Image | `pihole/pihole:2026.09.0` (pinned) — Core v6.4.3, Web v6.6, FTL v6.7.1 |
| Network | Docker bridge `pi-hole_default` `172.21.0.0/16` |
| DNS | `53/tcp` + `53/udp` on all host interfaces |
| Web UI | `192.168.0.200:8081` (http) and `:8443` (https), admin at `http://192.168.0.200:8081/admin` |
| Capabilities | `NET_ADMIN` only |
| Restart | `unless-stopped` |
| Blocklist | Default list, ~72,526 domains |

Environment: `TZ=America/New_York`, `FTLCONF_dns_listeningMode=ALL`, `FTLCONF_ntp_sync_active=false`, `FTLCONF_ntp_ipv4_active=false`, `FTLCONF_ntp_ipv6_active=false`.

Volumes:

- `/data/compose/4/etc-pihole:/etc/pihole`
- `/data/compose/4/log-pihole:/var/log/pihole` (source for future Wazuh DNS log ingestion)

Admin password: set with `pihole setpassword` inside the container (not an `FTLCONF_webserver_api_password` env var, which would expose it in Portainer inspect and lock `setpassword`). Credential is kept in Bitwarden, never in this repo.

> **Deviation from plan:** the 2026-10-08 plan sized a dedicated LXC on the M715q. Pi-hole was instead deployed as a Docker stack on existing CT 101, so no new CT/RAM was allocated.

## Network enablement

**Before:** every VLAN used its gateway for DNS; the ER605 forwarded to the Verizon ISP resolvers learned on WAN1 (`68.237.161.12`, `71.243.0.12`). No filtering or per-client logging.

**2026-10-14:**

- ER605 WAN DNS left on automatic (ISP). WAN DNS is the router's own upstream and is not where clients are pointed.
- Omada LAN **Trusted** (VLAN 10, `192.168.10.1/24`, pool `.100–.199`, lease 120 min): DHCP DNS changed Auto → **Manual `192.168.0.200`**, **no secondary** so clients cannot bypass Pi-hole.
- Verified the same day: queries arriving in Pi-hole from multiple Trusted clients.

## Open items

- [ ] Roll out to remaining VLANs (Management 1, IoT 20, Guest 30, Lab 40); confirm inter-VLAN ACLs allow TCP/UDP 53 to `192.168.0.200`.
- [ ] Choose upstream resolvers (Quad9 recommended; not decided).
- [ ] Verify Pi-hole sees real client IPs, not Docker NAT `172.21.0.1`. If NATed, consider host or macvlan networking.
- [ ] Ship `/var/log/pihole` to Wazuh (step 4 of the [telemetry plan](wazuh-network-telemetry-plan.md)).
- [ ] Optional: Omada LAN DNS record `pihole.home` → `192.168.0.200`.
