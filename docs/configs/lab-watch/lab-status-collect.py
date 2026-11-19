#!/usr/bin/env python3
"""Lab Watch morning collector — RO only. Runs on Proxmox debian (.176).

Loads /root/secrets/lab.env via safe KEY=VALUE parse (never bash source).
Writes sanitized lab-status.json (no tokens). Exit 0 even on partial failure
so cron stays quiet; per-source errors go in errors[].

Install:
  sudo install -m 0755 lab-status-collect.py /usr/local/bin/lab-status-collect.py
  sudo mkdir -p /var/lib/lab-watch
  # cron example (America/New_York morning, before Chief 06:45):
  # 20 6 * * 1-5 root /usr/local/bin/lab-status-collect.py

Env (lab.env):
  NB_URL, NB_TOKEN_READ
  PVE_URL, PVE_TOKEN_ID, PVE_TOKEN_SECRET
  WAZUH_API (or WAZUH_URL), WAZUH_USER, WAZUH_PASSWORD
    Manager API only. Alerts are not on :55000.
  LAB_ATTENTION_CMD
    Optional. Command on .176 whose stdout is one wazuh.attention JSON
    object from wazuh-attention.py on .178. The collector appends
    --since <previous collected_at>. No password is passed.
    Example (not enabled until you set it):
      ssh -i /root/secrets/id_ed25519_labwatch -o BatchMode=yes \
        -o ConnectTimeout=8 labwatch@192.168.0.178 -- \
        /usr/local/bin/wazuh-attention.py
    Unset: wazuh.attention.error, manager/agent pull still runs.
    Omada IDS is not queried.
  OMADA_URL, OMADA_ID, OMADA_CLIENT_ID, OMADA_CLIENT_SECRET
    Open API app must be read-only (Viewer role). omada.rf and
    omada.disconnects_24h are GETs only; see _omada_rf / _omada_disconnects.
"""
from __future__ import annotations

import base64
import json
import re
import os
import shlex
import ssl
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

ENV_FILE = Path(os.environ.get("LAB_ENV_FILE", "/root/secrets/lab.env"))
OUT_PATH = Path(os.environ.get("LAB_STATUS_OUT", "/var/lib/lab-watch/lab-status.json"))
ET = ZoneInfo("America/New_York")
CTX = ssl._create_unverified_context()
TIMEOUT = 20


def load_env(path: Path) -> dict[str, str]:
    kv: dict[str, str] = {}
    if not path.is_file():
        raise FileNotFoundError(f"missing {path}")
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue
        key, val = line.split("=", 1)
        key = key.strip()
        if not key.isidentifier():
            continue
        val = val.strip()
        if (val.startswith("'") and val.endswith("'")) or (
            val.startswith('"') and val.endswith('"')
        ):
            val = val[1:-1]
        elif " #" in val:
            val = val.split(" #", 1)[0].rstrip()
        kv[key] = val
    return kv


def http_json(
    url: str,
    headers: dict[str, str] | None = None,
    data: bytes | None = None,
    method: str | None = None,
) -> tuple[int, Any]:
    req = urllib.request.Request(
        url, data=data, headers=headers or {}, method=method or ("POST" if data else "GET")
    )
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=TIMEOUT) as resp:
            body = resp.read()
            if not body:
                return resp.status, None
            try:
                return resp.status, json.loads(body.decode())
            except json.JSONDecodeError:
                return resp.status, {"_raw_len": len(body)}
    except urllib.error.HTTPError as e:
        try:
            err_body = e.read().decode()[:200]
        except Exception:
            err_body = ""
        raise RuntimeError(f"HTTP {e.code} {url.split('?', 1)[0]} {err_body}") from e
    except Exception as e:
        raise RuntimeError(f"{type(e).__name__}: {url.split('?', 1)[0]}") from e


def pct(used: float | int | None, total: float | int | None) -> float | None:
    if used is None or total is None or not total:
        return None
    return round(100.0 * float(used) / float(total), 1)


