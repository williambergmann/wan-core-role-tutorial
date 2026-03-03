# 🎯 BGP Cheatsheet

> Quick reference for BGP operations in the WAN core.

---

## Path Selection Algorithm (Memorize This)

```
1. ⭐ Highest Weight (Cisco only, local to router)
2. ⭐ Highest Local Preference (iBGP only, default 100)
3. Locally originated routes preferred
4. ⭐ Shortest AS-Path
5. Lowest Origin type (IGP < EGP < Incomplete)
6. ⭐ Lowest MED (same neighbor AS only)
7. eBGP over iBGP
8. Lowest IGP metric to BGP next-hop
9. Oldest eBGP route (stability)
10. Lowest Router-ID / Peer IP (tie-breaker)

⭐ = The ones you use daily for WAN traffic engineering
```

## Community Format Quick Reference

| Type     | Format            | Bits   | Example                                |
| -------- | ----------------- | ------ | -------------------------------------- |
| Standard | `ASN:Value`       | 32-bit | `65001:100`                            |
| Extended | `type:ASN:Value`  | 64-bit | `rt:65000:50001` (Route Target)        |
| Large    | `ASN:Data1:Data2` | 96-bit | `65001:100:1` (Site:Function:Priority) |

## Well-Known Communities

| Community      | Meaning                                             |
| -------------- | --------------------------------------------------- |
| `no-export`    | Don't advertise to eBGP peers                       |
| `no-advertise` | Don't advertise to ANY peer                         |
| `local-as`     | Don't advertise outside local AS (including confed) |
| `no-peer`      | Don't advertise to bilateral peers                  |

## Essential Show Commands

```bash
# NX-OS
show bgp l2vpn evpn summary                    # EVPN peer overview
show bgp ipv4 unicast summary                  # IPv4 peer overview
show bgp neighbor X.X.X.X                       # Peer detail
show bgp l2vpn evpn X.X.X.X/Y                  # Specific route
show bgp l2vpn evpn neighbors X advertised      # What you're sending
show bgp l2vpn evpn neighbors X routes          # What you're receiving

# Junos
show bgp summary
show bgp neighbor X.X.X.X
show route X.X.X.X/Y detail
show route advertising-protocol bgp X.X.X.X
show route receive-protocol bgp X.X.X.X
```

## Common BGP States

| State           | Meaning                 | Likely Problem                            |
| --------------- | ----------------------- | ----------------------------------------- |
| Idle            | Not trying to connect   | Check config, is neighbor defined?        |
| Connect         | TCP SYN sent, waiting   | Firewall blocking TCP 179?                |
| Active          | Retrying TCP connection | **Most common** — wrong IP, no route, ACL |
| OpenSent        | TCP up, OPEN sent       | AS mismatch, auth failure                 |
| OpenConfirm     | OPEN received, waiting  | Capability mismatch                       |
| **Established** | ✅ Working!             | —                                         |

## Quick Troubleshooting

```
BGP not Established?
├── Check: Can you ping the peer? (Layer 3 reachability)
├── Check: Is TCP 179 allowed? (Firewall/ACL)
├── Check: Is the ASN correct? (show bgp neighbor)
├── Check: Is update-source configured? (iBGP needs it)
├── Check: Is ebgp-multihop needed? (if not directly connected)
└── Check: Authentication match? (MD5 password must match on both sides)
```
