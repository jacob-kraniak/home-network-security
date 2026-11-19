# INSTALL-STEPS: Omada → Wazuh → Grok Bot real-time pipeline

**For:** Jacob, by hand. No bot touches the rack. **Drafted:** 2026-11-17 (ET).
**Hosts:** `.176` = Proxmox node `debian` (collector, push, checker). `.178` = **CT 100**, the Wazuh 4.8.2 manager (decoders, rules, integration). CT 101 = Omada controller (UI only).
Paths in the steps below are repo paths. Copy them onto the hosts however you like, for example `git clone` on .176 and then `pct push 100 <src> <dst>`.

---

## Branch and commit

- Branch: `feat/omada-wazuh-realtime`
- Commit message:

```
feat(wazuh): Omada real-time rules, Grok Bot integration, RF collector

- Add omada_realtime_rules.xml (100620-100649): device up/down, AP isolated,
  channel change, radar, rogue DHCP, gateway attacks, failed client connects,
  global controller events (node down, primary/secondary switch, cloud access
  failure, too many incidents, backup/log/mail failures), audit login
  failures, audit refinements; per-client (5/10 min) and per-AP (10/10 min)
  disconnect frequency rules
- Extend omada_controller_decoders.xml: device/client tags, rssi, reason,
  channel from/to; tag rule 100603 with omada_client_offline
- Add custom-grokbot Wazuh integration + ossec.conf snippet (secrets in env file)
- Add omada-event-inventory.md, omada-webhook-evaluation.md, omada-log-inventory.py
- Add docs/services/omada-log-inventory/: public Omada alert/event dictionary
  (19 global, 82+80 site types, audit categories) built from a live
  controller capture by docs/configs/omada/build-omada-dictionary.py
- omada-controller parent decoder: accept multi-word controller names
- Add lab-status-collect.py (per-radio RF + 24h disconnects) and lab-status-push.sh
- Tested with wazuh-logtest on a disposable 4.8.2 manager

Assisted-by: Grok Bot (Ship Desk)
Approved-by: Jacob Kraniak <jacob-kraniak@users.noreply.github.com>
```

---

## A. CT 100 (.178): decoders and rules

1. **Back up**, then run the collision check (both greps must print nothing new):
   ```bash
   ts=$(date +%Y%m%d-%H%M)
   cp -a /var/ossec/etc/decoders /root/decoders.bak-$ts
   cp -a /var/ossec/etc/rules    /root/rules.bak-$ts
   cp -a /var/ossec/etc/ossec.conf /root/ossec.conf.bak-$ts
   grep -rn 'id="1006[2-4][0-9]"' /var/ossec/etc/rules/         # must be empty
   grep -rn 'name="custom-grokbot"\|<integration>' /var/ossec/etc/ossec.conf   # see note below
   ```
   Note: if the second grep shows an existing `<integration>` block, that's what fed the "Wazuh alert webhook" routine on Oct 30. It isn't in the repo. Write down its `<name>` and `<level>`/`<group>`, and keep or replace it on purpose, so you don't end up sending everything twice.
2. **Copy** these repo files onto CT 100:
   `docs/configs/wazuh/decoders/omada_controller_decoders.xml`, `docs/configs/wazuh/rules/omada_controller_rules.xml`, `docs/configs/wazuh/rules/omada_realtime_rules.xml`, `docs/configs/wazuh/tests/omada_controller_samples.log`, `docs/configs/wazuh/tests/omada_realtime_samples.log`
3. **Install:**
   ```bash
   install -o wazuh -g wazuh -m 660 omada_controller_decoders.xml /var/ossec/etc/decoders/
   install -o wazuh -g wazuh -m 660 omada_controller_rules.xml omada_realtime_rules.xml /var/ossec/etc/rules/
   /var/ossec/bin/wazuh-analysisd -t          # prints nothing on success
   ```
