# Breakfix Scenario 01: OSPF Area Mismatch

## Symptom

OSPF neighbor stuck in **INIT** state. Devices can ping each other on the directly-connected link, but OSPF adjacency never forms.

## Topology

```
[Leaf-1] ----P2P---- [Spine-1]
  OSPF Area 0          OSPF Area ???
```

## Broken Config Snippet (Spine-1)

```
router ospf 1
  router-id 10.255.0.1

interface ethernet1/1
  ip router ospf 1 area 1        ← WRONG! Should be area 0
  ip ospf network point-to-point
```

## Hints

1. Look at the OSPF layer — what must match for adjacency?
2. Check `show ip ospf neighbor` — what state is it stuck in?
3. Check `show ip ospf interface` on both sides — compare the area

## Solution

```
interface ethernet1/1
  no ip router ospf 1 area 1
  ip router ospf 1 area 0
```

## Root Cause Explanation

OSPF adjacency requires matching: **area, network type, hello/dead timers, authentication**. Both sides must be in the same area. When areas don't match, the routers see each other's hellos but reject them because the area ID in the OSPF header doesn't match.

## Key Takeaway

> Always verify `show ip ospf interface` on BOTH sides when troubleshooting OSPF adjacency.
