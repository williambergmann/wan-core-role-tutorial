# Breakfix Scenario 02: MTU Mismatch

## Symptom

OSPF neighbor stuck in **EXSTART/EXCHANGE** state. Devices can ping each other with small packets, but OSPF adjacency never reaches FULL.

## Topology

```
[Leaf-1] ----P2P---- [Spine-1]
  MTU 9214              MTU 1500 ← WRONG
```

## Broken Config Snippet (Spine-1)

```
interface ethernet1/1
  mtu 1500                        ← Should be 9214 for VXLAN fabric
  ip router ospf 1 area 0
  ip ospf network point-to-point
```

## Hints

1. OSPF adjacency starts forming (hellos exchange) — so area/timers match
2. It gets stuck when trying to exchange the Database Description (DBD) packets
3. DBD packets are larger than regular hellos — MTU matters here
4. Check `show ip ospf neighbor detail` — look for the state and any MTU flags

## Solution

```
interface ethernet1/1
  mtu 9214
```

## Root Cause Explanation

OSPF includes an MTU field in Database Description (DBD) packets. When the MTU values don't match between neighbors, the side with the smaller MTU rejects the DBD from the larger-MTU side because the packet exceeds the interface MTU. The adjacency loops between EXSTART and EXCHANGE forever.

Additionally, MTU 1500 is far too small for a VXLAN fabric — VXLAN adds ~50 bytes of overhead, so jumbo frames (≥9214) are required for the underlay.

## Key Takeaway

> OSPF stuck in EXSTART → check MTU on both sides. For VXLAN fabrics, EVERY underlay link must be jumbo (9214+).
