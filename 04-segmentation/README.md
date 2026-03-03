# 🔒 Module 04: Segmentation — VRF, L3VNI, and PCI-DSS

> At Fiserv, network segmentation isn't optional — it's mandated by PCI-DSS. This module covers multi-VRF design, L3VNI isolation, controlled route leaking, and mapping PCI zones to fabric constructs.

---

## Why Segmentation Matters at Fiserv

Fiserv processes credit/debit card transactions. PCI-DSS requires the **Cardholder Data Environment (CDE)** to be completely isolated from general corporate traffic. EVPN/VXLAN VRFs provide this isolation at the routing level.

---

## Multi-VRF Design

### Standard VRF Layout for Financial Services

| VRF             | L3VNI | PCI Zone        | Purpose               | Route Leaking         |
| --------------- | ----- | --------------- | --------------------- | --------------------- |
| **CDE**         | 50001 | Cardholder Data | Payment processing    | To/from Mgmt (via FW) |
| **Corporate**   | 50002 | Corporate       | User workstations     | Isolated from CDE     |
| **DMZ**         | 50003 | DMZ             | Internet-facing       | No CDE access ever    |
| **Management**  | 50004 | Management      | NOC, monitoring       | To/from CDE (via FW)  |
| **Development** | 50005 | Dev/Test        | Development workloads | Fully isolated        |

### VRF Configuration — NX-OS

```
! CDE VRF — most restricted
vrf context CDE
  vni 50001
  rd 10.255.1.1:50001
  address-family ipv4 unicast
    route-target import 65000:50001
    route-target import 65000:50001 evpn
    route-target export 65000:50001
    route-target export 65000:50001 evpn

! L3VNI transit VLAN
vlan 901
  name L3VNI-CDE-Transit
  vn-segment 50001

interface vlan 901
  no shutdown
  vrf member CDE
  ip forward

! Data VLAN in CDE
vlan 100
  name Payment-Servers
  vn-segment 10100

interface vlan 100
  no shutdown
  vrf member CDE
  ip address 10.100.0.1/24
  fabric forwarding mode anycast-gateway
```

---

## Route Leaking — Controlled Cross-VRF Communication

### When to Leak Routes

- **CDE ↔ Management:** NOC needs to monitor CDE servers (but ALL traffic through firewall)
- **Corporate ↔ Management:** Users need access to internal tools
- **NEVER:** CDE ↔ Corporate (direct), CDE ↔ DMZ (direct)

### How Route Leaking Works

```
VRF: CDE                          VRF: Management
RT import 65000:50001              RT import 65000:50004
RT export 65000:50001              RT export 65000:50004
                                   RT import 65000:50001  ← leaks CDE routes IN

→ Management VRF can see CDE routes
→ But traffic MUST traverse a firewall (PBR or service insertion)
```

### Configuration — Route Leaking via Import/Export RT

```
! Management VRF leaks FROM CDE
vrf context MANAGEMENT
  vni 50004
  rd 10.255.1.1:50004
  address-family ipv4 unicast
    route-target import 65000:50004
    route-target import 65000:50004 evpn
    route-target export 65000:50004
    route-target export 65000:50004 evpn
    ! Import CDE routes (for monitoring access)
    route-target import 65000:50001
    route-target import 65000:50001 evpn
```

> **WARNING:** Route leaking alone is NOT sufficient for PCI compliance. Traffic between PCI zones must be inspected by a firewall. Use service insertion or PBR to force traffic through a firewall.

---

## Firewall Insertion in EVPN Fabric

### Option 1: Service Leaf

```
                    [Spine]
                   /      \
           [Leaf-1]        [Service Leaf] ← Firewall connected here
              |                  |
         [Hosts]           [Palo Alto FW]
                                |
                           VRF CDE ↔ VRF Mgmt
                           (all cross-VRF traffic
                            flows through FW)
```

### Option 2: VRF-Aware Firewall (Inline)

The firewall has interfaces in multiple VRFs and routes between them:

```
Firewall:
  eth1 → VRF CDE (10.100.0.0/24)
  eth2 → VRF Management (10.104.0.0/24)
  Policy: Allow monitoring (SNMP, ICMP) from Mgmt → CDE
  Policy: Deny everything else
```

---

## Verifying VRF Isolation

```bash
# Verify hosts in different VRFs CANNOT communicate
# From a host in CDE:
ping 10.102.0.10    # Corporate IP — should FAIL (isolated)
ping 10.103.0.10    # DMZ IP — should FAIL (isolated)
ping 10.104.0.10    # Management IP — should succeed ONLY via firewall

# Verify VRF routing tables are separate
show ip route vrf CDE
show ip route vrf CORPORATE
show ip route vrf MANAGEMENT
# Each should only contain routes from its own VRF + leaked routes
```

---

## Labs

| Lab                                            | Skills Practiced                          |
| ---------------------------------------------- | ----------------------------------------- |
| [Multi-VRF](./labs/configs/multi-vrf/)         | 3 VRFs with L3VNI isolation               |
| [PCI-DSS Zones](./labs/configs/pci-dss-zones/) | CDE/Corporate/DMZ with route leaking + FW |

## AI-Assisted Workflows

| Prompt                                                             | Use Case                                       |
| ------------------------------------------------------------------ | ---------------------------------------------- |
| [vrf-designer.md](./ai-assist/vrf-designer.md)                     | "Design VRF segmentation for this environment" |
| [pci-compliance-checker.md](./ai-assist/pci-compliance-checker.md) | "Check this config for PCI compliance"         |

## Quiz

See [quiz.md](./quiz.md) — 10 questions on segmentation.
