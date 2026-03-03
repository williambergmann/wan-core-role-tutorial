# 🔄 Vendor CLI Comparison — Juniper Junos vs Cisco NX-OS/IOS-XE

> Side-by-side reference for EVPN/VXLAN, BGP, and common operations.  
> Updated with Fiserv context: primary platform is **Cisco** + **Versa Networks**.

---

## Quick Reference: CLI Modes

| Action               | Junos                 | Cisco NX-OS                            | Cisco IOS-XE                  |
| -------------------- | --------------------- | -------------------------------------- | ----------------------------- |
| Enter config mode    | `configure`           | `configure terminal`                   | `configure terminal`          |
| Show pending changes | `show \| compare`     | `show running diff`                    | N/A                           |
| Commit safely        | `commit confirmed 5`  | `checkpoint; configure terminal`       | N/A                           |
| Rollback             | `rollback 1`          | `rollback running-config checkpoint X` | N/A                           |
| Save config          | `commit` (auto-saves) | `copy running-config startup-config`   | `write memory`                |
| Show routes          | `show route`          | `show ip route`                        | `show ip route`               |
| Show BGP             | `show bgp summary`    | `show bgp l2vpn evpn summary`          | `show bgp l2vpn evpn summary` |

---

## EVPN/VXLAN Fabric Configuration

### 1. Enable EVPN + VXLAN Features

**Junos:**

```junos
set protocols evpn encapsulation vxlan
set protocols evpn extended-vni-list all
```

**Cisco NX-OS:**

```
feature nv overlay
feature vn-segment-vlan-based
nv overlay evpn
feature bgp
feature interface-vlan
feature fabric forwarding
```

---

### 2. VLAN → VNI Mapping (L2VNI)

**Junos:**

```junos
set vlans VLAN100 vlan-id 100
set vlans VLAN100 vxlan vni 10100
set vlans VLAN100 vxlan ingress-node-replication
```

**Cisco NX-OS:**

```
vlan 100
  name Users
  vn-segment 10100

interface nve1
  no shutdown
  source-interface loopback0
  host-reachability protocol bgp
  member vni 10100
    ingress-replication protocol bgp
```

---

### 3. VTEP Source Interface

**Junos:**

```junos
set switch-options vtep-source-interface lo0.0
```

**Cisco NX-OS:**

```
interface nve1
  source-interface loopback0
```

---

### 4. VRF + L3VNI (Multi-Tenancy)

**Junos:**

```junos
set routing-instances VRF-TENANT-A instance-type vrf
set routing-instances VRF-TENANT-A interface irb.100
set routing-instances VRF-TENANT-A interface irb.999
set routing-instances VRF-TENANT-A route-distinguisher 10.255.1.1:1
set routing-instances VRF-TENANT-A vrf-target target:65000:50001
set routing-instances VRF-TENANT-A vrf-table-label

set vlans VLAN999 vlan-id 999
set vlans VLAN999 vxlan vni 50001
```

**Cisco NX-OS:**

```
vrf context TENANT-A
  vni 50001
  rd 10.255.1.1:1
  address-family ipv4 unicast
    route-target import 65000:50001
    route-target import 65000:50001 evpn
    route-target export 65000:50001
    route-target export 65000:50001 evpn

vlan 999
  name L3VNI-Transit
  vn-segment 50001

interface vlan 999
  no shutdown
  vrf member TENANT-A
  ip forward

interface nve1
  member vni 50001 associate-vrf
```

---

### 5. Anycast Gateway (IRB / SVI)

**Junos:**

```junos
set interfaces irb unit 100 family inet address 10.100.0.1/24 virtual-gateway-address 10.100.0.1
set interfaces irb unit 100 virtual-gateway-v4-mac 00:00:5e:00:01:01
```

**Cisco NX-OS:**

```
fabric forwarding anycast-gateway-mac 0000.5e00.0101   ! Global config

interface vlan 100
  no shutdown
  vrf member TENANT-A
  ip address 10.100.0.1/24
  fabric forwarding mode anycast-gateway
```

> **Note:** On Cisco, the anycast-gateway-mac is set globally (once), not per-interface.

---

### 6. BGP EVPN Peering (Leaf → Spine RR)

**Junos (Leaf):**

```junos
set routing-options autonomous-system 65000
set routing-options router-id 10.255.1.1

set protocols bgp group EVPN-OVERLAY type internal
set protocols bgp group EVPN-OVERLAY local-address 10.255.1.1
set protocols bgp group EVPN-OVERLAY family evpn signaling
set protocols bgp group EVPN-OVERLAY neighbor 10.255.0.1 description spine-1-rr
set protocols bgp group EVPN-OVERLAY neighbor 10.255.0.2 description spine-2-rr
```

**Cisco NX-OS (Leaf):**

