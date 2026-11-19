# Omada alert/event dictionary: Global (controller) level

Types configured under **Global View > Logs > Setting > Alerts / Events**. They describe the controller itself (backups, cloud access, controller nodes, global log delivery), not your sites.

Captured 2026-11-18 from an Omada Software Controller (see [README.md](README.md#capture)). Columns are explained in [README.md](README.md#columns). Per-instance enable, email and webhook state is not recorded here.

**Differences from TP-Link's Open API guide (§5.6.1):**
- **In the guide but not on this controller:** `LOGIN_OK`, `LOGIN_FL`, `HS_LOGIN_OK`, `HS_LOGIN_FL`, `SITE_ADD`, `SITE_MIGR`, `RO_O_SS`, plus the hardware-controller-only `NETWORK_CHECK_MAIL_FL` and `LOG_FULL`. Controller logins seem to be recorded only in the global **Audit Logs** (Account / User Activity) on this version. That's an inference.
- **On this controller but not in the guide:** `PRIMARY_SECOND_SWITCHING`, `NODE_DISCONNECT`, `NODE_CONNECT`, `ANOMALY_EVENT_FULL`. The *node* types probably relate to controller clustering / primary-secondary controllers (inference).
- **Renamed:** `AUTO_BK_OK` is *Backup Schedule Executed* and `AUTO_BK_FL` is *Backup Schedule Failed* (the guide says *Auto Backup …*).

<!-- GENERATED:START (build-omada-dictionary.py) -->
**2 alerts + 17 events = 19 types.**

### Alerts

| # | Key | shortMsg (verbatim) | Kind | Module | Level | Device types | Client types | Webhook-capable | TP-Link guide | What it means / why you'd care |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `PRIMARY_SECOND_SWITCHING` | Primary-Second Switching | alert | System | Warning | — | — | yes | not listed |  |
| 2 | `NODE_DISCONNECT` | Node was disconnected | alert | System | Warning | — | — | yes | not listed |  |

### Events

| # | Key | shortMsg (verbatim) | Kind | Module | Device types | Client types | Webhook-capable | TP-Link guide | What it means / why you'd care |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `AUTO_BK_OK` | Backup Schedule Executed | event | System | — | — | yes | name differs: 'Auto Backup Executed' |  |
| 2 | `AUTO_BK_FL` | Backup Schedule Failed | event | System | — | — | yes | name differs: 'Auto Backup Failed' |  |
| 3 | `EMAIL_LIMIT_REACHED` | Email Limit Reached | event | System | — | — | yes | same name |  |
| 4 | `MNG_PORT_C` | Controller Access Port Changed | event | System | — | — | yes | same name |  |
| 5 | `PRT_PORT_C` | Portal Port Changed | event | System | — | — | yes | same name |  |
| 6 | `DEVICE_LIST_MAIL_FL` | Device List Schedule Mail Failed | event | System | — | — | yes | same name |  |
| 7 | `DEVICE_LIST_SCHEDULE_EXECUTED` | Device List Schedule Executed | event | System | — | — | yes | same name |  |
| 8 | `GLOBAL_LOG_MAIL_OK` | Global Logs Mailed Automatically | event | System | — | — | yes | same name |  |
| 9 | `GLOBAL_LOG_MAIL_FL` | Automatic Global Logs Mail Failed | event | System | — | — | yes | same name |  |
| 10 | `GLOBAL_LOG_SRV_OK` | Global Logs Sent to Log Server | event | System | — | — | yes | same name |  |
| 11 | `GLOBAL_LOG_SRV_FL` | Sending Global Logs to Log Server Failed | event | System | — | — | yes | same name |  |
| 12 | `CONNECTED_CLOUD_ACCESS_SUCCESS` | Cloud Access Success | event | System | — | — | yes | same name |  |
| 13 | `CLOUD_ACCESS_CONNECTION_FAILED` | Network Disconnection | event | System | — | — | yes | same name |  |
| 14 | `CLOSE_CLOUD_ACCESS_SUCCESS` | Cloud Access Closed | event | System | — | — | yes | same name |  |
| 15 | `DEV_DISCOVER` | Device Discovered | event | Device | olt, gateway, ap, switch | — | yes | same name |  |
| 16 | `NODE_CONNECT` | Node was connected | event | System | — | — | yes | not listed |  |
| 17 | `ANOMALY_EVENT_FULL` | Too Many Incidents | event | System | — | — | yes | not listed |  |
<!-- GENERATED:END -->
