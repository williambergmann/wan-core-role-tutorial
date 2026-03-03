# Breakfix Scenario 08: Route-Map Deny All

## Symptom

Border gateway BGP session is Established with the remote site. Routes are being received, but **no routes are being advertised outbound**. The remote site sees 0 prefixes from your AS.

## Topology

```
[Border-GW1 AS 65001] ----eBGP---- [Remote-GW AS 65002]
                                    (sees 0 routes from 65001)
```

## Broken Config Snippet (Border-GW1)

```
route-map EXPORT-TO-REMOTE permit 10
  match ip address prefix-list SITE-AGGREGATES
  set community 65001:100:1

! Missing: the prefix-list is EMPTY or doesn't match anything

ip prefix-list SITE-AGGREGATES permit 10.1.0.0/8    ← /8 won't match /16 exactly
                                                       (aggregate is 10.1.0.0/16)

router bgp 65001
  neighbor 10.255.0.2 remote-as 65002
    address-family ipv4 unicast
      route-map EXPORT-TO-REMOTE out
```

## Hints

1. Session is up, routes received — so BGP is working bidirectionally at the control plane
2. No routes advertised — check the export route-map
3. Run `show route-map EXPORT-TO-REMOTE` — look at the match count (should be >0)
4. Run `show ip prefix-list SITE-AGGREGATES` — does it match the routes you expect?
5. Test: `show bgp ipv4 unicast neighbors X.X.X.X advertised-routes` — empty?

## Solution

```
! Fix the prefix-list to match the actual aggregate
no ip prefix-list SITE-AGGREGATES permit 10.1.0.0/8
ip prefix-list SITE-AGGREGATES permit 10.1.0.0/16

! Or use 'le' for range matching
ip prefix-list SITE-AGGREGATES permit 10.1.0.0/16 le 24
```

## Root Cause Explanation

The route-map matches on a prefix-list, but the prefix-list entry (`10.1.0.0/8`) doesn't match the actual aggregate route (`10.1.0.0/16`). Prefix-lists are exact match by default — `10.1.0.0/8` only matches a route with exactly /8 mask length. Since no routes match, the route-map permits nothing (implicit deny at end), and zero routes are advertised.

## Key Takeaway

> Zero routes advertised but session is up → always check the export route-map AND the prefix-list it references. Run `show route-map` to see if the match count is 0. Prefix-lists are exact-match by default — use `le`/`ge` for range matching.
