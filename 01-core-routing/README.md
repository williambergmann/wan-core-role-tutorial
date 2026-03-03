# 🔀 Module 01: Core Routing — BGP + OSPF for WAN

> BGP and OSPF are the two protocols you'll touch every single day. BGP connects sites across the WAN. OSPF provides the underlay inside each site. This module covers both in the WAN core context.

---

## Table of Contents

1. [BGP Design Patterns](#bgp-design-patterns)
2. [OSPF as WAN Underlay](#ospf-as-wan-underlay)
3. [BGP + OSPF Interaction](#bgp--ospf-interaction)
4. [Configuration Templates](#configuration-templates)
5. [Labs](#labs)
6. [AI-Assisted Workflows](#ai-assisted-workflows)

---

## BGP Design Patterns

### Pattern 1: eBGP Between Sites (Most Common)

Each site is a separate AS. Border gateways peer via eBGP across the WAN.

```
        AS 65001 (Site A)            AS 65002 (Site B)
        ┌──────────────┐            ┌──────────────┐
        │  OSPF Area 0 │            │  OSPF Area 0 │
        │              │            │              │
        │  [Spine1/2]  │            │  [Spine1/2]  │
        │      |       │            │      |       │
        │  [Leaves]    │            │  [Leaves]    │
        │      |       │            │      |       │
        │ [Border-GW1] │──eBGP──── │ [Border-GW1] │
        │ [Border-GW2] │──eBGP──── │ [Border-GW2] │
        └──────────────┘            └──────────────┘
```

**Design rules:**

- Each site gets its own private ASN (65001, 65002, etc.)
- Routes are **summarized at the border** — don't leak /32s across the WAN
- BGP communities tag routes with source site for policy control
- BFD on all eBGP sessions (300ms × 3 = sub-second failover)

### Pattern 2: iBGP with Route Reflectors (Within a Region)

Multiple sites in the same AS use route reflectors to avoid full-mesh iBGP.

```
        Region: US-East (AS 65000)
        ┌─────────────────────────────────────┐
        │                                     │
        │   [RR1]─────────────[RR2]           │
        │    / \                / \            │
        │ [GW-A] [GW-B]   [GW-C] [GW-D]      │
        │   |      |         |      |         │
        │ SiteA  SiteB    SiteC  SiteD        │
        └─────────────────────────────────────┘
                         |
                      eBGP to other regions
```

**When to use:** Multiple sites under single admin domain, need policy consistency.

### Pattern 3: BGP + OSPF Interaction

```
                    eBGP (WAN links)
    [Site A Border]─────────────────[Site B Border]
         |                                |
    OSPF Area 0 (Site A)            OSPF Area 0 (Site B)
         |                                |
    [Site A Spines]                  [Site B Spines]
         |                                |
    [Site A Leaves]                  [Site B Leaves]
```

**The golden rule: MINIMAL redistribution.**

- OSPF carries: loopbacks (/32), P2P link subnets, within-site only
- BGP carries: EVPN routes, inter-site prefixes, application routes
- **Never redistribute BGP into OSPF** — creates routing loops and defeats summarization

---

## BGP Path Selection — WAN Core Perspective

The attributes you use most daily:

| Attribute            | WAN Use Case                              | Example                               |
| -------------------- | ----------------------------------------- | ------------------------------------- |
| **Local Preference** | Prefer primary WAN path over backup       | Primary=200, Backup=100               |
| **AS-Path Prepend**  | Discourage inbound traffic on backup link | Prepend 3× on backup                  |
| **MED**              | Suggest entry point to remote AS          | Lower MED on preferred border GW      |
| **Communities**      | Tag routes for downstream policy          | `65001:100:1` = Site A originated     |
| **Weight**           | Local-only preference (Cisco)             | Override all other attributes locally |

### BGP Path Selection Algorithm (Memorize This)

```
1. Highest Weight (Cisco only, local)
2. Highest Local Preference
3. Locally originated routes
4. Shortest AS-Path
5. Lowest Origin type (IGP < EGP < Incomplete)
6. Lowest MED
7. eBGP over iBGP
8. Lowest IGP metric to next-hop
9. Oldest eBGP route
10. Lowest Router-ID / Peer IP
```

---

## OSPF as WAN Underlay

### Why OSPF (Not IS-IS or eBGP) for Underlay?

1. **Simplicity** — well-understood by most engineers
2. **Fast convergence** — SPF + BFD = sub-second failover
3. **Loopback distribution** — efficiently distributes /32 VTEP IPs
4. **No policy complexity** — unlike BGP, doesn't need route-maps for basic operation
5. **Scale is sufficient** — enterprise sites rarely hit OSPF limits

### OSPF Design Rules for Fabric Underlay

```
                Site A
        ┌─────────────────┐
        │   OSPF Area 0   │
        │                 │
        │ [Border-GW1] lo0: 10.1.255.1/32 (VTEP)
        │ [Border-GW2] lo0: 10.1.255.2/32 (VTEP)
        │ [Spine-1]    lo0: 10.1.255.3/32
        │ [Spine-2]    lo0: 10.1.255.4/32
        │ [Leaf-1]     lo0: 10.1.255.11/32 (VTEP)
        │ [Leaf-2]     lo0: 10.1.255.12/32 (VTEP)
        └─────────────────┘
```

- **All fabric links in Area 0** — keep it simple
- **Loopbacks as /32** — for VTEP reachability and BGP peering
- **P2P links** — no DR/BDR election, faster adjacency
- **BFD enabled** on all OSPF adjacencies
- **Passive interfaces** on non-fabric ports

---

## Configuration Templates

### Junos — WAN Border Gateway eBGP

```
protocols {
    bgp {
        group WAN-PEERS {
            type external;
            multihop { ttl 2; }
            local-as 65001;
            neighbor 10.255.0.2 {
                description "Site-B Border-GW1";
                peer-as 65002;
                family inet { unicast; }
                family evpn { signaling; }
                import IMPORT-FROM-SITE-B;
                export EXPORT-TO-SITE-B;
                authentication-key "$9$encrypted";
            }
        }
    }
}

policy-options {
    policy-statement EXPORT-TO-SITE-B {
        term ADVERTISE-AGGREGATES {
            from {
                protocol aggregate;
                route-filter 10.1.0.0/16 exact;
            }
            then {
                community add SITE-A-ORIGINATED;
                accept;
            }
        }
        term ADVERTISE-EVPN {
            from { family evpn; }
            then accept;
        }
        term DEFAULT-DENY { then reject; }
    }
    community SITE-A-ORIGINATED members 65001:100:1;
}
```

### Cisco NX-OS — WAN Border Gateway eBGP

```
router bgp 65001
  router-id 10.1.255.1
  neighbor 10.255.0.2 remote-as 65002
    description Site-B-Border-GW1
    update-source loopback0
    address-family ipv4 unicast
      route-map EXPORT-TO-SITE-B out
      route-map IMPORT-FROM-SITE-B in
      send-community both
    address-family l2vpn evpn
      send-community both

route-map EXPORT-TO-SITE-B permit 10
  match ip address prefix-list SITE-A-AGGREGATES
  set community 65001:100:1

ip prefix-list SITE-A-AGGREGATES permit 10.1.0.0/16
```

### Junos — OSPF Underlay

```
protocols {
    ospf {
        area 0.0.0.0 {
            interface lo0.0 { passive; }
            interface et-0/0/0.0 {
                interface-type p2p;
                bfd-liveness-detection {
                    minimum-interval 300;
                    multiplier 3;
                }
            }
        }
    }
}
```

### Cisco NX-OS — OSPF Underlay

```
feature ospf
router ospf 1
  router-id 10.1.255.11

interface loopback0
  ip router ospf 1 area 0

interface ethernet1/1
  ip router ospf 1 area 0
  ip ospf network point-to-point
  ip ospf bfd
```

---

## BFD — Sub-Second Failure Detection

**Always enable BFD** on both BGP and OSPF sessions:

| Parameter      | Recommended Value | Purpose                                  |
| -------------- | ----------------- | ---------------------------------------- |
| Interval       | 300ms             | How often to send BFD packets            |
| Multiplier     | 3×                | How many misses before declaring failure |
| Detection time | 900ms             | 300ms × 3 = sub-second failover          |

---

## Labs

| Lab                                                  | Topology          | Skills Practiced                        |
| ---------------------------------------------------- | ----------------- | --------------------------------------- |
| [BGP Fundamentals](./labs/configs/bgp-fundamentals/) | 5 routers, 3 ASNs | eBGP + iBGP peering, path selection     |
| [BGP Policy](./labs/configs/bgp-policy/)             | Same + policies   | Communities, local-pref, MED, filtering |
| [OSPF Underlay](./labs/configs/ospf-underlay/)       | Leaf-spine fabric | P2P links, BFD, loopback distribution   |

### Lab Validation

Run the validation script to auto-check your lab:

```bash
python labs/validate.py --lab bgp-fundamentals --hosts inventory.yml
```

---

## AI-Assisted Workflows

| Prompt                                                     | Use Case                                     |
| ---------------------------------------------------------- | -------------------------------------------- |
| [config-from-intent.md](./ai-assist/config-from-intent.md) | "Generate BGP config for these 3 sites"      |
| [bgp-troubleshooter.md](./ai-assist/bgp-troubleshooter.md) | "Here's my show bgp summary — what's wrong?" |

---

## Quiz

See [quiz.md](./quiz.md) — 15 questions on BGP and OSPF in the WAN context.
