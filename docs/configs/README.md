# Config files

Scripts, decoders, and rules live in this tree as files. Docs under `docs/services/` and `docs/phases/` link here instead of pasting those files in full.

Each system has its own subfolder. `.gitkeep` stays so the directory exists even when a clone has no system files yet.

## proxmox

| File | Purpose |
|------|---------|
| [pve-ct-notes.sh](proxmox/pve-ct-notes.sh) | Nightly rewrite of each LXC container's Proxmox Notes. Install and cron steps: [proxmox-ct-notes.md](../services/proxmox-ct-notes.md). |