def collect_netbox(kv: dict[str, str]) -> dict[str, Any]:
    base = (kv.get("NB_URL") or "").rstrip("/")
    tok = kv.get("NB_TOKEN_READ") or ""
    if not base or not tok:
        raise RuntimeError("NB_URL or NB_TOKEN_READ missing")
    h = {"Authorization": f"Token {tok}"}
    st, status = http_json(f"{base}/api/status/", h)
    counts: dict[str, int | None] = {}
    for name, path in (
        ("devices", "/api/dcim/devices/"),
        ("ip_addresses", "/api/ipam/ip-addresses/"),
        ("prefixes", "/api/ipam/prefixes/"),
        ("vlans", "/api/ipam/vlans/"),
        ("cables", "/api/dcim/cables/"),
        ("wireless_lans", "/api/wireless/wireless-lans/"),
    ):
        _, j = http_json(f"{base}{path}?limit=1", h)
        counts[name] = j.get("count") if isinstance(j, dict) else None
    return {
        "ok": st == 200,
        "version": (status or {}).get("netbox-version")
        or (status or {}).get("netbox-full-version"),
        "counts": counts,
    }


def collect_proxmox(kv: dict[str, str]) -> dict[str, Any]:
    base = (kv.get("PVE_URL") or "").rstrip("/")
    tid = kv.get("PVE_TOKEN_ID") or ""
    sec = kv.get("PVE_TOKEN_SECRET") or ""
    if not base or not tid or not sec:
        raise RuntimeError("PVE_URL / PVE_TOKEN_ID / PVE_TOKEN_SECRET missing")
    h = {"Authorization": f"PVEAPIToken={tid}={sec}"}

    _, ver = http_json(f"{base}/api2/json/version", h)
    _, nodes_j = http_json(f"{base}/api2/json/nodes", h)
    nodes = (nodes_j or {}).get("data") or []
    node = None
    if nodes:
        n0 = nodes[0]
        node = {
            "name": n0.get("node"),
            "online": (n0.get("status") or "").lower() == "online",
            "uptime_s": n0.get("uptime"),
            "cpu": n0.get("cpu"),
            "mem_used": n0.get("mem"),
            "mem_total": n0.get("maxmem"),
            "mem_pct": pct(n0.get("mem"), n0.get("maxmem")),
            "disk_used": n0.get("disk"),
            "disk_total": n0.get("maxdisk"),
            "disk_pct": pct(n0.get("disk"), n0.get("maxdisk")),
        }

    storage: list[dict[str, Any]] = []
    node_name = (node or {}).get("name")
    if node_name:
        try:
            _, stor_j = http_json(f"{base}/api2/json/nodes/{node_name}/storage", h)
            for s in (stor_j or {}).get("data") or []:
                # skip templates/iso noise if enabled=0
                if s.get("enabled") == 0:
                    continue
                storage.append(
                    {
                        "storage": s.get("storage"),
                        "type": s.get("type"),
                        "active": bool(s.get("active")),
                        "used": s.get("used"),
                        "total": s.get("total"),
                        "avail": s.get("avail"),
                        "used_pct": pct(s.get("used"), s.get("total")),
                    }
                )
        except Exception as e:
            storage = [{"error": str(e)}]

    backup: dict[str, Any] = {
        "last_ok_at": None,
        "last_fail_at": None,
        "last_status": None,
        "last_type": None,
        "last_id": None,
        "source": None,
        "vzdump_seen": 0,
    }
    try:
        # vzdump ONLY — never fall back to vncshell/apt/other tasks
        tasks: list[Any] = []
        source = None
        for url in (
            f"{base}/api2/json/cluster/tasks?typefilter=vzdump",
            f"{base}/api2/json/cluster/tasks",
        ):
            try:
                _, tj = http_json(url, h)
                raw = (tj or {}).get("data") or []
                vzdumps = [x for x in raw if (x.get("type") or "") == "vzdump"]
                if vzdumps:
                    tasks = vzdumps
                    source = url.split("json/", 1)[-1]
                    break
                # typefilter unsupported or empty: keep scanning unfiltered for type==vzdump only
                if "typefilter" not in url:
                    tasks = []
                    source = url.split("json/", 1)[-1]
            except Exception:
                continue

        backup["source"] = source or "cluster/tasks"
        backup["vzdump_seen"] = len(tasks)
        if not tasks:
            backup["last_status"] = "none"
            backup["note"] = "no vzdump tasks in recent cluster/tasks window"
        else:
            best_ok = None
            best_fail = None
            best_any = None

            def _ts(task: dict[str, Any]) -> float:
                v = task.get("endtime") or task.get("starttime") or 0
                try:
                    return float(v)
                except (TypeError, ValueError):
                    return 0.0

            def _is_ok(task: dict[str, Any]) -> bool:
                st = str(task.get("status") or task.get("exitstatus") or "")
                low = st.lower()
                if "error" in low or "fail" in low:
                    return False
                return st == "OK" or low == "ok" or low.endswith(":ok")

            for tsk in tasks:
                rec = {
                    "endtime": tsk.get("endtime") or tsk.get("starttime"),
                    "status": tsk.get("status") or tsk.get("exitstatus"),
                    "type": tsk.get("type"),
                    "id": tsk.get("id"),
                    "node": tsk.get("node"),
                }
                if best_any is None or _ts(tsk) > _ts(best_any):
                    best_any = rec
                if _is_ok(tsk):
                    if best_ok is None or _ts(tsk) > _ts(best_ok):
                        best_ok = rec
                else:
                    if best_fail is None or _ts(tsk) > _ts(best_fail):
                        best_fail = rec

            def _iso(rec: dict[str, Any] | None) -> str | None:
                if not rec:
                    return None
                ts = rec.get("endtime")
                if isinstance(ts, (int, float)) and ts > 0:
                    return datetime.fromtimestamp(ts, tz=timezone.utc).astimezone(ET).isoformat()
                return None

            if best_ok:
                backup["last_ok_at"] = _iso(best_ok)
                backup["last_status"] = best_ok.get("status")
                backup["last_type"] = "vzdump"
                backup["last_id"] = best_ok.get("id")
            else:
                # vzdumps exist but none OK in window
                pick = best_fail or best_any
                backup["last_status"] = (pick or {}).get("status") or "unknown"
                backup["last_type"] = "vzdump"
                backup["last_id"] = (pick or {}).get("id")
                backup["last_fail_at"] = _iso(pick)
                backup["note"] = "vzdump tasks seen but none with OK status in window"
    except Exception as e:
        backup["error"] = str(e)

    return {
        "version": ((ver or {}).get("data") or {}),
        "node": node,
        "storage": storage,
        "backup": backup,
    }



