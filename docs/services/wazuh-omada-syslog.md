# Wazuh Data Source — Omada Syslog

**Verified:** 2026-10-04 (EDT); Wireless IDS hardware limitation verified 2026-10-06  
**Manager:** CT 100 Wazuh `192.168.0.178` on PVE node `debian` `192.168.0.176` (bridge `vmbr0`)  
**Related:** [Services index](README.md) · [ROADMAP § Phase 2](../ROADMAP.md#phase-2-self-hosted-services-build-in-progress-) · [Phase 2 checkpoint](../phases/phase-2-checkpoint-2026-09-16.md)

RFC1918 only. No PSKs, tokens, passwords, or MAC addresses. APs are referenced by IP; MACs in samples are placeholders.

---

## Milestone

**Omada syslog is onboarded into Wazuh.** Omada Remote Logging sends to the native `wazuh-remoted` syslog listener on CT 100. AP per-connection traffic records are decoded but stay at level 0 (no alert, not on the dashboard). The Wireless IDS rule is **blocked on AP hardware**. See [Omada Wireless IDS/IPS: hardware limitation](#omada-wireless-idsips--hardware-limitation-verified-2026-10-06).

---

## Source (Omada)

| Field | Value |
|-------|-------|
| Platform | TP-Link Omada SDN (controller on CT 101) |
| Senders | EAP access points `192.168.0.100` and `192.168.0.101`; gateway `192.168.0.1` also sends `user.notice` |
| Remote Logging | Enabled → `192.168.0.178` UDP `514` |
| Wireless IDS/IPS | Enabled on the controller (Detection Level **High**, all detection types; WIPS Deauthenticate + Dynamic Block List on). **No events are generated on current APs.** See the [hardware limitation](#omada-wireless-idsips--hardware-limitation-verified-2026-10-06) section. |

---

## Ingest (Wazuh)

| Field | Value |
|-------|-------|
| Listener | Native `wazuh-remoted` syslog on `0.0.0.0:514/udp` — no separate rsyslog collector |
| `ossec.conf` `<remote>` syslog `allowed-ips` | `192.168.0.0/24`, `192.168.10.0/24`, `192.168.20.0/24` |
| Not allowed (intentional) | Guest `192.168.30.0/24` and Lab VLAN 40. Do not widen to a `/16`. |
| `logall` / `logall_json` | **On** (confirmed in CT 100 `ossec.conf` on 2026-10-31) |

On 2026-10-04 `logall` was meant to be on only briefly for verification, but the `ossec.conf` global block checked on 2026-10-31 shows it still on. With it on, archives grew ~0.2 MB per 30 s (~500 MB/day), mostly AP per-connection traffic records. Watch CT 100 disk headroom (see the ROADMAP risk note), and turn it off when archive samples are no longer needed for rule work.

---

## Verification (2026-10-04)

- `archives.log` showed lines from `192.168.0.100` and `192.168.0.101` (while `logall` was temporarily on).
- `wazuh-analysisd.state` showed events received with **0 dropped**.
- `wazuh-logtest` decoded a sample AP traffic line with the [AP traffic decoder](../configs/wazuh/decoders/omada_ap_traffic_decoders.xml).

---

## Custom decoder

**File:** [`docs/configs/wazuh/decoders/omada_ap_traffic_decoders.xml`](../configs/wazuh/decoders/omada_ap_traffic_decoders.xml). On CT 100 this decoder is in `/var/ossec/etc/decoders/local_decoder.xml`.  
Decode only — **no rule**, so traffic lines stay level 0 and do not alert or reach the dashboard.

**Fields:** `ap_mac`, `srcmac`, `srcip`, `dstip`, `protocol`, `srcport`, `dstport`

**Sample line format** (placeholders, not real MACs):

```
Oct  4 22:12:09 192.168.0.101 [<epoch.nanos>] AP MAC=<ap-mac> MAC SRC=<client-mac> IP SRC=192.168.10.110 IP DST=172.217.119.4 IP proto=6 SPT=33552 DPT=443
```

---

## Omada controller 6.3.x decoders and rules

**Status:** drafted 2026-10-30 and revised 2026-10-31. On 2026-10-31 Jacob deployed an earlier version on CT 100 by copying it from chat, and the first level-5 alert (100606) came in that day. This repo holds the latest revision sent to him: it adds online/offline, DHCP rejected, admin login, band steer, and the catch-all. Deploying that revision on CT 100 is still pending. If CT 100 differs from this repo, CT 100 is the live copy, so reconcile the two. Every sample line was tested on a disposable Wazuh 4.14.9 manager, not on CT 100.
**Files:** [`omada_controller_decoders.xml`](../configs/wazuh/decoders/omada_controller_decoders.xml) · [`omada_controller_rules.xml`](../configs/wazuh/rules/omada_controller_rules.xml) · [samples](../configs/wazuh/tests/omada_controller_samples.log) (placeholder MACs, site, and client names) · [logtest output](../configs/wazuh/tests/omada_controller_logtest.txt)

### Data source

There is no Wazuh agent on the Omada controller. The data source is **agentless syslog**:

- The controller on CT 101 (`192.168.0.200`) sends Remote Logging over UDP 514 to `wazuh-remoted` on the CT 100 manager (`192.168.0.178`). The listener and `allowed-ips` are listed under [Ingest](#ingest-wazuh).
- Lines arrive as `1 2026-10-30 22:40:47 Omada <site> - - - <message>`.
- Wazuh's pre-decoder leaves this header alone because the timestamp has a space, not a `T`. So the parent decoder `omada-controller` matches it directly.
- With `logall` on, raw lines also land in `/var/ossec/logs/archives/archives.log`. That is where new samples come from.

The controller's syslog only carries event types that it records. Types switched off under the controller's alert and event settings are probably never sent.

**Not in this repo:** the ER605 decoders (`omada-er605`, `omada-er605-dhcp`) and rule 100500 exist only on CT 100 in `local_decoder.xml` and `local_rules.xml`. These files do not change them. The AP flow lines from `192.168.0.101` are already handled by `omada-ap-traffic` (level 0), so they get no new decoder.

### Rules

Rules are listed in file order. Children of 100600 are tried top to bottom, so 100619 must stay last.

| Rule | Level | Event | Key fields |
|------|-------|-------|------------|
| 100600 | 0 | Any controller event (base) | `omada_site` |
| 100601 | 3 | Client roamed between APs | `client_name`, `client_mac`, `from_ap_name`, `from_ap_mac`, `from_channel`, `to_ap_name`, `to_ap_mac`, `to_channel`, `ssid` |
| 100607 | 0 | Band or channel steer on the same AP (both AP MACs match). Not counted by 100606. | as 100601 |
| 100602 | 3 | Wireless client online (`(IP: ...)` is optional) | `client_name`, `client_mac`, `client_ip`, `to_ap_name`, `to_ap_mac`, `ssid`, `to_channel` |
| 100603 | 3 | Wireless client offline | `client_name`, `client_mac`, `client_ip`, `ssid`, `from_ap_name`, `from_ap_mac`, `connected_time`, `traffic` |
| 100604 | 0 | Controller copy of a DHCP allocation (no alert, so it doesn't double up with ER605 rule 100500) | `client_ip`, `client_mac` |
| 100608 | 5 | DHCP server rejected a request | `client_mac`, `client_ip` |
| 100605 | 3 | Audit entry with a JSON body (config change and similar) | `operation`, `details.newValue`, `details.oldValue` |
| 100609 | 5 | Audit: admin login succeeded (child of 100605) | `operation` |
| 100606 | 5 | Same `client_mac` roams between APs 3+ times in 10 min | as 100601 |
| 100619 | 5 | **Catch-all:** a controller line no rule above claimed, such as a new or rare type like a rogue DHCP server or an attack alert. Group `omada_unclassified`. | `omada_site` |

IDs 100600–100619 are reserved for this file. 100610–100618 are free for new types.

Not covered yet: wired client online/offline (`[switch:...]` wording). The decoder file has a TODO for it, to fill in once real samples exist.

### `omada_unclassified` workflow

1. In the Wazuh dashboard, filter alerts on `rule.groups: omada_unclassified` (rule 100619).
2. For each new message shape, take the full line from `archives.log` or the alert's `full_log`. Before committing it to `docs/configs/wazuh/tests/omada_controller_samples.log`, replace MACs with placeholders (`00-00-5E-00-53-xx`) and use placeholder site and client names.
3. Add a decoder sibling block if fields are needed. Add a rule in 100610–100618 **above** 100619, and add the new message's text to 100619's `negate` regex so the catch-all stops claiming it.
4. Re-run `wazuh-analysisd -t` and `wazuh-logtest` with the samples, then deploy.

### Deploy and test (run on CT 100 yourself)

```bash
# 1. Collision check. On a fresh install both commands must print nothing.
#    If this file is already deployed, only it should match.
grep -rn 'id="1006[01][0-9]"' /var/ossec/etc/rules/
grep -rn 'name="omada-controller' /var/ossec/etc/decoders/

# 2. Copy these repo files onto CT 100, then install them:
#    docs/configs/wazuh/decoders/omada_controller_decoders.xml
#    docs/configs/wazuh/rules/omada_controller_rules.xml
cp omada_controller_decoders.xml /var/ossec/etc/decoders/
cp omada_controller_rules.xml /var/ossec/etc/rules/
chown wazuh:wazuh /var/ossec/etc/decoders/omada_controller_decoders.xml /var/ossec/etc/rules/omada_controller_rules.xml
chmod 660 /var/ossec/etc/decoders/omada_controller_decoders.xml /var/ossec/etc/rules/omada_controller_rules.xml

# 3. Config check (prints nothing on success)
/var/ossec/bin/wazuh-analysisd -t

# 4. Test with docs/configs/wazuh/tests/omada_controller_samples.log.
#    Expected rule per line, in order:
#    100604, 100601, 100605, (omada-ap-traffic, no rule), 100601, 100601, 100606,
#    100602, 100602, 100602, 100603, 100603, 100608, 100609, 100605,
#    100607, 100601, 100604, 100619, 100607, 100607, 100601, 100606, 100601
#    Saved output: docs/configs/wazuh/tests/omada_controller_logtest.txt
/var/ossec/bin/wazuh-logtest < omada_controller_samples.log

# 5. Apply
systemctl restart wazuh-manager
```

Rollback: delete the two files and restart `wazuh-manager`.

---

## Known issue — AP timestamps 1 hour behind

AP-embedded syslog timestamps run 1 hour behind (UTC-5 instead of EDT UTC-4), even though the Omada site timezone is Eastern with DST Auto and NTP is `129.6.15.28` (NIST). Likely AP firmware lacking DST support; firmware update pending. Cosmetic for Wazuh, which uses receive time.

---

## Omada Wireless IDS/IPS — hardware limitation (verified 2026-10-06)

**Bottom line:** the current EAP225 v4 APs can't run Omada WIDS/WIPS, so Wazuh can't receive any Omada wireless IDS events on this hardware.

### Site hardware (Omada Devices page, 2026-10-06)

| Device | Hardware ver. | Firmware |
|--------|---------------|----------|
| ER605 (gateway) | v2.30 | 2.4.5 |
| SG2008P (switch) | v3.20 | 3.20.24 |
| EAP225(US) AP | v4.0 | 5.2.4 |
| EAP225(US) AP | v4.0 | 5.2.3 |

### What we see

- Wireless IDS/IPS is **enabled** on the controller: Detection Level **High** with all detection types on. WIPS **Deauthenticate** and **Dynamic Block List** are on, with a lock time of **1000 s**.
- The WIDS **Monitor** table has been **empty from Sep 22 to Oct 6 2026**. The Dynamic Block List has **no entries**.

### Cause

- WIDS/WIPS **runs on the EAPs**. The controller only configures it and logs the results.
- The feature first came to the standard Omada Software Controller in **v6.3** (released 2026-08-31). It needs **Wi-Fi 6 or Wi-Fi 7 APs** on **AP firmware 1.10 or newer**.
- The EAP225 v4 is a **Wi-Fi 5** AP on firmware 5.2.x, so it can't do WIDS. The controller **accepts the setting anyway** and gives no warning.
- The **ER605 has no role** in WIDS/WIPS.

### Sources

- Omada Software Controller v6.3.0 release note: <https://static.tp-link.com/upload/software/2026/202609/20260904/Omada%20Software%20Controller%20v6.3.0%20Release%20Note.pdf>
- TP-Link staff on what the AP does vs what the controller does: <https://community.tp-link.com/en/business/forum/topic/871456>
- EAP firmware 1.10.0 beta with WIDS/WIPS for EAP650 v2/v3, EAP650-Desktop, EAP650-Wall v2.20, EAP653 v3, EAP653 UR, and EAP603-Outdoor: <https://community.tp-link.com/en/business/forum/topic/868902>
- AP beta thread that also lists 1.10.0 for some Wi-Fi 7 models (EAP723 v1, EAP770 v2, EAP772 v2, EAP773 v2, EAP775-Wall, EAP787, EAP772-Outdoor): <https://community.tp-link.com/en/business/forum/topic/869714>

Caveats:
- No official list of supported models was found.
- No public reports were found of anyone confirming that WIDS events actually fire in practice.

### What this means

- Wazuh **can't receive Omada IDS events** on the current hardware. The planned IDS decoder and **level-12** rule are **blocked until the AP hardware changes**. The hardware pointer is in [Compute Sizing § Hardware acquisition list](self-hosted-services-roadmap.md#hardware-acquisition-list-phase-3-trigger-tied-to-plane).
- Syslog traffic decoding (`omada-ap-traffic`) is **not affected**.
- **Separate issue:** the controller **Events** log has looked empty for months. That started **before 6.3** and has nothing to do with WIDS. It is still an open check: the log's default date range, the event category settings, and History Data Retention.

---

## Still open

1. Omada Wireless IDS → Wazuh is **blocked until the Wi-Fi 6/7 AP upgrade** (see the [hardware limitation](#omada-wireless-idsips--hardware-limitation-verified-2026-10-06) section). After the upgrade, test it on my own equipment (a hotspot spoofing one of my SSIDs, or a deauth test). Then write the decoder and a **level-12** rule so the alerts show up in the planned Lab Watch Wazuh attention summary (threshold level >= 12).
2. Decide whether to allow Guest `192.168.30.0/24` in `allowed-ips`.
3. Find out why the controller **Events** log looks empty. This predates 6.3 and is separate from WIDS. Check the log's default date range, the event category settings, and History Data Retention.

---

*Written 2026-10-04 from CT 100 verification. Updated 2026-10-06 with the Omada WIDS/WIPS hardware limitation (from the Omada controller UI and TP-Link sources). Updated 2026-11-01 with the controller 6.3.x rule set (online/offline, DHCP rejected, admin login, band steer, catch-all) and the `logall` status. Secrets stay on the guest.*