```
router bgp 65000
  router-id 10.255.1.1
  neighbor 10.255.0.1 remote-as 65000
    description spine-1-rr
    update-source loopback0
    address-family l2vpn evpn
      send-community both
  neighbor 10.255.0.2 remote-as 65000
    description spine-2-rr
    update-source loopback0
    address-family l2vpn evpn
      send-community both
```

---

### 7. BGP EVPN Route Reflector (Spine)

**Junos (Spine):**

```junos
set protocols bgp group EVPN-OVERLAY type internal
set protocols bgp group EVPN-OVERLAY local-address 10.255.0.1
set protocols bgp group EVPN-OVERLAY family evpn signaling
set protocols bgp group EVPN-OVERLAY cluster 10.255.0.1
set protocols bgp group EVPN-OVERLAY neighbor 10.255.1.1 description leaf-1
set protocols bgp group EVPN-OVERLAY neighbor 10.255.1.2 description leaf-2
set protocols bgp group EVPN-OVERLAY neighbor 10.255.1.3 description leaf-3
```

**Cisco NX-OS (Spine):**

```
router bgp 65000
  router-id 10.255.0.1
  neighbor 10.255.1.1 remote-as 65000
    description leaf-1
    update-source loopback0
    address-family l2vpn evpn
      send-community both
      route-reflector-client
  neighbor 10.255.1.2 remote-as 65000
    description leaf-2
    update-source loopback0
    address-family l2vpn evpn
      send-community both
      route-reflector-client
  neighbor 10.255.1.3 remote-as 65000
    description leaf-3
    update-source loopback0
    address-family l2vpn evpn
      send-community both
      route-reflector-client
```

---

### 8. OSPF Underlay

**Junos:**

```junos
set protocols ospf area 0 interface lo0.0 passive
set protocols ospf area 0 interface xe-0/0/0.0 point-to-point
set protocols ospf area 0 interface xe-0/0/1.0 point-to-point
```

**Cisco NX-OS:**

```
feature ospf

router ospf 1
  router-id 10.255.1.1

interface loopback0
  ip router ospf 1 area 0

interface ethernet1/1
  ip router ospf 1 area 0
  ip ospf network point-to-point

interface ethernet1/2
  ip router ospf 1 area 0
  ip ospf network point-to-point
```

---

## Verification Commands

| Purpose               | Junos                                                   | Cisco NX-OS                            |
| --------------------- | ------------------------------------------------------- | -------------------------------------- |
| **BGP EVPN peers**    | `show bgp summary`                                      | `show bgp l2vpn evpn summary`          |
| **EVPN MAC/IP table** | `show evpn database`                                    | `show l2route evpn mac all`            |
| **EVPN routes (raw)** | `show route table bgp.evpn.0`                           | `show bgp l2vpn evpn`                  |
| **VXLAN tunnels**     | `show ethernet-switching vxlan-tunnel-end-point remote` | `show nve peers`                       |
| **VNI status**        | `show vlans extensive`                                  | `show nve vni`                         |
| **MAC table**         | `show ethernet-switching table`                         | `show mac address-table`               |
| **VRF routes**        | `show route table VRF-TENANT-A.inet.0`                  | `show ip route vrf TENANT-A`           |
| **OSPF neighbors**    | `show ospf neighbor`                                    | `show ip ospf neighbor`                |
| **OSPF routes**       | `show route protocol ospf`                              | `show ip route ospf`                   |
| **Interface status**  | `show interfaces terse`                                 | `show interface brief`                 |
| **EVPN Type-2**       | `show evpn database mac-address`                        | `show bgp l2vpn evpn route-type 2`     |
| **EVPN Type-5**       | `show route table VRF.evpn.0 evpn-ip-prefix`            | `show bgp l2vpn evpn route-type 5`     |
| **ARP suppression**   | `show evpn arp-table`                                   | `show l2route evpn mac-ip all`         |
| **ECMP verification** | `show route 10.255.1.3/32 detail`                       | `show ip route 10.255.1.3/32`          |
| **Config diff**       | `show \| compare`                                       | `show running diff`                    |
| **Rollback**          | `rollback 1; commit`                                    | `rollback running-config checkpoint X` |

---

## Key Differences to Watch For

| Feature            | Junos                                | Cisco NX-OS                                 |
| ------------------ | ------------------------------------ | ------------------------------------------- |
| **Config model**   | Candidate config → commit            | Direct apply (no commit)                    |
| **Safe changes**   | `commit confirmed 5` (auto-rollback) | `checkpoint` before changes                 |
| **EVPN enable**    | `set protocols evpn`                 | `nv overlay evpn` + `feature` commands      |
| **VNI config**     | Under VLAN stanza                    | VLAN stanza + NVE interface                 |
| **Anycast GW MAC** | Per-interface                        | Global config                               |
| **Route Targets**  | `vrf-target target:ASN:VALUE`        | Separate import/export + `evpn` keyword     |
| **L3VNI**          | VRF + transit VLAN                   | VRF + transit VLAN + `associate-vrf` on NVE |
