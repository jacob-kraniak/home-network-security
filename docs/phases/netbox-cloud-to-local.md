# NetBox Cloud → Local Import

**Status:** Import/reconcile path remains open; **SoT flipped 2026-09-21** (on-prem authoritative; Cloud archive)  
**Local (SoT):** `http://192.168.0.200:8000` — NetBox Community v4.7.0 / `v4.7-5.1.1` on CT 101  
**Cloud:** private NetBox Cloud instance — **archive / reference only** (URL not repeated here; already in older docs)  
**Issue:** [#28](https://github.com/jacob-kraniak/home-network-security/issues/28)

> **Authority note (Jacob GO 2026-09-21):** On-prem NetBox is IPAM SoT **now**. This runbook remains the historical Cloud→local import path for reconcile; do not treat Cloud as authoritative. No live sync from bots without Jacob yes.

Cloud Free does not give a usable `pg_dump`. Official docs cover OSS → Cloud, not the reverse. Path is **REST API export → JSON on disk → REST API import**. Tokens stay off this repo and off chat pastes.

Free Cloud cap is **10k API requests / month**. Dump once to files; do not re-walk Cloud during import retries.

---

## Tokens (you create these)

1. Cloud: Admin → API Tokens → token with **read** on the objects below.
2. Local: Admin → API Tokens → token with **write**.
3. On a workstation that can reach **both** Cloud HTTPS and `192.168.0.200`:

```bash
export NB_CLOUD_URL='https://YOUR-INSTANCE.cloud.netboxapp.com'
export NB_CLOUD_TOKEN='nbt_...'          # never commit
export NB_LOCAL_URL='http://192.168.0.200:8000'
export NB_LOCAL_TOKEN='...'              # never commit
```

Probe counts (safe, few requests):

```bash
for path in \
  dcim/sites dcim/racks dcim/manufacturers dcim/device-types dcim/device-roles dcim/devices \
  dcim/interfaces dcim/cables \
  ipam/vlan-groups ipam/vlans ipam/prefixes ipam/ip-addresses \
  extras/tags wireless/wireless-lans virtualization/clusters virtualization/virtual-machines
do
  echo -n "$path cloud="
  curl -sS -H "Authorization: Token $NB_CLOUD_TOKEN" "$NB_CLOUD_URL/api/$path/?limit=1" | python3 -c 'import sys,json; print(json.load(sys.stdin).get("count"))'
  echo -n "$path local="
  curl -sS -H "Authorization: Token $NB_LOCAL_TOKEN" "$NB_LOCAL_URL/api/$path/?limit=1" | python3 -c 'import sys,json; print(json.load(sys.stdin).get("count"))'
done
```

Paste **counts only** back into this project. That is the baseline before any write.

---

## Import order (dependencies)

Create on local in this order. Slugs must match Cloud.

1. `extras/tags` (and custom fields if any)
2. `dcim/regions`, `site-groups`, `sites`, `locations`
3. `dcim/rack-roles`, `racks`
4. `dcim/manufacturers`, `platforms`, `device-roles`, `device-types`
5. `tenancy/tenants`, `contacts` (if used)
6. `ipam/rirs`, `aggregates`, `vrfs`, `vlan-groups`, `vlans`, `prefixes`, `ip-ranges`
7. `dcim/devices`
8. `dcim/interfaces`
9. `ipam/ip-addresses` (assign to interfaces by name, not Cloud PK)
10. `wireless/wireless-lans`, `wireless-links`
11. `dcim/cables` last (needs both ends)
12. `virtualization/*` if anything exists in Cloud

Do **not** copy primary keys. Resolve FKs by slug/name. Skip `core/object-changes` (changelog noise).

Expected Cloud ballpark from [NetBox-Inventory-Progress.md](../NetBox-Inventory-Progress.md): ~53 devices, 3 VLANs, 3 prefixes, `key:value` tags.

---

## Dump Cloud to disk first

On the workstation, not on the public repo:

```bash
mkdir -p ~/netbox-migrate/cloud && cd ~/netbox-migrate/cloud

python3 - <<'PY'
import json, os, urllib.request

base = os.environ["NB_CLOUD_URL"].rstrip("/")
token = os.environ["NB_CLOUD_TOKEN"]
headers = {"Authorization": f"Token {token}", "Accept": "application/json"}

def all_pages(path):
    url = f"{base}/api/{path}/?limit=200"
    out = []
    while url:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=60) as r:
            body = json.load(r)
        out.extend(body.get("results", []))
        url = body.get("next")
    return out

endpoints = [
    "extras/tags",
    "dcim/sites", "dcim/locations", "dcim/racks",
    "dcim/manufacturers", "dcim/platforms", "dcim/device-roles", "dcim/device-types",
    "dcim/devices", "dcim/interfaces", "dcim/cables",
    "ipam/vlan-groups", "ipam/vlans", "ipam/prefixes", "ipam/ip-addresses",
    "wireless/wireless-lans",
    "virtualization/cluster-types", "virtualization/clusters", "virtualization/virtual-machines",
]
for path in endpoints:
    rows = all_pages(path)
    name = path.replace("/", "_") + ".json"
    with open(name, "w") as f:
        json.dump(rows, f, indent=2)
    print(f"{path} {len(rows)}")
PY
```

Keep `~/netbox-migrate/` local / gitignored. It contains live IPs and MACs.

---

## Import

Prefer a small pynetbox loader that maps slugs instead of raw POST of Cloud JSON (nested IDs will 400). Do core taxonomy by hand in the local UI if the dump is small: 1 site, 3 VLANs, 3 prefixes, a handful of roles/types — then script devices + IPs.

After each layer:

```text
cloud count == local count  (or document the delta)
```

When devices, prefixes, VLANs, and tags match (or deltas are documented):

1. Point `netbox-nmap-scan` (if the private repo is still in play) at `NB_LOCAL_URL` only.
2. **SoT docs:** already flipped 2026-09-21 — on-prem authoritative; Cloud archive. Keep `GROK-WORKSPACE.md` / `network-overview.md` / `NetBox-Inventory-Progress.md` aligned if wording drifts.
3. Check [phase-2-close-linkedin.md](phase-2-close-linkedin.md).

---

## Do not

- Commit dump JSON or tokens
- `compose down -v` on CT 101
- Re-scan Cloud on every retry (use the files)
- Enable PVE SDN NetBox IPAM as part of this import
- WAN-publish `:8000`
- Treat Cloud as authoritative after the 2026-09-21 SoT flip
