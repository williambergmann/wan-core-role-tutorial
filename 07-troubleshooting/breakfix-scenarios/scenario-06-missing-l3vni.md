# Breakfix Scenario 06: Missing L3VNI

## Symptom

Inter-VLAN routing within the same VRF is broken across leaves. Hosts in VLAN 100 on Leaf-1 cannot reach hosts in VLAN 200 on Leaf-3. Same-VLAN connectivity across leaves works fine (L2VNI is OK). Same-leaf inter-VLAN routing works.

## Topology

```
[Leaf-1]                              [Leaf-3]
VLAN 100 (VNI 10100), VRF TENANT-A   VLAN 200 (VNI 10200), VRF TENANT-A
Host-A: 10.100.0.10                   Host-B: 10.200.0.20
                                      L3VNI: NOT CONFIGURED ← PROBLEM
```

## Broken Config Snippet (Leaf-3)

```
vrf context TENANT-A
  ! Missing: vni 50001
  rd 10.255.1.3:1
  address-family ipv4 unicast
    route-target import 65000:50001
    route-target import 65000:50001 evpn
    route-target export 65000:50001
    route-target export 65000:50001 evpn

! Missing: VLAN 999 (transit VLAN) and SVI for L3VNI
! Missing: member vni 50001 associate-vrf on NVE interface
```

## Hints

1. L2 works cross-leaf → underlay, overlay, and L2VNI are all fine
2. Inter-VLAN works on the same leaf → VRF and IRB interfaces are fine locally
3. Inter-VLAN fails cross-leaf → the L3VNI (transit VNI) is needed for Symmetric IRB
4. Check `show vrf` — does it show a VNI assigned?
5. Check `show nve vni` — is the L3VNI (50001) present?

## Solution

```
! Add L3VNI to VRF
vrf context TENANT-A
  vni 50001

! Create transit VLAN and SVI
vlan 999
  name L3VNI-Transit
  vn-segment 50001

interface vlan 999
  no shutdown
  vrf member TENANT-A
  ip forward

! Register L3VNI on NVE
interface nve1
  member vni 50001 associate-vrf
```

## Root Cause Explanation

Symmetric IRB requires an L3VNI (transit VNI) to route traffic between subnets across leaves. When Host-A on Leaf-1 sends traffic to Host-B on Leaf-3 (different subnet), Leaf-1 does a VRF route lookup and encapsulates the packet with the L3VNI. If Leaf-3 doesn't have the L3VNI configured, it can't decapsulate and route the packet into the destination VLAN.

The L3VNI requires three things:

1. VNI assignment in the VRF context (`vni 50001`)
2. A transit VLAN mapped to that VNI (`vn-segment 50001`)
3. An SVI on that transit VLAN with `ip forward`
4. `associate-vrf` on the NVE interface

## Key Takeaway

> L2 works cross-leaf but L3 doesn't → check L3VNI configuration. `show vrf` should show the VNI; `show nve vni` should show it as type "L3". All 4 components (VRF vni, transit VLAN, SVI, NVE associate-vrf) must be present.
