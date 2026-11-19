# Omada event inventory: what reaches Wazuh (syslog) and Grok Bot (webhook)

**Drafted:** 2026-11-17 (ET), **updated 2026-11-18** with the live global list [L1], on branch `feat/omada-wazuh-realtime`. **Controller:** Omada Software Controller 6.3 on CT 101. **Manager:** Wazuh 4.8.2 on CT 100 (#44).
**Related:** [wazuh-omada-syslog.md](wazuh-omada-syslog.md) · [omada-webhook-evaluation.md](omada-webhook-evaluation.md) · rules [`omada_realtime_rules.xml`](../configs/wazuh/rules/omada_realtime_rules.xml) · read-only checker [`omada-log-inventory.py`](../configs/omada/omada-log-inventory.py)

> **What exists:** the public [Omada alert/event dictionary](omada-log-inventory/README.md) is the source of truth for which alert/event types and audit categories exist (built from a live capture on 2026-11-18). This file is HNS-specific: it maps those types to our Wazuh rules and records how *this* lab's controller is wired to Wazuh. TP-Link docs ([S1]–[S9]) are secondary, used for menu paths and anything not captured yet (site audit categories).

No IPs, MACs, serials, tokens or webhook URLs in this file. Placeholders: `WAZUH_MANAGER_IP`, `OMADA_CONTROLLER_IP`.

---

## Sources

Official TP-Link / Omada:

- **[S1]** How to Configure Email Notification and Remote Logging on Omada Controller (rev. 10-20-2026): <https://support.omadanetworks.com/us/document/13012/>
- **[S2]** Omada Controller User Guide V6.0: <https://support.omadanetworks.com/en/document/111217/> (sections "Monitor the Network with Logs", "Configure Alert/Event Notifications", "Configure Audit Log Notifications", "Configure Remote Logging", "Webhooks", "History Data Retention")
- **[S3]** How to Configure Webhook on Omada Controller: <https://support.omadanetworks.com/en/document/53570/>
- **[S4]** Omada Open API docs and the embedded *Open API Access Guide*: <https://use1-omada-northbound.tplinkcloud.com/doc.html> (machine-readable: <https://use1-omada-northbound.tplinkcloud.com/v3/api-docs>). Appendix §5.2 Audit Log, §5.3.1 Webhook Message Template, §5.6.1 Log Notification Key, §5.7 Insight.
- **[S5]** How to Troubleshoot Wi-Fi Connection Failures on Omada EAP: <https://support.omadanetworks.com/us/document/13171/>
- **[S6]** How to Export System Logs from Omada Devices: <https://support.omadanetworks.com/us/document/135217/>
- **[S7]** How to Create Site in Omada Controller via Open API (Open API app setup): <https://support.omadanetworks.com/en/document/109315/>
- **[S8]** Interference Detection on Omada Controller: <https://support.omadanetworks.com/us/document/109958/>
- **[S9]** Older revision of [S1] as indexed at <https://www.tp-link.com/us/document/13012/>: "For system logs, Omada Controller will send the logs to the log server in real-time. For client logs, Omada Controller will send them every two minutes." The current revision no longer says this.

Live controller evidence:

- **[L1]** Global View notification-settings JSON from Jacob's controller, 2026-11-18 (`errorCode 0`): 2 alerts and 17 events; `webhookSetting.webhookEnable=false`; no syslog field. The raw JSON stays out of the repo. Type list: [omada-log-inventory/global.md](omada-log-inventory/global.md).
- **[L2]** Jacob's screenshots of Global View > Logs > Setting, 2026-11-18. **Advanced:** Remote Logging enabled, sending to the Wazuh manager (CT100) on UDP 514. **Audit Logs:** webhook off, 16 categories listed ([omada-log-inventory/audit-categories.md](omada-log-inventory/audit-categories.md)). The controller display name is two words, `Omada Network_<suffix>`.
- **[L3]** Site-level notification-settings JSON from Jacob's controller, 2026-11-18 (`errorCode 0`): 82 alerts and 80 events (158 unique keys; 4 in both lists). The raw JSON stays out of the repo. Type list and meanings: [omada-log-inventory/site.md](omada-log-inventory/site.md).

Community, not official (used only where marked):

- **[C1]** Client events off by default; enabled under Site > Logs > Notifications > Event > Client; a reboot was needed: <https://community.tp-link.com/en/business/forum/topic/747980>
- **[C2]** Syslog facility per log tab on controller 4.2.4 (Device local0, Client local1, Operation local2, System local3): <https://community.tp-link.com/en/business/forum/topic/239930>
- **[C3]** TP-Link staff: AP channel changes show in the Logs page when that log type is enabled: <https://community.tp-link.com/en/business/forum/topic/841552>

Repo evidence: [`omada_controller_samples.log`](../configs/wazuh/tests/omada_controller_samples.log) (real lines, placeholders swapped in) and [wazuh-omada-syslog.md](wazuh-omada-syslog.md).

---

## How Omada classifies logs

**Evidence:**

- Logs exist at two hierarchies, **Controller** (Global) and **Site**. Only Main Administrators see controller-level logs. [S2]
- Each log type can be classified as **Alert** or **Event**, with severities Critical, Error, Warning, Info, and content types Operation, System, Device, Client. [S2]
- **Audit Logs** record which account did what, and when. [S2][S6]
- The complete list of alert/event types is the *Log Notification Key* table in the Open API Access Guide, split into MSP, Global and Site levels, with Pro and Non-Pro support columns. [S4 §5.6.1] Audit logs are grouped into categories instead of types. [S4 §5.2]
- Every log row the API returns has a `key` (the Log Notification Key), `module` and `content`. [S4, `GET /openapi/v1/{omadacId}/sites/{siteId}/logs/events`]

**Inference:** the API `content` text of an event is probably the same text the controller sends over syslog. Both use `[client:<name>:<MAC>]` / `[ap:<name>:<MAC>]` tags, and the collector's disconnect parser relies on that. Check it by comparing one Events-page entry with the same line in `archives.log`.

---

## The two separate log configurations

**Evidence [S1]:** Remote logging is configured twice, at two levels:

| Level | Menu path (confirmed in [S1]) | What it carries |
|---|---|---|
| **Global** | **Global View > Logs > Setting** > **Advanced** (log server; click **Apply**), then **Alerts**, **Events**, **Audit Logs** tabs (tick what to send; click **Save**) | "global related alerts and events": controller-level types (table A) and global audit categories |
| **Site** | **(your site) > Logs > Setting** > **Advanced** (log server; click **Apply**), then **Alerts**, **Events**, **Audit Logs** tabs (click **Save**) | "site related alerts and events": site-level types (table B) and site audit categories |

- [S2] confirms the site path ("Go to Logs, click the Setting icon in the upper right, then go to the Advanced page") and the fields **Syslog Server IP/Hostname**, **Syslog Server Port** and **More Detail Logs** ("the logs of AP clients and switch system will be sent to the Syslog Server").
- The Open API has a separate endpoint for each level: `GET /openapi/v1/{omadacId}/global/controller/setting/syslog` (enable, host, port) and `GET /openapi/v1/{omadacId}/sites/{siteId}/remote-logging` (enable, host, port, `moreClientLog`). [S4]

**What the repo shows (evidence):** every real controller line in the samples starts `Omada Network_<placeholder> - - -`. On 2026-11-18 Jacob's controller **display name** turned out to be `Omada Network_<suffix>` [L2]. So that header field is the **controller name, not the site name**, and the header can't tell a global line from a site line. The audit entries that did arrive are an admin login (probably the global *Account*/*User Activity* category; inference) and "Log Notifications of Site configured successfully" (site). No sample has a Device-module type (device connected/disconnected, channel change, radar), apart from the gateway rogue DHCP line.

**Inference (verify with the checklist):**

1. **Corrected 2026-11-18.** The earlier inference that the Oct 7 setup configured only the Site level was **wrong**. Global remote logging is on, pointing at the Wazuh manager on port 514, and all 16 global audit categories are ticked [L2]. No clearly global alert/event line (backup failed, node, cloud access) has shown up yet. Possible reasons, none confirmed: (a) none of those rare events has happened; (b) global lines use a header the parent decoder doesn't match; (c) they arrive but aren't decoded or alerted. The old parent decoder **does** match Jacob's two-word name (box logtest), so a space in the name alone doesn't explain it. It would only fail for names of 3+ words, which the 2026-11 decoder now handles. To confirm: `logall` on CT 100 plus `archives.log` (INSTALL-STEPS step 9b).
2. Site **audit** logs *do* reach Wazuh. Site **alerts** do too, at least the rogue DHCP alert on 2026-10-31. So "alerts and audit never reached Wazuh" is only true for the **Global** level.
3. The missing **Device** events (AP up/down, channel change, radar) are more likely switched off in the site's Events/Alerts tabs than lost to a wrong level. That also fits the open item "controller Events log looks empty" in wazuh-omada-syslog.md.

---

## Export paths per type

Footnotes for the tables:

- **¹ Syslog:** the notification settings have no syslog field [L1], so this column is inferred: yes, but only when the type is ticked under **Alerts** or **Events** at *its own level* and remote logging is on at that level. [S1] Per-type behaviour is inferred from [S1]'s procedure, because TP-Link doesn't publish a per-type syslog matrix. `omada-log-inventory.py` prints the live state.
- **Webhook (site):** each site type has a **Webhook Notification** checkbox, and the site needs a webhook selected. [S2][S3] Caveat: the Open API describes the per-type `webhook` flag as "applies to the Omada Pro Controller only". [S4, `LogNotificationOpenApiVO`] Check that the checkbox shows on the software controller.
- **Webhook (global):** Jacob's controller returns per-type `webhook` flags and a global master switch (`webhookSetting.webhookEnable`, currently **false**) [L1]. The global webhook option therefore exists on this software controller. Whether it actually delivers on a non-Pro controller is unconfirmed: the API calls the per-type flag Pro-only [S4]. A type is only sent by webhook when its flag **and** the master switch are both on. The master switch is off here.
- **Sample:** "real" means a real line is in the repo samples. "Guessed" means the Wazuh rule keys on loose wording and needs a real line.

### A. Global level (Global View > Logs > Setting): 19 types

Key list from the live capture [L1]; full dictionary with notes: [omada-log-inventory/global.md](omada-log-inventory/global.md). This table only adds the HNS Wazuh mapping.

| Kind | Key | shortMsg (live) | Module | Alert level | Syslog | Wazuh rule (level) | Sample |
|---|---|---|---|---|---|---|---|
| alert | `PRIMARY_SECOND_SWITCHING` | Primary-Second Switching | System | Warning | yes¹ | 100631 (8) | guessed |
| alert | `NODE_DISCONNECT` | Node was disconnected | System | Warning | yes¹ | 100630 (10) | guessed |
| event | `AUTO_BK_OK` | Backup Schedule Executed | System | — | yes¹ | 100619 (5) catch-all | none |
| event | `AUTO_BK_FL` | Backup Schedule Failed | System | — | yes¹ | 100632 (7) | guessed |
| event | `EMAIL_LIMIT_REACHED` | Email Limit Reached | System | — | yes¹ | 100619 (5) catch-all | none |
| event | `MNG_PORT_C` | Controller Access Port Changed | System | — | yes¹ | 100619 (5) catch-all | none |
| event | `PRT_PORT_C` | Portal Port Changed | System | — | yes¹ | 100619 (5) catch-all | none |
| event | `DEVICE_LIST_MAIL_FL` | Device List Schedule Mail Failed | System | — | yes¹ | 100632 (7) | guessed |
| event | `DEVICE_LIST_SCHEDULE_EXECUTED` | Device List Schedule Executed | System | — | yes¹ | 100619 (5) catch-all | none |
| event | `GLOBAL_LOG_MAIL_OK` | Global Logs Mailed Automatically | System | — | yes¹ | 100619 (5) catch-all | none |
| event | `GLOBAL_LOG_MAIL_FL` | Automatic Global Logs Mail Failed | System | — | yes¹ | 100632 (7) | guessed |
| event | `GLOBAL_LOG_SRV_OK` | Global Logs Sent to Log Server | System | — | yes¹ | 100619 (5) catch-all | none |
| event | `GLOBAL_LOG_SRV_FL` | Sending Global Logs to Log Server Failed | System | — | yes¹ | 100632 (7) | guessed |
| event | `CONNECTED_CLOUD_ACCESS_SUCCESS` | Cloud Access Success | System | — | yes¹ | 100619 (5) catch-all | none |
| event | `CLOUD_ACCESS_CONNECTION_FAILED` | Network Disconnection | System | — | yes¹ | 100645 (7) | guessed |
| event | `CLOSE_CLOUD_ACCESS_SUCCESS` | Cloud Access Closed | System | — | yes¹ | 100619 (5) catch-all | none |
| event | `DEV_DISCOVER` | Device Discovered | Device | — | yes¹ | 100619 (5) catch-all | none |
| event | `NODE_CONNECT` | Node was connected | System | — | yes¹ | 100619 (5) catch-all | none |
| event | `ANOMALY_EVENT_FULL` | Too Many Incidents | System | — | yes¹ | 100646 (8) | guessed |

`DEV_DISCOVER` covers device types olt, gateway, ap and switch (live `deviceTypes`).

**Listed in the API guide but not present on this controller** (§5.6.1 [S4] versus [L1]): `LOGIN_OK` (User Logged In), `LOGIN_FL` (User Login Failed), `HS_LOGIN_OK` (Hotspot Operator Logged In), `HS_LOGIN_FL` (Hotspot Operator Login Failed), `SITE_ADD` (Site Created), `SITE_MIGR` (Site Migrated), `RO_O_SS` (Running Out Of Storage Space). The guide's two hardware-controller-only types (`NETWORK_CHECK_MAIL_FL`, `LOG_FULL`) are also absent, as expected.

**Inference, not confirmed:** controller login activity is now recorded only in the **Global Audit Logs** (categories `ACCOUNT` / `USER_ACTIVITY`, table C), not as alert/event types. So login monitoring in Wazuh depends on the Global Audit Logs reaching syslog (rules 100648/100649). No source says this outright. Check it with one wrong-password login (checklist step 14). I found no replacement for the storage warning.

**Top-level fields in [L1]:** `webhookSetting.webhookEnable = false` (the global webhook master switch is **off**, so no global type is sent by webhook). **The JSON has no syslog field anywhere.** This endpoint controls email and webhook only. Syslog export is set separately by the global remote log server (`GET /openapi/v1/{omadacId}/global/controller/setting/syslog` [S4]). **That is confirmed on**: Remote Logging is enabled to the Wazuh manager (CT100), port 514 [L2]. So every global type that's enabled should go out over syslog when it happens. None has been seen in Wazuh yet (see the corrected inference under *The two separate log configurations*).

### B. Site level (Site > Logs > Setting): 82 alerts + 80 events, 158 unique keys

Key list from the live capture [L3]; full dictionary with meanings: [omada-log-inventory/site.md](omada-log-inventory/site.md). ⇄ = the key is in both the alert and the event list (`DEV_DISCONN`, `AP_ISOLATE`, `DEV_C_DSYNC`, `LOG_ONU_IS_OFFLINE`), so it appears twice below. Rows for keys TP-Link's guide lists but this controller lacks were removed. Those 38 keys (31 Operation types such as `DEV_ADOPT_OK`, plus `OSG_WAN_UP`, `DEV_READOPT_OK` and others) are listed in the dictionary's `meta.counts`.

| Kind | Key | shortMsg (live) | Module | Alert level | Syslog | Wazuh rule (level) | Sample |
|---|---|---|---|---|---|---|---|
| alert | `OSW_DET_STORM` | Switch Detected Storm | Device | Warning | yes¹ | 100634 (6) | guessed |
| alert | `OSW_DET_LOOP` | Detected Loops | Device | Warning | yes¹ | 100634 (6) | guessed |
| alert | `OSW_PB` | Port Blocked | Device | Warning | yes¹ | 100634 (6) | guessed |
| alert | `OSW_TOPO_C` | STP Topology Changed | Device | Information | yes¹ | 100619 (5) catch-all | none |
| alert | `OSG_WAN_DOWN` | WAN is down | Device | Warning | yes¹ | 100633 (6) | guessed |
| alert | `WAN_LINK_BACKUP` | WAN Link Backup | Device | Information | yes¹ | 100619 (5) catch-all | none |
| alert | `WAN_ONLINE_DETECTION` | WAN Online Detection | Device | Information | yes¹ | 100619 (5) catch-all | none |
| alert | `PHYSICAL_PORT_CONNECTION` | Physical Port Connection | Device | Information | yes¹ | 100619 (5) catch-all | none |
| alert | `OSG_PPPOE_FL` | PPPoE Connection Failed | Device | Error | yes¹ | 100619 (5) catch-all | none |
| alert | `WAN_IP_O_F` | WAN IP address Obtaining Failed | Device | Error | yes¹ | 100619 (5) catch-all | none |
| alert | `OSG_IPSEC_FL` | IPsec Connection Disconnected | Device | Warning | yes¹ | 100633 (6) | guessed |
| alert | `OSG_C_VPN_FL` | PPTP/L2TP Client Connection Failed | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `ADOPTED_ACCOUNT_DELETED` | OLT Adopted Account Deleted | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `PASSWORD_CHANGE_OF_ADOPTED_ACCOUNT` | OLT Adopted Account Password Changed | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `LEVEL_CHANGE_OF_ADOPTED_ACCOUNT` | OLT Adopted Account Level Changed | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `LOG_ONU_IS_OFFLINE` ⇄ | ONU Disconnected | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `LOG_ONU_LOSS_OF_SIGNAL` | ONU Loss of Signal | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `LOG_ONU_LOSS_OF_FRAME` | ONU Loss of Frames | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `LOG_ONU_LOSS_OF_PLOAM` | ONU Loss of PLOAM | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `LOG_ONU_SIGNAL_FAILED` | ONU Signal Transmission Failed | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `LOG_ONU_STARTUP_FAILED` | ONU Startup Failed | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `LOG_ONU_DYING_GASP` | ONU Dying Gasp | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `DST_C_FAIL` | DST configuration error. | System | Error | yes¹ | 100619 (5) catch-all | none |
| alert | `DEV_DISCONN` ⇄ | Device Disconnected | Device | Error | yes¹ | 100620 (8), 100641 (10) | guessed |
| alert | `AP_ISOLATE` ⇄ | EAP Isolated | Device | Error | yes¹ | 100621 (8) | guessed |
| alert | `DEV_C_DSYNC` ⇄ | Device Configurations Desynchronized | Device | Error | yes¹ | 100619 (5) catch-all | none |
| alert | `OSG_ATK` | Gateway Detected Attack | Device | Warning | yes¹ | 100626 (10) | guessed |
| alert | `OSG_SF_ATK` | Gateway Detected Stationary Flood Attack | Device | Warning | yes¹ | 100626 (10) | guessed |
| alert | `OSG_ARP_ATK` | Gateway Detected ARP Conflicts | Device | Warning | yes¹ | 100626 (10) | guessed |
| alert | `OSG_LARGE_PING_ATTACK` | Large Ping Attack | Device | Warning | yes¹ | 100626 (10) | guessed |
| alert | `OSG_DHCP_LEASE_POOL_EXHAUSTED` | The DHCP lease pool is exhausted | Device | Warning | yes¹ | 100628 (8) | guessed |
| alert | `OSG_ROGUE_DHCP_SERVER_DETECTED` | A rogue DHCP server is detected | Device | Warning | yes¹ | 100625 (10) | real (repo samples, line 19) |
| alert | `OSG_IP_CONFLICT_DETECTED` | An IP conflict is detected | Device | Warning | yes¹ | 100628 (8) | guessed |
| alert | `MANAGE_INTERFACE_CHANGED` | OLT Manage Interface Changed | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `LOG_CPU_LOAD_EXCEED` | OLT CPU Load Exceed | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `LOG_MEM_LOAD_EXCEED` | OLT Memory Load Exceed | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `LOG_ONU_SIGNAL_DEGRADE` | ONU Signal Degrade | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `LOG_ONU_PHYSICAL_EQUIP_ERR_RECEIVED` | ONU Fault PLOAM Received | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `LOG_ONU_PST_PLOAM_RECEIVED` | ONU PST PLOAM Received | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `LOG_ONU_UNKNOWN_PLOAM_RECEIVED` | ONU Unknown PLOAM Received | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `LOG_ONU_TRANSMISSION_INTERFERENCE_THRESHOLD` | ONU TIW Exceed | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `LOG_ONT_REMOTE_ERROR_INDICATION` | ONU Error Reported(Downstream) | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `LOG_ONT_ONU_ERROR_INDICATION` | ONU Error Reported(Upstream) | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `LOG_SERVICE_PROFILE_CAPABILITY_MATCH_FAILED` | ONU Capability Failed to Match Profile | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `LOG_PORT_INGRESS_REACH` | OLT Limitation of ingress bandwidth | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `LOG_PORT_EGRESS_REACH` | OLT Limitation of egress bandwidth | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `LOG_BCSTORM_CONTROL_REACH` | OLT Broadcast Storm | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `LOG_MCSTORM_CONTROL_REACH` | OLT Multicast Storm | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `LOG_UNKSTORM_CONTROL_REACH` | OLT Unicast Storm | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `LOG_PORT_STORM_CONTROL_SHUTDOWN` | OLT Port Shutdown (Storm Control) | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `AUTO_ADD_MAC_FILTER_FL` | Automatic Add MAC Filtering Allow List Failed | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `REBOOT_RECOVERY` | IntelliRecover - Reboot Recovery Initiated | System | Information | yes¹ | 100619 (5) catch-all | none |
| alert | `REBOOT_RECOVERY_FAIL` | IntelliRecover - Reboot Recovery Failed | System | Error | yes¹ | 100619 (5) catch-all | none |
| alert | `REBOOT_RECOVERY_EXCEED_LIMIT` | IntelliRecover - Retry Limit Exceeded | System | Error | yes¹ | 100619 (5) catch-all | none |
| alert | `DEVICE_MONITOR_STATUS_LINK_DOWN` | Device informed monitor link down | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `DEVICE_MONITOR_STATUS_LINK_ERROR` | Device informed monitor link error | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `DEVICE_MONITOR_STATUS_DEVICE_ERROR` | Device informed monitor link internal error | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `LAN_CONFLICT_AVOIDANCE` | Gateway’s LAN segment is modified | System | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `REPORT_SCHEDULE_REACH_RATE_LIMIT` | Report export Schedule Failure | System | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `MDNS_RULE_NOT_EFFECT` | The mDNS rules are not working | System | Error | yes¹ | 100619 (5) catch-all | none |
| alert | `REPLACE_FAILED` | Replace action failed | Device | Error | yes¹ | 100619 (5) catch-all | none |
| alert | `OSW_STORM_SHUTDOWN` | Switch Storm Shutdown | Device | Warning | yes¹ | 100634 (6) | guessed |
| alert | `OSW_QOS_VLAN_EXCEED` | Switch Qos for Vlan Rule Exceeded | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `OSW_QOS_RULE_EXCEED` | Switch Qos Rule Exceeded | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `OSW_PWR_ERR` | Switch Redundant Power Supply Failure | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `OSW_FAN_ERR` | Switch Fan Failure | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `OSW_KEY_HEALING_MGMTVLAN_DNSV4_CLEAR_FAILED` | Mgmt Vlan DnsV4 Cleared Failed Alert. | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `OSW_KEY_HEALING_MGMTVLAN_DNSV6_CLEAR_FAILED` | Mgmt Vlan DnsV6 Cleared Failed Alert. | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `OSW_KEY_HEALING_MGMTVLAN_CREATE_FAILED` | Mgmt Vlan Create Failed Alert. | Device | Critial | yes¹ | 100619 (5) catch-all | none |
| alert | `OSW_KEY_HEALING_MGMTVLAN_CFG_FAILED` | Mgmt Vlan Configured Failed Alert. | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `OSW_KEY_HEALING_SYSTEMIP_CFG_FAILED` | System Ip Configured Failed Alert. | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `OSW_KEY_HEALING_MGMTVLAN_SET_FAILED` | Mgmt Vlan Set Failed Alert. | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `OSW_DHCP_SNOOP_ALERT` | Dhcp snoop alert | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `OSW_ARP_DETECTION_ALERT` | Arp detection alert | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `OSW_INTERFACE_VLANIF_DOWN` | Switch VLAN interface Down Event | Device | Information | yes¹ | 100619 (5) catch-all | none |
| alert | `OSW_KEY_HEALING_INTF_RECOVER_FAILED` | Netif Healing Recover Failed Alert. | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `OSW_KEY_HEALING_GATE_RECOVER_FAILED` | Netif Healing Gate Recover Failed Alert. | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `OSW_OUI_BASED_VLAN_NUM_LIMIT_EXCEED` | Switch OUI Based VLAN rules exceeded the maximum simultaneous entry limit | Device | Information | yes¹ | 100619 (5) catch-all | none |
| alert | `OSW_INSTALL_ROLLBACK` | Failed To Upgrade | Device | Warning | yes¹ | 100619 (5) catch-all | none |
| alert | `OSG_OVPN_OP_ERR` | OpenVPN Operation Failed | Device | Error | yes¹ | 100619 (5) catch-all | none |
| alert | `OSG_LAN_IP_CONFLICT` | LAN IP Is Conflict With Other Interfaces | Device | Warning | yes¹ | 100628 (8) | guessed |
| alert | `WAN_IP_OBTAIN` | WAN IP address Obtaining | Device | Error | yes¹ | 100619 (5) catch-all | none |
| event | `DEV_IP_C` | Device IP Changed | Device | — | yes¹ | 100619 (5) catch-all | none |
| event | `AP_RADAR` | EAP Detected Radar | Device | — | yes¹ | 100624 (6) | guessed |
| event | `AP_CH_C` | EAP Channel Changed | Device | — | yes¹ | 100623 (5), 100638 (8) | guessed |
| event | `AP_C_FL` | Client Connection Failed (Wireless) | Client | — | yes¹ | 100629 (4), 100639 (7) | guessed |
| event | `OSW_C_1X_OK` | Client Authenticated with 802.1X | Client | — | yes¹ | 100619 (5) catch-all | none |
| event | `OSW_C_1X_FL` | 802.1X Authentication Failed | Client | — | yes¹ | 100619 (5) catch-all | none |
| event | `OSG_BK_WAN_UP` | Backup WAN Takes Effect | Device | — | yes¹ | 100619 (5) catch-all | none |
| event | `OSG_IPSEC_FO` | IPsec failover took effect | Device | — | yes¹ | 100619 (5) catch-all | none |
| event | `OSG_RC_VPN_OK` | Remote PPTP/L2TP Client Connected | Device | — | yes¹ | 100619 (5) catch-all | none |
| event | `OSG_RC_VPN_FL` | Remote PPTP/L2TP Client Connection Failed | Device | — | yes¹ | 100619 (5) catch-all | none |
| event | `OSG_RC_VPN_LO` | Remote PPTP/L2TP Client Logged Out | Device | — | yes¹ | 100619 (5) catch-all | none |
| event | `OSG_DDNS` | Gateway DDNS Module Information | Device | — | yes¹ | 100619 (5) catch-all | none |
| event | `OSG_IPSEC` | Gateway IPsec Module Information | Device | — | yes¹ | 100619 (5) catch-all | none |
| event | `OSG_IPV6` | Gateway IPv6 Module Information | Device | — | yes¹ | 100619 (5) catch-all | none |
| event | `OSG_PPP` | Gateway PPP Module Information | Device | — | yes¹ | 100619 (5) catch-all | none |
| event | `OSG_PPPOE` | Gateway PPPoE Module Information | Device | — | yes¹ | 100619 (5) catch-all | none |
| event | `OSG_SSL_VPN` | Gateway SSL VPN Module Information | Device | — | yes¹ | 100619 (5) catch-all | none |
| event | `OSG_DHCP_C` | Gateway DHCP Client Module Information | Device | — | yes¹ | 100619 (5) catch-all | none |
| event | `OSG_DHCP_S` | Gateway DHCP Server Module Information | Device | — | yes¹ | 100604 (0), 100608 (5) | real, mapping inferred ("DHCP Server allocated/rejected" lines) |
| event | `LOG_TRAFFIC_CLEAR` | OLT Traffic Cleared | Device | — | yes¹ | 100619 (5) catch-all | none |
| event | `LOG_SRV_OK` | Site Logs Sent to Log Server | System | — | yes¹ | 100619 (5) catch-all | none |
| event | `LOG_SRV_FL` | Sending Site Logs to Log Server Failed | System | — | yes¹ | 100632 (7) | guessed |
| event | `LOG_MAIL_OK` | Logs Mailed Automatically | System | — | yes¹ | 100619 (5) catch-all | none |
| event | `LOG_MAIL_FL` | Automatic Logs Mail Failed | System | — | yes¹ | 100619 (5) catch-all | none |
| event | `REBOOT_SC_OK` | Reboot Schedule Executed | System | — | yes¹ | 100619 (5) catch-all | none |
| event | `REBOOT_SC_FL` | Reboot Schedule Execution Failed | System | — | yes¹ | 100619 (5) catch-all | none |
| event | `POE_SC_OK` | PoE Schedule Executed | System | — | yes¹ | 100619 (5) catch-all | none |
| event | `POE_SC_FL` | PoE Schedule Execution Failed | System | — | yes¹ | 100619 (5) catch-all | none |
| event | `REPORT_SENDING_FAILED` | Report Sending Failed | System | — | yes¹ | 100619 (5) catch-all | none |
| event | `REPORT_SCHEDULE_EXECUTED` | Report Schedule Executed | System | — | yes¹ | 100619 (5) catch-all | none |
| event | `REPORT_GENERATION_FAILED` | Report Generation Failed | System | — | yes¹ | 100619 (5) catch-all | none |
| event | `SITE_DEVICE_LIST_MAIL_FL` | Site Device List Schedule Mail Failed | System | — | yes¹ | 100619 (5) catch-all | none |
| event | `SITE_DEVICE_LIST_SCHEDULE_EXECUTED` | Site Device List Schedule Executed | System | — | yes¹ | 100619 (5) catch-all | none |
| event | `INCIDENT_MAILED_FAILED` | Incidents auto mailed failed | System | — | yes¹ | 100619 (5) catch-all | none |
| event | `PORT_SC_OK` | Port Schedule Executed | System | — | yes¹ | 100619 (5) catch-all | none |
| event | `PORT_SC_FL` | Port Schedule Execution Failed | System | — | yes¹ | 100619 (5) catch-all | none |
| event | `SITE_NETWORK_CHECK_MAIL_FL` | Site Network check Mail Failed | System | — | yes¹ | 100619 (5) catch-all | none |
| event | `TERMINAL_MAIL_FL` | Site Terminal Mail Failed | System | — | yes¹ | 100619 (5) catch-all | none |
| event | `DEV_CONN` | Device Connected | Device | — | yes¹ | 100622 (3) | guessed |
| event | `DEV_RECONN` | Device Reconnected | Device | — | yes¹ | 100622 (3) | guessed |
| event | `DEV_DISCONN` ⇄ | Device Disconnected | Device | — | yes¹ | 100620 (8), 100641 (10) | guessed |
| event | `LOG_ONU_IS_ONLINE` | ONU Connected | Device | — | yes¹ | 100619 (5) catch-all | none |
| event | `LOG_ONU_IS_OFFLINE` ⇄ | ONU Disconnected | Device | — | yes¹ | 100619 (5) catch-all | none |
| event | `AP_ISOLATE` ⇄ | EAP Isolated | Device | — | yes¹ | 100621 (8) | guessed |
| event | `DEV_C_DSYNC` ⇄ | Device Configurations Desynchronized | Device | — | yes¹ | 100619 (5) catch-all | none |
| event | `DEV_READOPT_FL` | Automatic Device Readopt Failed | Device | — | yes¹ | 100619 (5) catch-all | none |
| event | `W_C_ROAM` | Client Roaming (Wireless) | Client | — | yes¹ | 100601 (3), 100607 (0), 100606 (5) | real (repo samples) |
| event | `W_C_DISCONN` | Client Offline (Wireless) | Client | — | yes¹ | 100603 (3), 100635 (4), 100636 (8), 100637 (10) | real (repo samples) |
| event | `AP_C_OK` | Client Online (Wireless) | Client | — | yes¹ | 100602 (3) | real (repo samples) |
| event | `L_C_DISCONN` | Client Offline (Wired) | Client | — | yes¹ | 100619 (5) catch-all | none |
| event | `L_C_CONN` | Client Online (Wired) | Client | — | yes¹ | 100619 (5) catch-all | none |
| event | `W_C_PRT_OK` | Client Authenticated with Portal (Wireless) | Client | — | yes¹ | 100619 (5) catch-all | none |
| event | `W_C_PRT_FL` | Portal Authentication Failed (Wireless) | Client | — | yes¹ | 100619 (5) catch-all | none |
| event | `W_C_PRT_EXP` | Client Authentication Expired (Wireless) | Client | — | yes¹ | 100619 (5) catch-all | none |
| event | `L_C_PTR_OK` | Client Authenticated with Portal (Wired) | Client | — | yes¹ | 100619 (5) catch-all | none |
| event | `L_C_PTR_FL` | Portal Authentication Failed (Wired) | Client | — | yes¹ | 100619 (5) catch-all | none |
| event | `L_C_AUTH_EXP` | Client Authenticated Expired (Wired) | Client | — | yes¹ | 100619 (5) catch-all | none |
| event | `C_AUTH_OPT` | Client Authorized/Unauthorized by Admin | Client | — | yes¹ | 100619 (5) catch-all | none |
| event | `C_PRT_EXT` | Client Authentication Extended by Admin | Client | — | yes¹ | 100619 (5) catch-all | none |
| event | `DEV_CONN_REMEMBER` | Remembered Device Readopted After Factory Reset | Device | — | yes¹ | 100622 (3) | guessed |
| event | `REBOOT_RECOVERY_SUCCESS` | IntelliRecover - Device Back Online | System | — | yes¹ | 100619 (5) catch-all | none |
| event | `NAT_TRAVERSAL_CLOSED` | NAT Traversal Tunnel Closed | System | — | yes¹ | 100619 (5) catch-all | none |
| event | `REPLACE_SUCCEED` | Replace action succeed | Device | — | yes¹ | 100619 (5) catch-all | none |
| event | `OSW_LOOP_C` | Loop Cleared | Device | — | yes¹ | 100619 (5) catch-all | none |
| event | `OSW_DEPEND_INFO` | Ecs Info | Device | — | yes¹ | 100619 (5) catch-all | none |
| event | `OSW_STP_FWD` | STP Topology Changed | Device | — | yes¹ | 100619 (5) catch-all | none |
| event | `OSW_STP_BLOCK` | STP Port Blocked | Device | — | yes¹ | 100634 (6) | guessed |
| event | `OSW_VLAN_8021Q_CFG_FAIL` | VLAN Configuration Fail | Device | — | yes¹ | 100619 (5) catch-all | none |
| event | `OSW_LAG_PORT_UP` | LAG Member Port Up Event | Device | — | yes¹ | 100619 (5) catch-all | none |
| event | `OSW_LAG_PORT_DOWN` | LAG Member Port Down Event | Device | — | yes¹ | 100619 (5) catch-all | none |
| event | `OSW_KEY_HEALING_INTF_CHECK_FAILED` | Netif Healing Check Failed Alert. | Device | — | yes¹ | 100619 (5) catch-all | none |
| event | `OSW_KEY_HEALING_INTF_RECOVER_NOT_EXEC` | Netif Healing Not Exec Failed Alert. | Device | — | yes¹ | 100619 (5) catch-all | none |
| event | `OSW_OUI_BASED_VLAN_EFFECT` | Switch OUI Based VLAN rule applied | Device | — | yes¹ | 100619 (5) catch-all | none |
| event | `OSW_INSTALL_REBOOT` | Device Automatically Rebooted | Device | — | yes¹ | 100619 (5) catch-all | none |
| event | `OSW_INSTALL_ROLLBACK_FAILED` | Failed To Rollback | Device | — | yes¹ | 100619 (5) catch-all | none |
| event | `OSG_PRI_WAN_UP` | Primary WAN Takes Effect | Device | — | yes¹ | 100619 (5) catch-all | none |
| event | `OSG_NHRP` | Gateway SDWAN Module Information | Device | — | yes¹ | 100619 (5) catch-all | none |
| event | `OSG_OPENVPN` | Gateway OpenVPN Module Information | Device | — | yes¹ | 100619 (5) catch-all | none |
| event | `OSG_MAPE` | Gateway MAP-E Module Information | Device | — | yes¹ | 100619 (5) catch-all | none |
| event | `OSG_DSLITE` | Gateway DS-Lite Module Information | Device | — | yes¹ | 100619 (5) catch-all | none |

### C. Audit log categories (Logs > Setting > Audit Logs) [S4 §5.2]

| Level | Categories | Syslog | Webhook | Wazuh |
|---|---|---|---|---|
| Global (16, captured [L2]) | Account, Backup, Cloud Access, Controller Settings, Data Export, **Firmware**, Log, Migration, Restore, **SD-WAN**, Site Management, **Site Template**, System Settings, User Activity, User Interface, Webhook. All ticked. Bold = not in the guide. The guide's `IPS` and `LICENSE` aren't on this controller | yes¹. Global remote logging is on [L2]; whether lines are seen in Wazuh is unconfirmed (may be among the samples, since the header doesn't show the level) | Audit webhook toggle **off** [L2] | 100605 (3), 100609, 100648 (8) and 100649 (10) for login failures (guessed wording), 100642 (6), 100643 (7), 100644 (5) |
| Site (23) | ABNORMAL, APPLICATION_CONTROL, AUTHENTICATION, CLI, CLIENTS, DASHBOARD, DEVICE_MANAGEMENT, HOTSPOT_MANAGER, INSIGHT, IPS, LOG, MAP, NETWORK_SECURITY, PROFILES, REPORT, SIM, SITE_SERVICES, SITE_SETTINGS, TOOLS, TRANSMISSION, VPN, WIRED_NETWORKS, WIRELESS_NETWORKS | yes, **seen** (JSON body lines in repo samples) | yes: Site > Logs > Setting > Audit Logs > enable Webhook, pick categories [S2] | same |

### D. Not exported by syslog or webhook (API polling only)

| Data | Why it matters here | How to get it | Source |
|---|---|---|---|
| Per-radio channel, width, Tx power, Tx/Rx/interference utilization | Direct evidence for channel crowding | `GET .../aps/{apMac}/radios` → `lab-status-collect.py` `omada.rf` | [S4] |
| Client RSSI, SNR, radio, channel | Weak signal versus crowding | `GET .../sites/{siteId}/clients` | [S4] |
| Client disconnect timeline | Per-client drop history | `GET .../clients/{clientMac}/client-timeline?type=3` (Disconnection) | [S4] |
| Insight incidents, e.g. 01009002 *High AP channel utilization*, 01009010 *AP wireless interference rate too high*, 01009009 *AP noise floor too high*, 01004002 *Client Ping-pong roaming*, 01003014 *Client failed to connect* | Omada's own crowding and roaming detectors | `GET .../anomaly/incidents`; no log key, so no syslog/webhook. Availability on a non-Pro controller is unconfirmed | [S4 §5.7] |
| Rogue AP scan results | Neighbouring APs on your channels | `GET .../insight/rogueaps`. **No log key** in §5.6.1. Enabling the scan disconnects clients during the scan [S9] | [S4], [S9] |
| Wireless IDS entries and dynamic block list | Deauth floods, spoofing | `GET .../insight/wids`, `.../insight/wids/blacklist`. **No log key** in §5.6.1. Blocked on EAP225 v4 anyway | [S4]; wazuh-omada-syslog.md |
| Interference Detection scan results | Channel occupancy per AP | `GET .../aps/{apMac}/full-channel-detect/channel-load` and `/wlan-interference` (a scan has to run first) | [S4], [S8] |

### Summary counts

| | Types | Syslog | Webhook | Neither (API only) | Seen in Wazuh today |
|---|---|---|---|---|---|
| Global alert/event | **19** (2 alerts, 17 events [L1]). Guide lists 24: 7 absent, 2 hardware-only, 4 extra here | 19 (global remote logging on [L2]) | 2 flagged, **0 effective** (master switch off) | 0 | 0 |
| Site alert/event | **158 unique keys** (82 alerts + 80 events, 4 in both [L3]). Guide lists 116: 38 absent here, 80 captured keys not in the guide | 158 (if the type is enabled and site remote logging is on) | 158 expose a per-type webhook flag (Pro-only caveat) | 0 | 5 (`AP_C_OK`, `W_C_DISCONN`, `W_C_ROAM`, `OSG_ROGUE_DHCP_SERVER_DETECTED`, DHCP lines likely `OSG_DHCP_S`) |
| Audit categories | 39 (16 global, live [L2], + 23 site, guide) | 39 (global: enabled and ticked [L2]; site: if enabled) | global webhook off [L2]; site per guide | 0 | site seen; global possibly (header can't tell) |
| RF/RSSI/Insight/Rogue AP/WIDS | 7 data sets (table D) | 0 | 0 | 7 | via collector once deployed |

**Key types missing today** (inferred from the samples; confirm with the checker): `DEV_DISCONN`/`DEV_CONN`, `AP_CH_C` (EAP Channel Changed), `AP_RADAR`, `AP_ISOLATE`, `AP_C_FL` (Client Connection Failed, Wireless), every global type (`NODE_DISCONNECT`, `PRIMARY_SECOND_SWITCHING`, `AUTO_BK_FL`, `CLOUD_ACCESS_CONNECTION_FAILED`, `ANOMALY_EVENT_FULL`), and global audit (where controller login failures now live; inferred).

**Deauth reason and RSSI:** none of the documented log types documents a deauth reason or RSSI field. The wireless offline line carries only connected time and traffic (real samples). The API's client history has undocumented `reason`/`reasonType` fields, and the client timeline has an `attributes` map. The collector forwards any rssi/signal/reason attributes it finds and labels them unconfirmed. The decoders also pick up `rssi`/`reason` if a future line contains them.

---

## Uncertain (check these yourself)

1. **Global per-type webhook** and **per-type webhook on a non-Pro controller.** [S2] and [S4] disagree. Look for a Webhook column in each Logs > Setting tab.
2. **Wording of the "guessed" types.** Rules 100620–100634, 100645, 100646 and 100648 key on loose words. Paste the first real line of each into `wazuh-logtest` and tighten the rule.
3. **Controller-level syslog header (partly resolved 2026-11-18).** The header field is the controller display name [L2]. Jacob's has two words (`Omada Network_<suffix>`), and the old parent decoder already handles that. The new parent accepts 1–6 words after `Omada` and was tested with a 4-word name (samples 57–59). **Still open:** whether *global* lines use the same header shape at all. Check `archives.log` with `logall` on. `NODE_*` and `PRIMARY_SECOND_SWITCHING` probably refer to controller cluster nodes (inference), so they may never fire on a single controller.
4. **Client log batching.** An older revision of [S1] says client logs go out every two minutes [S9]. Real-time here may mean up to about two minutes of lag for client events.
5. **Rogue AP / WIDS log keys.** None in §5.6.1. The 6.3 WIDS feature may have added keys after the guide was written. The checker's dump will show them if so.
6. **Reboot after enabling client events.** One user needed a controller restart [C1], which isn't official. Only restart CT 101's controller if new types don't show up within about 10 minutes.
7. **Viewer-role Open API app.** It may not be allowed to read global settings endpoints. The checker reports "unavailable" per call instead of failing.

---

## UI checklist (Jacob, in the Omada web UI)

Menu paths marked ✔ are confirmed in the cited doc. Paths marked ◐ are named in the doc, but the sub-tab names come from screenshots I couldn't read.

**Before you start:** on CT 100, `wazuh-remoted` already listens on UDP 514. `allowed-ips` already covers the management /24 that `OMADA_CONTROLLER_IP` sits in (wazuh-omada-syslog.md). Nothing to change in Wazuh for this checklist.

**Global level**

1. ✔ Log in as the Main Administrator, then **Global View > Logs > Setting**. [S1 step 6]
2. ✔ **Advanced**: **already done** (screenshot 2026-11-18 [L2]): Remote Logging is enabled to the Wazuh manager (CT100), port 514. Nothing to change.
3. ✔ **Alerts** and **Events** tabs: keep the types in table A that have a Wazuh rule switched on. *User Login Failed* and *Running Out Of Storage Space* don't exist on this controller. Syslog itself comes from step 2 [L1].
4. ✔ **Webhook:** the global master switch is **off** [L1], so no per-type webhook flag sends anything. **Leave it off** ([omada-webhook-evaluation.md](omada-webhook-evaluation.md)).
5. ✔ **Audit Logs** tab: **already done** [L2]. All 16 global categories are ticked, including **Account** and **User Activity**, where controller login monitoring now comes from (inference). The audit webhook toggle is off; leave it off.

**Site level** (repeat per site; there is one site today)

6. ✔ Open the site, then **Logs > Setting** (Setting icon, upper right). [S1 step 4; S2]
7. ✔ **Advanced**: confirm Remote Logging is on with Server = `WAZUH_MANAGER_IP`, Port = `514`. Turn on **More Detail Logs** (the AP client and switch logs). **Apply**. [S1 step 5; S2]
8. ✔ **Events > Client**: enable *Client Online (Wireless)*, *Client Offline (Wireless)*, *Client Roaming (Wireless)*, *Client Connection Failed (Wireless)*, *Client Online/Offline (Wired)*. **Save**. [S5; S2]
9. ✔ **Alerts / Events, Device types** (names from the live list [L3]): make sure these are on: *Device Disconnected*, *Device Connected*, *Device Reconnected*, *EAP Isolated*, *EAP Channel Changed*, *EAP Detected Radar*, *Device IP Changed*, *A rogue DHCP server is detected*, *An IP conflict is detected*, *The DHCP lease pool is exhausted*, *Gateway Detected Attack / Stationary Flood Attack / ARP Conflicts*, *Large Ping Attack*, *Switch Detected Storm*, *Detected Loops*, *Port Blocked*, *WAN is down*. **Save**.
10. ✔ **System types:** at least *Sending Site Logs to Log Server Failed*. This controller has no site *Operation* types; those actions show up as audit logs (inference). **Save**.
11. ✔ **Audit Logs** page: tick every site category (table C). **Save**. [S1 step 6; S2]
12. ✔ **Global View > Settings > History Data Retention**: make sure **Clients' History Data** / **Client History Retention** is on, so the API can serve client history to the collector. [S2; S5]

**Verify**

13. Run `omada-log-inventory.py` on .176 ([INSTALL-STEPS](omada-wazuh-realtime-INSTALL-STEPS.md) step 15) to check the site remote logging and per-type settings. Keep its output local: per-instance settings don't go in the repo. Global remote logging is already confirmed on [L2]. To contribute the still-missing site audit categories to the dictionary, follow [omada-log-inventory/README.md](omada-log-inventory/README.md#contribute-a-snapshot).
14. Trigger safe test events: log out and log in to the controller with a **wrong password once** (expect a Global audit line, rule 100648; if nothing arrives, the inference about the audit log is wrong); toggle Wi-Fi on a phone (online/offline); reboot one AP from the UI at a quiet time (device disconnect/connect, possibly a channel change). Then check `archives.log` on CT 100 for a controller-level header, and the Wazuh dashboard for `rule.groups: omada_realtime`.
15. If a type shows in the Omada Logs page but not in `archives.log` after about 10 minutes, see uncertainty 6.

*Optional webhook path:* see [omada-webhook-evaluation.md](omada-webhook-evaluation.md). It isn't needed for the steps above.
