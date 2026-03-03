# Breakfix Scenario 04: Missing EVPN Address Family

## Symptom

BGP session shows **Established**, but no EVPN routes are being exchanged. `show bgp l2vpn evpn summary` shows 0 prefixes received from the peer.

## Topology

```
[Leaf-1] ----iBGP---- [Spine-1 (RR)]
  BGP up, 0 EVPN routes
```

## Broken Config Snippet (Spine-1)

```
router bgp 65000
  router-id 10.255.0.1
  neighbor 10.255.1.1 remote-as 65000
    description leaf-1
    update-source loopback0
    address-family ipv4 unicast           ← IPv4 is configured
      send-community both
      route-reflector-client
    ! Missing: address-family l2vpn evpn  ← EVPN AFI not configured!
```

## Hints

1. BGP is Established — so Layer 3 + TCP 179 are fine
2. Check `show bgp l2vpn evpn summary` — 0 prefixes is the clue
3. Check `show bgp neighbor X.X.X.X` — look at "For address family: L2VPN EVPN"

## Solution

```
router bgp 65000
  neighbor 10.255.1.1
    address-family l2vpn evpn
      send-community both
      route-reflector-client
```

## Root Cause Explanation

BGP is modular — each address family must be explicitly configured. A BGP session can be Established for IPv4 unicast but have NO capability for L2VPN EVPN. The EVPN AFI/SAFI (AFI 25, SAFI 70) must be negotiated during OPEN message exchange. If one side doesn't configure it, EVPN routes are never exchanged.

## Key Takeaway

> "BGP Established" doesn't mean "all address families are working." Always check `show bgp l2vpn evpn summary` specifically for EVPN.