4. **Logtest** (expected rule IDs, in order):
   ```bash
   cat omada_controller_samples.log omada_realtime_samples.log | /var/ossec/bin/wazuh-logtest 2>&1 | grep -E "^\s+id: '"
   ```
   - Lines 1–24 (old samples): `100604, 100601, 100605, (AP traffic, no rule), 100601, 100601, 100606, 100602, 100602, 100602, 100603, 100635, 100608, 100609, 100605, 100607, 100601, 100604, 100625, 100607, 100607, 100601, 100606, 100601`. Two lines changed on purpose versus the Nov 1 run: line 12 is now 100635 (short session) and line 19 is now 100625 (rogue DHCP).
   - Lines 25–61 (new samples): `100635, 100603, 100636, 100603, 100635, 100603, 100603, 100603, 100603, 100637, 100620, 100622, 100623, 100623, 100638, 100624, 100621, 100625, 100626, 100629, 100648, 100643, 100644, 100642, 100634, 100648, 100649, 100630, 100631, 100645, 100646, 100632, 100602, 100632, 100643, 100622, 100628` (rerun 2026-11-18). Lines 60–61 are guessed `DEV_RECONN` and `OSG_LAN_IP_CONFLICT` lines. Lines 57–59 use a 4-word controller name (`Omada Home Lab Controller`) to test the multi-word header fix. With the old parent decoder, those 3 lines didn't decode.
   - Reference output: `docs/configs/wazuh/tests/omada_realtime_logtest.txt`
   - Lines 35–45, 50–56 and 60–61 use **guessed** wording. That includes the global lines (node down, primary/secondary switch, cloud access, too many incidents, backup failed) and the audit login-failed lines. Once a real line of that type shows up in `/var/ossec/logs/archives/archives.log`, run it through `wazuh-logtest` the same way, and fix the rule if it lands on 100619.
5. **Apply:** `systemctl restart wazuh-manager`, then `tail -n 50 /var/ossec/logs/ossec.log | grep -i -E "error|warn"`.

## B. CT 100 (.178): real-time integration to Grok Bot

6. **Script:**
   ```bash
   install -o root -g wazuh -m 750 custom-grokbot /var/ossec/integrations/custom-grokbot
   head -1 /var/ossec/integrations/custom-grokbot   # must be /var/ossec/framework/python/bin/python3
   ```
7. **Secrets file.** You type the values; they never go in chat or the repo:
   ```bash
   install -o root -g wazuh -m 640 /dev/null /var/ossec/etc/grokbot-webhook.env
   nano /var/ossec/etc/grokbot-webhook.env
   #   GROKBOT_WEBHOOK_URL=https://<Wazuh alert webhook routine URL>
   #   GROKBOT_WEBHOOK_KEY=<its key>
   #   (optional) GROKBOT_AUTH_HEADER=Authorization  GROKBOT_AUTH_SCHEME=Bearer
   #   (optional) GROKBOT_DEDUP_SECONDS=300  GROKBOT_MAX_PER_MINUTE=20
   ```
   Check which header the routine expects. The default is `Authorization: Bearer <key>`.
8. **ossec.conf:** paste Block A from `docs/configs/wazuh/ossec-conf/integration-grokbot.xml` inside `<ossec_config>` (group `omada`, level ≥ 6, JSON). Then run `systemctl restart wazuh-manager`.
9. **Test end to end** (temporary local file, removed afterwards):
   ```bash
   # add inside <ossec_config>, restart, then:
   #   <localfile><log_format>syslog</log_format><location>/root/omada-test.log</location></localfile>
   grep '\[ap:.*was disconnected' omada_realtime_samples.log >> /root/omada-test.log
   sleep 10; tail -n 5 /var/ossec/logs/integrations.log   # expect: custom-grokbot: sent rule 100620 level 8 -> HTTP 2xx
   # then remove the <localfile> block and restart
   ```
   If it fails, `integrations.log` shows `HTTP <code>` or an error class, never the URL or key.

9b. **Find out whether global lines arrive at all.** Global syslog is already on (screenshot 2026-11-18), but no clearly global line has shown up in Wazuh. Run this after step 5, so the new decoder is live:
   ```bash
   # 1. In ossec.conf <global>, set <logall>yes</logall>, then: systemctl restart wazuh-manager
   # 2. In the Omada UI: log out, try ONE wrong password, log in (Global audit: Account / User Activity)
   # 3. Every raw line from the controller in the last few minutes (OMADA_CONTROLLER_IP = CT 101's address):
   grep -a 'OMADA_CONTROLLER_IP' /var/ossec/logs/archives/archives.log | tail -n 30
   #    Lines whose header is NOT "1 <date> <time> Omada ... - - - " are the ones the parent decoder can't see:
   grep -a 'OMADA_CONTROLLER_IP' /var/ossec/logs/archives/archives.log | grep -av ' 1 20[0-9][0-9]-[0-9-]* [0-9:]* Omada .* - - - ' | tail
   # 4. Paste one login line (text after "->OMADA_CONTROLLER_IP ") into /var/ossec/bin/wazuh-logtest:
   #    expect decoder omada-controller, rule 100609 (success) or 100648 (failure)
   # 5. Set <logall>no</logall> again and restart (archives grow fast)
   ```
   Interpreting the result:
   - Login lines are in `archives.log` and decode: global audit works, and the missing global alerts/events are simply rare.
   - Lines are present but step 3's second grep shows them: the header differs. Paste two of them (redact the name suffix and IPs) and the parent decoder gets a second prematch.
   - No lines at all: the controller isn't sending global logs, despite the setting. Check Global View > Logs for the event, then Omada's *Sending Global Logs to Log Server Failed* event.

