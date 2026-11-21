# Omada → Wazuh gap analysis: from "logs arrive" to "I can troubleshoot with them"

**Drafted:** 2026-11-19 (ET), docs only. **Scope:** home-network-security (HNS) lab, one Omada site.
**Stack:** Omada Software Controller 6.3 on CT 101 (6.3.0.45 per [PHASE-ARTIFACTS](../phases/PHASE-ARTIFACTS.md)) · ER605 V2 gateway · SG2008P switch · 2× EAP225 v4 ([wazuh-omada-syslog.md](wazuh-omada-syslog.md#site-hardware-omada-devices-page-2026-10-06)) · Wazuh **4.8.2** manager on CT 100 ([#44](https://github.com/jacob-kraniak/home-network-security/issues/44)) · Lab Watch collector on the Proxmox node `.176`.
**Related:** [omada-event-inventory.md](omada-event-inventory.md) (per-type mapping) · [Omada dictionaries](omada-log-inventory/README.md) (alerts/events, [incidents](omada-log-inventory/incidents.md)) · [INSTALL-STEPS](omada-wazuh-realtime-INSTALL-STEPS.md) · [webhook evaluation](omada-webhook-evaluation.md) · [telemetry plan](wazuh-network-telemetry-plan.md)

No IPs, MACs, serials, site IDs, tokens, or per-type enable/email/webhook settings in this file. Every proposal below is for Jacob to install by hand. Nothing here changes a live system.

**How to read the labels**

| Label | Meaning |
|---|---|
| **E** | Evidence: a real log line, a capture, or a repo file says so. Source in brackets. |
| **I** | Inference: reasoned from evidence, not yet observed. Each one has a check in [Verify first](#4-verify-first-jacob-read-only-from-ship-desks-side). |
| **G** | Guessed wording: a rule exists but keys on message text nobody has seen yet. |

**Sources.** Repo: **[R1]** [`omada_controller_rules.xml`](../configs/wazuh/rules/omada_controller_rules.xml) (100600–100619) · **[R2]** [`omada_realtime_rules.xml`](../configs/wazuh/rules/omada_realtime_rules.xml) (100620–100649) · **[R3]** [`omada_controller_decoders.xml`](../configs/wazuh/decoders/omada_controller_decoders.xml) · **[R4]** [test samples](../configs/wazuh/tests/) · **[R5]** [wazuh-omada-syslog.md](wazuh-omada-syslog.md) · **[R6]** [omada-event-inventory.md](omada-event-inventory.md) · **[R7]** [INSTALL-STEPS](omada-wazuh-realtime-INSTALL-STEPS.md) · **[R8]** [omada-log-inventory/](omada-log-inventory/README.md) · **[R9]** [`lab-status-collect.py`](../configs/lab-watch/lab-status-collect.py) · **[R10]** [omada-webhook-evaluation.md](omada-webhook-evaluation.md) · **[R11]** [wazuh-network-telemetry-plan.md](wazuh-network-telemetry-plan.md).
Public: **[P1]** [Omada doc 13012, remote logging](https://support.omadanetworks.com/us/document/13012/) · **[P2]** [doc 135217, device syslog export](https://support.omadanetworks.com/us/document/135217/) · **[P3]** [doc 131451, incidents](https://support.omadanetworks.com/us/document/131451/) and the [Incident white paper](https://static.tp-link.com/upload/document-and-bulletins/2026/202610/20261016/Omada%20Incident%20Detection%20and%20Health%20Assessment%20White%20Paper.pdf) · **[P4]** [doc 53570, webhooks](https://support.omadanetworks.com/en/document/53570/) · **[P5]** forum threads on the Gateway ACL Log toggle: [671998](https://community.tp-link.com/en/business/forum/topic/671998), [737936](https://community.tp-link.com/en/business/forum/topic/737936), [866070](https://community.tp-link.com/en/business/forum/topic/866070) · **[P6]** [Grafana-Omada-Dashboard](https://github.com/Matvalicious/Grafana-Omada-Dashboard) (`[ACL]GATEWAY` syslog format; "seems … NOT available on the ER605") · **[P7]** [dfla-me/omada-mcp](https://github.com/dfla-me/omada-mcp) (community map of Open API v1 log and threat-management paths) · **[P8]** RFC 5424 timestamp change: forum [707118](https://community.tp-link.com/en/smart-home/forum/topic/707118), [802182](https://community.tp-link.com/en/business/forum/topic/802182) · **[P9]** IDS/IPS not in system log: forum [622524](https://community.tp-link.com/en/business/forum/topic/622524) · **[P10]** [Open API docs 6.3.0](https://omada-northbound-docs.tplinkcloud.com/6.3.0/).

---

## 1. Summary

**Bottom line (I):** the pipe works, but most of what Omada knows about a *problem* never becomes a specific Wazuh alert. Four reasons:

1. **Nothing from 100620–100649 is live yet** (E [R7]: merged, not installed). Today CT 100 has 100600–100619 only. Real lines back just five site keys: roam, client online, client offline, rogue DHCP, and DHCP allocate/reject. Site audit lines are also real (E [R4] lines 1–24).
2. **143 of the 181 alert/event rows land on the catch-all** 100619 (level 5, "unclassified") even after install (E [R6] tables A/B). Among them are the keys that matter most for troubleshooting: STP topology changes, WAN failover/recovery, WAN IP/PPPoE failures, switch DHCP-snooping and ARP-detection alerts, wired client on/off, config desync and IntelliRecover reboots.
3. **The best diagnostic data isn't in syslog at all.** Incidents (Omada's own RF, roaming, loop, port-flap and WAN-latency detectors; 45 types on this controller) go out by email only (E [P3], [R8 incidents]). RF utilisation, RSSI and SNR come only from the Open API (E [R8 README]). IDS/IPS threat entries aren't in the system log (E [P9]).
4. **The guessed wording in 100620–100649 hasn't been checked.** 20 sample lines use guessed text (E [R7] step 4: lines 35–45, 50–56, 60–61). Every rule built on them is **G** until a real `archives.log` line confirms it.

Enablement on the controller is not the bottleneck (I, checked against a local capture that stays out of the repo). The work is in rules, delivery checks, and a second (API) path.

### 1a. Coverage matrix

| # | Telemetry source | Reaches Wazuh today? | Via | Rule coverage | Confidence |
|---|---|---|---|---|---|
| 1 | **Site alerts/events** (158 keys, [R8 site](omada-log-inventory/site.md)) | **Yes**, for enabled types | Site remote logging → UDP 514 → `wazuh-remoted` → decoder `omada-controller` [R3] | **Live:** 100601–100609 (5 keys). **Merged, not installed:** 100620–100641 add ~24 keys (G). **Rest:** catch-all 100619 | **E** for delivery and the 5 keys (real lines [R4]; first live alert 100606 on 2026-10-31 [R5]). **G** for the 24 |
| 2 | **Global alerts/events** (19 keys, [R8 global](omada-log-inventory/global.md)) | **Unknown** | Global remote logging is on (E: screenshot 2026-11-18 [R6 L2]), but no global line has been seen in Wazuh | 100630, 100631, 100632, 100645, 100646 (all G); 14 keys on the catch-all | **I**. Settled by INSTALL-STEPS step 9b [R7] |
| 3 | **Audit logs** (16 global + 23 site categories) | **Site: yes. Global: unknown** | Same syslog paths; JSON body → child decoder `omada-controller-audit` [R3] | 100605, 100609 (real); 100642–100644, 100648, 100649 (G) | **E** site ([R4] lines 3, 14, 15). **I** global |
| 4 | **Incidents** (45 on the controller, 88 in the UI bundle, [R8 incidents](omada-log-inventory/incidents.md)) | **No** | Officially email only [P3]. No syslog, webhook or documented Open API list path [P7] | None. Only indirect signals: `INCIDENT_MAILED_FAILED` (site event, catch-all) and `ANOMALY_EVENT_FULL` (100646, G) | **E** for the docs; **I** that none leak into syslog (test in V7) |
| 5 | **Gateway ACL hits** (`[ACL]GATEWAY=…`) | **No** | Would be gateway syslog via remote logging, if the ER605 V2 firmware has the per-rule Log toggle [P5] | None (no decoder) | **I**. Community reports say it's absent on ER605 [P6]; unverified on V2 / fw 2.4.5 (V5) |
| 6 | **IDS/IPS threat management** | **No** | Not in the system log [P9]. Open API v1 `…/security/threat-management` per a community spec [P7] | None | **I**. ER605 V2 IPS support and the endpoint are both unverified (V6) |
| 7 | **Wireless IDS/WIPS** | **No** | Runs on Wi-Fi 6/7 APs only | None (100627 is a placeholder) | **E**: blocked on EAP225 v4 [R5] |
| 8 | **Open API RF / client stats** (per-radio utilisation, interference, channel, Tx power; client RSSI; disconnect timeline) | **No** (goes to Lab Watch, not Wazuh) | `lab-status-collect.py` on `.176` → push to the Lab Watch ingest twice a day [R9], [R7] steps 11–14. Merged, not installed | None in Wazuh | **E** for the code path; **I** for the live output (V9) |
| 9 | **Device-level syslog** | **Partly** | EAP per-connection traffic lines (decoder `omada-ap-traffic`, level 0). ER605 `user.notice` lines (decoders `omada-er605*` + rule 100500 live **only on CT 100**, not in the repo) [R5] | AP traffic: decode only. ER605: DHCP only | **E** [R5] (verified 2026-10-04). Switch syslog: none seen (I) |
| 10 | **Omada webhook** | **No** (master switch off) | Would carry the same types as syslog [R10] | — | **E** [R10]. Not recommended except as a backup path |

---

## 2. Troubleshooting playbooks

One row per symptom. **Signals** lists what Omada can tell you. **Wazuh today** means after PR #59 is installed (otherwise only the 100600–100619 IDs apply). **Add** points to the gap IDs in [section 3](#3-prioritised-gaps).

Incident codes are from [incidents.md](omada-log-inventory/incidents.md). "Bundle-only" means the type is in the UI bundle but not in this controller's list, so it won't fire here. Thresholds are the observed values in that dictionary.

| # | Symptom | Syslog keys (site unless noted) | Incident codes | API fields | Wazuh today | Gap → add |
|---|---|---|---|---|---|---|
| 1 | **Client keeps dropping** | `W_C_DISCONN`, `AP_C_OK`, `W_C_ROAM` | 01009001 SNR exception (<20 dB, 80% of 15 min), 01009003 negotiation-rate exception; bundle-only 01003013, 01003002 | `/clients` RSSI/SNR; `client-timeline?type=3` attributes (names undocumented) [R9] | 100603 → 100635 (short session) → **100636** (5 drops/10 min, same client). E: real lines | No RSSI or reason in the syslog line (E [R8 README]). Add the RSSI-at-drop join and incident feed → **G8, G5** |
| 2 | **Slow Wi-Fi in one room** | `AP_CH_C`, `AP_RADAR` | **01009002** channel utilisation >70%, **01009009** noise floor >−85 dBm, **01009010** interference >50% (each 80% of samples over 15 min) | `/aps/{mac}/radios`: `txUtil`, `rxUtil`, `interUtil`, `busyUtil`, channel, width, Tx power [R9] | 100623 / **100638** (3 channel changes/h, G), 100624 radar (G). No utilisation data | Syslog has no utilisation figures. Add RF threshold lines from the collector + incidents → **G8, G5** |
| 3 | **Whole AP drops its clients** | `W_C_DISCONN` (many clients, one AP), `DEV_DISCONN`, `AP_ISOLATE`, `AP_RADAR` | **01001001** AP offline ≥2×/h, 01007001 AP CPU ≥90%. *01001003 (batch AP offline) needs ≥6 APs, so it can't fire on a 2-AP site* (E, definition) | AP uptime, CPU, uplink | **100637** (10 drops/10 min, same AP), 100620/100641 device down (G), 100621 isolated (G) | Correlate 100637 with RF and PoE → **G8**. PoE budget: incident 03007009 → **G5** |
| 4 | **Client can't join / no IP** | `AP_C_FL`, `OSG_DHCP_S` (reject), `OSW_C_1X_FL` | **01003014** failed to connect, **01003016** failed to obtain IP; bundle-only 01003015, 01003017 | — | 100629 / **100639** (5 fails/10 min, G); 100608 DHCP rejected (E) | Burst rule on 100608 → **G7** (100671) |
| 5 | **Ping-pong or sticky roaming** | `W_C_ROAM` | **01004002** ping-pong (≥4 roams in 5 min), **01004005** sticky | — | 100601 / **100606** (3 roams/10 min, E); 100607 drops band steers (E) | Sticky roaming has no syslog form → **G5** |
| 6 | **Switch loop / broadcast storm** | `OSW_DET_LOOP`, `OSW_DET_STORM`, `OSW_STORM_SHUTDOWN`, `OSW_PB`, `OSW_STP_BLOCK`, `OSW_TOPO_C`, `OSW_STP_FWD`, `OSW_LOOP_C` | **03001001** loop detected, **03009004** storm control, **03005004** MAC moved ports ≥10× in 30 s, 03005010 illegal multicast | Switch port stats | 100634 lumps storm, loop, port blocked and STP blocked at level 6 (G). STP topology changes and loop-cleared go to the catch-all | Split STP churn from real loops; add recovery → **G2** |
| 7 | **WAN flapping / ISP outage** | `OSG_WAN_DOWN`, `WAN_IP_O_F`, `WAN_IP_OBTAIN`, `OSG_PPPOE_FL`, `WAN_ONLINE_DETECTION`, `OSG_BK_WAN_UP`, `OSG_PRI_WAN_UP`, `WAN_LINK_BACKUP`, `PHYSICAL_PORT_CONNECTION` | **02009003** WAN latency >3000 ms, 02009001 WAN bandwidth >90%, **02001001** gateway offline ≥4×/h, 02005003 DDNS abnormal; bundle-only 02009002 WAN loss, 02005001 dial-up failed | Gateway WAN status | 100633 "WAN or VPN down" (G; also catches IPsec). No recovery, no flap count | Split WAN from VPN, add recovery/failover, a flap counter and IP-obtain failures → **G4** |
| 8 | **Device offline or reboot loop** | `DEV_DISCONN`, `DEV_CONN`, `DEV_RECONN`, `DEV_C_DSYNC`, `DEV_READOPT_FL`, `REBOOT_RECOVERY*`, `OSW_INSTALL_REBOOT`, `DEVICE_MONITOR_STATUS_*` | 01001001, 02001001, **03001002** (switch offline ≥4×/h), **03007009** PoE over limit, 03007011 switch CPU | Device uptime | 100620 → **100641** (3 down/h, G); 100622 up (G) | IntelliRecover, auto-reboot, desync and monitor-link go to the catch-all → **G6** |
| 9 | **DHCP exhaustion / rogue DHCP** | `OSG_ROGUE_DHCP_SERVER_DETECTED`, `OSG_DHCP_LEASE_POOL_EXHAUSTED`, `OSW_DHCP_SNOOP_ALERT`, `OSG_DHCP_S` | **03003009** DHCP server conflict; bundle-only 03003010/03003011 pool warning/exhausted | DHCP lease table | **100625** rogue DHCP (E, real line), 100628 pool exhausted (G). Snooping goes to the catch-all | Dedicated snooping rule, DHCP-reject burst → **G2, G7** |
| 10 | **IP conflict** | `OSG_IP_CONFLICT_DETECTED`, `OSG_LAN_IP_CONFLICT`, `OSG_ARP_ATK`, `OSW_ARP_DETECTION_ALERT`, `DEV_IP_C` | **03003008** interface IP conflict | — | 100628 (G); `OSG_ARP_ATK` in 100626 "attack" (G). ARP detection goes to the catch-all | Dedicated ARP-detection rule + burst; `DEV_IP_C` → **G2, G6** |
| 11 | **Controller login brute force** | Global audit: Account / User Activity | Device-side: **02008001** (gateway), **03008001** (switch) unauthorised login via SSH/Telnet/web | — | 100648 → **100649** (3 fails/5 min, G); 100609 success (E) | Global audit delivery unverified (V4). Device-login incidents only by email → **G5** |
| 12 | **Syslog delivery failing** | `LOG_SRV_FL` (site), `GLOBAL_LOG_SRV_FL` (global) | — | `/logs/events` with key `LOG_SRV_FL` | 100632 lumps it with backup and mail failures, level 7 (G) | **I:** a failure report travels over the failing channel, so it may only show up after delivery recovers. Needs an out-of-band heartbeat → **G3** |
| 13 | **Wired port flapping / bad cable** | `L_C_CONN`, `L_C_DISCONN`, `PHYSICAL_PORT_CONNECTION`, `DEVICE_MONITOR_STATUS_LINK_*` | **03007015** port up/down ≥4×/min, 03007013 error packets, 03009003 port loss >50% | Switch port stats | Catch-all only. No wired client decoder (E: TODO in [R3]) | Wired client decoder + flap rule → **G6** |
| 14 | **Attack traffic at the gateway** | `OSG_ATK`, `OSG_SF_ATK`, `OSG_ARP_ATK`, `OSG_LARGE_PING_ATTACK` | **02008002** WAN/LAN attack packets | Threat management (if IPS is supported) | 100626 (level 10, G) | ACL hits and threat entries → **G11, G12** |

---

## 3. Prioritised gaps

**Rule IDs:** new IDs come from **100650–100699**, which is free in the repo (E: no matches on 2026-11-19). Proposed file: `docs/configs/wazuh/rules/omada_troubleshooting_rules.xml`. Overlap rule (I, needs `wazuh-logtest`): the new rules are children of 100619 (or of an existing rule they refine). Where an existing loose regex would claim the line first, narrow that regex in [R2] in the same PR. Known overlaps:

- 100625 `Rogue DHCP server` could catch a switch snooping line.
- 100626 `arp conflict` could catch ARP detection.
- 100634 also matches `port blocked` for STP.
- 100633 matches IPsec as well as WAN.
- 100632 lumps log-server failures with backup and mail failures.

Effort: **S** = rules/decoders + samples only. **M** = also touches the collector or adds a decoder file. **L** = a new data path or host change.

### P1: do these first

| ID | Gap | Value | Effort | Files a later PR would change | Proposed IDs | Verify |
|---|---|---|---|---|---|---|
| **G1** | **Install PR #59, then replace guessed wording with real lines** | Everything else rests on it. Today 20 sample lines are guesses | S (Jacob installs; doc/rule edits after) | `rules/omada_realtime_rules.xml` (tighten regexes), `tests/omada_realtime_samples.log`, `tests/omada_realtime_logtest.txt` | — (edits 100620–100649) | V1 + V2: every captured type decodes as `omada-controller` and none lands on 100619 |
| **G2** | **Dedicated L2 safety rules**: `OSW_DHCP_SNOOP_ALERT`, `OSW_ARP_DETECTION_ALERT`, STP churn vs real loops, loop cleared | Playbooks 6, 9, 10. These are the fastest signs of a rogue device or a loop on a flat home LAN | S | New `omada_troubleshooting_rules.xml`; narrow 100625/100626/100634 in [R2]; decoder sibling for `port <n>` → field `switch_port` in [R3]; samples + logtest | 100650 DHCP snoop (lvl 10) · 100651 ARP detection (8) · 100652 ARP detection 3+/10 min, same device (10) · 100653 STP topology change `OSW_TOPO_C`/`OSW_STP_FWD` (3) · 100654 STP churn 5+/10 min, same switch (8) · 100655 STP port blocked `OSW_STP_BLOCK` (5) · 100656 loop cleared `OSW_LOOP_C` (3) | V2 capture of one real line for each (snooping/ARP only if they fire naturally; **don't create a loop or a rogue DHCP server on purpose**) |
| **G3** | **Pipeline health**: `LOG_SRV_FL`/`GLOBAL_LOG_SRV_FL` as their own rule, plus a heartbeat that notices when Omada lines stop | Playbook 12. Without it, a silent pipe looks like a healthy network. Wazuh 4.8 has no "no events for N minutes" rule (I) | M | `omada_troubleshooting_rules.xml`; narrow 100632; `lab-status-collect.py`: in `collect_wazuh`, query the newest alert with `rule.groups: omada_controller` and emit `omada_last_seen_min`; when stale, emit an `omada-api` line (see G8) | 100657 log-server delivery failed (10) · 100683 collector heartbeat stale, Omada silent > 30 min (10) | Compare `omada_last_seen_min` with `archives.log`. Optional: a Cronitor check on the push (roadmap Cronitor line) |
| **G4** | **WAN troubleshooting set**: split WAN from IPsec, add IP-obtain/PPPoE failures, failover/recovery, a flap counter, online detection | Playbook 7, the most common "internet is down" call at home | S | `omada_troubleshooting_rules.xml`; narrow 100633 to WAN only (IPsec → its own branch); samples + logtest | 100658 WAN IP/PPPoE failure `WAN_IP_O_F`/`WAN_IP_OBTAIN`/`OSG_PPPOE_FL` (8) · 100659 failover/recovered `OSG_BK_WAN_UP`/`OSG_PRI_WAN_UP`/`WAN_LINK_BACKUP` (5) · 100660 WAN down 3+/h, same gateway (10) · 100661 `WAN_ONLINE_DETECTION` (6; meaning to confirm from a real line) | V2: capture on the next natural ISP blip. A planned WAN unplug only if Jacob accepts the household outage |
| **G5** | **Incidents path: choose one** (options and trade-offs below) | Playbooks 1–3, 5, 6, 8, 11, 13: Omada's own threshold detectors (RF, roaming, loop, port flap, WAN latency, PoE) | S to test; M to build | Depends on the option: `lab-status-collect.py` (Open API or UI poll) or a mail fetcher on a lab host + `localfile`; decoder `omada_api_decoders.xml` | 100676–100679 incident by level: Critical (10), Error (8), Warning (6), Info (3) · 100670 `INCIDENT_MAILED_FAILED` (7) | V7 (does any incident reach syslog?) and V8 (does the Open API serve incident records?) |

**G5: incident path options**

| Option | How | For | Against | Recommendation |
|---|---|---|---|---|
| **A. Open API** | Collector polls an incident-list endpoint with the existing read-only Open API app and emits one JSON line per new incident | Official auth, read-only app already exists, structured (`anomalyCode`, level, object) | [R6] cites `GET …/anomaly/incidents` [S4 §5.7]. The community spec marks `anomaly/*` Pro-only with **no** Incident Analysis list path [P7]. The sources disagree | **Test first** (V8). It's cheap, and if it works it's the best |
| **B. Email → Wazuh** | Incidents > Notification to a dedicated local-only mailbox; a fetcher on a lab host writes each mail to a file; Wazuh `localfile` + decoder | Officially supported [P3]; immediate send at 100 incidents (131451 Q2) | Needs controller SMTP and a mailbox credential on a lab host (Jacob sets it up; never in the repo or chat); unknown body format; more moving parts; email latency | **Fallback** if A fails |
| **C. Web-UI API poll** | Poll the undocumented UI endpoint that served the incident-settings capture | Same data as the UI | Needs a UI login session, not an Open API app. Undocumented, so it can break on upgrade. A stored admin-type credential on `.176` | **Avoid**, unless a Viewer-only UI account is acceptable to Jacob |
| D. Webhook | — | — | Incidents aren't in the webhook [P4], [R10] | Not an option |

### P2: next

| ID | Gap | Value | Effort | Files | Proposed IDs | Verify |
|---|---|---|---|---|---|---|
| **G6** | **Wired clients and device health**: `L_C_CONN`/`L_C_DISCONN` decoder + flap; `DEV_C_DSYNC`, `DEV_READOPT_FL`, IntelliRecover, `OSW_INSTALL_REBOOT`, monitor-link, `DEV_IP_C` | Playbooks 8, 10, 13. Wired-side flaps and reboot loops are invisible today | M (needs a decoder sibling) | [R3]: fill the wired-client TODO (fields `client_name`, `client_mac`, `switch_name`, `switch_port` if present); `omada_troubleshooting_rules.xml` | 100662 wired online (3) · 100663 wired offline (3) · 100664 wired flap 5+/10 min, same client (8) · 100665 config desync / readopt failed (7) · 100666 auto reboot / IntelliRecover (7) · 100667 reboot loop 3+/h, same device (10) · 100668 monitor link down/error (7) · 100669 device IP changed (5) | V2: unplug and replug one wired client; reboot the switch from the UI at a quiet time (also yields DEV_*) |
| **G7** | **DHCP reject burst** | Playbooks 4, 9: pool trouble or a misbehaving client | S | `omada_troubleshooting_rules.xml` | 100671 10+ `DHCP Server rejected` in 10 min (frequency on 100608) (8) | Logtest with 10 copies of [R4] line 13 |
| **G8** | **Open API bridge into Wazuh** (RF over threshold, threat entries, incidents, heartbeat) + **RF ↔ disconnect correlation** | Playbooks 1–3: answers *why* an AP dropped clients (interference vs utilisation vs PoE) instead of only *that* it did | M | `lab-status-collect.py`: a separate cron every 5–15 min that emits compact JSON over syslog (`logger -t omada-api`) or to a file read by a Wazuh agent; new `decoders/omada_api_decoders.xml` (`program_name` `omada-api` + `JSON_Decoder`); rules. Use the **same AP MAC field name and format** as [R3] (`from_ap_mac`, dashed upper-case) so `same_field` can join them | 100675 omada-api base (0) · 100680 threat-management entry (10) · 100681 radio over threshold (interference ≥50% or utilisation ≥70%, mirroring incidents 01009010/01009002) (6) · 100682 AP drop storm (100637) within 30 min of an over-threshold radio on the same AP (10) | V9: collector output has `rf[]` with numbers; logtest one emitted line; then a natural evening of busy RF |
| **G9** | **Dashboards and saved searches** | Turns alerts into a troubleshooting view: "what happened on AP X tonight" | M | New `docs/configs/wazuh/dashboards/omada-troubleshooting.ndjson` (saved objects export, scrubbed of index IDs and hostnames) + a short README | — | Import on CT 100; every panel returns data for the last 7 days |
| **G10** | **Alert-fatigue tuning** | Keeps level-6+ pages (Grok Bot integration, block A [`integration-grokbot.xml`](../configs/wazuh/ossec-conf/integration-grokbot.xml)) worth reading | S | `omada_troubleshooting_rules.xml`; [R2] (add `<ignore>` to frequency rules); CDB list **on CT 100 only** for known-noisy client MACs (never committed) | 100672–100674 explicit level-3 rules for informational keys (`OSG_*` "Module Information", `OSW_LAG_PORT_*`, `DEV_DISCOVER`, `AUTO_BK_OK`, `CONNECTED_CLOUD_ACCESS_SUCCESS`, `LOG_SRV_OK`), so 100619 means "really new" | After a week: count of 100619 per day, and pages per day from block A |

**G9 starter saved searches** (filter → question it answers):

| Saved search | Filter | Question |
|---|---|---|
| Flapping clients | `rule.groups: omada_client_flap` | Who keeps dropping, and on which AP? |
| AP drop storms | `rule.groups: omada_ap_flap` | Which AP shed clients, and when? |
| RF churn | `rule.groups: omada_rf` | Channel changes, radar, (later) RF over threshold |
| Devices down | `rule.groups: omada_device_down` | AP/switch/gateway offline and flaps |
| WAN | `rule.groups: omada_wan` | ISP outages and failovers |
| Security | `rule.groups: omada_security OR authentication_failures` | Rogue DHCP, attacks, login failures |
| Unclassified | `rule.groups: omada_unclassified` | New message shapes to write rules for ([R5 workflow](wazuh-omada-syslog.md#omada_unclassified-workflow)) |
| Admin changes | `rule.groups: omada_audit_admin OR omada_audit_wifi` | "Did someone change something before it broke?" |

Visualisations: disconnects per `data.from_ap_name` over time (stacked by SSID); top `data.client_mac` by 100636; channel changes per AP; level-6+ count per day.

**G10 tuning notes (I):**

- **Wired client lines:** once installed, any enabled site type without a rule lands on 100619 at level 5. Wired client on/off may be the noisiest, so G6 before or alongside G10.
- **100634:** STP port blocking is normal STP behaviour. Splitting it (G2) stops level-6 noise.
- **100635/100636:** IoT devices with aggressive power-save produce short sessions. Use a CDB list on CT 100 to drop known flappers to level 3, rather than raising the threshold for everyone.
- **Frequency rules** (100636, 100637, 100641, 100649): add `<ignore>600</ignore>` so one storm pages once.
- **`logall`:** it was found on (2026-10-31, [R5]) at ~500 MB/day. Turn it off after V2 captures are done.

### P3: later or conditional

| ID | Gap | Condition | Effort | Files | Proposed IDs | Verify |
|---|---|---|---|---|---|---|
| **G11** | **Gateway ACL hit logging** | Only if V5 shows a per-rule **Log** toggle on the ER605 V2. Community says it's likely absent [P6] | M | New `decoders/omada_gateway_acl_decoders.xml` (format `firewall<5>: [ACL]GATEWAY=…,ACTION=Block\|Allow,…` per [P6]); rules | 100690 ACL base (0) · 100691 block into the management network (7) · 100692 same source blocked 20+/5 min (10) · 100693–100699 reserved | Enable Log on **one** deny rule (for example guest → management) for 10 minutes; grep `[ACL]GATEWAY`. High volume if it's left on an allow rule |
| **G12** | **IDS/IPS threat entries** | Only if IDS/IPS can be enabled with the ER605 V2 (V6) | M (rides on G8) | `lab-status-collect.py` (threat-management endpoint per [P7]); rule 100680 | (100680) | One test signature hit, if the UI offers a test; otherwise wait |
| **G13** | **Email → Wazuh for incidents** | Only if G5 option A fails | L | Mail fetcher on a lab host; `localfile`; decoder | (100676–100679) | One incident email decoded end to end |
| **G14** | **Wazuh 5.x drops the built-in 514 listener** [R11] | Matters if #44 ever targets 5.x (current plan: 4.14.x [ROADMAP](../ROADMAP.md)) | L | rsyslog on CT 100 → file → `localfile`; decoders unchanged if the header is preserved | — | Before any 5.x upgrade, replay `archives.log` samples through the new path |
| **G15** | **Wireless IDS** | Wi-Fi 6/7 APs on firmware 1.10+ [R5] | M | Decoder + level-12 rule (planned in [R5]) | 100627 → real rule | Hardware change first |
| **G16** | **Webhook backup path** | Only if Wazuh downtime becomes a real problem | M | See [R10] | — | — |

---

## 4. Verify first (Jacob; read-only from Ship Desk's side)

Ship Desk drafts and reviews. Jacob runs every command and makes every UI change. Paste results back with IPs, MACs and the controller-name suffix redacted.

| # | Check | How | What it decides |
|---|---|---|---|
| **V1** | **Baseline install** | [INSTALL-STEPS](omada-wazuh-realtime-INSTALL-STEPS.md) A1–A5: `wazuh-analysisd -t` is clean, logtest IDs match | G1 can start |
| **V2** | **Capture one real line per category** | `logall` on ([R7] 9b step 1). Use safe triggers: toggle phone Wi-Fi (`AP_C_OK`/`W_C_DISCONN`); wrong Wi-Fi password on a test device (`AP_C_FL`); reboot one AP from the UI at a quiet time (`DEV_DISCONN`/`DEV_CONN`, maybe `AP_CH_C`); unplug and replug one wired client (`L_C_*`); change one AP's channel in the UI (audit → 100644, maybe `AP_CH_C`). Then `grep -a 'OMADA_CONTROLLER_IP' /var/ossec/logs/archives/archives.log \| tail -n 50` and run each line through `wazuh-logtest` | Replaces guessed wording (G1); gives G2/G4/G6 their exact text. Anything that lands on 100619 is a new rule candidate |
| **V3** | **Timestamp format on 6.x** | `grep -aE ' 1 20[0-9]{2}-[0-9]{2}-[0-9]{2}T[0-9]' archives.log \| head`. It should print nothing. The parent decoder expects a **space**, not `T` [R3]. E: site lines from 6.3 have the space ([R4] lines 1–24, real) | If global lines use `T`, the pre-decoder strips the header and `omada-controller` never matches. That needs a second prematch [P8] |
| **V4** | **Site vs global lines arrive** | [R7] step 9b: one wrong controller password, then look for the audit line and its header | Row 2/3 confidence in the matrix; whether 100648/100649 can ever fire |
| **V5** | **ER605 V2 ACL Log toggle** | Omada UI: open an existing **Gateway ACL** rule (the site's network security / ACL settings; the menu name varies by version) and look for a **Log** switch. Then `grep -a '\[ACL\]GATEWAY' archives.log` | G11 go/no-go |
| **V6** | **IDS/IPS on the ER605 V2** | Omada UI: is IDS/IPS offered for this gateway, and does *Threat Management* have entries? Don't enable it if the UI warns about throughput | G12 go/no-go |
| **V7** | **Do incidents ever reach syslog?** | When something appears under *Incidents > Incident Analysis*, note the time and name; search `archives.log` for that time, the UI name and the `anomalyCode` ([incidents.md test](omada-log-inventory/incidents.md#how-this-relates-to-syslog--wazuh)) | Confirms or refutes "email only" for this controller |
| **V8** | **Open API incident endpoint** | With the existing read-only Open API app, search the [6.3.0 Open API docs](https://omada-northbound-docs.tplinkcloud.com/6.3.0/) for "anomaly"/"incident", try the list call once, and report **only** the HTTP status and the top-level field names | G5 option A vs B |
| **V9** | **Collector output** | After INSTALL-STEPS D11: `rf[]` has per-radio numbers; `disconnects_24h.total` > 0; whether `timeline_top_clients` shows any `rssi`/`reason` attribute | G8 design; whether RSSI-at-drop is available at all |
| **V10** | **What pages Grok Bot** | After install, count the alerts per day at level ≥6 in group `omada` | G10 thresholds |

---

## 5. Evidence vs inference (consolidated)

| Claim | Label | Basis |
|---|---|---|
| Site remote logging delivers to Wazuh and decodes | **E** | Real lines [R4]; first live alert on 2026-10-31 [R5] |
| Global remote logging is configured | **E** | Screenshot 2026-11-18 [R6 L2] |
| Global lines actually arrive | **Unverified** | V4 |
| 143/181 alert/event rows have no dedicated rule | **E** | [R6] tables A/B (rule column) |
| 20 sample lines use guessed wording | **E** | [R7] step 4 |
| Incidents are email-only | **E** (docs) / **I** (this controller) | [P3]; V7 |
| Open API serves incident records on a non-Pro controller | **Conflicting** | [R6] vs [P7]; V8 |
| ER605 V2 lacks the ACL Log toggle | **I** | [P6] on ER605 generally; V5 |
| IDS/IPS entries never reach syslog | **E** (community + vendor guide) | [P9] |
| `LOG_SRV_FL` may arrive late or never during an outage | **I** | Same channel as the failure; G3 |
| 01001003 can't fire with 2 APs | **E** | Incident definition (≥6 APs) [R8 incidents] |
| Wazuh 4.8 can't alert on the *absence* of events by itself | **I** | No absence rule type in 4.8; heartbeat in G3 |
| Overlapping loose regexes in 100625/100626/100632–100634 will steal new keys | **I** | Rule order [R1]/[R2]; logtest in G2/G4 |

---

*Drafted by Ship Desk from repo `main` and public sources listed above. No live system was touched.*
