# Omada alert/event dictionary

A field-tested list of every **alert and event type** a TP-Link Omada controller can log, with the exact key and label the controller uses. It's for homelabbers and Omada users who want Omada as a log source: syslog into Wazuh, Graylog, Loki or Splunk, or a webhook into automation.

A separate feature, **Intelligent Incident Detection** (*Site > Incidents*, v6.3+), has its own type list. That dictionary — anomaly codes, UI names, definitions, categories, levels and trigger parameters — is in [incidents.md](incidents.md). Whether those incident records also appear in syslog is unverified; see that page.

Why not just use TP-Link's docs? Because they don't match a real controller. The Open API guide's key table lists 116 site types, but this capture has 158 unique site keys, and 38 of the guide's keys aren't on the controller at all. Labels and categories differ too. This dictionary is built from what a controller actually returns.

| File | What |
|---|---|
| [site.md](site.md) | **Site level**: 82 alerts and 80 events (158 unique keys), plus the Wi-Fi quick pick. Start here. |
| [global.md](global.md) | **Global (controller) level**: 2 alerts and 17 events |
| [audit-categories.md](audit-categories.md) | Audit log categories: 16 global (captured); site list from TP-Link docs, pending capture |
| [incidents.md](incidents.md) | **Incidents (anomalies)**: 45 types on this controller, plus 43 more listed only in the UI bundle. Separate from alerts/events. |
| [omada-alert-dictionary.json](omada-alert-dictionary.json) / [.csv](omada-alert-dictionary.csv) | Machine-readable alerts/events: 181 rows (one per level, list and key), with counts in `meta.counts` |
| [omada-incident-dictionary.json](omada-incident-dictionary.json) / [.csv](omada-incident-dictionary.csv) | Machine-readable incidents: 88 rows (45 captured + 43 bundle-only), with counts in `meta.counts` |
| [sources/tplink-openapi-guide-5.6.1-keys.json](sources/tplink-openapi-guide-5.6.1-keys.json) | TP-Link's published alert/event key list, kept for comparison (secondary source) |
| [sources/omada-ui-incident-titles.json](sources/omada-ui-incident-titles.json) | Incident names and definitions extracted from the Omada controller web UI bundle (Settings-page dictionary) |
| Generators | Alerts/events: [`../../configs/omada/build-omada-dictionary.py`](../../configs/omada/build-omada-dictionary.py). Incidents: [`../../configs/omada/build-omada-incident-dictionary.py`](../../configs/omada/build-omada-incident-dictionary.py) |

## Capture

