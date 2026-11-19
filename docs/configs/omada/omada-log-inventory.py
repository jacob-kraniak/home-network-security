#!/usr/bin/env python3
"""Read-only dump of Omada log export settings at BOTH levels (Global and each Site).

Answers "which Omada log types can reach Wazuh (syslog) or Grok Bot (webhook) right now?"
from the controller itself, so the inventory in docs/services/omada-event-inventory.md can be
checked against the live controller. GET requests only. Run on .176 as root (same lab.env as
lab-status-collect.py); output is Markdown on stdout. Prints no token, secret, URL or host.

Endpoints (Omada Open API, https://use1-omada-northbound.tplinkcloud.com/doc.html):
  GET /openapi/v1/{omadacId}/global/controller/setting/syslog      Global remote logging
  GET /openapi/v1/{omadacId}/sites/{siteId}/remote-logging         Site remote logging
  GET /openapi/v2/{omadacId}/log-notification                      Global alert/event flags per key
  GET /openapi/v2/{omadacId}/sites/{siteId}/site/log-notification  Site alert/event flags per key
  GET /openapi/v1/{omadacId}/audit-notification                    Global audit categories
  GET /openapi/v1/{omadacId}/sites/{siteId}/site/audit-notification Site audit categories
  GET /openapi/v1/{omadacId}/webhook/settings                      Webhook entries (name only)

Usage: omada-log-inventory.py [--env /root/secrets/lab.env] > omada-log-inventory.md
"""
from __future__ import annotations

import argparse
import json
import ssl
import sys
import urllib.request
from pathlib import Path
from typing import Any

CTX = ssl._create_unverified_context()


def load_env(path: Path) -> dict[str, str]:
    kv: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.removeprefix("export ").split("=", 1)
        v = v.strip()
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "'\"":
            v = v[1:-1]
        kv[k.strip()] = v
    return kv


def call(url: str, headers: dict[str, str], data: bytes | None = None) -> Any:
    req = urllib.request.Request(url, data=data, headers=headers, method="POST" if data else "GET")
    with urllib.request.urlopen(req, context=CTX, timeout=20) as r:
        j = json.loads(r.read().decode() or "{}")
    if j.get("errorCode") not in (0, None):
        raise RuntimeError(f"errorCode={j.get('errorCode')} {j.get('msg')}")
    return j.get("result")


def yn(v: Any) -> str:
    return "yes" if v is True else ("no" if v is False else "?")


def notif_rows(res: Any) -> list[tuple[str, dict]]:
    """Normalise the two shapes seen for log-notification responses.

    v1 (Open API spec): logNotifications[] with alert/event booleans.
    v2 (Open API spec, and the shape Jacob's controller returned on 2026-11-18):
    alertNotifications[] and eventNotifications[] with an enable boolean each.
    """
    res = res or {}
    if "alertNotifications" in res or "eventNotifications" in res:
        return ([("Alert", n) for n in res.get("alertNotifications") or []]
                + [("Event", n) for n in res.get("eventNotifications") or []])
    out = []
    for n in res.get("logNotifications") or []:
        kind = "Alert" if n.get("alert") is True else ("Event" if n.get("event") is True else "off")
        out.append((kind, dict(n, enable=n.get("alert") is True or n.get("event") is True)))
    return out


def notif_table(title: str, res: Any, remote_on: bool) -> list[str]:
    res = res or {}
    # The live controller calls it webhookSetting; the published spec calls it webhookConfig.
    wh = res.get("webhookSetting") or res.get("webhookConfig") or {}
    wh_on = wh.get("webhookEnable")
    rows = notif_rows(res)
    out = [f"### {title}", "",
           f"Types listed: {len(rows)} ({sum(1 for k, _ in rows if k == 'Alert')} alerts). "
           f"Webhook master switch for this level: {yn(wh_on)}. "
           f"Remote logging for this level: {yn(remote_on)}. "
           f"Email recipients configured: {len(res.get('recipients') or [])}.", "",
           "Note: this endpoint only holds email/webhook flags. Syslog export follows the remote "
           "log server setting above, so the Syslog column is inferred.", "",
           "| Key | Name | Class | Enabled | Email | Webhook flag | Webhook effective | Syslog (inferred) |",
           "|---|---|---|---|---|---|---|---|"]
    for kind, n in rows:
        on = n.get("enable") is True
        syslog = "yes" if (on and remote_on) else ("type disabled" if remote_on else "remote logging off")
        eff = "yes" if (n.get("webhook") is True and wh_on is True) else "no"
        out.append(f"| {n.get('key')} | {n.get('shortMsg')} | {kind} | {yn(n.get('enable'))} | "
                   f"{yn(n.get('email'))} | {yn(n.get('webhook'))} | {eff} | {syslog} |")
    return out + [""]