ATTENTION_MIN_LEVEL = 12
ATTENTION_CAP = 10
ATTENTION_INDEX = "wazuh-alerts-*"
ATTENTION_MAX_WINDOW = timedelta(hours=36)
ATTENTION_DEFAULT_WINDOW = timedelta(hours=24)
ATTENTION_NOTE = (
    "Omada IDS is not queried. A quiet needs_you list is not an Omada IDS quiet."
)


def _safe_http_error(exc: BaseException) -> str:
    msg = str(exc)
    if msg.startswith("HTTP "):
        parts = msg.split(" ", 2)
        if len(parts) > 1 and parts[1].isdigit():
            return f"HTTP {parts[1]}"
    low = msg.lower()
    if any(s in low for s in ("password", "authorization", "basic ")):
        return type(exc).__name__
    if "@" in msg:
        msg = msg.split("@", 1)[-1]
    return msg[:160]


def attention_window(now: datetime) -> tuple[datetime, bool]:
    """Return (since, window_capped). Capped means no usable prior collect."""
    prev: datetime | None = None
    try:
        if OUT_PATH.is_file():
            raw = json.loads(OUT_PATH.read_text(encoding="utf-8"))
            stamp = raw.get("collected_at") if isinstance(raw, dict) else None
            if isinstance(stamp, str) and stamp:
                prev = datetime.fromisoformat(stamp)
                if prev.tzinfo is None:
                    prev = prev.replace(tzinfo=ET)
    except Exception:
        prev = None
    if prev is not None and now - ATTENTION_MAX_WINDOW <= prev < now:
        return prev, False
    return now - ATTENTION_DEFAULT_WINDOW, True