| | |
|---|---|
| Controller | Omada **Software Controller** (self-hosted), version: `<fill in from Settings > About>` |
| Captured | 2026-11-18 |
| Method | Read-only: the controller's **alert/event notification-settings** response at the Global and Site levels (the same data the web UI's *Logs > Setting > Alerts / Events* tabs show), plus the *Audit Logs* tab. The incident capture and the UI-bundle extract are described in [incidents.md](incidents.md#capture). |
| Removed | Per-instance state: whether each type is enabled, emailed or sent by webhook. The dictionary says what *exists*, not how one network is set up. |

Hardware controllers (OC200/OC300) and Omada Pro may expose a different set. TP-Link's guide marks a few types as hardware-controller-only or Pro-only. Contributions from other controller types are welcome.

## How Omada logging is organised

- **Two levels.** *Global View > Logs > Setting* holds controller-level types (backups, cloud access, controller nodes, global log delivery) and global audit categories. *(site) > Logs > Setting* holds everything about the network: clients, APs, switches, gateways, WAN, attacks. Each level has its own **Alerts**, **Events** and **Audit Logs** tabs.
- **Alert vs event.** A type can be classified as an alert (it gets a level: Warning, Error, Information, or the controller's own spelling `Critial`), as an event, or, for a few keys, as both. Over syslog both look the same, and the message text identifies the type.
- **Remote syslog is configured separately at each level**, under *Logs > Setting > Advanced* (server, port, and at site level *More Detail Logs*). Enabling it at the site doesn't send global logs, and the other way round. The alert/event notification settings only control email and webhook. They have no syslog flag. [TP-Link: Email Notification and Remote Logging](https://support.omadanetworks.com/us/document/13012/)
- **Syslog header.** The controller sends lines like `1 2026-10-30 22:40:47 <controller display name> - - - <message>`. The field before `- - -` is the controller's **display name**, which may contain spaces, not the site. Parsers that assume one token there will miss lines.
- **Webhook-capable.** Every captured type has a per-type webhook flag. TP-Link's Open API says that flag applies to *Omada Pro* controllers only, so treat "webhook-capable" as "the controller exposes the switch", not "it works on yours". The webhook body carries the same free text as syslog, with the shared secret inside the JSON and no signature. [Webhook setup](https://support.omadanetworks.com/en/document/53570/) · [Open API docs](https://use1-omada-northbound.tplinkcloud.com/doc.html)
- **Incidents are separate.** *Site > Incidents* is not a Logs > Setting tab. Official docs describe incident notifications as email. Remote logging is documented for alerts, events and audit logs only. Whether incident records also go to syslog or a webhook is unverified; see [incidents.md](incidents.md#how-this-relates-to-syslog--wazuh).

## Columns

| Column | Meaning |
|---|---|
| Key | The controller's internal type key, for example `W_C_DISCONN`. Stable and best for matching. |
| shortMsg | The label the UI shows, **verbatim**, typos and punctuation included. |
| Kind | `alert` or `event`. Keys in both lists are marked ⇄ in the tables and `inBothLists` in the JSON. |
| Module | Device, Client or System, as returned. |
| Level | Alert level (alerts only), as returned, including `Critial`. |
| Device types / client types | Which device or client types the type applies to, as returned (`ap`, `switch`, `gateway`, `olt`; `wireless`, `wired`). Blank means the controller didn't say. |
| Webhook-capable | The controller exposes a per-type webhook flag (see the caveat above). |
| TP-Link guide | Whether the key is in TP-Link's Open API guide §5.6.1, and whether the name matches. |
| Note | Short, neutral "what it means / why you'd care" for the types most people will use. |

## Homelab Wi-Fi troubleshooting quick pick

For client disconnects and channel crowding, enable (as alert or event, with syslog on at the **site** level) at least: `W_C_DISCONN`, `AP_C_OK`, `W_C_ROAM`, `AP_C_FL`, `AP_CH_C`, `AP_RADAR`, `AP_ISOLATE`, `DEV_DISCONN`, `DEV_RECONN`, `DEV_CONN`. One-line explanations are in [site.md](site.md#homelab-wi-fi-troubleshooting-quick-pick).

Useful patterns: several `W_C_DISCONN` for the same client within 10 minutes (a flapping client); many across clients on one AP (an AP or RF problem); repeated `AP_CH_C` on one AP (auto-channel fighting interference); `AP_RADAR` followed by a burst of disconnects (DFS move).

## What the logs don't tell you

**No alert/event type carries RSSI, SNR, a deauth/disassociation reason code, channel utilization or interference.** Rogue-AP scan results and WIDS findings have no log type either. For those, poll the Omada **Open API** with a read-only app (a Viewer-role app should do for these reads; not verified on every version). [Open API docs](https://use1-omada-northbound.tplinkcloud.com/doc.html) · [Open API app setup](https://support.omadanetworks.com/en/document/109315/)

| Need | Endpoint (under `/openapi/v1/{omadacId}/sites/{siteId}`) |
|---|---|
| Per-radio channel, width, Tx power, Tx/Rx/interference utilization | `GET /aps/{apMac}/radios` |
| Client RSSI, SNR, radio, AP | `GET /clients` |
| Per-client disconnect timeline | `GET /clients/{clientMac}/client-timeline?type=3` (attribute fields undocumented) |
| Event log with keys, for backfill | `GET /logs/events` (rows include `key`, `module`, `content`, `time`) |
| Rogue APs, WIDS | `GET /insight/rogueaps`, `GET /insight/wids` (hardware support varies) |

## Contribute a snapshot

1. **Capture**, read-only, using either:
   - **Web UI:** screenshots of *Logs > Setting > Alerts*, *Events* and *Audit Logs* at Global View and at one site.
   - **API / JSON:** the notification-settings responses (`GET /openapi/v2/{omadacId}/log-notification` and `GET /openapi/v2/{omadacId}/sites/{siteId}/site/log-notification` with a Viewer-role Open API app, or the same JSON from your browser's developer tools on the Alerts/Events tabs).
2. **Redact** before sharing:
   - The controller display-name suffix.
   - Site names and site IDs, and `omadacId`.
   - IP addresses and hostnames.
   - MAC addresses and serials.
   - Email recipients, webhook names/URLs and secrets.
   - Account names.

   The notification JSON usually contains none of these, but check. You don't need to share your enable/email/webhook choices; the generator drops them anyway.
3. **Regenerate:**
   ```bash
   python3 docs/configs/omada/build-omada-dictionary.py \
     --global global.json --site site.json \
     --guide docs/services/omada-log-inventory/sources/tplink-openapi-guide-5.6.1-keys.json \
     --out docs/services/omada-log-inventory --captured YYYY-MM-DD \
     --controller "Omada Software Controller (version: x.y.z)"
   ```
   The script validates the input (errorCode 0, every entry has key and shortMsg, no duplicate key within a list), rewrites the tables between the `GENERATED` markers, and prints the counts. Don't commit the raw JSON.

   For an Incidents > Settings snapshot, use the command in [incidents.md](incidents.md#contribute-a-snapshot). Don't commit that raw JSON either (it includes per-type enable flags).
4. Open a PR saying which controller type and version you captured. If your list differs, we'll add a per-version column rather than overwrite.

## Sources and where they disagree

- **Primary:** the controller capture above. Incident names and definitions are from the Omada controller web UI bundle (version per the Capture table); see [incidents.md](incidents.md#sources).
- **Secondary (TP-Link):**
  - [Open API Access Guide §5.6.1 / §5.2](https://use1-omada-northbound.tplinkcloud.com/v3/api-docs) (key and audit category lists).
  - [Controller User Guide V6](https://support.omadanetworks.com/en/document/111217/) and [User Guide V6.3](https://static.tp-link.com/upload/manual/2026/202608/20260818/1900004421_Omada%20SDN%20Controller_V6.3_User%20Guide.pdf) §17.5 (incidents).
  - [Remote logging how-to](https://support.omadanetworks.com/us/document/13012/).
  - [Intelligent Incident Detection (v6.3 or above)](https://support.omadanetworks.com/en/document/131451/) and the [Incident Detection white paper](https://static.tp-link.com/upload/document-and-bulletins/2026/202610/20261016/Omada%20Incident%20Detection%20and%20Health%20Assessment%20White%20Paper.pdf).
- **Disagreements found:**
  - **Site keys:** 38 guide keys absent here, 80 captured keys missing from the guide, and one name differs.
  - **Global keys:** 9 guide keys absent, including `LOGIN_FL` and `RO_O_SS`; 4 captured keys aren't in the guide.
  - **Audit categories:** the guide lacks Firmware, SD-WAN and Site Template, and lists IPS and License, which this controller doesn't have.
  - **Webhook:** TP-Link calls the per-type flag Pro-only, yet a software controller exposes it.
  - **Details:** see each page's notes and `meta.counts`.
