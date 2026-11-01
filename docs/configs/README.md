# Config files

Files under `docs/configs/` are organized by platform, then by process:

```
docs/configs/<platform>/<process>/
```

Docs under `docs/services/` and `docs/phases/` link to these files. Secrets are never committed: no keys, passwords, `authd.pass`, or `client.keys`.

`.gitkeep` is added only in a directory that would otherwise be empty.

## proxmox

| Path | Purpose |
|------|---------|
| [host-scripts/pve-ct-notes.sh](proxmox/host-scripts/pve-ct-notes.sh) | Nightly rewrite of each LXC container's Notes. |
| [cron/pve-ct-notes.cron](proxmox/cron/pve-ct-notes.cron) | Cron line for that script (`15 3 * * *`). |
| [sync/](proxmox/sync/README.md) | Placeholder for future synchronization jobs. |

Install and behavior: [proxmox-ct-notes.md](../services/proxmox-ct-notes.md).

## wazuh

These subfolders land with #43. They are not in this branch yet.

| Path | Purpose |
|------|---------|
| `wazuh/decoders/` | Wazuh decoder XML. |
| `wazuh/rules/` | Wazuh rule XML. |
| `wazuh/tests/` | Sample logs and `wazuh-logtest` output. |
| `wazuh/ossec-conf/` | Sanitized `ossec.conf` backups only. No keys, passwords, `authd.pass`, or `client.keys`. |
