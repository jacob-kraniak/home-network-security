# Hardware Decisions Log (Updated September 9, 2026)

## Deployed Hardware (Phase 1 network + Phase 2 Proxmox)

- **Router/Gateway (Phase 1, live):** TP-Link **ER605 V2** — primary Omada SDN gateway (purchased 2026-06-09). VLAN tagging for 1/10/20. See [devices-summary.md](../inventory/devices-summary.md) and [network-overview.md](../network-overview.md).
- **Core Switch:** TP-Link SG2008P v3.20 (K108-MSW-1)
  - Serial Number: Y25A081000375
  - MAC Address: 10:5a:95:3a:16:b4
  - IP Address: 192.168.0.146
  - Firmware: 3.20.24 Build 20260509 Rel.2353
  - VLAN capable, Omada integrated.
- **APs:** Omada EAP225 coverage (office AP live). SSIDs: K108-Home-Secure (vid10), K108-Home-IoT (vid20). Additional AP conversion tracked in inventory.
- **Compute/Services Host (Phase 2):** **Lenovo ThinkCentre M715q Tiny** (type 10M3000PUS, S/N MJ067MNT) — free employer surplus 2026-07-09/10.
  - **Live 2026-09-05:** PVE 9.2.4 node `debian` `192.168.0.176`.
  - CPU: AMD PRO A12-9800E R7 (4C+8G).
  - **RAM:** 2×8 GB DDR4 SO-DIMM; PVE/top ~**14.6 GiB** after 2026-09-05 reboot (Aug 29 ~7.2 GiB reading was one stick not visible to the kernel).
  - Disk: KingSpec 512GB NVMe (serial 9K60519000031). SanDisk Z400 still not detected — RAID1 plan on hold.
  - Support page: https://pcsupport.lenovo.com/us/en/products/desktops-and-all-in-ones/thinkcentre-m-series-desktops/m715q/10m3/10m3000pus/mj067mnt
- **Phase 2 guests (live 2026-09-05):** CT 100 Wazuh AIO (6 GiB); CT 101 Portainer (2 GiB / 4G rootfs). Details in [phase-2-checkpoint-2026-09-05.md](../phases/phase-2-checkpoint-2026-09-05.md).
- **External media/backup:** Seagate Backup+ Desk 3TB exFAT at `/mnt/seagate3tb` (USB 2) — media/backups only, not PVE VM disks.
- **Clients:** Prefer NetBox / Omada for live counts; older “21 clients” snapshot remains June Omada context only.

## Rationale

- Omada (ER605 + SG2008P + EAP225) chosen for warranty, UI, VLAN isolation, and family-network priority (Phase 1 complete).
- M715q acquired free for Proxmox (low power, Tiny form factor). Cost $0 vs planned refurb.
- **Constraint updated 2026-09-05:** with ~14.6 GiB host RAM and CT split 6G/2G, Wazuh + Portainer + a small next app fit without buying another DIMM. Still grow CT 101 disk and prefer USB 3 before media stacks.
- Single NIC on the services host is acceptable (downstream of router/switch).

**Links**
- Inventory: [devices-summary.md](../inventory/devices-summary.md)
- Rack: [RACK.md](RACK.md)
- Live checkpoint: [phase-2-checkpoint-2026-09-05.md](../phases/phase-2-checkpoint-2026-09-05.md)
- Wazuh outage narrative: [phase-2-baseline-2026-08-29.md](../phases/phase-2-baseline-2026-08-29.md)
- Root status: [README.md](../../README.md)
