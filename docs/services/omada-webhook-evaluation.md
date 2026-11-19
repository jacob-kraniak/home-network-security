# Evaluation: direct Omada webhook as a second path

**Drafted:** 2026-11-17 (ET). **Question:** should Omada also push events straight to a Grok Bot webhook, for anything syslog → Wazuh doesn't carry?
**Short answer:** not yet. Omada's webhook carries the **same log types** as syslog, so it adds no new event types. It's worth it later only as a **backup path for a few high-value types** (device down, rogue DHCP, controller node down) if Wazuh is down. The data syslog really lacks (RF utilization, RSSI, Insight incidents, rogue AP scans, WIDS) has no webhook either and comes from API polling instead (`lab-status-collect.py`).

Source keys [S1]–[S9] are listed in [omada-event-inventory.md](omada-event-inventory.md#sources).

## What Omada's webhook supports (evidence)

| Item | Detail | Source |
|---|---|---|
| Where to create it | **Global View > Settings > Platform Integration > Webhooks > Create New Webhook** | [S2], [S3] |
| Fields | Name, **Shared Secret** (auto-generated if left blank), **URL**, **Payload Template**, **Retry Policy** | [S2] |
| Payload templates | **Omada** or **Google Chat** | [S3]; API `template` 0 = Omada, 1 = Google Chat [S4] |
| Retry policy | None; Important (up to 5 retries over 60 min); Critical (up to 5 retries over 24 h) | [S2], [S3] |
| Test and audit trail | ACTION column: test connectivity, view **dispatch logs**, edit, delete. API: `GET /openapi/v1/{omadacId}/webhook/settings/dispatch-logs` | [S2], [S4] |
| Which events (site alerts/events) | Site > **Logs > Setting > Alerts / Events**: enable **Webhook**, pick the webhook, tick **Webhook Notification** per type | [S2], [S3] |
| Which events (audit) | Site > **Logs > Setting > Audit Logs**: enable Webhook, pick webhooks, pick categories | [S2] |
| Global level | Jacob's controller (live JSON, 2026-11-18): master switch `webhookSetting.webhookEnable` = **false**; every global and site type exposes a per-type `webhook` flag (see the [dictionary](omada-log-inventory/README.md)). While the master switch is off, no flag sends anything. The global UI path for the switch isn't confirmed | [L1 in the inventory], [S4] |
| Pro caveat | API: per-type `webhook` flag "applies to the Omada Pro Controller only" (contradicts [S2]/[S3], which show it on the standard controller) | [S4] |

## Payload format (Omada template)

From Open API Access Guide §5.3.1 [S4]:

```json
{
  "Site": "site-name (only site-level logs have this field)",
  "description": "This is a webhook message from Omada Controller",
  "shardSecret": "shard secret of webhook",
  "text": ["content of audit log"],
  "Controller": "controller-name",
  "timestamp": 1692128478856
}
```

What this means (inference):

- **No signature header is documented.** The shared secret travels **inside the JSON body** (`shardSecret`), so the receiver authenticates by comparing that value. The URL must be HTTPS, and the routine must reject any body whose `shardSecret` doesn't match.
- `text` is an **array of the same free-text content** that syslog carries, with no `key`, level or structured fields. The receiver would need the same parsing as the Wazuh decoders.
- `timestamp` is epoch milliseconds, and `Site` is missing for controller-level logs.

## Comparison

| | Syslog → Wazuh → `custom-grokbot` (primary) | Omada webhook → Grok Bot (optional) |
|---|---|---|
| Event types | All 132 alert/event types that apply here (19 global, confirmed live, + 113 site) + 38 audit categories, if enabled | Same types, but only those ticked for webhook (and maybe Pro-only per type) |
| Severity / correlation | Wazuh levels and frequency rules (repeat disconnects per client and per AP, channel churn) | None. Every event becomes one POST |
| Volume control | Integration filter (level 6+, group `omada`) plus dedup and rate cap in `custom-grokbot` | Only per-type on/off. A disconnect storm means a POST storm (token budget) |
| Works when Wazuh is down | No | **Yes** |
| Network need | LAN only (UDP 514), then CT 100 → Grok Bot over HTTPS | CT 101 (controller) needs outbound HTTPS to the Grok Bot webhook |
| Dashboards (Jacob's goal) | Yes, alerts indexed in Wazuh | No |
| Secrets | URL and key in `/var/ossec/etc/grokbot-webhook.env` on CT 100 | URL and shared secret stored in the Omada controller |

## Recommendation

1. **Now:** don't enable the Omada webhook. Leave the global master switch **off**, as it is today. Fix the two-level syslog config (inventory checklist), deploy the rules, and use `custom-grokbot` for real-time delivery.
2. **Later, optional:** if Lab Watch wants a backup path while Wazuh is being upgraded (#44), create one webhook (template **Omada**, retry **Important**) for a short list of types only: *Device Disconnected*, *EAP Isolated*, *A rogue DHCP server is detected*, *Gateway Detected Attack*. Use a **separate** Grok Bot routine URL, so the two paths are easy to tell apart and the Wazuh routine isn't double-fed. Jacob enters the URL and secret in the UI himself.
3. Whoever owns the "Wazuh alert webhook" routine has to confirm it accepts the Omada body shape before step 2. I can't inspect the routine.
