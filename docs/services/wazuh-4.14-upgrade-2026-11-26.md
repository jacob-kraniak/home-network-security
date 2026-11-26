# Wazuh 4.8.2 → 4.14.11 upgrade

**Verified:** 2026-11-26 (ET)
**Host:** CT 100
**Related:** [ROADMAP § Phase 2](../ROADMAP.md#phase-2-self-hosted-services-build-in-progress-) · [#44](https://github.com/jacob-kraniak/home-network-security/issues/44) · [#57](https://github.com/jacob-kraniak/home-network-security/issues/57) · [#64](https://github.com/jacob-kraniak/home-network-security/issues/64)

No addresses, MACs, SSIDs, or credentials in this note.

## Result

CT 100 moved from Wazuh **4.8.2** to **4.14.11-1** for `wazuh-indexer`, `wazuh-manager`, and `wazuh-dashboard`. `filebeat` is **7.10.2-2**. The Wazuh apt repository was disabled after the upgrade. The dashboard is back online.

## Backup

`vzdump 100` was run on Proxmox before the changes.

## Manager changes

- Added the three 4.12+ malicious-ioc CDB lists to `ossec.conf`.
- Aligned `opensearch_dashboards.yml` certificate paths to `wazuh-dashboard*.pem` and the indexer at `127.0.0.1:9200`.
- Rotated the `admin` and `kibanaserver` accounts with `wazuh-passwords-tool.sh`. Password values stay off this page.

## Agents

| ID | Name | State on 2026-11-26 |
|----|------|---------------------|
| 002 | JKALI01 | Active |
| 003 | pve-debian | Upgraded to 4.14.11 and Active |
| 004 | ct101-portainer | Active |
| 005 | bazzite | Active |
| 006 | Christines_Laptop | Stale duplicate of 007. Removal is still a manual decision ([#57](https://github.com/jacob-kraniak/home-network-security/issues/57)). |

The package version recorded for an agent is 003 at 4.14.11. Agents 002, 004, and 005 are recorded as Active only. Agent 007's connection state is outside this check.

Agent 003 returned to Active after two edits on that host:

- Commented out the `cdrom://` line in apt `sources.list`.
- Removed a misplaced `<vulnerability-detection>` block and a malformed `<github>` block from the agent `ossec.conf`.

## Follow-up

`wazuh-analysisd -t` flagged duplicate rule **100600** between `local_rules.xml` and `omada_controller_rules.xml`. Clean that up before the [#64](https://github.com/jacob-kraniak/home-network-security/issues/64) install. That `wazuh-analysisd -t` run failed on the duplicate.
