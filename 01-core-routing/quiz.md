# Module 01 Quiz — Core Routing (BGP + OSPF)

> 15 questions. Target: ≥80% (12/15). Open-book is fine for first attempt.

---

### Q1. In a WAN core design, why do we use eBGP between sites rather than extending OSPF?

<details><summary>Answer</summary>

eBGP provides policy control (communities, local-pref), natural isolation between sites (each AS is independent), and scales to thousands of prefixes without flooding. OSPF's link-state database would become too large across many sites, and SPF calculations would be unpredictable.

</details>

### Q2. What is the default BGP Local Preference, and how do you use it for path selection?

<details><summary>Answer</summary>

Default LP is 100. Higher LP is preferred. Set LP 200 on the primary WAN path and leave LP 100 on the backup. LP is only significant within the same AS (iBGP).

</details>

### Q3. Why do we configure OSPF links as point-to-point in a leaf-spine fabric?

<details><summary>Answer</summary>

P2P eliminates DR/BDR election (unnecessary on point-to-point links), forms adjacencies faster, and avoids the 40-second wait timer for DR election on broadcast networks.

</details>

### Q4. What is BFD and why is it critical on WAN links?

<details><summary>Answer</summary>

Bidirectional Forwarding Detection provides sub-second link failure detection (300ms × 3 = 900ms) vs. BGP's default holdtime of 180 seconds. Essential for meeting sub-second failover SLAs.

</details>

### Q5. Explain the difference between BGP communities and large communities (RFC 8092).

<details><summary>Answer</summary>

Standard communities are 32-bit (`ASN:Value`). Large communities are 96-bit (`ASN:Data1:Data2`), providing three fields for more granular tagging. Use large communities when you need hierarchical tagging (e.g., site:function:priority).

</details>

### Q6. What is a Route Reflector and when do you deploy one?

<details><summary>Answer</summary>

A Route Reflector re-advertises iBGP routes to clients, eliminating the need for full-mesh iBGP. Deploy when you have >5 iBGP peers. Always deploy in pairs for redundancy. RRs add Cluster-ID and Originator-ID to prevent loops but never modify AS-Path.

</details>

### Q7. Why should you NEVER redistribute BGP into OSPF in a WAN design?

<details><summary>Answer</summary>

Redistributing BGP into OSPF floods external routes into the OSPF domain, defeats summarization (specifics leak everywhere), and creates routing loops during convergence events. Keep the domains separate — OSPF carries infrastructure, BGP carries application/WAN routes.

</details>

### Q8. What does AS-Path prepending do, and when would you use it?

<details><summary>Answer</summary>

AS-path prepending artificially lengthens the AS-path by repeating your ASN, making a path less attractive to external peers. Use it on a backup WAN link to discourage inbound traffic (prepend 2-3× on the backup).

</details>

### Q9. What is the purpose of the `next-hop-self` configuration in iBGP?

<details><summary>Answer</summary>

In iBGP, the next-hop is preserved from the eBGP peer (an external IP). If the iBGP client doesn't have a route to that external next-hop, the route is unusable. `next-hop-self` rewrites the next-hop to the iBGP speaker's own loopback, which IS reachable via OSPF.

</details>

### Q10. MED is often called a "suggestion." Why?

<details><summary>Answer</summary>

MED is only compared between routes from the same neighboring AS. It suggests which entry point to prefer but the receiving AS can override it with local-pref. It's a hint, not a requirement. Also, MED comparison is disabled by default in some implementations.

</details>

### Q11. What OSPF timers are most important in a fabric underlay, and what are typical values?

<details><summary>Answer</summary>

Hello timer (10s default), Dead timer (40s default), SPF throttle timers. With BFD enabled, the OSPF timers become less critical for failure detection — BFD handles sub-second failover. SPF initial delay should be tuned for fast convergence (~50ms initial, 200ms max).

</details>

### Q12. How do you verify that BGP communities are propagating end-to-end?

<details><summary>Answer</summary>

`show route X.X.X.X/Y detail` (Junos) or `show bgp X.X.X.X/Y` (NX-OS) — look for the Communities field. Also verify `send-community both` is configured on all iBGP and eBGP sessions, and that no route-map is stripping communities.

</details>

### Q13. What is the difference between a route-map (Cisco) and a policy-statement (Junos)?

<details><summary>Answer</summary>

Functionally equivalent — both match routes and modify attributes. Junos policy-statements use `from` (match) and `then` (action) with terms. Cisco route-maps use `match` and `set` with sequence numbers. Key difference: Junos has an implicit reject at the end; Cisco has an implicit deny.

</details>

### Q14. In the WAN core, what does the border gateway do? (In terms of routing domains)

<details><summary>Answer</summary>

The border gateway participates in both OSPF (intra-site) and BGP (inter-site). It's the boundary between routing domains. It summarizes internal routes before advertising to BGP, and advertises external routes to the internal fabric via iBGP. It keeps the domains isolated.

</details>

### Q15. Draw (in text) a WAN core topology with 3 sites. Label the routing protocols on each link.

<details><summary>Answer</summary>

```
Site A (AS 65001)         WAN Core (transit)        Site B (AS 65002)
[Leaves]-OSPF-[Spines]                             [Spines]-OSPF-[Leaves]
              |                                          |
         [Border-GW]--eBGP--[Core-Rx]--eBGP--[Border-GW]
              |                                          |
         iBGP EVPN                                  iBGP EVPN
         (within site)                              (within site)
```

</details>
