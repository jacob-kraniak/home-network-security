# Omada alert/event dictionary: Site level

Types configured under **(site) > Logs > Setting > Alerts / Events**. This is where nearly everything about your network shows up: clients, APs, switches, gateways, WAN, and attacks. If you use Omada as a log source, start here.

Captured 2026-11-18 from an Omada Software Controller (see [README.md](README.md#capture)). Columns are explained in [README.md](README.md#columns). Per-instance enable, email and webhook state is not recorded here.

Things to know about the data:

- **Four keys appear in both lists** (marked ⇄): `DEV_DISCONN`, `AP_ISOLATE`, `DEV_C_DSYNC`, `LOG_ONU_IS_OFFLINE`. The controller lets you classify the same type as an alert, an event, or both. In syslog you'll see the same message text either way; the key, not the list, is what identifies it.
- **Shared shortMsg:** `OSW_TOPO_C` (alert) and `OSW_STP_FWD` (event) are both labelled *STP Topology Changed*. Use the key to tell them apart.
- **shortMsg is verbatim**, including the controller's own spelling, spacing and punctuation: *Gateway’s* (curly apostrophe), trailing full stops on the *… Failed Alert.* types, *Replace action succeed*. One alert has the level spelled **`Critial`** (`OSW_KEY_HEALING_MGMTVLAN_CREATE_FAILED`). Match it as-is if you filter on level.
- **Alert levels used:** Warning, Error, Information, `Critial`. Events have no level.
- **Not in any list:** RSSI, SNR, deauth/disassociation reason codes, channel utilization, interference, rogue AP scans and WIDS findings. No notification type carries these. Get them from the Open API (see [README.md](README.md#what-the-logs-dont-tell-you)).
- **Versus TP-Link's guide:** the guide's site table has 116 keys, and 38 of them aren't on this controller. 29 are *Operation* types: adoptions, forget/move, manual upgrades, reboots, vouchers, form auth, SSID/WLAN changes, client block/unblock, switch stacks. This version appears to record those as Audit Logs instead (inference). The other 9 are Device types: the "up/OK" counterparts `OSG_WAN_UP`, `OSG_IPSEC_OK`, `OSG_PPPOE_OK`, `OSG_C_VPN_OK`, `DEV_READOPT_OK`, plus online-upgrade results `DEV_UP_OL_OK`, `DEV_UP_OL_FL`, `STACK_UP_OL_OK`, `STACK_UP_OL_FL`. In the other direction, **80 captured keys aren't in the guide**: OLT/ONU (GPON), switch self-healing, IntelliRecover, monitor-link, STP/LAG, QoS, DHCP snooping/ARP detection, fan/PSU, OpenVPN/SD-WAN/MAP-E/DS-Lite modules, `DEV_RECONN` and more. One shared key is renamed: `OSG_PRI_WAN_UP` is *Primary WAN Takes Effect* here and *Primary WAN Recovered* in the guide. Per-key detail: the *TP-Link guide* column below, and `meta.counts` in the JSON.

<!-- GENERATED:START (build-omada-dictionary.py) -->
**82 alerts + 80 events = 162 rows, 158 unique keys** (4 keys appear in both lists, marked ⇄: `AP_ISOLATE`, `DEV_C_DSYNC`, `DEV_DISCONN`, `LOG_ONU_IS_OFFLINE`).

### Homelab Wi-Fi troubleshooting quick pick

| Key | shortMsg | Kind | Why |
|---|---|---|---|
| `W_C_DISCONN` | Client Offline (Wireless) | event | A wireless client left. The syslog line carries the SSID, AP, connected time and traffic, but no reason code or RSSI. Repeats in a short window are the main signal of flapping clients. |
| `AP_C_OK` | Client Online (Wireless) | event | A wireless client joined (SSID, AP, channel). Pair it with W_C_DISCONN to measure session length. |
| `W_C_ROAM` | Client Roaming (Wireless) | event | A client moved between APs; the line includes both APs and channels. Frequent back-and-forth roams point at overlapping coverage or a sticky client. |
| `AP_C_FL` | Client Connection Failed (Wireless) | event | A wireless client tried and failed to connect (wrong key, auth timeout, RADIUS, and similar). Bursts from one client often mean a saved wrong password or a weak-signal edge. |
| `AP_CH_C` | EAP Channel Changed | event | An AP changed channel, usually auto-channel reacting to interference. Several in an hour on one AP suggests a crowded band. |
| `AP_RADAR` | EAP Detected Radar | event | DFS radar detected on a 5 GHz channel. The AP must vacate the channel, and connected clients drop or move. |
| `AP_ISOLATE` | EAP Isolated | alert + event | The AP lost its wired uplink (often a mesh fallback). Clients on it may lose connectivity. |
| `DEV_DISCONN` | Device Disconnected | alert + event | The controller lost contact with an adopted device (AP, switch, gateway, OLT). Appears in both the alert and the event list. |
| `DEV_RECONN` | Device Reconnected | event | A device reconnected after a disconnect. Useful for measuring outage length with DEV_DISCONN. |
| `DEV_CONN` | Device Connected | event | A device connected to the controller. |

**None of these types carries RSSI, SNR or a deauth/disassociation reason code.** For signal, channel utilization and interference, poll the Open API instead (see [README.md](README.md#what-the-logs-dont-tell-you)).

### Site alerts

| # | Key | shortMsg (verbatim) | Kind | Module | Level | Device types | Client types | Webhook-capable | TP-Link guide | What it means / why you'd care |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `OSW_DET_STORM` | Switch Detected Storm | alert | Device | Warning | switch | — | yes | same name | A broadcast/multicast storm crossed the storm-control threshold. |
| 2 | `OSW_DET_LOOP` | Detected Loops | alert | Device | Warning | switch | — | yes | same name | Switch loop detection fired. Loops can take down the whole LAN. |
| 3 | `OSW_PB` | Port Blocked | alert | Device | Warning | switch | — | yes | same name | A switch port was blocked (loop prevention). |
| 4 | `OSW_TOPO_C` | STP Topology Changed | alert | Device | Information | switch | — | yes | same name | STP topology change (alert list). Shares its shortMsg with OSW_STP_FWD. |
| 5 | `OSG_WAN_DOWN` | WAN is down | alert | Device | Warning | gateway | — | yes | same name | A WAN link went down. |
| 6 | `WAN_LINK_BACKUP` | WAN Link Backup | alert | Device | Information | gateway | — | yes | same name |  |
| 7 | `WAN_ONLINE_DETECTION` | WAN Online Detection | alert | Device | Information | gateway | — | yes | same name |  |
| 8 | `PHYSICAL_PORT_CONNECTION` | Physical Port Connection | alert | Device | Information | gateway | — | yes | not listed |  |
| 9 | `OSG_PPPOE_FL` | PPPoE Connection Failed | alert | Device | Error | gateway | — | yes | same name | PPPoE session to the ISP failed. |
| 10 | `WAN_IP_O_F` | WAN IP address Obtaining Failed | alert | Device | Error | gateway | — | yes | same name | The gateway could not obtain a WAN IP (DHCP/PPPoE upstream problem). |
| 11 | `OSG_IPSEC_FL` | IPsec Connection Disconnected | alert | Device | Warning | gateway | — | yes | same name | Site-to-site IPsec tunnel went down. |
| 12 | `OSG_C_VPN_FL` | PPTP/L2TP Client Connection Failed | alert | Device | Warning | gateway | — | yes | same name |  |
| 13 | `ADOPTED_ACCOUNT_DELETED` | OLT Adopted Account Deleted | alert | Device | Warning | olt | — | yes | not listed |  |
| 14 | `PASSWORD_CHANGE_OF_ADOPTED_ACCOUNT` | OLT Adopted Account Password Changed | alert | Device | Warning | olt | — | yes | not listed |  |
| 15 | `LEVEL_CHANGE_OF_ADOPTED_ACCOUNT` | OLT Adopted Account Level Changed | alert | Device | Warning | olt | — | yes | not listed |  |
| 16 | `LOG_ONU_IS_OFFLINE` ⇄ | ONU Disconnected | alert | Device | Warning | — | — | yes | not listed | ONU (fiber terminal) went offline. Appears in both lists. Only relevant with an Omada OLT. |
| 17 | `LOG_ONU_LOSS_OF_SIGNAL` | ONU Loss of Signal | alert | Device | Warning | — | — | yes | not listed |  |
| 18 | `LOG_ONU_LOSS_OF_FRAME` | ONU Loss of Frames | alert | Device | Warning | — | — | yes | not listed |  |
| 19 | `LOG_ONU_LOSS_OF_PLOAM` | ONU Loss of PLOAM | alert | Device | Warning | — | — | yes | not listed |  |
| 20 | `LOG_ONU_SIGNAL_FAILED` | ONU Signal Transmission Failed | alert | Device | Warning | — | — | yes | not listed |  |
| 21 | `LOG_ONU_STARTUP_FAILED` | ONU Startup Failed | alert | Device | Warning | — | — | yes | not listed |  |
| 22 | `LOG_ONU_DYING_GASP` | ONU Dying Gasp | alert | Device | Warning | — | — | yes | not listed | ONU reported loss of power before going offline. Only relevant with an Omada OLT. |
| 23 | `DST_C_FAIL` | DST configuration error. | alert | System | Error | — | — | yes | same name | Daylight-saving-time configuration error; timestamps may be off. |
| 24 | `DEV_DISCONN` ⇄ | Device Disconnected | alert | Device | Error | olt, gateway, ap, switch | — | yes | same name | The controller lost contact with an adopted device (AP, switch, gateway, OLT). Appears in both the alert and the event list. |
| 25 | `AP_ISOLATE` ⇄ | EAP Isolated | alert | Device | Error | ap | — | yes | same name | The AP lost its wired uplink (often a mesh fallback). Clients on it may lose connectivity. |
| 26 | `DEV_C_DSYNC` ⇄ | Device Configurations Desynchronized | alert | Device | Error | gateway, ap, switch | — | yes | same name | Device config no longer matches what the controller pushed. Appears in both lists. |
| 27 | `OSG_ATK` | Gateway Detected Attack | alert | Device | Warning | gateway | — | yes | same name | The gateway's attack defense detected an attack (flood, scan and similar). |
| 28 | `OSG_SF_ATK` | Gateway Detected Stationary Flood Attack | alert | Device | Warning | gateway | — | yes | same name | Gateway detected a stationary flood attack. |
| 29 | `OSG_ARP_ATK` | Gateway Detected ARP Conflicts | alert | Device | Warning | gateway | — | yes | same name | Gateway detected ARP conflicts (possible spoofing or a duplicate IP). |
| 30 | `OSG_LARGE_PING_ATTACK` | Large Ping Attack | alert | Device | Warning | gateway | — | yes | same name | Gateway detected oversized ICMP (ping) traffic. |
| 31 | `OSG_DHCP_LEASE_POOL_EXHAUSTED` | The DHCP lease pool is exhausted | alert | Device | Warning | gateway | — | yes | same name | A DHCP pool has no free leases; new clients can't get an address. |
| 32 | `OSG_ROGUE_DHCP_SERVER_DETECTED` | A rogue DHCP server is detected | alert | Device | Warning | gateway | — | yes | same name | Another DHCP server is answering on a gateway network. Common cause: a consumer router plugged in as a client. |
| 33 | `OSG_IP_CONFLICT_DETECTED` | An IP conflict is detected | alert | Device | Warning | gateway | — | yes | same name | Two hosts are using the same IP address. |
| 34 | `MANAGE_INTERFACE_CHANGED` | OLT Manage Interface Changed | alert | Device | Warning | olt | — | yes | not listed |  |
| 35 | `LOG_CPU_LOAD_EXCEED` | OLT CPU Load Exceed | alert | Device | Warning | olt | — | yes | not listed |  |
| 36 | `LOG_MEM_LOAD_EXCEED` | OLT Memory Load Exceed | alert | Device | Warning | olt | — | yes | not listed |  |
| 37 | `LOG_ONU_SIGNAL_DEGRADE` | ONU Signal Degrade | alert | Device | Warning | — | — | yes | not listed |  |
| 38 | `LOG_ONU_PHYSICAL_EQUIP_ERR_RECEIVED` | ONU Fault PLOAM Received | alert | Device | Warning | — | — | yes | not listed |  |
| 39 | `LOG_ONU_PST_PLOAM_RECEIVED` | ONU PST PLOAM Received | alert | Device | Warning | — | — | yes | not listed |  |
| 40 | `LOG_ONU_UNKNOWN_PLOAM_RECEIVED` | ONU Unknown PLOAM Received | alert | Device | Warning | — | — | yes | not listed |  |
| 41 | `LOG_ONU_TRANSMISSION_INTERFERENCE_THRESHOLD` | ONU TIW Exceed | alert | Device | Warning | — | — | yes | not listed |  |
| 42 | `LOG_ONT_REMOTE_ERROR_INDICATION` | ONU Error Reported(Downstream) | alert | Device | Warning | — | — | yes | not listed |  |
| 43 | `LOG_ONT_ONU_ERROR_INDICATION` | ONU Error Reported(Upstream) | alert | Device | Warning | — | — | yes | not listed |  |
| 44 | `LOG_SERVICE_PROFILE_CAPABILITY_MATCH_FAILED` | ONU Capability Failed to Match Profile | alert | Device | Warning | — | — | yes | not listed |  |
| 45 | `LOG_PORT_INGRESS_REACH` | OLT Limitation of ingress bandwidth | alert | Device | Warning | olt | — | yes | not listed |  |
| 46 | `LOG_PORT_EGRESS_REACH` | OLT Limitation of egress bandwidth | alert | Device | Warning | olt | — | yes | not listed |  |
| 47 | `LOG_BCSTORM_CONTROL_REACH` | OLT Broadcast Storm | alert | Device | Warning | olt | — | yes | not listed |  |
| 48 | `LOG_MCSTORM_CONTROL_REACH` | OLT Multicast Storm | alert | Device | Warning | olt | — | yes | not listed |  |
| 49 | `LOG_UNKSTORM_CONTROL_REACH` | OLT Unicast Storm | alert | Device | Warning | olt | — | yes | not listed |  |
| 50 | `LOG_PORT_STORM_CONTROL_SHUTDOWN` | OLT Port Shutdown (Storm Control) | alert | Device | Warning | olt | — | yes | not listed |  |
| 51 | `AUTO_ADD_MAC_FILTER_FL` | Automatic Add MAC Filtering Allow List Failed | alert | Device | Warning | gateway | — | yes | not listed |  |
| 52 | `REBOOT_RECOVERY` | IntelliRecover - Reboot Recovery Initiated | alert | System | Information | ap | — | yes | not listed | IntelliRecover started an automatic reboot to recover an AP. |
| 53 | `REBOOT_RECOVERY_FAIL` | IntelliRecover - Reboot Recovery Failed | alert | System | Error | — | — | yes | not listed | IntelliRecover reboot did not bring the device back. |
| 54 | `REBOOT_RECOVERY_EXCEED_LIMIT` | IntelliRecover - Retry Limit Exceeded | alert | System | Error | — | — | yes | not listed |  |
| 55 | `DEVICE_MONITOR_STATUS_LINK_DOWN` | Device informed monitor link down | alert | Device | Warning | gateway, ap, switch | — | yes | not listed | A device reported a monitored link down. |
| 56 | `DEVICE_MONITOR_STATUS_LINK_ERROR` | Device informed monitor link error | alert | Device | Warning | gateway, ap, switch | — | yes | not listed |  |
| 57 | `DEVICE_MONITOR_STATUS_DEVICE_ERROR` | Device informed monitor link internal error | alert | Device | Warning | gateway, ap, switch | — | yes | not listed |  |
| 58 | `LAN_CONFLICT_AVOIDANCE` | Gateway’s LAN segment is modified | alert | System | Warning | — | — | yes | not listed | The gateway changed a LAN segment to avoid a conflict (for example with the WAN subnet). |
| 59 | `REPORT_SCHEDULE_REACH_RATE_LIMIT` | Report export Schedule Failure | alert | System | Warning | — | — | yes | not listed |  |
| 60 | `MDNS_RULE_NOT_EFFECT` | The mDNS rules are not working | alert | System | Error | gateway | — | yes | not listed | Configured mDNS reflection rules are not working. |
| 61 | `REPLACE_FAILED` | Replace action failed | alert | Device | Error | ap, switch | — | yes | not listed |  |
| 62 | `OSW_STORM_SHUTDOWN` | Switch Storm Shutdown | alert | Device | Warning | switch | — | yes | not listed | A switch port was shut down by storm control. |
| 63 | `OSW_QOS_VLAN_EXCEED` | Switch Qos for Vlan Rule Exceeded | alert | Device | Warning | switch | — | yes | not listed |  |
| 64 | `OSW_QOS_RULE_EXCEED` | Switch Qos Rule Exceeded | alert | Device | Warning | switch | — | yes | not listed |  |
| 65 | `OSW_PWR_ERR` | Switch Redundant Power Supply Failure | alert | Device | Warning | switch | — | yes | not listed | Switch redundant power supply failure. |
| 66 | `OSW_FAN_ERR` | Switch Fan Failure | alert | Device | Warning | switch | — | yes | not listed | Switch fan failure. |
| 67 | `OSW_KEY_HEALING_MGMTVLAN_DNSV4_CLEAR_FAILED` | Mgmt Vlan DnsV4 Cleared Failed Alert. | alert | Device | Warning | switch | — | yes | not listed |  |
| 68 | `OSW_KEY_HEALING_MGMTVLAN_DNSV6_CLEAR_FAILED` | Mgmt Vlan DnsV6 Cleared Failed Alert. | alert | Device | Warning | switch | — | yes | not listed |  |
| 69 | `OSW_KEY_HEALING_MGMTVLAN_CREATE_FAILED` | Mgmt Vlan Create Failed Alert. | alert | Device | Critial | switch | — | yes | not listed | Switch self-healing could not recreate the management VLAN. The only alert with level 'Critial' (sic) in the capture. |
| 70 | `OSW_KEY_HEALING_MGMTVLAN_CFG_FAILED` | Mgmt Vlan Configured Failed Alert. | alert | Device | Warning | switch | — | yes | not listed |  |
| 71 | `OSW_KEY_HEALING_SYSTEMIP_CFG_FAILED` | System Ip Configured Failed Alert. | alert | Device | Warning | switch | — | yes | not listed |  |
| 72 | `OSW_KEY_HEALING_MGMTVLAN_SET_FAILED` | Mgmt Vlan Set Failed Alert. | alert | Device | Warning | switch | — | yes | not listed |  |
| 73 | `OSW_DHCP_SNOOP_ALERT` | Dhcp snoop alert | alert | Device | Warning | switch | — | yes | not listed | DHCP snooping on a switch flagged an untrusted DHCP server or packet. |
| 74 | `OSW_ARP_DETECTION_ALERT` | Arp detection alert | alert | Device | Warning | switch | — | yes | not listed | ARP inspection on a switch flagged a suspicious ARP packet. |
| 75 | `OSW_INTERFACE_VLANIF_DOWN` | Switch VLAN interface Down Event | alert | Device | Information | switch | — | yes | not listed |  |
| 76 | `OSW_KEY_HEALING_INTF_RECOVER_FAILED` | Netif Healing Recover Failed Alert. | alert | Device | Warning | switch | — | yes | not listed |  |
| 77 | `OSW_KEY_HEALING_GATE_RECOVER_FAILED` | Netif Healing Gate Recover Failed Alert. | alert | Device | Warning | switch | — | yes | not listed |  |
| 78 | `OSW_OUI_BASED_VLAN_NUM_LIMIT_EXCEED` | Switch OUI Based VLAN rules exceeded the maximum simultaneous entry limit | alert | Device | Information | switch | — | yes | same name |  |
| 79 | `OSW_INSTALL_ROLLBACK` | Failed To Upgrade | alert | Device | Warning | switch | — | yes | not listed | A switch firmware upgrade failed. |
| 80 | `OSG_OVPN_OP_ERR` | OpenVPN Operation Failed | alert | Device | Error | gateway | — | yes | not listed |  |
| 81 | `OSG_LAN_IP_CONFLICT` | LAN IP Is Conflict With Other Interfaces | alert | Device | Warning | gateway | — | yes | not listed | A gateway LAN IP overlaps another interface. |
| 82 | `WAN_IP_OBTAIN` | WAN IP address Obtaining | alert | Device | Error | gateway | — | yes | not listed |  |

### Site events

| # | Key | shortMsg (verbatim) | Kind | Module | Device types | Client types | Webhook-capable | TP-Link guide | What it means / why you'd care |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `DEV_IP_C` | Device IP Changed | event | Device | switch, gateway | — | yes | same name | A switch or gateway changed its IP address. |
| 2 | `AP_RADAR` | EAP Detected Radar | event | Device | ap | — | yes | same name | DFS radar detected on a 5 GHz channel. The AP must vacate the channel, and connected clients drop or move. |
| 3 | `AP_CH_C` | EAP Channel Changed | event | Device | ap | — | yes | same name | An AP changed channel, usually auto-channel reacting to interference. Several in an hour on one AP suggests a crowded band. |
| 4 | `AP_C_FL` | Client Connection Failed (Wireless) | event | Client | — | wireless | yes | same name | A wireless client tried and failed to connect (wrong key, auth timeout, RADIUS, and similar). Bursts from one client often mean a saved wrong password or a weak-signal edge. |
| 5 | `OSW_C_1X_OK` | Client Authenticated with 802.1X | event | Client | switch | wired | yes | same name |  |
| 6 | `OSW_C_1X_FL` | 802.1X Authentication Failed | event | Client | switch | wired | yes | same name | 802.1X authentication failed on a switch port. |
| 7 | `OSG_BK_WAN_UP` | Backup WAN Takes Effect | event | Device | gateway | — | yes | same name | Traffic failed over to the backup WAN. |
| 8 | `OSG_IPSEC_FO` | IPsec failover took effect | event | Device | gateway | — | yes | same name |  |
| 9 | `OSG_RC_VPN_OK` | Remote PPTP/L2TP Client Connected | event | Device | gateway | — | yes | same name |  |
| 10 | `OSG_RC_VPN_FL` | Remote PPTP/L2TP Client Connection Failed | event | Device | gateway | — | yes | same name |  |
| 11 | `OSG_RC_VPN_LO` | Remote PPTP/L2TP Client Logged Out | event | Device | gateway | — | yes | same name |  |
| 12 | `OSG_DDNS` | Gateway DDNS Module Information | event | Device | gateway | — | yes | same name |  |
| 13 | `OSG_IPSEC` | Gateway IPsec Module Information | event | Device | gateway | — | yes | same name |  |
| 14 | `OSG_IPV6` | Gateway IPv6 Module Information | event | Device | gateway | — | yes | same name |  |
| 15 | `OSG_PPP` | Gateway PPP Module Information | event | Device | gateway | — | yes | same name |  |
| 16 | `OSG_PPPOE` | Gateway PPPoE Module Information | event | Device | gateway | — | yes | same name |  |
| 17 | `OSG_SSL_VPN` | Gateway SSL VPN Module Information | event | Device | gateway | — | yes | same name |  |
| 18 | `OSG_DHCP_C` | Gateway DHCP Client Module Information | event | Device | gateway | — | yes | same name |  |
| 19 | `OSG_DHCP_S` | Gateway DHCP Server Module Information | event | Device | gateway | — | yes | same name | Gateway DHCP server messages (lease allocated/rejected). High volume. |
| 20 | `LOG_TRAFFIC_CLEAR` | OLT Traffic Cleared | event | Device | olt | — | yes | not listed |  |
| 21 | `LOG_SRV_OK` | Site Logs Sent to Log Server | event | System | — | — | yes | same name |  |
| 22 | `LOG_SRV_FL` | Sending Site Logs to Log Server Failed | event | System | — | — | yes | same name | The controller failed to send site logs to the remote log server. Worth alerting on if syslog is your pipeline. |
| 23 | `LOG_MAIL_OK` | Logs Mailed Automatically | event | System | — | — | yes | same name |  |
| 24 | `LOG_MAIL_FL` | Automatic Logs Mail Failed | event | System | — | — | yes | same name |  |
| 25 | `REBOOT_SC_OK` | Reboot Schedule Executed | event | System | — | — | yes | same name |  |
| 26 | `REBOOT_SC_FL` | Reboot Schedule Execution Failed | event | System | — | — | yes | same name |  |
| 27 | `POE_SC_OK` | PoE Schedule Executed | event | System | — | — | yes | same name |  |
| 28 | `POE_SC_FL` | PoE Schedule Execution Failed | event | System | — | — | yes | same name |  |
| 29 | `REPORT_SENDING_FAILED` | Report Sending Failed | event | System | — | — | yes | same name |  |
| 30 | `REPORT_SCHEDULE_EXECUTED` | Report Schedule Executed | event | System | — | — | yes | same name |  |
| 31 | `REPORT_GENERATION_FAILED` | Report Generation Failed | event | System | — | — | yes | same name |  |
| 32 | `SITE_DEVICE_LIST_MAIL_FL` | Site Device List Schedule Mail Failed | event | System | — | — | yes | same name |  |
| 33 | `SITE_DEVICE_LIST_SCHEDULE_EXECUTED` | Site Device List Schedule Executed | event | System | — | — | yes | same name |  |
| 34 | `INCIDENT_MAILED_FAILED` | Incidents auto mailed failed | event | System | — | — | yes | same name |  |
| 35 | `PORT_SC_OK` | Port Schedule Executed | event | System | — | — | yes | same name |  |
| 36 | `PORT_SC_FL` | Port Schedule Execution Failed | event | System | — | — | yes | same name |  |
| 37 | `SITE_NETWORK_CHECK_MAIL_FL` | Site Network check Mail Failed | event | System | — | — | yes | same name |  |
| 38 | `TERMINAL_MAIL_FL` | Site Terminal Mail Failed | event | System | — | — | yes | same name |  |
| 39 | `DEV_CONN` | Device Connected | event | Device | olt, gateway, ap, switch | — | yes | same name | A device connected to the controller. |
| 40 | `DEV_RECONN` | Device Reconnected | event | Device | olt, gateway, ap, switch | — | yes | not listed | A device reconnected after a disconnect. Useful for measuring outage length with DEV_DISCONN. |
| 41 | `DEV_DISCONN` ⇄ | Device Disconnected | event | Device | olt, gateway, ap, switch | — | yes | same name | The controller lost contact with an adopted device (AP, switch, gateway, OLT). Appears in both the alert and the event list. |
| 42 | `LOG_ONU_IS_ONLINE` | ONU Connected | event | Device | — | — | yes | not listed |  |
| 43 | `LOG_ONU_IS_OFFLINE` ⇄ | ONU Disconnected | event | Device | — | — | yes | not listed | ONU (fiber terminal) went offline. Appears in both lists. Only relevant with an Omada OLT. |
| 44 | `AP_ISOLATE` ⇄ | EAP Isolated | event | Device | ap | — | yes | same name | The AP lost its wired uplink (often a mesh fallback). Clients on it may lose connectivity. |
| 45 | `DEV_C_DSYNC` ⇄ | Device Configurations Desynchronized | event | Device | gateway, ap, switch | — | yes | same name | Device config no longer matches what the controller pushed. Appears in both lists. |
| 46 | `DEV_READOPT_FL` | Automatic Device Readopt Failed | event | Device | olt, gateway, ap, switch | — | yes | same name | The controller could not re-adopt a device automatically. |
| 47 | `W_C_ROAM` | Client Roaming (Wireless) | event | Client | — | wireless | yes | same name | A client moved between APs; the line includes both APs and channels. Frequent back-and-forth roams point at overlapping coverage or a sticky client. |
| 48 | `W_C_DISCONN` | Client Offline (Wireless) | event | Client | — | wireless | yes | same name | A wireless client left. The syslog line carries the SSID, AP, connected time and traffic, but no reason code or RSSI. Repeats in a short window are the main signal of flapping clients. |
| 49 | `AP_C_OK` | Client Online (Wireless) | event | Client | — | wireless | yes | same name | A wireless client joined (SSID, AP, channel). Pair it with W_C_DISCONN to measure session length. |
| 50 | `L_C_DISCONN` | Client Offline (Wired) | event | Client | — | wired | yes | same name | A wired client went offline. |
| 51 | `L_C_CONN` | Client Online (Wired) | event | Client | — | wired | yes | same name | A wired client came online on a switch or gateway port. |
| 52 | `W_C_PRT_OK` | Client Authenticated with Portal (Wireless) | event | Client | — | wireless | yes | same name |  |
| 53 | `W_C_PRT_FL` | Portal Authentication Failed (Wireless) | event | Client | — | wireless | yes | same name | Captive-portal authentication failed (wireless). |
| 54 | `W_C_PRT_EXP` | Client Authentication Expired (Wireless) | event | Client | — | wireless | yes | same name |  |
| 55 | `L_C_PTR_OK` | Client Authenticated with Portal (Wired) | event | Client | — | wired | yes | same name |  |
| 56 | `L_C_PTR_FL` | Portal Authentication Failed (Wired) | event | Client | — | wired | yes | same name |  |
| 57 | `L_C_AUTH_EXP` | Client Authenticated Expired (Wired) | event | Client | — | wired | yes | same name |  |
| 58 | `C_AUTH_OPT` | Client Authorized/Unauthorized by Admin | event | Client | — | wired, wireless | yes | same name |  |
| 59 | `C_PRT_EXT` | Client Authentication Extended by Admin | event | Client | — | wired, wireless | yes | same name |  |
| 60 | `DEV_CONN_REMEMBER` | Remembered Device Readopted After Factory Reset | event | Device | gateway, ap, switch | — | yes | not listed | A previously known device was re-adopted after a factory reset. |
| 61 | `REBOOT_RECOVERY_SUCCESS` | IntelliRecover - Device Back Online | event | System | — | — | yes | not listed | IntelliRecover: the device is back online. |
| 62 | `NAT_TRAVERSAL_CLOSED` | NAT Traversal Tunnel Closed | event | System | — | — | yes | not listed |  |
| 63 | `REPLACE_SUCCEED` | Replace action succeed | event | Device | ap, switch | — | yes | not listed |  |
| 64 | `OSW_LOOP_C` | Loop Cleared | event | Device | ap, switch | — | yes | same name | A previously detected loop has cleared. |
| 65 | `OSW_DEPEND_INFO` | Ecs Info | event | Device | switch | — | yes | not listed |  |
| 66 | `OSW_STP_FWD` | STP Topology Changed | event | Device | switch | — | yes | not listed | STP port moved to forwarding (event list). Shares its shortMsg 'STP Topology Changed' with OSW_TOPO_C. |
| 67 | `OSW_STP_BLOCK` | STP Port Blocked | event | Device | switch | — | yes | not listed | STP put a port into blocking. |
| 68 | `OSW_VLAN_8021Q_CFG_FAIL` | VLAN Configuration Fail | event | Device | switch | — | yes | not listed |  |
| 69 | `OSW_LAG_PORT_UP` | LAG Member Port Up Event | event | Device | switch | — | yes | not listed |  |
| 70 | `OSW_LAG_PORT_DOWN` | LAG Member Port Down Event | event | Device | switch | — | yes | not listed |  |
| 71 | `OSW_KEY_HEALING_INTF_CHECK_FAILED` | Netif Healing Check Failed Alert. | event | Device | switch | — | yes | not listed |  |
| 72 | `OSW_KEY_HEALING_INTF_RECOVER_NOT_EXEC` | Netif Healing Not Exec Failed Alert. | event | Device | switch | — | yes | not listed |  |
| 73 | `OSW_OUI_BASED_VLAN_EFFECT` | Switch OUI Based VLAN rule applied | event | Device | switch | — | yes | same name |  |
| 74 | `OSW_INSTALL_REBOOT` | Device Automatically Rebooted | event | Device | switch | — | yes | not listed | A switch rebooted itself (for example after an upgrade). |
| 75 | `OSW_INSTALL_ROLLBACK_FAILED` | Failed To Rollback | event | Device | switch | — | yes | not listed |  |
| 76 | `OSG_PRI_WAN_UP` | Primary WAN Takes Effect | event | Device | gateway | — | yes | name differs: 'Primary WAN Recovered' | Traffic is back on the primary WAN. TP-Link's guide calls this 'Primary WAN Recovered'. |
| 77 | `OSG_NHRP` | Gateway SDWAN Module Information | event | Device | gateway | — | yes | not listed |  |
| 78 | `OSG_OPENVPN` | Gateway OpenVPN Module Information | event | Device | gateway | — | yes | not listed |  |
| 79 | `OSG_MAPE` | Gateway MAP-E Module Information | event | Device | gateway | — | yes | not listed |  |
| 80 | `OSG_DSLITE` | Gateway DS-Lite Module Information | event | Device | gateway | — | yes | not listed |  |
<!-- GENERATED:END -->
