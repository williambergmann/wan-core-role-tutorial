# 🎯 Scenario Practice — Whiteboard Exercises

> 5 whiteboard-style scenarios that test your ability to design, troubleshoot, and plan. Practice these by talking through your solution out loud — that's how interviews work.

---

## Scenario 1: Design a WAN for 5 Sites

**Setup:** "We have 5 sites that need to be interconnected. Each site has a leaf-spine EVPN/VXLAN fabric. Design the WAN interconnect."

**Talk through:**

1. ASN assignment — one per site (65001–65005) or regional grouping?
2. eBGP between site border gateways
3. Route summarization at each border (one /16 per site)
4. BGP communities for site identification
5. Primary/backup paths with Local Preference
6. BFD for sub-second failover
7. VRF isolation across the WAN (CDE traffic encrypted)

**Good answer hits:** ASN design, summarization, communities, BFD, PCI-DSS VRF awareness.

---

## Scenario 2: Troubleshoot a DCI Failure

**Setup:** "Site A can't reach Site B. BGP sessions are up, but no routes are being exchanged. What do you check?"

**Talk through:**

1. Verify BGP session state: `show bgp l2vpn evpn summary` — Established? How many prefixes?
2. Check address family: Is l2vpn evpn AFI/SAFI negotiated?
3. Check route-maps: Is an export map blocking routes? `show route-map`
4. Check route targets: Do the import/export RTs match?
5. Check the remote side: Is it advertising? `show bgp neighbor X advertised-routes`
6. Check communities: Is `send-community both` configured?
7. Physical check: Are the WAN links up?

**Good answer hits:** Systematic top-down approach, specific show commands, checks both sides.

---

## Scenario 3: Plan a Fabric Migration

**Setup:** "We need to onboard a new site's EVPN fabric and connect it to the existing WAN core. Walk me through the plan."

**Talk through:**

1. **Design phase:** IP addressing, ASN, VNI/VRF mapping, border GW peering design
2. **Build phase:** Deploy OSPF underlay, BGP EVPN overlay, VXLAN VNIs, border GW configs
3. **Validate phase:** Functional tests (all neighbors up), scale tests, resiliency tests
4. **Migrate phase:** Maintenance window, pre-checks, phased app migration, post-checks
5. **Rollback plan:** What triggers rollback, exact steps to revert
6. **Documentation:** Update IPAM, design docs, runbooks

**Good answer hits:** All 4 phases, pre/post checks, rollback criteria, documentation update.

---

## Scenario 4: PCI-DSS Segmentation Design

**Setup:** "Design the VRF segmentation for a site that handles credit card transactions."

**Talk through:**

1. VRF layout: CDE, Corporate, DMZ, Management (minimum 4 VRFs)
2. L3VNI per VRF for fabric-wide isolation
3. Firewall insertion: All CDE↔non-CDE traffic through firewall
4. Route leaking: Management → CDE (monitoring), but only through FW
5. No direct path: CDE ↔ DMZ, CDE ↔ Corporate
6. WAN encryption: IPsec on any WAN link carrying CDE traffic
7. Audit: NetFlow/sFlow on all CDE interfaces

**Good answer hits:** VRF-to-PCI zone mapping, firewall mandatory, encryption, audit trail.

---

## Scenario 5: Scale Failure

**Setup:** "We added 500 new VNIs to the fabric, and now BGP is unstable. What's happening?"

**Talk through:**

1. Check BGP memory: `show bgp process` — is the RIB too large?
2. Check TCAM: `show hardware capacity` — are we out of hardware entries?
3. Check BGP convergence: Is SPF/best-path running constantly? Check CPU.
4. Check NVE: Are all VNIs operational? `show nve vni`
5. Mitigation: Route filtering, RT-constrain (only import needed VNIs), aggregate routes
6. Long-term: Pod architecture (break into smaller fabrics), hardware upgrade

**Good answer hits:** Hardware limits (TCAM), BGP process memory, RT-constrain, pod design.
