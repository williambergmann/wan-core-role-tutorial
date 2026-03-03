# 🏗️ Module 02: EVPN/VXLAN Fabric

> EVPN/VXLAN is the overlay technology that makes modern data center and WAN fabrics work. This module covers VXLAN encapsulation, EVPN control plane, L2VNI/L3VNI segmentation, and Symmetric IRB — all in the WAN core context.

---

## VXLAN — The Data Plane

VXLAN encapsulates Layer 2 frames inside UDP packets so they can be transported across a routed underlay:

```
┌─────────┬──────────┬───────┬─────────────┬───────────┬──────────┬─────────┐
│Outer Eth│ Outer IP │  UDP  │ VXLAN Header│ Inner Eth │ Inner IP │ Payload │
│  14B    │   20B    │  8B   │     8B      │   14B     │   20B    │   ...   │
└─────────┴──────────┴───────┴─────────────┴───────────┴──────────┴─────────┘
                                  │
                           VNI (24-bit) = 16M segments
                           UDP port 4789
```

**Key numbers:**

- VXLAN overhead: ~50 bytes
- Underlay MTU must be ≥9214 (jumbo frames required)
- VNI range: 1–16,777,215 (24 bits)

---

## EVPN — The Control Plane

EVPN uses BGP to advertise MAC/IP bindings, replacing traditional flood-and-learn:

### Route Types

| Type  | Name                    | Purpose                                     | When You See It                |
| ----- | ----------------------- | ------------------------------------------- | ------------------------------ |
| **1** | Ethernet Auto-Discovery | Multi-homing (ESI/MLAG redundancy)          | Dual-homed server setups       |
| **2** | MAC/IP Advertisement    | **Host learning** — the most important type | Every host connected = Type 2  |
| **3** | Inclusive Multicast     | BUM traffic flooding tree setup             | One per VNI per VTEP           |
| **4** | Ethernet Segment        | DF election for multi-homing                | ESI environments only          |
| **5** | IP Prefix Route         | L3 routing (external prefixes in EVPN)      | Inter-site routing, VRF routes |

### L2VNI vs L3VNI

```
L2VNI (Layer 2 VNI)                    L3VNI (Layer 3 VNI)
├── Maps to a VLAN                     ├── Maps to a VRF
├── Extends broadcast domain           ├── Enables inter-subnet routing
├── Same VLAN across leaves            ├── Transit VNI for Symmetric IRB
├── Example: VNI 10100 = VLAN 100      ├── Example: VNI 50001 = VRF Tenant-A
└── Hosts on same subnet               └── Routing between subnets
```

### Symmetric IRB — How Inter-Subnet Routing Works

```
Host A (VLAN 100, Leaf-1)  →  Host B (VLAN 200, Leaf-3)

Step 1: Leaf-1 routes VLAN 100 → L3VNI 50001 (VRF lookup)
Step 2: VXLAN encap with VNI 50001 → sends to Leaf-3 VTEP
Step 3: Leaf-3 decaps → routes L3VNI 50001 → VLAN 200
Step 4: Delivers to Host B

Key: BOTH leaves perform routing (symmetric)
Benefit: Each leaf only needs VLANs it locally hosts
```

### Anycast Gateway

Same IP + same virtual MAC on every leaf for a given VLAN:

```
Leaf-1: VLAN 100 gateway = 10.100.0.1/24, MAC 00:00:5e:00:01:01
Leaf-2: VLAN 100 gateway = 10.100.0.1/24, MAC 00:00:5e:00:01:01
Leaf-3: VLAN 100 gateway = 10.100.0.1/24, MAC 00:00:5e:00:01:01

→ Host can move between leaves without re-ARPing for the gateway
```

---

## Configuration — NX-OS

### Enable Features

```
feature nv overlay
feature vn-segment-vlan-based
nv overlay evpn
feature bgp
feature interface-vlan
feature fabric forwarding
```

### L2VNI (VLAN 100 → VNI 10100)

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

### L3VNI (VRF Tenant-A → VNI 50001)

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

### Anycast Gateway

```
fabric forwarding anycast-gateway-mac 0000.5e00.0101

interface vlan 100
  no shutdown
  vrf member TENANT-A
  ip address 10.100.0.1/24
  fabric forwarding mode anycast-gateway
```

---

## Configuration — Junos

### L2VNI

```
set vlans VLAN100 vlan-id 100
set vlans VLAN100 vxlan vni 10100
set vlans VLAN100 vxlan ingress-node-replication
```

### L3VNI / VRF

```
set routing-instances VRF-TENANT-A instance-type vrf
set routing-instances VRF-TENANT-A interface irb.100
set routing-instances VRF-TENANT-A route-distinguisher 10.255.1.1:1
set routing-instances VRF-TENANT-A vrf-target target:65000:50001
set routing-instances VRF-TENANT-A vrf-table-label
```

### Anycast Gateway

```
set interfaces irb unit 100 family inet address 10.100.0.1/24
set interfaces irb unit 100 virtual-gateway-address 10.100.0.1
set interfaces irb unit 100 virtual-gateway-v4-mac 00:00:5e:00:01:01
```

---

## Verification Commands

| Purpose           | NX-OS                              | Junos                                                   |
| ----------------- | ---------------------------------- | ------------------------------------------------------- |
| EVPN MAC/IP table | `show l2route evpn mac all`        | `show evpn database`                                    |
| VXLAN tunnels     | `show nve peers`                   | `show ethernet-switching vxlan-tunnel-end-point remote` |
| VNI status        | `show nve vni`                     | `show vlans extensive`                                  |
| EVPN routes       | `show bgp l2vpn evpn`              | `show route table bgp.evpn.0`                           |
| Type-2 routes     | `show bgp l2vpn evpn route-type 2` | `show evpn database mac-address`                        |
| VRF routes        | `show ip route vrf TENANT-A`       | `show route table VRF-TENANT-A.inet.0`                  |

---

## Labs

| Lab                                                      | Skills Practiced                            |
| -------------------------------------------------------- | ------------------------------------------- |
| [Single-Site Fabric](./labs/configs/single-site-fabric/) | 2-spine, 3-leaf fabric with L2VNI + L3VNI   |
| [Symmetric IRB](./labs/configs/symmetric-irb/)           | Cross-VLAN, cross-leaf routing verification |

## AI-Assisted Workflows

| Prompt                                               | Use Case                                 |
| ---------------------------------------------------- | ---------------------------------------- |
| [evpn-explainer.md](./ai-assist/evpn-explainer.md)   | "Explain this EVPN route entry"          |
| [fabric-designer.md](./ai-assist/fabric-designer.md) | "Design a fabric for these requirements" |

## Quiz

See [quiz.md](./quiz.md) — 15 questions on EVPN/VXLAN.
