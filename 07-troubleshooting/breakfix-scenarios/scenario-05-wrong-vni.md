# Breakfix Scenario 05: Wrong VNI Mapping

## Symptom

L2 connectivity is broken for VLAN 100. Hosts on the same VLAN but different leaves cannot communicate. Hosts on the same leaf work fine. VTEP peers show UP.

## Topology

```
[Leaf-1]                    [Leaf-2]
VLAN 100 → VNI 10100       VLAN 100 → VNI 10200 ← WRONG
Host-A: 10.100.0.10        Host-B: 10.100.0.20
```

## Broken Config Snippet (Leaf-2)

```
vlan 100
  name Users
  vn-segment 10200           ← WRONG! Should be 10100

interface nve1
  member vni 10200
    ingress-replication protocol bgp
```

## Hints

1. Intra-leaf communication works — so the VLAN config is fine locally
2. Cross-leaf fails — so the overlay tunnel or VNI must be wrong
3. Check `show nve vni` on both leaves — compare VNI numbers for VLAN 100
4. Check `show bgp l2vpn evpn route-type 3` — do both leaves announce the same VNI?

## Solution

```
! Fix the VNI mapping on Leaf-2
vlan 100
  vn-segment 10100

interface nve1
  no member vni 10200
  member vni 10100
    ingress-replication protocol bgp
```

## Root Cause Explanation

VXLAN uses the VNI to identify which L2 segment traffic belongs to. If Leaf-1 sends traffic in VNI 10100 but Leaf-2 maps VLAN 100 to VNI 10200, Leaf-2 will not associate the incoming VXLAN traffic with the correct VLAN. The VNIs must match across all leaves for the same VLAN.

## Key Takeaway

> Cross-leaf L2 broken but intra-leaf works → check VNI-to-VLAN mapping consistency across ALL leaves. `show nve vni` is your go-to command.
