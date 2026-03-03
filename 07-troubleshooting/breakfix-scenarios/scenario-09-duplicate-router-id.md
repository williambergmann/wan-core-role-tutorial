# Breakfix Scenario 09: Duplicate Router-ID

## Symptom

Weird routing instability — routes flap, OSPF adjacencies bounce intermittently, and syslog shows "duplicate router-id" warnings. Two devices in the same OSPF domain have the same router-id.

## Topology

```
[Leaf-1]   lo0: 10.255.1.1      OSPF RID: 10.255.1.1
[Leaf-2]   lo0: 10.255.1.1  ←   OSPF RID: 10.255.1.1   ← DUPLICATE!
[Spine-1]  lo0: 10.255.0.1      OSPF RID: 10.255.0.1
```

## Broken Config Snippet (Leaf-2)

```
interface loopback0
  ip address 10.255.1.1/32        ← Same as Leaf-1!

router ospf 1
  router-id 10.255.1.1            ← Same as Leaf-1!
```

## Hints

1. The symptoms are inconsistent — sometimes it works, sometimes routes disappear
2. Check `show logging | grep "duplicate"` — OSPF logs duplicate router-id warnings
3. Check `show ip ospf` on all devices — compare router-ids
4. Also check BGP: duplicate router-ids cause problems there too (originator-id loops)

## Solution

```
! Fix Leaf-2 to use the correct, unique loopback and router-id
interface loopback0
  ip address 10.255.1.2/32

router ospf 1
  router-id 10.255.1.2

router bgp 65000
  router-id 10.255.1.2
```

> Note: You'll need to clear OSPF and BGP processes for the new router-id to take effect:
> `clear ip ospf process` and `clear bgp * all`

## Root Cause Explanation

OSPF requires unique router-IDs within an area. When two routers share the same router-ID, they both generate LSAs with the same originator. The LSDB becomes inconsistent — each router's LSA overwrites the other's, causing constant SPF recalculations, route flaps, and unpredictable forwarding.

BGP also uses router-id for loop prevention (originator-id in route reflector setups). Duplicate router-ids can cause routes to be dropped as loops.

## Key Takeaway

> Intermittent routing instability with OSPF/BGP → check for duplicate router-IDs. Always use a checklist to verify unique loopbacks and router-IDs BEFORE deploying a new device. Use IPAM (NetBox) to prevent allocating the same IP twice.
