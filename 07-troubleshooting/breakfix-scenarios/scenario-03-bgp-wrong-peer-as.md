# Breakfix Scenario 03: Wrong BGP Peer-AS

## Symptom

BGP session stuck in **ACTIVE** or **OPENSENT** state. TCP connection succeeds (you can see the session attempt in logs), but BGP never reaches Established.

## Topology

```
[Border-GW1 AS 65001] ----eBGP---- [Border-GW2 AS 65002]
```

## Broken Config Snippet (Border-GW1)

```
router bgp 65001
  neighbor 10.255.0.2 remote-as 65003   ← WRONG! Should be 65002
    description Site-B-Border-GW2
    update-source loopback0
    address-family l2vpn evpn
      send-community both
```

## Hints

1. The session is attempting to connect — so Layer 3 is fine
2. Check `show bgp neighbor 10.255.0.2` — look for "last reset reason"
3. Check syslog: `show logging | grep BGP` — look for "OPEN message error"
4. The OPEN message includes the local ASN — if the remote side sees a different ASN than configured, it rejects

## Solution

```
router bgp 65001
  neighbor 10.255.0.2 remote-as 65002
```

## Root Cause Explanation

When BGP sends an OPEN message, it includes the local ASN. The receiving router checks if the ASN in the OPEN matches what it has configured as `remote-as` for that peer. If they don't match, the OPEN is rejected with a NOTIFICATION (Error Code 2 - OPEN Message Error, SubCode 2 - Bad Peer AS).

## Key Takeaway

> BGP stuck in ACTIVE/OPENSENT → verify `remote-as` is correct on BOTH sides. Check syslog for "Bad Peer AS" notifications.
