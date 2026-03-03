# 🌐 Module 03: WAN DCI — Multi-Site EVPN

> This is the core of the job — connecting EVPN fabrics across the WAN. This module covers DCI architecture, border gateway design, eBGP EVPN peering between sites, and resiliency testing for WAN links.

---

## Two DCI Approaches

### Approach 1: EVPN Multi-Site (Border Gateway Re-origination)

```
Site A Fabric              WAN Core              Site B Fabric
┌────────────┐        ┌──────────────┐        ┌────────────┐
│  Leaves    │        │              │        │  Leaves    │
│    ↕       │        │  eBGP        │        │    ↕       │
│  Spines    │        │  transit     │        │  Spines    │
│    ↕       │        │              │        │    ↕       │
│ Border-GW  │──eBGP──│  WAN Core Rx │──eBGP──│ Border-GW  │
│ (VTEP)     │ EVPN AF│ (pass-through│ EVPN AF│ (VTEP)     │
└────────────┘        │  or re-orig) │        └────────────┘
                      └──────────────┘
```

- Border GWs terminate VXLAN tunnels locally
- Re-originate EVPN routes toward remote sites with new next-hop
- WAN core only sees BGP prefixes, NOT VXLAN
- **Pros:** Clean separation, WAN core doesn't need VXLAN capability
- **Cons:** Additional config at border GWs

### Approach 2: Stretch VXLAN (Direct Tunnel)

- VXLAN tunnels extend directly between VTEPs across the WAN
- WAN core must support jumbo frames (MTU 9214+)
- **Pros:** Simpler overlay, fewer devices involved
- **Cons:** MTU across WAN must accommodate VXLAN overhead, blast radius is larger

### Which One Will You Use at Fiserv?

Most likely **Approach 1** (Multi-Site border gateway) because:

- Versa SD-WAN devices act as border gateways with VTEP capability
- PCI-DSS requires clean segmentation boundaries at each site
- WAN transport (internet/MPLS) may not support jumbo MTU

---

## What Crosses the WAN

| Route Type                       | Purpose                                      | When Exchanged                          |
| -------------------------------- | -------------------------------------------- | --------------------------------------- |
| **Type 2 (MAC/IP)**              | Stretched VLANs — host learning across sites | When VLANs span sites (L2 extension)    |
| **Type 5 (IP Prefix)**           | Inter-site L3 routing — application prefixes | Always — the primary route type for WAN |
| **Type 3 (Inclusive Multicast)** | BUM flooding tree                            | Only for stretched L2 VLANs             |

### Design Decision: When to Stretch L2 vs. Route L3

| Scenario                                    | Recommendation                  | Route Type   |
| ------------------------------------------- | ------------------------------- | ------------ |
| Application requires same subnet across DCs | Stretch L2VNI (Type 2 + Type 3) | L2 extension |
| Normal inter-site routing                   | Route via L3VNI (Type 5)        | L3 only      |
| Disaster recovery / active-passive          | Stretch L2 for quick failover   | L2 extension |
| **Default for new deployments**             | **Route L3 only**               | **Type 5**   |

> **Rule of thumb:** Always prefer L3 routing over L2 stretch. Only stretch L2 when the application absolutely requires it.

---

## WAN eBGP Peering Configuration

### NX-OS — Border Gateway (Site A)

```
router bgp 65001
  router-id 10.1.255.1

  ! WAN eBGP to remote site
  neighbor 10.2.255.1 remote-as 65002
    description Site-B-Border-GW1
    update-source loopback0
    ebgp-multihop 3
    address-family ipv4 unicast
      route-map EXPORT-TO-SITE-B out
      route-map IMPORT-FROM-SITE-B in
      send-community both
      next-hop-self
    address-family l2vpn evpn
      send-community both
      rewrite-evpn-rt-asn

! Summarize before advertising to WAN
ip prefix-list SITE-A-SUMMARY permit 10.1.0.0/16

route-map EXPORT-TO-SITE-B permit 10
  match ip address prefix-list SITE-A-SUMMARY
  set community 65001:100:1
route-map EXPORT-TO-SITE-B deny 999

route-map IMPORT-FROM-SITE-B permit 10
  set local-preference 200
```

### Key Design Points

1. **`rewrite-evpn-rt-asn`** — Rewrites route targets with local ASN when routes cross AS boundary
2. **Summarization** — Always summarize at the WAN boundary
3. **Communities** — Tag routes with site origin for policy
4. **BFD** — Enable on all WAN eBGP sessions

---

## Resiliency Testing for DCI

| Test                      | Steps                            | Expected Result                         |
| ------------------------- | -------------------------------- | --------------------------------------- |
| **Kill primary WAN link** | Shut the primary inter-site link | Traffic fails over to backup in <3s     |
| **Kill border GW**        | Shut the primary border gateway  | Routes reconverge via secondary GW      |
| **WAN link flap**         | Bounce the link 5× in 60 seconds | No routing loops, clean reconvergence   |
| **Asymmetric failure**    | Kill one direction only          | BFD detects, tears down session         |
| **Recovery**              | Restore all components           | Clean re-establishment, no stale routes |

---

## Labs

| Lab                                                  | Skills Practiced              |
| ---------------------------------------------------- | ----------------------------- |
| [eBGP WAN Peering](./labs/configs/ebgp-wan-peering/) | Two-site DCI with eBGP EVPN   |
| [EVPN Multi-Site](./labs/configs/evpn-multisite/)    | Border gateway re-origination |

## AI-Assisted Workflows

| Prompt                                                       | Use Case                            |
| ------------------------------------------------------------ | ----------------------------------- |
| [dci-design-reviewer.md](./ai-assist/dci-design-reviewer.md) | "Review this DCI design for issues" |

## Quiz

See [quiz.md](./quiz.md) — 10 questions on WAN DCI.
