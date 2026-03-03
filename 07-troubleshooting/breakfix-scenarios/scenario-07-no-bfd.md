# Breakfix Scenario 07: BFD Not Enabled

## Symptom

During a maintenance window, a WAN link cable is unplugged for testing. Traffic takes **~180 seconds** (3 minutes) to fail over to the backup path. The SLA requires < 3 seconds.

## Topology

```
[Border-GW1] ----eBGP---- [Remote-GW]    (Primary, BFD missing)
[Border-GW2] ----eBGP---- [Remote-GW]    (Backup, LP 100)
```

## Broken Config Snippet (Border-GW1)

```
router bgp 65001
  neighbor 10.255.0.2 remote-as 65002
    description Remote-GW-Primary
    timers 60 180                      ← Default BGP timers
    ! Missing: bfd
    address-family ipv4 unicast
      send-community both
```

## Hints

1. The failover works — it just takes 180 seconds (BGP holdtime default)
2. Without BFD, BGP relies on keepalive/holdtime (60/180s default) to detect link failure
3. Check `show bfd neighbors` — are there any BFD sessions?
4. Measure the actual convergence: start continuous ping, pull cable, count drops

## Solution

```
! Enable BFD on the eBGP session
router bgp 65001
  neighbor 10.255.0.2
    bfd

! Optionally configure BFD globally
bfd interval 300 min_rx 300 multiplier 3
```

## Root Cause Explanation

Without BFD, BGP depends on its keepalive/holdtime timers for failure detection. Default keepalive is 60 seconds, holdtime is 180 seconds. Even if you reduce these (e.g., to 3/9 seconds), BGP timers run in user-space and aren't reliable for sub-second detection.

BFD (Bidirectional Forwarding Detection) runs in the forwarding plane (hardware assist on most platforms), sending lightweight probes every 300ms. With a multiplier of 3, failure is detected in 900ms — well within the < 3 second SLA.

## Key Takeaway

> Slow failover (minutes, not seconds) → BFD is missing or misconfigured. Always enable BFD on ALL BGP and OSPF sessions in production. 300ms × 3 = sub-second detection.