def _attention_error(now: datetime, since: datetime, capped: bool, message: str) -> dict[str, Any]:
    return {
        "window": {
            "since": since.astimezone(ET).isoformat(),
            "until": now.astimezone(ET).isoformat(),
            "window_capped": capped,
        },
        "min_level": ATTENTION_MIN_LEVEL,
        "index": ATTENTION_INDEX,
        "omada_ids": "not_assumed",
        "note": ATTENTION_NOTE,
        "error": message,
        "needs_you": None,
        "by_severity": None,
    }


def merge_wazuh_attention(now: datetime) -> dict[str, Any]:
    """Run LAB_ATTENTION_CMD and keep its one JSON object. Never sends a password."""
    since, capped = attention_window(now)
    cmd = (os.environ.get("LAB_ATTENTION_CMD") or "").strip()
    if not cmd:
        return _attention_error(now, since, capped, "attention script not configured")
    argv = shlex.split(cmd) + ["--since", since.astimezone(ET).isoformat()]
    try:
        proc = subprocess.run(
            argv,
            capture_output=True,
            text=True,
            timeout=TIMEOUT,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return _attention_error(now, since, capped, "attention script timed out")
    except Exception as e:
        return _attention_error(now, since, capped, _safe_http_error(e))
    raw = (proc.stdout or "").strip()
    try:
        doc = json.loads(raw)
    except json.JSONDecodeError:
        return _attention_error(now, since, capped, f"attention script exit {proc.returncode} returned no JSON")
    if not isinstance(doc, dict):
        return _attention_error(now, since, capped, "attention script JSON was not an object")
    return _sanitize_attention(doc)


_ATTENTION_KEYS = {
    "window",
    "min_level",
    "index",
    "omada_ids",
    "note",
    "error",
    "needs_you",
    "by_severity",
    "truncated",
}
_ROW_KEYS = {"level", "rule_id", "agent", "summary", "count", "last_seen"}


def _sanitize_attention(doc: dict[str, Any]) -> dict[str, Any]:
    out = {k: doc[k] for k in _ATTENTION_KEYS if k in doc}
    rows = out.get("needs_you")
    if rows is None:
        out["needs_you"] = None
    elif isinstance(rows, list):
        clean = []
        for row in rows:
            if not isinstance(row, dict):
                continue
            item = {k: row[k] for k in _ROW_KEYS if k in row}
            summary = item.get("summary")
            if isinstance(summary, str) and "password" in summary.lower():
                item["summary"] = "(redacted)"
            clean.append(item)
        out["needs_you"] = clean[:ATTENTION_CAP]
    else:
        out["needs_you"] = None
        out["error"] = out.get("error") or "attention needs_you was not a list"
    if "omada_ids" not in out:
        out["omada_ids"] = "not_assumed"
    return out


def collect_wazuh(kv: dict[str, str]) -> dict[str, Any]:
    base = (kv.get("WAZUH_API") or kv.get("WAZUH_URL") or "").rstrip("/")
    user = kv.get("WAZUH_USER") or ""
    pw = kv.get("WAZUH_PASSWORD") or ""
    if not base or not user or not pw:
        raise RuntimeError("WAZUH_API/URL or USER/PASSWORD missing")
    auth = base64.b64encode(f"{user}:{pw}".encode()).decode()
    _, auth_j = http_json(
        f"{base}/security/user/authenticate",
        headers={"Authorization": f"Basic {auth}", "Content-Type": "application/json"},
        data=b"",
        method="POST",
    )
    token = ((auth_j or {}).get("data") or {}).get("token") or ""
    if not token:
        raise RuntimeError("Wazuh auth returned no token")
    h = {"Authorization": f"Bearer {token}"}

    manager_ok = False
    manager_version = None
    try:
        _, mi = http_json(f"{base}/manager/info", h)
        items = ((mi or {}).get("data") or {}).get("affected_items") or []
        manager_ok = bool(items)
        if items:
            manager_version = items[0].get("version")
    except Exception:
        manager_ok = False

    agents = {"active": None, "disconnected": None, "never_connected": None, "pending": None}
    disconnected_names: list[str] = []
    try:
        _, sm = http_json(f"{base}/agents/summary/status", h)
        data = (sm or {}).get("data") or sm or {}
        # shapes vary: data.connection or flat
        conn = data.get("connection") or data.get("agent_status") or data
        for k in ("active", "disconnected", "never_connected", "pending"):
            if k in conn:
                agents[k] = conn[k]
            elif k.replace("_", "") in {x.replace("_", "") for x in conn}:
                agents[k] = conn.get(k)
        # alternate keys
        if agents["active"] is None and isinstance(data, dict):
            for src in (data, data.get("connection") or {}):
                if not isinstance(src, dict):
                    continue
                agents["active"] = src.get("active", agents["active"])
                agents["disconnected"] = src.get("disconnected", agents["disconnected"])
                agents["never_connected"] = src.get(
                    "never_connected", src.get("neverConnected", agents["never_connected"])
                )
                agents["pending"] = src.get("pending", agents["pending"])
    except Exception as e:
        agents["error"] = str(e)

    try:
        _, ag = http_json(
            f"{base}/agents?select=id,name,status,lastKeepAlive,ip,version&status=disconnected&limit=50",
            h,
        )
        for item in ((ag or {}).get("data") or {}).get("affected_items") or []:
            disconnected_names.append(item.get("name") or item.get("id") or "?")
    except Exception:
        pass

    out: dict[str, Any] = {
        "manager_ok": manager_ok,
        "manager_version": manager_version,
        "agents": agents,
    }
    if disconnected_names:
        out["disconnected_names"] = disconnected_names
    try:
        out["attention"] = merge_wazuh_attention(datetime.now(ET))
    except Exception as e:
        now = datetime.now(ET)
        since, capped = attention_window(now)
        out["attention"] = _attention_error(now, since, capped, _safe_http_error(e))
    return out


OMADA_BANDS = {"wp2g": "2.4GHz", "wp5g": "5GHz", "wp5g2": "5GHz-2", "wp6g": "6GHz"}
RADIO_ID_BAND = {0: "2.4GHz", 1: "5GHz", 2: "5GHz-2", 3: "6GHz"}
OFFLINE_RE = re.compile(
    r"\[client:(?P<name>.+?):(?P<mac>[0-9A-F]{2}(?:-[0-9A-F]{2}){5})\]\s+(?:\(IP: \S+\) )?"
    r"went offline from SSID \"(?P<ssid>.*)\" on \[ap:(?P<ap>.+?):(?P<apmac>[0-9A-F]{2}(?:-[0-9A-F]{2}){5})\]"
    r" \((?P<dur>\S+) connected"
)


def _omada_list(result: Any) -> list[dict[str, Any]]:
    if isinstance(result, list):
        return result
    result = result or {}
    return result.get("data") or result.get("list") or []


def _omada_rf(base: str, oid: str, site_id: str, h: dict[str, str],
              aps: list[dict[str, str]], clients: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Per AP radio: GET /openapi/v1/{omadacId}/sites/{siteId}/aps/{apMac}/radios
    (Omada Open API "Get AP radio detail": wp2g/wp5g/wp5g2/wp6g with actualChannel,
    bandWidth, txPower, txUtil, rxUtil, interUtil, busyUtil). Client counts come from the
    /clients list already fetched (apMac + radioId)."""
    per_radio: dict[tuple[str, str], int] = {}
    for c in clients:
        if not c.get("wireless") and c.get("connectDevType") != "ap":
            continue
        band = RADIO_ID_BAND.get(c.get("radioId"), "unknown")
        k = (str(c.get("apMac") or ""), band)
        per_radio[k] = per_radio.get(k, 0) + 1
    out: list[dict[str, Any]] = []
    for ap in aps:
        mac = ap["mac"]
        entry: dict[str, Any] = {"ap": ap["name"], "mac": mac, "radios": []}
        try:
            _, j = http_json(f"{base}/openapi/v1/{oid}/sites/{site_id}/aps/{mac}/radios", h)
            res = (j or {}).get("result") or {}
            for key, band in OMADA_BANDS.items():
                r = res.get(key)
                if not r:
                    continue
                parts = [r.get(x) for x in ("txUtil", "rxUtil", "interUtil")]
                total = sum(p for p in parts if isinstance(p, int)) if any(isinstance(p, int) for p in parts) else None
                entry["radios"].append({
                    "band": band,
                    "channel": r.get("actualChannel"),
                    "width": r.get("bandWidth"),
                    "tx_power": r.get("txPower"),
                    "util_tx_pct": r.get("txUtil"),
                    "util_rx_pct": r.get("rxUtil"),
                    "interference_pct": r.get("interUtil"),
                    "busy_pct": r.get("busyUtil"),
                    "util_total_pct": min(total, 100) if total is not None else None,
                    "clients": per_radio.get((mac, band), 0),
                })
        except Exception as e:
            entry["error"] = _safe_http_error(e)
        out.append(entry)
    return out


def _omada_disconnects(base: str, oid: str, site_id: str, h: dict[str, str],
                       clients: list[dict[str, Any]]) -> dict[str, Any]:
    """Last 24h wireless disconnects from the site Events log:
    GET /openapi/v1/{omadacId}/sites/{siteId}/logs/events (filters.module=Client),
    keeping key W_C_DISCONN ("Client Offline (Wireless)"; key and name confirmed in a live site list 2026-11-18)
    or content "went offline from SSID". Empty unless that type is enabled as an Event
    in Site > Logs > Setting (see omada-event-inventory.md).
    RSSI at disconnect is not in the log text. rssi_now_dbm is the client's current RSSI
    from /clients (only if it is back online). For the 5 clients with the most drops we also
    read GET .../clients/{mac}/client-timeline?type=3 (Disconnection) and keep any
    rssi/signal/reason attributes; those attribute names are not documented (unconfirmed)."""
    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    start_ms = now_ms - 24 * 3600 * 1000
    events: list[dict[str, Any]] = []
    for page in range(1, 11):
        q = urllib.parse.urlencode({
            "page": page, "pageSize": 100, "filters.timeStart": start_ms,
            "filters.timeEnd": now_ms, "filters.module": "Client",
        })
        _, j = http_json(f"{base}/openapi/v1/{oid}/sites/{site_id}/logs/events?{q}", h)
        rows = _omada_list((j or {}).get("result"))
        for row in rows:
            content = str(row.get("content") or "")
            if row.get("key") != "W_C_DISCONN" and "went offline from SSID" not in content:
                continue
            m = OFFLINE_RE.search(content)
            ev: dict[str, Any] = {"time_ms": row.get("time"), "key": row.get("key")}
            if m:
                ev.update(client=m["name"], client_mac=m["mac"], ssid=m["ssid"],
                          ap=m["ap"], ap_mac=m["apmac"], connected=m["dur"])
            else:
                ev["content"] = content[:200]
            events.append(ev)
        if len(rows) < 100:
            break
    rssi_now = {str(c.get("mac")): c.get("rssi") for c in clients if c.get("rssi") is not None}
    by_ap: dict[str, int] = {}
    by_client: dict[str, int] = {}
    short = 0
    for ev in events:
        if ev.get("ap"):
            by_ap[ev["ap"]] = by_ap.get(ev["ap"], 0) + 1
        if ev.get("client_mac"):
            by_client[ev["client_mac"]] = by_client.get(ev["client_mac"], 0) + 1
            ev["rssi_now_dbm"] = rssi_now.get(ev["client_mac"])
        if re.fullmatch(r"\d+s", str(ev.get("connected") or "")):
            short += 1
    top = sorted(by_client.items(), key=lambda kv_: kv_[1], reverse=True)[:5]
    timeline: dict[str, Any] = {}
    for mac, _n in top:
        try:
            q = urllib.parse.urlencode({"start": start_ms, "end": now_ms, "type": 3})
            _, j = http_json(f"{base}/openapi/v1/{oid}/sites/{site_id}/clients/{mac}/client-timeline?{q}", h)
            keep = []
            for block in (j or {}).get("result") or []:
                for e in block.get("events") or []:
                    attrs = e.get("attributes") or {}
                    extra = {k: v for k, v in attrs.items() if re.search(r"rssi|signal|snr|reason", str(k), re.I)}
                    keep.append({"time_ms": e.get("time"), "eventType": e.get("eventType"), **extra})
            timeline[mac] = keep[-20:]
        except Exception as e:
            timeline[mac] = {"error": _safe_http_error(e)}
    return {
        "window_hours": 24,
        "total": len(events),
        "short_sessions_lt_60s": short,
        "by_ap": by_ap,
        "top_clients": [{"client_mac": m, "count": n} for m, n in top],
        "timeline_top_clients": timeline,
        "events": events[:200],
        "note": "rssi_now_dbm is current RSSI, not RSSI at disconnect.",
    }


def collect_omada(kv: dict[str, str]) -> dict[str, Any]:
    base = (kv.get("OMADA_URL") or "").rstrip("/")
    oid = kv.get("OMADA_ID") or ""
    cid = kv.get("OMADA_CLIENT_ID") or ""
    csec = kv.get("OMADA_CLIENT_SECRET") or ""
    if not base or not oid or not cid or not csec:
        raise RuntimeError("OMADA_URL / OMADA_ID / CLIENT_ID / CLIENT_SECRET missing")

    payload = json.dumps(
        {"omadacId": oid, "client_id": cid, "client_secret": csec}
    ).encode()
    _, tok_j = http_json(
        f"{base}/openapi/authorize/token?grant_type=client_credentials",
        headers={"Content-Type": "application/json"},
        data=payload,
        method="POST",
    )
    ec = (tok_j or {}).get("errorCode")
    if ec not in (0, "0", None):
        raise RuntimeError(f"Omada token errorCode={ec} msg={(tok_j or {}).get('msg')}")
    token = ((tok_j or {}).get("result") or {}).get("accessToken") or ""
    if not token:
        raise RuntimeError("Omada token missing accessToken")
    h = {"Authorization": f"AccessToken={token}"}

    _, sites_j = http_json(f"{base}/openapi/v1/{oid}/sites?pageSize=10&page=1", h)
    result = (sites_j or {}).get("result") or {}
    sites = result.get("data") or result.get("list") or []
    if isinstance(result, list):
        sites = result
    site = sites[0] if sites else {}
    site_id = site.get("siteId") or site.get("id")
    site_name = site.get("name")

    devices_adopted = 0
    devices_online = 0
    offline: list[dict[str, str]] = []
    type_counts: dict[str, int] = {}
    aps: list[dict[str, str]] = []
    if site_id:
        _, dev_j = http_json(
            f"{base}/openapi/v1/{oid}/sites/{site_id}/devices?pageSize=100&page=1", h
        )
        dres = (dev_j or {}).get("result") or {}
        devices = dres.get("data") or dres.get("list") or []
        if isinstance(dres, list):
            devices = dres
        for d in devices or []:
            devices_adopted += 1
            dtype = str(d.get("type") or d.get("deviceType") or "unknown")
            type_counts[dtype] = type_counts.get(dtype, 0) + 1
            status = str(d.get("status") or d.get("deviceStatus") or "").lower()
            # Omada often: 1=online / 0=offline or strings
            online = status in ("1", "online", "connected", "running") or d.get("status") == 1
            name = str(d.get("name") or d.get("deviceName") or "?")
            mac = str(d.get("mac") or d.get("macAddress") or "")
            if dtype.lower() == "ap" and mac:
                aps.append({"name": name, "mac": mac})
            if online:
                devices_online += 1
            else:
                offline.append({"name": name, "mac": mac, "type": dtype, "status": str(d.get("status"))})

    guest: dict[str, Any] = {"ssids_seen": [], "client_count_by_ssid": {}}
    clients: list[dict[str, Any]] = []
    if site_id:
        try:
            _, cl_j = http_json(
                f"{base}/openapi/v1/{oid}/sites/{site_id}/clients?pageSize=1000&page=1", h
            )
            clients = _omada_list((cl_j or {}).get("result"))
            by: dict[str, int] = {}
            for c in clients or []:
                ssid = c.get("ssid") or c.get("ssidName") or c.get("wirelessNetwork") or "(wired/unknown)"
                ssid = str(ssid)
                by[ssid] = by.get(ssid, 0) + 1
            guest["client_count_by_ssid"] = by
            guest["ssids_seen"] = sorted(by.keys())
            # heuristic: guest-ish names
            guest_hits = [s for s in by if "guest" in s.lower()]
            guest["guest_ssids"] = guest_hits
            guest["guest_client_count"] = sum(by[s] for s in guest_hits)
        except Exception as e:
            guest["error"] = str(e)

    return {
        "controller_ok": True,
        "site_id": site_id,
        "site_name": site_name,
        "eap": {
            "note": "controller has no /eaps path; using /devices",
            "adopted": devices_adopted,
            "online": devices_online,
            "offline": offline,
            "type_counts": type_counts,
        },
        "guest_ssid": guest,
        "rf": _omada_try(lambda: _omada_rf(base, oid, site_id, h, aps, clients)) if site_id else None,
        "disconnects_24h": _omada_try(lambda: _omada_disconnects(base, oid, site_id, h, clients)) if site_id else None,
    }


def _omada_try(fn: Any) -> Any:
    try:
        return fn()
    except Exception as e:
        return {"error": _safe_http_error(e)}


def main() -> int:
    collected_at = datetime.now(ET).isoformat()
    out: dict[str, Any] = {
        "collected_at": collected_at,
        "collector": "lab-status-collect.py",
        "host_hint": "proxmox-debian",
        "proxmox": None,
        "wazuh": None,
        "omada": None,
        "netbox": None,
        "errors": [],
    }
    try:
        kv = load_env(ENV_FILE)
    except Exception as e:
        out["errors"].append({"source": "lab.env", "error": str(e)})
        OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        OUT_PATH.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {OUT_PATH} (env load failed)", file=sys.stderr)
        return 0

    for name, fn in (
        ("proxmox", collect_proxmox),
        ("wazuh", collect_wazuh),
        ("omada", collect_omada),
        ("netbox", collect_netbox),
    ):
        try:
            out[name] = fn(kv)
        except Exception as e:
            out[name] = None
            out["errors"].append({"source": name, "error": str(e)})

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = OUT_PATH.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    tmp.replace(OUT_PATH)
    err_n = len(out["errors"])
    print(f"wrote {OUT_PATH} errors={err_n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
