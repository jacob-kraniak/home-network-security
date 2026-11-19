#!/usr/bin/env python3
"""Build the public Omada alert/event dictionary from notification-settings snapshots.

Input: the JSON that an Omada controller returns for its alert/event notification settings
(Global level and Site level; the same shape the web UI and the v2 Open API use:
result.alertNotifications[] and result.eventNotifications[]). Raw snapshots contain
per-instance state (enable, email, webhook on/off) and stay OUT of the repo. This script
keeps only the dictionary fields and writes:

  omada-alert-dictionary.json   one object per (level, list, key)
  omada-alert-dictionary.csv    same rows, flat
  global.md, site.md            Markdown tables (between the GENERATED markers)

Usage:
  build-omada-dictionary.py --global global.json --site site.json \
      [--guide sources/tplink-openapi-guide-5.6.1-keys.json] --out docs/services/omada-log-inventory

Stdlib only. Deterministic: rows keep the controller's order.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

STATE_FIELDS = {"enable", "email", "webhook"}  # per-instance; never written out
KNOWN_FIELDS = {"key", "shortMsg", "module", "level", "deviceTypes", "clientTypes"} | STATE_FIELDS

# Short, neutral notes for the types most people will care about. Keyed by notification key.
NOTES: dict[str, str] = {
    # Wi-Fi / clients
    "W_C_DISCONN": "A wireless client left. The syslog line carries the SSID, AP, connected time and traffic, but no reason code or RSSI. Repeats in a short window are the main signal of flapping clients.",
    "AP_C_OK": "A wireless client joined (SSID, AP, channel). Pair it with W_C_DISCONN to measure session length.",
    "W_C_ROAM": "A client moved between APs; the line includes both APs and channels. Frequent back-and-forth roams point at overlapping coverage or a sticky client.",
    "AP_C_FL": "A wireless client tried and failed to connect (wrong key, auth timeout, RADIUS, and similar). Bursts from one client often mean a saved wrong password or a weak-signal edge.",
    "AP_CH_C": "An AP changed channel, usually auto-channel reacting to interference. Several in an hour on one AP suggests a crowded band.",
    "AP_RADAR": "DFS radar detected on a 5 GHz channel. The AP must vacate the channel, and connected clients drop or move.",
    "AP_ISOLATE": "The AP lost its wired uplink (often a mesh fallback). Clients on it may lose connectivity.",
    "L_C_CONN": "A wired client came online on a switch or gateway port.",
    "L_C_DISCONN": "A wired client went offline.",
    "OSW_C_1X_FL": "802.1X authentication failed on a switch port.",
    "W_C_PRT_FL": "Captive-portal authentication failed (wireless).",
    # Devices
    "DEV_DISCONN": "The controller lost contact with an adopted device (AP, switch, gateway, OLT). Appears in both the alert and the event list.",
    "DEV_CONN": "A device connected to the controller.",
    "DEV_RECONN": "A device reconnected after a disconnect. Useful for measuring outage length with DEV_DISCONN.",
    "DEV_READOPT_FL": "The controller could not re-adopt a device automatically.",
    "DEV_CONN_REMEMBER": "A previously known device was re-adopted after a factory reset.",
    "DEV_C_DSYNC": "Device config no longer matches what the controller pushed. Appears in both lists.",
    "DEV_IP_C": "A switch or gateway changed its IP address.",
    "DEVICE_MONITOR_STATUS_LINK_DOWN": "A device reported a monitored link down.",
    "REBOOT_RECOVERY": "IntelliRecover started an automatic reboot to recover an AP.",
    "REBOOT_RECOVERY_FAIL": "IntelliRecover reboot did not bring the device back.",
    "REBOOT_RECOVERY_SUCCESS": "IntelliRecover: the device is back online.",
    "OSW_INSTALL_REBOOT": "A switch rebooted itself (for example after an upgrade).",
    "OSW_INSTALL_ROLLBACK": "A switch firmware upgrade failed.",
    # Switching / L2
    "OSW_DET_LOOP": "Switch loop detection fired. Loops can take down the whole LAN.",
    "OSW_DET_STORM": "A broadcast/multicast storm crossed the storm-control threshold.",
    "OSW_STORM_SHUTDOWN": "A switch port was shut down by storm control.",
    "OSW_PB": "A switch port was blocked (loop prevention).",
    "OSW_LOOP_C": "A previously detected loop has cleared.",
    "OSW_TOPO_C": "STP topology change (alert list). Shares its shortMsg with OSW_STP_FWD.",
    "OSW_STP_FWD": "STP port moved to forwarding (event list). Shares its shortMsg 'STP Topology Changed' with OSW_TOPO_C.",
    "OSW_STP_BLOCK": "STP put a port into blocking.",
    "OSW_DHCP_SNOOP_ALERT": "DHCP snooping on a switch flagged an untrusted DHCP server or packet.",
    "OSW_ARP_DETECTION_ALERT": "ARP inspection on a switch flagged a suspicious ARP packet.",
    "OSW_FAN_ERR": "Switch fan failure.",
    "OSW_PWR_ERR": "Switch redundant power supply failure.",
    "OSW_KEY_HEALING_MGMTVLAN_CREATE_FAILED": "Switch self-healing could not recreate the management VLAN. The only alert with level 'Critial' (sic) in the capture.",
    # Gateway / WAN / security
    "OSG_WAN_DOWN": "A WAN link went down.",
    "OSG_BK_WAN_UP": "Traffic failed over to the backup WAN.",
    "OSG_PRI_WAN_UP": "Traffic is back on the primary WAN. TP-Link's guide calls this 'Primary WAN Recovered'.",
    "WAN_IP_O_F": "The gateway could not obtain a WAN IP (DHCP/PPPoE upstream problem).",
    "OSG_PPPOE_FL": "PPPoE session to the ISP failed.",
    "OSG_ATK": "The gateway's attack defense detected an attack (flood, scan and similar).",
    "OSG_SF_ATK": "Gateway detected a stationary flood attack.",
    "OSG_ARP_ATK": "Gateway detected ARP conflicts (possible spoofing or a duplicate IP).",
    "OSG_LARGE_PING_ATTACK": "Gateway detected oversized ICMP (ping) traffic.",
    "OSG_ROGUE_DHCP_SERVER_DETECTED": "Another DHCP server is answering on a gateway network. Common cause: a consumer router plugged in as a client.",
    "OSG_IP_CONFLICT_DETECTED": "Two hosts are using the same IP address.",
    "OSG_DHCP_LEASE_POOL_EXHAUSTED": "A DHCP pool has no free leases; new clients can't get an address.",
    "OSG_LAN_IP_CONFLICT": "A gateway LAN IP overlaps another interface.",
    "LAN_CONFLICT_AVOIDANCE": "The gateway changed a LAN segment to avoid a conflict (for example with the WAN subnet).",
    "OSG_IPSEC_FL": "Site-to-site IPsec tunnel went down.",
    "OSG_DHCP_S": "Gateway DHCP server messages (lease allocated/rejected). High volume.",
    "MDNS_RULE_NOT_EFFECT": "Configured mDNS reflection rules are not working.",
    # System
    "LOG_SRV_FL": "The controller failed to send site logs to the remote log server. Worth alerting on if syslog is your pipeline.",
    "DST_C_FAIL": "Daylight-saving-time configuration error; timestamps may be off.",
    # OLT/ONU (GPON) — group note
    "LOG_ONU_IS_OFFLINE": "ONU (fiber terminal) went offline. Appears in both lists. Only relevant with an Omada OLT.",
    "LOG_ONU_DYING_GASP": "ONU reported loss of power before going offline. Only relevant with an Omada OLT.",
}

WIFI_QUICK_PICK = ["W_C_DISCONN", "AP_C_OK", "W_C_ROAM", "AP_C_FL", "AP_CH_C", "AP_RADAR",
                   "AP_ISOLATE", "DEV_DISCONN", "DEV_RECONN", "DEV_CONN"]


def load_lists(path: Path) -> tuple[list[dict], list[dict]]:
    d = json.loads(path.read_text(encoding="utf-8"))
    if d.get("errorCode", 0) != 0:
        sys.exit(f"{path}: errorCode {d.get('errorCode')}")
    r = d.get("result", d)
    a, e = r.get("alertNotifications") or [], r.get("eventNotifications") or []
    for name, lst in (("alertNotifications", a), ("eventNotifications", e)):
        keys = [x.get("key") for x in lst]
        if any(not x.get("key") or not x.get("shortMsg") for x in lst):
            sys.exit(f"{path}: {name} has an entry without key/shortMsg")
        if len(keys) != len(set(keys)):
            sys.exit(f"{path}: duplicate key in {name}")
        unknown = {f for x in lst for f in x} - KNOWN_FIELDS
        if unknown:
            print(f"note: {path.name} {name} has unrecognised fields kept out: {sorted(unknown)}", file=sys.stderr)
    return a, e


def rows_for(level: str, a: list[dict], e: list[dict], guide: dict[str, str] | None) -> list[dict]:
    both = {x["key"] for x in a} & {x["key"] for x in e}
    out = []
    for kind, lst in (("alert", a), ("event", e)):
        for x in lst:
            k = x["key"]
            g = None
            if guide is not None:
                g = "not listed" if k not in guide else ("same name" if guide[k] == x["shortMsg"] else f"name differs: '{guide[k]}'")
            out.append({
                "level": level,
                "kind": kind,
                "key": k,
                "shortMsg": x["shortMsg"],
                "module": x.get("module", ""),
                "alertLevel": x.get("level", "") if kind == "alert" else "",
                "deviceTypes": list(x.get("deviceTypes") or []),
                "clientTypes": list(x.get("clientTypes") or []),
                "webhookCapable": "webhook" in x,
                "inBothLists": k in both,
                "tplinkGuide": g,
                "note": NOTES.get(k, ""),
            })
    return out


def md_escape(s: str) -> str:
    return s.replace("|", "\\|")


def md_table(rows: list[dict], kind: str) -> list[str]:
    alert = kind == "alert"
    hdr = ["#", "Key", "shortMsg (verbatim)", "Kind", "Module"] + (["Level"] if alert else []) + \
          ["Device types", "Client types", "Webhook-capable", "TP-Link guide", "What it means / why you'd care"]
    out = ["| " + " | ".join(hdr) + " |", "|" + "---|" * len(hdr)]
    for i, r in enumerate([r for r in rows if r["kind"] == kind], 1):
        k = f"`{r['key']}`" + (" ⇄" if r["inBothLists"] else "")
        cells = [str(i), k, md_escape(r["shortMsg"]), r["kind"], r["module"]] + ([r["alertLevel"]] if alert else []) + \
                [", ".join(r["deviceTypes"]) or "—", ", ".join(r["clientTypes"]) or "—",
                 "yes" if r["webhookCapable"] else "no", md_escape(r["tplinkGuide"] or "—"), md_escape(r["note"])]
        out.append("| " + " | ".join(cells) + " |")
    return out


def replace_generated(path: Path, body: list[str]) -> None:
    start, end = "<!-- GENERATED:START (build-omada-dictionary.py) -->", "<!-- GENERATED:END -->"
    t = path.read_text(encoding="utf-8")
    if start not in t or end not in t:
        sys.exit(f"{path}: missing GENERATED markers")
    pre, rest = t.split(start, 1)
    _, post = rest.split(end, 1)
    path.write_text(pre + start + "\n" + "\n".join(body) + "\n" + end + post, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--global", dest="glob", required=True, type=Path)
    ap.add_argument("--site", required=True, type=Path)
    ap.add_argument("--guide", type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--captured", default="unknown")
    ap.add_argument("--controller", default="Omada Software Controller <version>")
    a = ap.parse_args()

    guide_g = guide_s = None
    if a.guide:
        gd = json.loads(a.guide.read_text(encoding="utf-8"))
        guide_g = {x["key"]: x["name"] for x in gd["global"]}
        guide_s = {x["key"]: x["name"] for x in gd["site"]}

    ga, ge = load_lists(a.glob)
    sa, se = load_lists(a.site)
    rows = rows_for("global", ga, ge, guide_g) + rows_for("site", sa, se, guide_s)

    site_keys = {r["key"] for r in rows if r["level"] == "site"}
    counts = {
        "global_alerts": len(ga), "global_events": len(ge),
        "site_alerts": len(sa), "site_events": len(se),
        "site_in_both_lists": sorted({x["key"] for x in sa} & {x["key"] for x in se}),
        "site_unique_keys": len(site_keys),
        "rows": len(rows),
    }
    if guide_s is not None:
        counts["site_in_guide_not_captured"] = sorted(set(guide_s) - site_keys)
        counts["site_captured_not_in_guide"] = len(site_keys - set(guide_s))
        gk = {r["key"] for r in rows if r["level"] == "global"}
        counts["global_in_guide_not_captured"] = sorted(set(guide_g) - gk)
        counts["global_captured_not_in_guide"] = sorted(gk - set(guide_g))

    meta = {
        "name": "Omada alert/event dictionary",
        "captured": a.captured,
        "controller": a.controller,
        "method": "Notification-settings JSON (Global and Site), read-only. Per-instance fields (enable, email, webhook on/off) removed.",
        "webhookCapable": "true when the controller exposes a per-type webhook flag for the key. TP-Link's Open API says that flag applies to Omada Pro controllers only; behaviour on software controllers is unverified.",
        "counts": counts,
    }
    a.out.mkdir(parents=True, exist_ok=True)
    (a.out / "omada-alert-dictionary.json").write_text(
        json.dumps({"meta": meta, "entries": rows}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    cols = ["level", "kind", "key", "shortMsg", "module", "alertLevel", "deviceTypes", "clientTypes",
            "webhookCapable", "inBothLists", "tplinkGuide", "note"]
    with (a.out / "omada-alert-dictionary.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({**r, "deviceTypes": ";".join(r["deviceTypes"]), "clientTypes": ";".join(r["clientTypes"]),
                        "tplinkGuide": r["tplinkGuide"] or ""})

    g = [r for r in rows if r["level"] == "global"]
    s = [r for r in rows if r["level"] == "site"]
    replace_generated(a.out / "global.md",
                      [f"**{len(ga)} alerts + {len(ge)} events = {len(g)} types.**", "", "### Alerts", ""] + md_table(g, "alert") +
                      ["", "### Events", ""] + md_table(g, "event"))
    quick = [r for k in WIFI_QUICK_PICK for r in s if r["key"] == k]
    seen, qrows = set(), []
    for r in quick:
        if r["key"] in seen:
            continue
        seen.add(r["key"])
        kinds = "alert + event" if r["inBothLists"] else r["kind"]
        qrows.append(f"| `{r['key']}` | {md_escape(r['shortMsg'])} | {kinds} | {md_escape(r['note'])} |")
    replace_generated(a.out / "site.md",
                      [f"**{len(sa)} alerts + {len(se)} events = {len(s)} rows, {len(site_keys)} unique keys** "
                       f"({len(counts['site_in_both_lists'])} keys appear in both lists, marked ⇄: "
                       + ", ".join(f"`{k}`" for k in counts["site_in_both_lists"]) + ").", "",
                       "### Homelab Wi-Fi troubleshooting quick pick", "",
                       "| Key | shortMsg | Kind | Why |", "|---|---|---|---|"] + qrows +
                      ["", "**None of these types carries RSSI, SNR or a deauth/disassociation reason code.** "
                       "For signal, channel utilization and interference, poll the Open API instead "
                       "(see [README.md](README.md#what-the-logs-dont-tell-you))."] +
                      ["", "### Site alerts", ""] + md_table(s, "alert") +
                      ["", "### Site events", ""] + md_table(s, "event"))
    print(json.dumps(counts, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