def audit_table(title: str, res: Any) -> list[str]:
    rows = (res or {}).get("auditLogNotifications") or []
    wh = (res or {}).get("webhookSetting") or (res or {}).get("webhookConfig") or {}
    out = [f"### {title}", "", f"Audit webhook enabled: {yn(wh.get('webhookEnable'))}", "",
           "| Category key | Name | Webhook |", "|---|---|---|"]
    out += [f"| {a.get('key')} | {a.get('shortMsg')} | {yn(a.get('webhook'))} |" for a in rows]
    return out + [""]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--env", default="/root/secrets/lab.env")
    a = ap.parse_args()
    kv = load_env(Path(a.env))
    base, oid = kv["OMADA_URL"].rstrip("/"), kv["OMADA_ID"]
    tok = call(f"{base}/openapi/authorize/token?grant_type=client_credentials",
               {"Content-Type": "application/json"},
               json.dumps({"omadacId": oid, "client_id": kv["OMADA_CLIENT_ID"],
                           "client_secret": kv["OMADA_CLIENT_SECRET"]}).encode())
    h = {"Authorization": f"AccessToken={tok['accessToken']}"}
    v1, v2 = f"{base}/openapi/v1/{oid}", f"{base}/openapi/v2/{oid}"
    md: list[str] = ["# Omada log export settings (read-only dump)", ""]

    def safe(fn, label):
        try:
            return fn()
        except Exception as e:  # keep going; never print URLs
            md.append(f"- {label}: unavailable ({type(e).__name__}: {str(e)[:80]})")
            return None

    g_sys = safe(lambda: call(f"{v1}/global/controller/setting/syslog", h), "Global remote logging") or {}
    md += ["## Global View", "", f"Remote logging enabled: {yn(g_sys.get('enable'))}, "
           f"port {g_sys.get('port', '?')} (host not printed).", ""]
    md += notif_table("Global alerts/events", safe(lambda: call(f"{v2}/log-notification", h), "Global log-notification"),
                      g_sys.get("enable") is True)
    md += audit_table("Global audit", safe(lambda: call(f"{v1}/audit-notification", h), "Global audit-notification"))

    sites = safe(lambda: call(f"{v1}/sites?pageSize=100&page=1", h), "Sites") or {}
    for s in (sites.get("data") if isinstance(sites, dict) else sites) or []:
        sid, name = s.get("siteId"), s.get("name")
        rl = (safe(lambda: call(f"{v1}/sites/{sid}/remote-logging", h), f"{name} remote logging") or {}).get("remoteLog") or {}
        md += [f"## Site: {name}", "",
               f"Remote logging enabled: {yn(rl.get('enable'))}, port {rl.get('port', '?')}, "
               f"More Client Detail Logs: {yn(rl.get('moreClientLog'))} (host not printed).", ""]
        md += notif_table(f"{name} alerts/events",
                          safe(lambda: call(f"{v2}/sites/{sid}/site/log-notification", h), f"{name} log-notification"),
                          rl.get("enable") is True)
        md += audit_table(f"{name} audit",
                          safe(lambda: call(f"{v1}/sites/{sid}/site/audit-notification", h), f"{name} audit-notification"))

    hooks = safe(lambda: call(f"{v1}/webhook/settings", h), "Webhooks") or []
    md += ["## Webhook entries (Global > Settings > Platform Integration > Webhooks)", ""]
    md += [f"- {w.get('name')}: template {w.get('template')} (0=Omada, 1=Google Chat), "
           f"retry {w.get('retryPolicy')}, {w.get('urlNum')} URL(s) (URL and secret not printed)" for w in hooks] or ["- none"]
    print("\n".join(md))
    return 0


if __name__ == "__main__":
    sys.exit(main())
