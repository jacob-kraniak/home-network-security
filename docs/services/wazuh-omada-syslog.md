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
| `logall` / `logall_json` | **Off** |

`logall` was enabled only briefly for verification. With it on, archives grew ~0.2 MB per 30 s (~500 MB/day), mostly AP per-connection traffic records. Keep it off (CT 100 disk headroom — see the ROADMAP risk note).

---

## Verification (2026-10-04)

- `archives.log` showed lines from `192.168.0.100` and `192.168.0.101` (while `logall` was temporarily on).
- `wazuh-analysisd.state` showed events received with **0 dropped**.
- `wazuh-logtest` decoded a sample AP traffic line with the custom decoder below.

---

## Custom decoder

**File:** `/var/ossec/etc/decoders/local_decoder.xml` on CT 100.  
Decode only — **no rule**, so traffic lines stay level 0 and do not alert or reach the dashboard.

```xml
<decoder name="omada-ap-traffic">
  <prematch>^[\d+.\d+] AP MAC=</prematch>
</decoder>

<decoder name="omada-ap-traffic-fields">
  <parent>omada-ap-traffic</parent>
  <regex>AP MAC=(\S+) MAC SRC=(\S+) IP SRC=(\S+) IP DST=(\S+) IP proto=(\d+) SPT=(\d+) DPT=(\d+)</regex>
  <order>ap_mac, srcmac, srcip, dstip, protocol, srcport, dstport</order>
</decoder>
```

**Fields:** `ap_mac`, `srcmac`, `srcip`, `dstip`, `protocol`, `srcport`, `dstport`

**Sample line format** (placeholders, not real MACs):

```
Oct  4 22:12:09 192.168.0.101 [<epoch.nanos>] AP MAC=<ap-mac> MAC SRC=<client-mac> IP SRC=192.168.10.110 IP DST=172.217.119.4 IP proto=6 SPT=33552 DPT=443
```

---

## Omada controller 6.3.x decoders and rules

**Status:** drafted 2026-10-30, tested on a disposable Wazuh 4.14.9 manager (not CT 100). Not deployed.
**Files:** [`omada_controller_decoders.xml`](../configs/wazuh/omada_controller_decoders.xml) · [`omada_controller_rules.xml`](../configs/wazuh/omada_controller_rules.xml) · [samples](../configs/wazuh/omada_controller_samples.log) (placeholder MACs) · [logtest output](../configs/wazuh/omada_controller_logtest.txt)

The controller (`192.168.0.200`) sends `1 2026-10-30 22:40:47 Omada <site> - - - <message>`. Wazuh's pre-decoder leaves this header alone (space, not `T`, in the timestamp), so the parent decoder `omada-controller` matches it directly. The ER605 decoders (`omada-er605`, `omada-er605-dhcp`), rule 100500, and `omada-ap-traffic` are not changed.

| Rule | Level | Event | Fields |
|------|-------|-------|--------|
| 100600 | 0 | Any controller event (base) | `omada_site` |
| 100601 | 3 | Client roaming | `client_name`, `client_mac`, `from_ap_name`, `from_ap_mac`, `from_channel`, `to_ap_name`, `to_ap_mac`, `to_channel`, `ssid` |
| 100602 / 100603 | — | Reserved: client online / offline (TODO, no samples yet) | — |
| 100604 | 0 | Controller copy of a DHCP allocation (no alert, so it doesn't double up with 100500) | `client_ip`, `client_mac` |
| 100605 | 3 | Audit entry with a JSON body | `operation`, `details.newValue`, `details.oldValue` (JSON strings) |
| 100606 | 5 | Same `client_mac` roaming 3+ times in 10 min | as 100601 |

AP flow lines from `192.168.0.101` are already handled by `omada-ap-traffic` (level 0); no new decoder.

### Deploy and test (run on CT 100 yourself)

```bash
# 1. Collision check: both commands must print nothing.
grep -rn 'id="10060[0-9]"' /var/ossec/etc/rules/
grep -rn 'name="omada-controller' /var/ossec/etc/decoders/

# 2. Copy the two files from this repo (docs/configs/wazuh/) onto CT 100, then:
cp omada_controller_decoders.xml /var/ossec/etc/decoders/
cp omada_controller_rules.xml /var/ossec/etc/rules/
chown wazuh:wazuh /var/ossec/etc/decoders/omada_controller_decoders.xml /var/ossec/etc/rules/omada_controller_rules.xml
chmod 660 /var/ossec/etc/decoders/omada_controller_decoders.xml /var/ossec/etc/rules/omada_controller_rules.xml

# 3. Config check (prints nothing on success)
/var/ossec/bin/wazuh-analysisd -t

# 4. Test with the samples (expect 100604, 100601, 100605, omada-ap-traffic, 100601, 100601, 100606)
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

*Written 2026-10-04 from CT 100 verification. Updated 2026-10-06 with the Omada WIDS/WIPS hardware limitation (from the Omada controller UI and TP-Link sources). Secrets stay on the guest.*
