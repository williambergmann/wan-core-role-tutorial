# 📚 Top 50 Show Commands for WAN Core Engineers

> These are the commands you'll use most frequently on the job, organized by protocol. Both Cisco NX-OS and Junos equivalents provided.

---

## BGP (Overlay & WAN Peering)

| #   | Purpose                    | NX-OS                                                     | Junos                                         |
| --- | -------------------------- | --------------------------------------------------------- | --------------------------------------------- |
| 1   | BGP EVPN peer summary      | `show bgp l2vpn evpn summary`                             | `show bgp summary`                            |
| 2   | BGP IPv4 summary           | `show bgp ipv4 unicast summary`                           | `show bgp summary`                            |
| 3   | BGP neighbor detail        | `show bgp neighbor X.X.X.X`                               | `show bgp neighbor X.X.X.X`                   |
| 4   | Routes received from peer  | `show bgp l2vpn evpn neighbors X.X.X.X routes`            | `show route receive-protocol bgp X.X.X.X`     |
| 5   | Routes advertised to peer  | `show bgp l2vpn evpn neighbors X.X.X.X advertised-routes` | `show route advertising-protocol bgp X.X.X.X` |
| 6   | Show specific route detail | `show bgp l2vpn evpn X.X.X.X`                             | `show route X.X.X.X detail`                   |
| 7   | Show Type-2 routes         | `show bgp l2vpn evpn route-type 2`                        | `show evpn database`                          |
| 8   | Show Type-5 routes         | `show bgp l2vpn evpn route-type 5`                        | `show route table VRF.evpn.0 evpn-ip-prefix`  |
| 9   | Show route-map hits        | `show route-map X`                                        | `show policy X`                               |
| 10  | BGP process info           | `show bgp process`                                        | `show bgp group`                              |

## OSPF (Underlay)

| #   | Purpose               | NX-OS                          | Junos                       |
| --- | --------------------- | ------------------------------ | --------------------------- |
| 11  | OSPF neighbor state   | `show ip ospf neighbor`        | `show ospf neighbor`        |
| 12  | OSPF neighbor detail  | `show ip ospf neighbor detail` | `show ospf neighbor detail` |
| 13  | OSPF interface        | `show ip ospf interface brief` | `show ospf interface`       |
| 14  | OSPF routes           | `show ip route ospf`           | `show route protocol ospf`  |
| 15  | OSPF database summary | `show ip ospf database`        | `show ospf database`        |

## VXLAN / EVPN Data Plane

| #   | Purpose           | NX-OS                          | Junos                                                   |
| --- | ----------------- | ------------------------------ | ------------------------------------------------------- |
| 16  | VTEP peers        | `show nve peers`               | `show ethernet-switching vxlan-tunnel-end-point remote` |
| 17  | VNI status        | `show nve vni`                 | `show vlans extensive`                                  |
| 18  | NVE interface     | `show nve interface nve1`      | `show interfaces vtep`                                  |
| 19  | EVPN MAC table    | `show l2route evpn mac all`    | `show evpn database`                                    |
| 20  | EVPN MAC-IP       | `show l2route evpn mac-ip all` | `show evpn arp-table`                                   |
| 21  | MAC address table | `show mac address-table`       | `show ethernet-switching table`                         |
| 22  | VXLAN counters    | `show nve vni counters`        | `show vxlan tunnel statistics`                          |

## VRF & Routing

| #   | Purpose           | NX-OS                           | Junos                           |
| --- | ----------------- | ------------------------------- | ------------------------------- |
| 23  | VRF info          | `show vrf`                      | `show route instance`           |
| 24  | VRF routing table | `show ip route vrf X`           | `show route table VRF-X.inet.0` |
| 25  | All VRF routes    | `show ip route vrf all`         | `show route instance detail`    |
| 26  | ARP table         | `show ip arp vrf all`           | `show arp no-resolve`           |
| 27  | Route summary     | `show ip route summary vrf all` | `show route summary`            |

## Interface & Physical

| #   | Purpose          | NX-OS                               | Junos                                |
| --- | ---------------- | ----------------------------------- | ------------------------------------ |
| 28  | Interface brief  | `show interface brief`              | `show interfaces terse`              |
| 29  | Interface detail | `show interface ethX/Y`             | `show interfaces et-0/0/X detail`    |
| 30  | Interface errors | `show interface counters errors`    | `show interfaces et-0/0/X extensive` |
| 31  | Optics/SFP info  | `show interface ethX/Y transceiver` | `show interfaces diagnostics optics` |
| 32  | LLDP neighbors   | `show lldp neighbors`               | `show lldp neighbors`                |

## BFD

| #   | Purpose      | NX-OS                       | Junos                     |
| --- | ------------ | --------------------------- | ------------------------- |
| 33  | BFD sessions | `show bfd neighbors`        | `show bfd session`        |
| 34  | BFD detail   | `show bfd neighbors detail` | `show bfd session detail` |

## System & Operations

| #   | Purpose         | NX-OS                   | Junos                          |
| --- | --------------- | ----------------------- | ------------------------------ |
| 35  | Running config  | `show running-config`   | `show configuration`           |
| 36  | Config diff     | `show running diff`     | `show \| compare`              |
| 37  | Syslog          | `show logging last 50`  | `show log messages \| last 50` |
| 38  | Uptime          | `show version`          | `show system uptime`           |
| 39  | CPU/Memory      | `show system resources` | `show chassis routing-engine`  |
| 40  | NTP status      | `show ntp peer-status`  | `show ntp associations`        |
| 41  | Users logged in | `show users`            | `show system users`            |
| 42  | VLAN info       | `show vlan brief`       | `show vlans`                   |

## Troubleshooting Specifics

| #   | Purpose                   | NX-OS                                              | Junos                                            |
| --- | ------------------------- | -------------------------------------------------- | ------------------------------------------------ |
| 43  | Ping with source          | `ping X.X.X.X source Y.Y.Y.Y vrf Z`                | `ping X.X.X.X source Y.Y.Y.Y routing-instance Z` |
| 44  | Traceroute                | `traceroute X.X.X.X vrf Z`                         | `traceroute X.X.X.X routing-instance Z`          |
| 45  | Ping with size (MTU test) | `ping X.X.X.X size 8972 df-bit`                    | `ping X.X.X.X size 8972 do-not-fragment`         |
| 46  | ECMP paths                | `show ip route X.X.X.X/Y`                          | `show route X.X.X.X/Y detail`                    |
| 47  | Checkpoint/rollback       | `checkpoint; rollback running-config checkpoint X` | `rollback 1; commit`                             |
| 48  | Feature status            | `show feature`                                     | N/A                                              |
| 49  | Process status            | `show processes cpu sort`                          | `show system processes brief`                    |
| 50  | Hardware info             | `show inventory`                                   | `show chassis hardware`                          |
