# Wazuh Data Source — Omada Syslog

**Verified:** 2026-10-04 (EDT)  
**Manager:** CT 100 Wazuh `192.168.0.178` on PVE node `debian` `192.168.0.176` (bridge `vmbr0`)  
**Related:** [Services index](README.md) · [ROADMAP § Phase 2](../ROADMAP.md#phase-2-self-hosted-services-build-in-progress-) · [Phase 2 checkpoint](../phases/phase-2-checkpoint-2026-09-16.md)

RFC1918 only. No PSKs, tokens, passwords, or MAC addresses. APs are referenced by IP; MACs in samples are placeholders.

---

## Milestone

**Omada syslog is onboarded into Wazuh.** Omada Remote Logging sends to the native `wazuh-remoted` syslog listener on CT 100. AP per-connection traffic records are decoded but stay at level 0 (no alert, not on the dashboard). Wireless IDS rule is still open (see below).

---

## Source (Omada)

| Field | Value |
|-------|-------|
| Platform | TP-Link Omada SDN (controller on CT 101) |
| Senders | EAP access points `192.168.0.100` and `192.168.0.101`; gateway `192.168.0.1` also sends `user.notice` |
| Remote Logging | Enabled → `192.168.0.178` UDP `514` |
| Wireless IDS | Enabled at **High** (deauth, AP spoofing, client flood, etc.) — detection-only on the Omada side |

---

## Ingest (Wazuh)

| Field | Value |
|-------|-------|
| Listener | Native `wazuh-remoted` syslog on `0.0.0.0:514/udp` — no separate rsyslog collector |
| `ossec.conf` `<remote>` syslog `allowed-ips` | `192.168.0.0/24`, `192.168.10.0/24`, `192.168.20.0/24` |
| Not allowed (intentional) | Guest `192.168.30.0/24` and Lab VLAN 40. Do not widen to a `/16`. |
| `logall` / `logall_json` | **Off** |

`logall` was enabled only briefly for verification. With it on, archives grew ~0.2 MB per 30 s (~500 MB/day), mostly AP per-connection traffic records. Keep it off (CT 100 disk headroom — see the ROADMAP risk note).

---

## Verification (2026-10-04)

- `archives.log` showed lines from `192.168.0.100` and `192.168.0.101` (while `logall` was temporarily on).
- `wazuh-analysisd.state` showed events received with **0 dropped**.
- `wazuh-logtest` decoded a sample AP traffic line with the custom decoder below.

---

## Custom decoder

**File:** `/var/ossec/etc/decoders/local_decoder.xml` on CT 100.  
Decode only — **no rule**, so traffic lines stay level 0 and do not alert or reach the dashboard.

```xml
<decoder name="omada-ap-traffic">
  <prematch>^[\d+.\d+] AP MAC=</prematch>
</decoder>

<decoder name="omada-ap-traffic-fields">
  <parent>omada-ap-traffic</parent>
  <regex>AP MAC=(\S+) MAC SRC=(\S+) IP SRC=(\S+) IP DST=(\S+) IP proto=(\d+) SPT=(\d+) DPT=(\d+)</regex>
  <order>ap_mac, srcmac, srcip, dstip, protocol, srcport, dstport</order>
</decoder>
```

**Fields:** `ap_mac`, `srcmac`, `srcip`, `dstip`, `protocol`, `srcport`, `dstport`

**Sample line format** (placeholders, not real MACs):

```
Oct  4 22:12:09 192.168.0.101 [<epoch.nanos>] AP MAC=<ap-mac> MAC SRC=<client-mac> IP SRC=192.168.10.110 IP DST=172.217.119.4 IP proto=6 SPT=33552 DPT=443
```

---

## Known issue — AP timestamps 1 hour behind

AP-embedded syslog timestamps run 1 hour behind (UTC-5 instead of EDT UTC-4), even though the Omada site timezone is Eastern with DST Auto and NTP is `129.6.15.28` (NIST). Likely AP firmware lacking DST support; firmware update pending. Cosmetic for Wazuh, which uses receive time.

---

## Still open

1. Capture a real Omada Wireless IDS syslog line, then add a decoder and a **level-12** rule so it surfaces in the planned Lab Watch Wazuh attention summary (threshold level >= 12).
2. Decide whether to allow Guest `192.168.30.0/24` in `allowed-ips`.

---

*Written 2026-10-04 from CT 100 verification. Secrets stay on the guest.*