## C. Omada UI (CT 101): global level already done; site level to check

10. Follow the **UI checklist** at the end of `docs/services/omada-event-inventory.md`. Short version:
    - ✔ **Global View > Logs > Setting > Advanced:** **already done**. Remote Logging is enabled to the Wazuh manager (CT100), port 514 (screenshot 2026-11-18). This is the setting that decides global syslog; the notification JSON has no syslog field.
    - **Global Alerts/Events tabs:** keep the types that have a Wazuh rule switched on (table A of omada-event-inventory.md). *User Login Failed* and *Running Out Of Storage Space* don't exist on this controller.
    - **Global webhook master switch:** it's off. Leave it off. No per-type webhook flag sends anything until it's on.
    - ✔ **Global Audit Logs tab:** **already done**. All 16 categories are ticked, webhook off. Controller login monitoring comes from Account / User Activity (inference; rules 100648/100649).
    - **Site > Logs > Setting:** Advanced (same server, **More Detail Logs** on), then Events > Client (online/offline/roam/connection failed) and Device types (disconnected/connected, isolated, channel changed, radar, rogue DHCP, attack, IP conflict, loop), plus all site audit categories.
    - **History Data Retention:** client history on.

## D. Proxmox .176: collector, push, checker

11. **Collector** (replaces the current copy; same env file `/root/secrets/lab.env`, read-only Omada Open API app):
    ```bash
    cp /usr/local/bin/lab-status-collect.py /root/lab-status-collect.py.bak-$(date +%Y%m%d)
    install -m 0755 docs/configs/lab-watch/lab-status-collect.py /usr/local/bin/lab-status-collect.py
    /usr/local/bin/lab-status-collect.py
    python3 -c "import json;d=json.load(open('/var/lib/lab-watch/lab-status.json'));o=d['omada'] or {};print('errors',d['errors']);print('rf aps',len(o.get('rf') or []));print('disc',(o.get('disconnects_24h') or {}).get('total'))"
    ```
    `disconnects_24h.total` stays 0 until *Client Offline (Wireless)* is enabled as an Event at the site (step 10).
12. **Push script and secrets:**
    ```bash
    install -m 0755 docs/configs/lab-watch/lab-status-push.sh /usr/local/bin/lab-status-push.sh
    install -d -m 700 /root/secrets
    install -m 600 docs/configs/lab-watch/labwatch-push.env.example /root/secrets/labwatch-push.env
    nano /root/secrets/labwatch-push.env     # set LABWATCH_PUSH_URL / LABWATCH_PUSH_KEY ("Lab status ingest" webhook)
    stat -c '%a %U' /root/secrets/labwatch-push.env    # must print: 600 root
    ```
13. **Dry run, then one real push:**
    ```bash
    /usr/local/bin/lab-status-push.sh --dry-run     # collects + validates, no POST
    /usr/local/bin/lab-status-push.sh               # expect: pushed N bytes to <host> (HTTP 2xx)
    ```
14. **Cron** (root crontab on .176). Same times as the existing collect/publish, so the ingest routine wakes twice a day. Tighten later if Lab Watch wants it:
    ```cron
    CRON_TZ=America/New_York
    20 6,21 * * * /usr/local/bin/lab-status-push.sh >>/var/log/lab-status-push.log 2>&1
    ```
    `lab-status-publish.sh` (labdrop SFTP) can keep running alongside. The collector only overwrites `/var/lib/lab-watch/lab-status.json`.
15. **Check both Omada log levels** (read-only):
    ```bash
    install -m 0755 docs/configs/omada/omada-log-inventory.py /usr/local/bin/omada-log-inventory.py
    /usr/local/bin/omada-log-inventory.py > /root/omada-log-inventory-$(date +%F).md && less /root/omada-log-inventory-$(date +%F).md
    ```
    Expect `Remote logging enabled: yes` under **Global View** (already confirmed by screenshot) and under the site. The global table should list 19 types, 2 alerts, `Webhook master switch: no`, and `Webhook effective: no` on every row. Don't commit this output: it lists your site, your webhook names and your per-type settings. The public dictionary in `docs/services/omada-log-inventory/` records only which types exist; regenerate it with `build-omada-dictionary.py` if the controller's list changes.

## Rollback

- CT 100: restore `/root/{decoders,rules}.bak-<ts>` and `ossec.conf.bak-<ts>`, delete `/var/ossec/integrations/custom-grokbot` and `/var/ossec/etc/grokbot-webhook.env`, then `systemctl restart wazuh-manager`.
- .176: restore `/root/lab-status-collect.py.bak-*` to `/usr/local/bin/`, remove the push cron line.
- Omada: untick the added site types and global audit categories. The remote log server settings can stay.
