# Omada incident / anomaly dictionary

A field-tested list of the **incident (anomaly) types** a TP-Link Omada controller can detect, with the anomaly code, object type, level, threshold parameters, and the name and definition the controller UI uses. Incidents are a separate feature from the [alert and event types](README.md) under *Logs > Setting*. They live under **Site > Incidents** (Intelligent Incident Detection, controller v6.3 and above).

This is for homelabbers and Omada users who want the incident dictionary itself: what exists, what it is called, and which parameters a type takes. It does not record which types one network has enabled.

## Capture

| | |
|---|---|
| Controller | Omada **Software Controller** (self-hosted), version: `<fill in from Settings > About>` |
| Captured | 2026-11-18 |
| Method | Read-only: the controller's **Incidents > Settings** response (the same list the web UI's *Site > Incidents > Settings* page shows: code, category, level, object type, and any trigger parameters). Names, definitions, category labels and level labels are from the **Omada controller web UI bundle** (version per the row above), from the Settings-page incident dictionary, not from the longer analysis-view title templates. |
| Removed | Per-instance state: whether each type is enabled. The dictionary says what *exists*, not how one network is set up. Parameter values in the Settings response are recorded as **observed values** (they often match the UI definition's defaults); they are not a record of anyone's policy. |

Hardware controllers (OC200/OC300) and Omada Pro may expose a different set. The UI bundle lists 88 types; this controller's Settings list had 45 of them. Contributions from other controller types are welcome.

## How this relates to syslog / Wazuh

**Unknown whether incident records themselves are sent over syslog or webhook.** Treat that as unverified.

- Incident *notifications* in the official docs are email: *Site > Incidents > Notification*, plus the per-user *Alert/Event/Incident Notification* checkbox. The UI bundle's incident-notification strings also describe email, not syslog. [User Guide V6.3 §17.5.2](https://static.tp-link.com/upload/manual/2026/202608/20260818/1900004421_Omada%20SDN%20Controller_V6.3_User%20Guide.pdf) · [Configure Intelligent Incident Detection](https://support.omadanetworks.com/en/document/131451/)
- Remote logging is configured separately under *Logs > Setting > Advanced*, and the official how-to tells you to enable **Alerts, Events and Audit Logs** for the syslog server. Incidents are not mentioned there. [Email Notification and Remote Logging](https://support.omadanetworks.com/us/document/13012/) · [User Guide V6.3 §17.4.6](https://static.tp-link.com/upload/manual/2026/202608/20260818/1900004421_Omada%20SDN%20Controller_V6.3_User%20Guide.pdf)
- The V6.3 datasheet lists Logs (alerts / events / webhook / remote logging) and Incidents (analysis / notifications / settings) as separate monitoring features.

Some alert/event types cover similar ground (loop detection, device disconnect, gateway attack, client connection failed, storm control). That overlap does not prove an incident is also emitted as a log line.

**A useful test:** wait for (or trigger) a type that already appears under *Incidents > Incident Analysis*, note the time and the UI name / `anomalyCode`, then search the syslog receiver (for example Wazuh `archives.log` with `logall`) for that code, the UI name, and the same timestamp. Also check whether a nearby alert/event key fired instead. If nothing shows up, incidents stay in the controller UI, email, and (if you poll it) the Open API, not in the log pipeline.

## Columns

| Column | Meaning |
|---|---|
| anomalyCode | The controller's 8-digit incident type key, for example `01009009`. Stable and best for matching. |
| Category | The numeric `category` from the Settings response, with the UI name joined as described below. The number-to-name join is an inference. |
| objectType | `ap`, `switch`, `gateway`, `wiredClient` or `wirelessClient`, as returned. |
| Level | The numeric `level` from the Settings response, with the UI name joined as described below. The number-to-name join is an inference. |
| Observed params | Trigger-parameter values from the Settings response, with units taken from the UI definition. Empty (`—`) means the type has no configurable threshold in this snapshot. These are observed values, not a policy record. |
| Name (from UI bundle) | The Settings-page title, verbatim except that `{SITE}` / `{SITE_LOWER}` (UI placeholders for the word “site”, not a site name or ID) are rendered as `site`. Typos and punctuation are kept, including *Unauthorized log in*. |
| Incident definition (from UI bundle) | The Settings-page definition. Placeholders such as `%threshold%` and `%count%` are the parameter names. |

The incident *analysis* view uses a longer title with device and client placeholders. Those templates are not listed here.

## Categories 11–19

The Settings JSON numbers categories **11–19** and does not name them. The UI bundle (`ABNORMAL_INCIDENT`) labels nine categories:

Access, Authentication, Roaming, Wireless Network, Wired Network, Link, WAN & Services, Device Status, Security (and an Other label unused in this capture).

Those are the same nine names in the [Omada Incident Detection and Health Assessment white paper](https://static.tp-link.com/upload/document-and-bulletins/2026/202610/20261016/Omada%20Incident%20Detection%20and%20Health%20Assessment%20White%20Paper.pdf) and in [User Guide V6.3 §17.5](https://static.tp-link.com/upload/manual/2026/202608/20260818/1900004421_Omada%20SDN%20Controller_V6.3_User%20Guide.pdf). One support article introduction also says *Wireless Environment* and *Wired Environment*; the UI bundle, the user guide and the white paper say *Wireless Network* and *Wired Network*.

**Inference:** every captured type's UI title belongs to exactly one of those nine, and the JSON `category` number follows this order:

| category | Name (from UI bundle) |
|---|---|
| 11 | Access |
| 12 | Authentication |
| 13 | Roaming |
| 14 | Wireless Network |
| 15 | Wired Network |
| 16 | Link |
| 17 | WAN & Services |
| 18 | Device Status |
| 19 | Security |

The bundle does not contain a literal `11: Access` assignment. Types that appear only in the UI bundle (not on this controller) are listed without a category number.

## Level mapping

The Settings JSON uses integer `level` values 0–3. The UI bundle labels the four incident levels **Critical, Error, Warning, Info** (`INCIDENT_CRITICAL`, `INCIDENT_ERROR`, `INCIDENT_WARNING`, `INCIDENT_INFO`, and the same four words under `ABNORMAL_SETTINGS`). The official docs use the same four names.

**Inference:** this capture's `statistic` object counted 4 critical, 5 error, 29 warning and 7 info, which matches the number of rows at levels 0, 1, 2 and 3 respectively. That is the basis for:

| level | Name (from UI bundle) |
|---|---|
| 0 | Critical |
| 1 | Error |
| 2 | Warning |
| 3 | Info |

The bundle does not contain a literal `0: Critical` assignment.

## anomalyCode structure

**Inference from the 88 codes in the UI bundle**, not a published layout. Each code is an 8-digit string that groups as `PP` + `GGG` + `SSS`:

- **PP (digits 1–2), object family:** `01` AP or wireless client; `02` gateway; `03` switch or wired client; `04` portal / wireless-client portal; `06` appears once, a site-wide portal-authentication type (`06003001`). The same prefix can cover more than one `objectType` (`01` is both `ap` and `wirelessClient`; `03` is both `switch` and `wiredClient`).
- **GGG (digits 3–5), metric group:** correlates with, but is not the same as, the category number. In this bundle: `001` offline or loop; `002` mesh; `003` access / authentication / portal; `004` roaming; `006` abnormal reboot; `007` device hardware (CPU, temperature, PoE, optical module); `008` security; `009` sampled performance; `010` signal-strength distribution.
- **SSS (digits 6–8):** the specific type inside that group.

## Types

<!-- GENERATED:START (build-omada-incident-dictionary.py) -->
**45 types** were in this controller's Incidents > Settings list. The UI bundle lists **88** types; **43** of those were not on this controller.

Category names and level names are labeled as inferred (see above). Parameter values are observed values from the Settings response, not a record of anyone's enable/threshold policy. `{SITE}` / `{SITE_LOWER}` in the UI strings are placeholders for the word “site” and are rendered as `site` here.

### Types on this controller

| # | anomalyCode | Category | objectType | Level | Observed params | Name (from UI bundle) | Incident definition (from UI bundle) |
|---|---|---|---|---|---|---|---|
| 1 | `01003014` | 11 Access | wirelessClient | 2 Warning | — | Client failed to connect | The client connection failed. |
| 2 | `01003016` | 11 Access | wirelessClient | 2 Warning | — | Client failed to obtain IP | The client failed to obtain an IP address. |
| 3 | `03003008` | 11 Access | switch | 2 Warning | — | Interface IP address conflict | An Interface IP address conflict was detected. |
| 4 | `03003009` | 11 Access | switch | 2 Warning | — | DHCP server conflicted | A DHCP server conflict was detected. |
| 5 | `02003001` | 11 Access | gateway | 3 Info | — | Gateway client limit reached | The number of connected clients has reached the device's limit. |
| 6 | `03003003` | 12 Authentication | wiredClient | 1 Error | — | Switch 802.1X authentication failure | Switch 802.1X authentication failed. |
| 7 | `04003001` | 12 Authentication | wirelessClient | 2 Warning | — | Client Portal authentication failure | Client Portal authentication failed. |
| 8 | `04003002` | 12 Authentication | wirelessClient | 2 Warning | threshold=2 s | Client Portal authentication too slow | The client takes ≥ %threshold% s to communicate with a device/external service during portal authentication. |
| 9 | `03003006` | 12 Authentication | wiredClient | 3 Info | threshold=3000 | Switch 802.1X authentication took too long | Switch 802.1X authentication took too long. |
| 10 | `01004002` | 13 Roaming | wirelessClient | 3 Info | threshold=4 times | Client ping-pong roaming | Within 5 min, the client roams between different bands of one AP or different APs %threshold% or more times. |
| 11 | `01004005` | 13 Roaming | wirelessClient | 3 Info | — | Client sticky roaming | The client is unable to roam. |
| 12 | `01009002` | 14 Wireless Network | ap | 2 Warning | count=80 %, threshold=70 % | AP channel utilization too high | Within 15 min, the percentage of channel utilization samples exceeding %threshold%% is ≥ %count%%. |
| 13 | `01009009` | 14 Wireless Network | ap | 2 Warning | count=80 %, threshold=-85 dBm | AP noise floor too high | Within 15 min, the percentage of noise floor samples exceeding %threshold% dBm is ≥ %count%%. |
| 14 | `01009010` | 14 Wireless Network | ap | 2 Warning | count=80 %, threshold=50 % | AP wireless interference rate too high | Within 15 min, the percentage of interference rate samples exceeding %threshold%% is ≥ %count%%. |
| 15 | `01009001` | 14 Wireless Network | wirelessClient | 3 Info | count=80 %, threshold=20 dB | Client SNR exception | Within 15 min, the percentage of SNR samples below %threshold% dB is ≥ %count%%. |
| 16 | `01009003` | 14 Wireless Network | wirelessClient | 3 Info | count=80 % | Client negotiation rate exception | Within 15 min, the percentage of abnormal negotiation rate samples is ≥ %count%%. |
| 17 | `03005010` | 15 Wired Network | switch | 1 Error | — | Illegal multicast packet | Illegal multicast packet was detected. |
| 18 | `03005006` | 15 Wired Network | switch | 2 Warning | — | Host routing entry overflow | Host routing entry overflow was detected. |
| 19 | `03005007` | 15 Wired Network | switch | 2 Warning | — | ARP table overflow | ARP table overflow was detected. |
| 20 | `03005009` | 15 Wired Network | switch | 2 Warning | — | Multicast table overflow was detected | Multicast table overflow was detected. |
| 21 | `03009001` | 15 Wired Network | switch | 2 Warning | count=80 %, threshold=90 % | Switch port traffic too high | Within 15 min, %count%% of the port traffic rate samples exceed %threshold%% of the maximum bandwidth of the port. |
| 22 | `03009002` | 15 Wired Network | switch | 2 Warning | count=80 %, threshold=50 % | Switch LAG Group member port load too different | Within 15 min, the difference between the highest and lowest member port rates exceeds %threshold%% in %count%% of the samples. |
| 23 | `03009003` | 15 Wired Network | switch | 2 Warning | count=80 %, threshold=50 % | Switch port packet loss rate too high | Within 15 min, %count%% of packet loss rate samples of a single port exceed %threshold%%. |
| 24 | `03009004` | 15 Wired Network | switch | 2 Warning | — | Storm control event | A storm control event occurred. |
| 25 | `03001001` | 16 Link | switch | 1 Error | — | Loop detected | A loop was detected. |
| 26 | `03005005` | 16 Link | switch | 1 Error | — | LACP convergence failure | LACP convergence failed. |
| 27 | `03007013` | 16 Link | switch | 1 Error | count=80 %, threshold=90 | Switch port detects error packets | The port detected error packets. |
| 28 | `03005004` | 16 Link | switch | 2 Warning | timeRange_s=30 s, changedTimes=10 times | Repeated address migrations | Within %timeRange_s% s, the same MAC address migrated between different ports in the same VLAN %changedTimes% times. |
| 29 | `03007015` | 16 Link | switch | 2 Warning | changedTimes=4 times, timeRange=1 min | Switch Port goes up/down frequently | Within %timeRange% min, the port up/down status changed %changedTimes% times or more. |
| 30 | `02005003` | 17 WAN & Services | gateway | 0 Critical | — | DDNS service abnormal | DDNS service is abnormal. |
| 31 | `02009001` | 17 WAN & Services | gateway | 2 Warning | count=80 %, threshold=90 % | Gateway WAN port bandwidth utilization rate too high | Within 15 min, %count%% of WAN port traffic samples exceed %threshold%% of the Bandwidth Control value or %threshold%% of the WAN port physical bandwidth. |
| 32 | `02009003` | 17 WAN & Services | gateway | 2 Warning | count=80 %, threshold=3000 ms | Gateway WAN port latency too high | Within 15 min, %count%% of the WAN port latency samples exceed %threshold% ms. |
| 33 | `02005002` | 17 WAN & Services | gateway | 3 Info | — | VPN connection failure | VPN connection failed. |
| 34 | `01001001` | 18 Device Status | ap | 0 Critical | offlineCount=2 times | AP frequently offline | Within 1 hour, the AP goes offline %offlineCount% or more times. |
| 35 | `01001003` | 18 Device Status | ap | 0 Critical | disconnectApPercent=60 %, disconnectCount=5 times, avgDisconnectCount=2 times | APs on site going offline in batches | When the total number of online APs is ≥ 6, the average number of APs going offline within 1 hour is ≥ %avgDisconnectCount%, the percentage of offline APs is ≥ %disconnectApPercent%%, or the number of offline APs is ≥ %disconnectCount%. |
| 36 | `02001001` | 18 Device Status | gateway | 0 Critical | offlineCount=4 times | Gateway goes offline from the controller frequently | Within 1 hour, the gateway goes offline %offlineCount% or more times. |
| 37 | `01007001` | 18 Device Status | ap | 2 Warning | count=80 %, threshold=90 % | AP CPU utilization rate too high | Within 10 min, the percentage of CPU samples at or above %threshold%% is ≥ %count%%. |
| 38 | `02007002` | 18 Device Status | gateway | 2 Warning | count=80 %, threshold=90 % | Gateway CPU utilization rate too high | Within 10 min, the percentage of CPU samples at %threshold%% or higher is ≥ %count%%. |
| 39 | `03001002` | 18 Device Status | switch | 2 Warning | offlineCount=4 times | Switch goes offline frequently | Within 1 hour, the switch goes offline %offlineCount% or more times. |
| 40 | `03007009` | 18 Device Status | switch | 2 Warning | — | Excessive PoE power | PoE power exceeds limit. |
| 41 | `03007011` | 18 Device Status | switch | 2 Warning | count=80 %, threshold=90 % | Switch CPU utilization rate too high | Within 10 min, the percentage of CPU samples at %threshold%% or higher is ≥ %count%%. |
| 42 | `03007016` | 18 Device Status | switch | 2 Warning | — | Abnormal optical module DDM | The optical module has abnormal parameters. |
| 43 | `02008001` | 19 Security | gateway | 2 Warning | — | Unauthorized log in from a gateway | Within 10 min, an unauthorized user attempted to log in to the device via the serial port/TELNET/SSH/WEB. |
| 44 | `02008002` | 19 Security | gateway | 2 Warning | — | Gateway WAN or LAN port detected attack packets | Gateway WAN or LAN port detected attack packets. |
| 45 | `03008001` | 19 Security | switch | 2 Warning | retryCnt=1 times | Unauthorized log in from a switch | Within 10 min, an unauthorized user attempted to log in to the device via the serial port/TELNET/SSH/WEB %retryCnt% or more times. |

### Types in the UI bundle, not on this controller's list

These codes appear in the same Settings-page dictionary in the UI bundle, but they were not in this controller's Settings response. No category, level, objectType or params were captured for them. They may exist on other controller types, versions or licenses.

| # | anomalyCode | Name (from UI bundle) | Incident definition (from UI bundle) |
|---|---|---|---|
| 1 | `01002001` | AP receiving weak mesh signals | Within 15 min, the percentage of AP RSSI samples at or below %threshold% dBm is ≥ %count%%. |
| 2 | `01002003` | Uplink AP offline | Uplink AP is offline. |
| 3 | `01002004` | Uplink AP disconnected and device out of range of other APs | The uplink AP is disconnected, and the device is not within the detection range of other APs. |
| 4 | `01002005` | Mesh AP isolated | Mesh AP is in the Isolated state. |
| 5 | `01003001` | Client association failure | The client association failed. |
| 6 | `01003002` | Client frequently offline | Within 15 min, the client goes offline %offlineCount% or more times. |
| 7 | `01003004` | Low client association success rate | Within 1 hour, the number of client associations is ≥ 8, and the association success rate is ≤ %threshold%%. |
| 8 | `01003005` | Client authentication failure | The client authentication failed. |
| 9 | `01003007` | Low client authentication success rate | Within 1 hour, the number of client authentications is ≥ 8, and the authentication success rate is ≤ %threshold%%. |
| 10 | `01003010` | Low AP client association success rate | Within 1 hour, the number of associated clients under the AP is ≥ 8, the total number of associations is ≥ 8, and the success rate of all association events is ≤ %threshold%%. |
| 11 | `01003011` | Low AP client authentication success rate | Within 1 hour, the number of authenticated clients under the AP is ≥ 8, the total number of authentications is ≥ 8, and the success rate of all authentication events is ≤ %threshold%%. |
| 12 | `01003013` | Abnormal client disconnection | The client disconnected abnormally. |
| 13 | `01003015` | Client slow to connect | The client takes ≥ %threshold% ms to complete association and authentication. |
| 14 | `01003017` | Client slow to obtain IP | The client takes ≥ %threshold% ms to obtain an IP address. |
| 15 | `01004001` | Low AP client roaming success rate | Within 1 hour, the successful roaming rate is ≤ %threshold%%. |
| 16 | `01004003` | Client roams frequently | Within 1 hour, the client roams %threshold% or more times. |
| 17 | `01004004` | Client roams slowly | Within 1 hour, the percentage of all client roaming times exceeding %duration% s is > %threshold%%. |
| 18 | `01006001` | Abnormal AP reboot | The AP rebooted abnormally. |
| 19 | `01007003` | AP temperature too high | Within 10 min, the device's temperature is too high. |
| 20 | `01009004` | Client negotiation rate distribution exception | Within 15 min, on the 2.4 GHz band, the percentage of the samples of the client's normal negotiation rate under the AP is ≤ %count2g%%. Within 15 min, on the 5 GHz band, the percentage of the samples of the client's normal negotiation rate under the AP is ≤ %count5g%%. Within 15 min, on the 5 GHz-2 band, the percentage of the samples of the client's normal negotiation rate under the AP is ≤ %count5g2%%. Within 15 min, on the 6 GHz band, the percentage of the samples of the client's normal negotiation rate under the AP is ≤ %count6g%%. |
| 21 | `01009006` | Client interferes with low negotiation rate | Within 15 min, on the 2.4 GHz band, the client negotiation rate is abnormal, the throughput is ≥ %throughput2g% Mb, and the channel utilization rate of this band is ≥ %util2g%%. Within 15 min, on the 5 GHz band, the client negotiation rate is abnormal, the throughput is ≥ %throughput5g% Mb, and the channel utilization rate of this band is ≥ %util5g%%. Within 15 min, on the 5 GHz-2 band, the client negotiation rate is abnormal, the throughput is ≥ %throughput5g2% Mb, and the channel utilization rate of this band is ≥ %util5g2%%. Within 15 min, on the 6 GHz band, the client negotiation rate is abnormal, the throughput is ≥ %throughput6g% Mb, and the channel utilization rate of this band is ≥ %util6g%%. |
| 22 | `01009007` | Client retransmission rate too high | Within 15 min, the percentage of the client retransmission rate samples exceeding %threshold%% is ≥ %count%%. |
| 23 | `01009008` | Client packet loss rate too high | Within 15 min, the percentage of the client packet loss rate samples exceeding %threshold%% is ≥ %count%%. |
| 24 | `01009011` | AP retransmission rate too high | Within 15 min, on the 2.4 GHz band, the percentage of the AP retransmission rate samples exceeding %threshold2g%% is ≥ %count2g%%. Within 15 min, on the 5 GHz band, the percentage of the AP retransmission rate samples exceeding %threshold5g%% is ≥ %count5g%%. Within 15 min, on the 5 GHz-2 band, the percentage of the AP retransmission rate samples exceeding %threshold5g2%% is ≥ %count5g2%%. Within 15 min, on the 6 GHz band, the percentage of the AP retransmission rate samples exceeding %threshold6g%% is ≥ %count6g%%. |
| 25 | `01009012` | AP packet loss rate too high | Within 15 min, on the 2.4 GHz band, the percentage of the AP packet loss rate samples exceeding %threshold2g%% is ≥ %count2g%%. Within 15 min, on the 5 GHz band, the percentage of the AP packet loss rate samples exceeding %threshold5g%% is ≥ %count5g%%. Within 15 min, on the 5 GHz-2 band, the percentage of the AP packet loss rate samples exceeding %threshold5g2%% is ≥ %count5g2%%. Within 15 min, on the 6 GHz band, the percentage of the AP packet loss rate samples exceeding %threshold6g%% is ≥ %count6g%%. |
| 26 | `01010001` | Client signal strength distribution exception | Within 15 min, less than %ratio2g%% of clients on the 2.4 GHz band have a signal strength between %lowerThreshold2g% dBm and %upperThreshold2g% dBm. Within 15 min, less than %ratio5g%% of clients on the 5 GHz band have a signal strength between %lowerThreshold5g% dBm and %upperThreshold5g% dBm. Within 15 min, less than %ratio5g2%% of clients on the 5 GHz-2 band have a signal strength between %lowerThreshold5g2% dBm and %upperThreshold5g2% dBm. Within 15 min, less than %ratio6g%% of clients on the 6 GHz band have a signal strength between %lowerThreshold6g% dBm and %upperThreshold6g% dBm. |
| 27 | `03003005` | Layer 3 interface down | Layer 3 interface is down. |
| 28 | `03003010` | DHCP address pool warning | More than %addressPoolRate%% of the address pool’s available resources have been allocated. |
| 29 | `03003011` | DHCP address pool exhausted | The DHCP address pool is exhausted. |
| 30 | `03005003` | Address table overflow alarm | The number of MAC addresses reached 99% of the maximum value that the device can learn. |
| 31 | `03007001` | Switch temperature too high | Within 10 min, switch temperature is too high. |
| 32 | `03007006` | PoE power supply disruption | The PoE stopped supplying power. |
| 33 | `03007008` | PoE short circuit | The PoE short circuited. |
| 34 | `03007017` | Optical module DDM below threshold | The optical module DDM is below the threshold. |
| 35 | `03007018` | Optical module not recognized | The optical module cannot be recognized. |
| 36 | `03003001` | 802.1X authentication success rate too low | Within 1 hour, the 802.1X authentication success rate is lower than %successRate%%. |
| 37 | `03003002` | 802.1X authentication takes too long | Within 1 hour, %count%% of the sampling data exceeds %threshold% ms. |
| 38 | `02005004` | DNS service abnormal | DNS service is abnormal. |
| 39 | `02007001` | Gateway fan abnormal | Gateway fan is abnormal. |
| 40 | `02007003` | Gateway temperature too high | Within 10 min, the device's temperature is too high. |
| 41 | `02009002` | Gateway WAN port packet loss rate too high | Within 15 min, %count%% of the WAN port packet loss rate samples exceed %threshold%%. |
| 42 | `06003001` | site's successful portal authentication rate too low | Within 1 hour, in the site, the clients' portal authentication success rate is less than or equal to %threshold%%. |
| 43 | `02005001` | WAN port dial-up failed | WAN port dial-up failed. |
<!-- GENERATED:END -->

## Sources

- **Primary (codes, object types, levels, categories, observed params):** the Settings capture above.
- **Primary (names, definitions, category labels, level labels):** Omada controller web UI bundle (version per README), Settings-page incident dictionary. The raw bundle is not in this repo; the extracted titles are in [sources/omada-ui-incident-titles.json](sources/omada-ui-incident-titles.json).
- **Secondary (TP-Link, confirmation only):**
  - [Omada Incident Detection and Health Assessment white paper](https://static.tp-link.com/upload/document-and-bulletins/2026/202610/20261016/Omada%20Incident%20Detection%20and%20Health%20Assessment%20White%20Paper.pdf) (category names, official type lists, some default-threshold wording).
  - [How to Configure Intelligent Incident Detection (v6.3 or above)](https://support.omadanetworks.com/en/document/131451/).
  - [User Guide V6.3 §17.5](https://static.tp-link.com/upload/manual/2026/202608/20260818/1900004421_Omada%20SDN%20Controller_V6.3_User%20Guide.pdf).
  - [Remote logging how-to](https://support.omadanetworks.com/us/document/13012/) and User Guide §17.4.6 (syslog covers alerts, events and audit logs; incidents are not mentioned).

## Contribute a snapshot

1. **Capture**, read-only, using either:
   - **Web UI:** screenshots of *Site > Incidents > Settings* (the name, definition, category, level and trigger parameters).
   - **API / JSON:** the Incidents > Settings response from your browser's developer tools, or the equivalent Open API path if your version documents one. The raw JSON includes an `enable` flag per type; do not commit that file.
2. **Redact** before sharing: site names and site IDs, `omadacId`, the controller display-name suffix, IP addresses, hostnames, MAC addresses, serials, account names. The Settings JSON usually contains none of these, but check. You do not need to share enable choices; the generator drops them.
3. **Regenerate:**
   ```bash
   python3 docs/configs/omada/build-omada-incident-dictionary.py \
     --settings incident-settings.json \
     --titles docs/services/omada-log-inventory/sources/omada-ui-incident-titles.json \
     --out docs/services/omada-log-inventory --captured YYYY-MM-DD \
     --controller "Omada Software Controller (version: x.y.z)"
   ```
   The script validates the input (`errorCode` 0, unique `anomalyCode`, `statistic` level counts matching the rows), rewrites the tables between the `GENERATED` markers, and prints the counts. Don't commit the raw Settings JSON.
4. Open a PR saying which controller type and version you captured. If your list differs, we'll add a per-version column rather than overwrite. If your UI bundle has a different title set, include an updated titles extract and say which controller version it came from.
