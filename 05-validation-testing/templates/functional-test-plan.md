# Functional Test Plan Template

## Test Plan Information

| Field   | Value                        |
| ------- | ---------------------------- |
| Project | [Fabric name / site]         |
| Author  | [Your name]                  |
| Date    | YYYY-MM-DD                   |
| Version | 1.0                          |
| Status  | Draft / In Review / Approved |

## Test Environment

- Platform: [Cisco NX-OS / Junos / Versa VOS]
- Topology: [Describe or link to diagram]
- Devices: [List all devices under test]

## Test Cases

### Underlay Tests

| ID    | Test                     | Steps                                  | Expected                  | Actual | P/F |
| ----- | ------------------------ | -------------------------------------- | ------------------------- | ------ | --- |
| F-001 | OSPF adjacency formation | `show ip ospf neighbor` on all devices | All neighbors FULL        |        |     |
| F-002 | Loopback reachability    | Ping all loopbacks from every device   | 100% success              |        |     |
| F-003 | BFD status               | `show bfd neighbors` on all devices    | All sessions UP           |        |     |
| F-004 | ECMP verification        | `show ip route X.X.X.X`                | Multiple equal-cost paths |        |     |

### Overlay Tests

| ID    | Test                  | Steps                                 | Expected                 | Actual | P/F |
| ----- | --------------------- | ------------------------------------- | ------------------------ | ------ | --- |
| F-005 | BGP EVPN peering      | `show bgp l2vpn evpn summary`         | All peers Established    |        |     |
| F-006 | VTEP discovery        | `show nve peers`                      | All VTEPs discovered     |        |     |
| F-007 | VNI status            | `show nve vni`                        | All VNIs UP              |        |     |
| F-008 | MAC learning (Type-2) | Learn MAC on Leaf-1, verify on Leaf-3 | MAC in remote EVPN table |        |     |
| F-009 | ARP suppression       | ARP from host, check flood scope      | Suppressed (local reply) |        |     |

### Connectivity Tests

| ID    | Test                 | Steps                                  | Expected                 | Actual | P/F |
| ----- | -------------------- | -------------------------------------- | ------------------------ | ------ | --- |
| F-010 | Same VLAN, same leaf | Ping Host-A → Host-B (both on Leaf-1)  | Success, <1ms            |        |     |
| F-011 | Same VLAN, diff leaf | Ping Host-A (Leaf-1) → Host-C (Leaf-3) | Success, <5ms            |        |     |
| F-012 | Diff VLAN, same VRF  | Ping VLAN100 → VLAN200 (Symmetric IRB) | Success, <5ms            |        |     |
| F-013 | Diff VRF isolation   | Ping CDE → Corporate                   | FAILURE (isolated)       |        |     |
| F-014 | Anycast GW           | `show int vlan 100` on all leaves      | Same IP & MAC everywhere |        |     |

## Sign-Off

| Role            | Name | Date | Signature |
| --------------- | ---- | ---- | --------- |
| Test Engineer   |      |      |           |
| Design Lead     |      |      |           |
| Operations Lead |      |      |           |
