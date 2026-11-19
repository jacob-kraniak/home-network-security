# Omada audit log categories

Audit logs record **who did what** on the controller (logins, configuration changes, backups). They're configured per level under **Logs > Setting > Audit Logs**: you tick categories, and there's an optional webhook toggle. Audit entries go out over the same remote syslog as alerts/events at that level. In syslog they appear as a JSON body, `{"details":{...},"operation":"..."}`.

## Global (controller) level: 16 categories, captured 2026-11-18

From the Global View > Logs > Setting > Audit Logs tab of an Omada Software Controller. UI names are verbatim. API keys come from TP-Link's Open API guide §5.2 where it lists them.

| # | Category (UI) | API key (guide §5.2) | In TP-Link guide? |
|---|---|---|---|
| 1 | Account | `ACCOUNT` | yes |
| 2 | Backup | `BACKUP` | yes |
| 3 | Cloud Access | `CLOUD_ACCESS` | yes |
| 4 | Controller Settings | `CONTROLLER_SETTINGS` | yes |
| 5 | Data Export | `DATA_EXPORT` | yes |
| 6 | Firmware | not listed | **no** |
| 7 | Log | `LOG` | yes |
| 8 | Migration | `MIGRATION` | yes |
| 9 | Restore | `RESTORE` | yes |
| 10 | SD-WAN | not listed | **no** |
| 11 | Site Management | `SITE_MANAGEMENT` | yes |
| 12 | Site Template | not listed | **no** |
| 13 | System Settings | `SYSTEM_SETTINGS` | yes |
| 14 | User Activity | `USER_ACTIVITY` | yes |
| 15 | User Interface | `USER_INTERFACE` | yes |
| 16 | Webhook | `WEBHOOK_SETTINGS` | yes |

**In the guide but not on this controller:** `IPS`, `LICENSE`.

Inference, not confirmed: on this version, controller logins (success and failure) are recorded under **Account** / **User Activity**, because the global alert/event list no longer has `LOGIN_*` types ([global.md](global.md)).

## Site level: 23 categories, from TP-Link docs, **pending capture**

Not yet captured from a controller. These come from TP-Link's Open API guide §5.2, which was wrong in places for the global level, so treat this list as provisional:

`ABNORMAL`, `APPLICATION_CONTROL`, `AUTHENTICATION`, `CLI`, `CLIENTS`, `DASHBOARD`, `DEVICE_MANAGEMENT`, `HOTSPOT_MANAGER`, `INSIGHT`, `IPS`, `LOG`, `MAP`, `NETWORK_SECURITY`, `PROFILES`, `REPORT`, `SIM`, `SITE_SERVICES`, `SITE_SETTINGS`, `TOOLS`, `TRANSMISSION`, `VPN`, `WIRED_NETWORKS`, `WIRELESS_NETWORKS`.

Site *Operation* types (adoptions, reboots, SSID changes and similar) that the guide lists as alerts/events aren't in this controller's site alert/event lists ([site.md](site.md)). They probably show up here as audit entries instead (inference).

To contribute the site list, follow [README.md](README.md#contribute-a-snapshot) and capture the site **Audit Logs** tab.
