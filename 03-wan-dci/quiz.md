# Module 03 Quiz — WAN DCI (Multi-Site EVPN)

> 10 questions. Target: ≥80% (8/10). This is the core of the WAN Core Engineer job.

---

### Q1. What is DCI and why does it matter for a WAN Core Engineer?

<details><summary>Answer</summary>

DCI (Data Center Interconnect) connects separate EVPN/VXLAN fabrics across a WAN. As a WAN Core Engineer, this is the primary responsibility — designing, building, and maintaining the eBGP EVPN peering between sites, ensuring routes propagate correctly, and traffic fails over within SLA.

</details>

### Q2. Explain the two main DCI approaches and which Fiserv likely uses.

<details><summary>Answer</summary>

**Approach 1: EVPN Multi-Site (Border Gateway Re-origination)** — Border GWs terminate VXLAN locally and re-originate EVPN routes with a new next-hop across the WAN. WAN core doesn't need VXLAN capability.

**Approach 2: Stretch VXLAN (Direct Tunnel)** — VXLAN tunnels extend directly across the WAN. Simpler, but requires jumbo MTU end-to-end.

**Fiserv likely uses Approach 1** because: Versa SD-WAN acts as the border gateway, PCI-DSS requires clean segmentation boundaries, and internet/MPLS WAN transport may not support jumbo MTU.

</details>

### Q3. Which EVPN route types cross the WAN, and when?

<details><summary>Answer</summary>

- **Type 5 (IP Prefix):** ALWAYS — this is the primary route type for inter-site L3 routing
- **Type 2 (MAC/IP):** Only when VLANs are stretched between sites (L2 extension)
- **Type 3 (Inclusive Multicast):** Only when L2 VLANs are stretched (for BUM flooding)

**Default:** Only Type 5 should cross the WAN. Type 2/3 are only for specific L2 stretch requirements.

</details>

### Q4. Why should you always prefer L3 routing (Type 5) over L2 stretch (Type 2) across the WAN?

<details><summary>Answer</summary>

L2 stretch across the WAN:

- Extends the broadcast domain (increased BUM traffic across WAN)
- Increases blast radius (L2 loops can span sites)
- Requires MTU accommodation for VXLAN + WAN overhead
- Complicates troubleshooting (MAC learning across sites)

L3 routing is cleaner — each site is an isolated L2 domain, with only summarized IP prefixes exchanged. Only stretch L2 when the application absolutely requires same-subnet connectivity across sites.

</details>

### Q5. What does `rewrite-evpn-rt-asn` do and when is it needed?

<details><summary>Answer</summary>

When EVPN routes cross an eBGP boundary (different AS), the Route Target (RT) format `ASN:Value` may not match the remote AS's import RT. `rewrite-evpn-rt-asn` automatically rewrites the ASN portion of the RT with the local ASN as routes are imported/exported across the eBGP boundary.

**Needed:** Whenever you have eBGP EVPN peering between sites with different ASNs (which is the most common DCI design).

</details>

### Q6. What is route summarization at the WAN boundary and why is it critical?

<details><summary>Answer</summary>

Route summarization means advertising a single aggregate route (e.g., 10.1.0.0/16) instead of all internal /24 or /32 routes to the WAN. This is critical because:

1. **Reduces WAN routing table size** — fewer BGP routes to carry across sites
2. **Improves convergence** — changes to internal routes don't trigger WAN BGP updates
3. **Hides internal topology** — remote sites don't need to know your leaf-level addressing
4. **PCI-DSS alignment** — limits exposure of internal network structure

</details>

### Q7. How would you test WAN DCI resiliency? List 3 specific tests.

<details><summary>Answer</summary>

1. **Kill primary WAN link:** Shut the primary inter-site link → verify traffic fails over to backup in < 3s (BFD + BGP)
2. **Kill border gateway:** Shut the primary border GW → verify routes reconverge via secondary GW
3. **WAN link flap:** Bounce the link 5× in 60 seconds → verify no routing loops, clean reconvergence, and route dampening doesn't permanently suppress routes

</details>

### Q8. What BGP communities would you use for WAN traffic engineering?

<details><summary>Answer</summary>

- **Site origin:** `65001:100:1` — identifies which site originated the route (useful for policy decisions)
- **Traffic class:** `65001:200:1` — marks routes for specific QoS treatment
- **Primary/backup:** Combined with local-preference (LP 200 for primary, LP 100 for backup)
- **No-export:** Prevent certain routes from being advertised beyond the local AS

</details>

### Q9. What is the purpose of BFD on WAN eBGP sessions, and what are typical settings?

<details><summary>Answer</summary>

BFD provides sub-second failure detection on the WAN link. Without BFD, BGP relies on its holdtime (default 180s) to detect a failure — far too slow for production.

Typical settings: **Interval 300ms, Multiplier 3 = 900ms detection time.** This means if 3 consecutive BFD packets are missed (900ms), the BGP session is immediately torn down and traffic fails over to the backup path.

</details>

### Q10. You're onboarding a new site to the WAN. What information do you need from the site fabric team?

<details><summary>Answer</summary>

1. **ASN** — what AS is the new site using?
2. **Border gateway loopback IPs** — for BGP peering
3. **WAN link IPs** — P2P subnet for the eBGP connection
4. **Route summary** — what aggregate prefix will they advertise?
5. **VRFs** — which VRFs need inter-site connectivity?
6. **Route targets** — for EVPN import/export
7. **Communities** — what community tags will they use?
8. **BFD settings** — must be consistent on both ends
9. **MTU** — verify jumbo frame support end-to-end
10. **PCI-DSS zone** — does this site carry CDE traffic?

</details>
