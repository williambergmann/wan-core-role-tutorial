# Module 02 Quiz — EVPN/VXLAN Fabric

> 15 questions. Target: ≥80% (12/15). Open-book is fine for first attempt.

---

### Q1. What is the purpose of VXLAN encapsulation?

<details><summary>Answer</summary>

VXLAN encapsulates Layer 2 Ethernet frames inside UDP packets (port 4789) so they can be transported across a Layer 3 routed underlay. This allows L2 segments to stretch across an IP network without requiring end-to-end L2 connectivity.

</details>

### Q2. How many segments does the 24-bit VNI support, and why does this matter?

<details><summary>Answer</summary>

2^24 = ~16.7 million segments. This matters because traditional 802.1Q VLANs are limited to 4,094 (12-bit VLAN ID). In large multi-tenant environments (like Fiserv post-merger), you need far more segmentation than 4K VLANs can provide.

</details>

### Q3. What is the minimum MTU required on VXLAN underlay links, and why?

<details><summary>Answer</summary>

9214 bytes (jumbo frames). VXLAN adds ~50 bytes of overhead (outer Ethernet 14B + outer IP 20B + UDP 8B + VXLAN header 8B). Without jumbo frames, inner frames above ~1450 bytes would be fragmented or dropped, causing silent failures for large packets.

</details>

### Q4. Name all 5 EVPN route types and their primary purpose.

<details><summary>Answer</summary>

1. **Type 1 (Ethernet Auto-Discovery):** Multi-homing — ESI membership and aliasing
2. **Type 2 (MAC/IP Advertisement):** Host learning — replaces flood-and-learn
3. **Type 3 (Inclusive Multicast):** BUM traffic flooding tree setup
4. **Type 4 (Ethernet Segment):** DF election for multi-homed hosts
5. **Type 5 (IP Prefix):** L3 routing — external prefix advertisement in EVPN

</details>

### Q5. What is the difference between an L2VNI and an L3VNI?

<details><summary>Answer</summary>

**L2VNI** maps to a VLAN and extends a Layer 2 broadcast domain across the VXLAN fabric. It carries MAC-level traffic within a single subnet.

**L3VNI** maps to a VRF and enables inter-subnet routing (Symmetric IRB). It's the "transit VNI" that carries routed traffic between different subnets/L2VNIs within the same VRF.

</details>

### Q6. Explain Symmetric IRB in your own words. Why is it called "symmetric"?

<details><summary>Answer</summary>

In Symmetric IRB, BOTH the ingress and egress VTEPs perform routing. The ingress leaf routes the packet from the source VLAN into the L3VNI (VRF transit), and the egress leaf routes from the L3VNI into the destination VLAN. It's "symmetric" because both sides do a routing lookup (unlike Asymmetric IRB where only the ingress side routes).

**Key advantage:** Each leaf only needs to have the VLANs that are locally present — it doesn't need every VLAN in the fabric.

</details>

### Q7. What is an Anycast Gateway, and why is it important for VM mobility?

<details><summary>Answer</summary>

An Anycast Gateway is the same IP address AND the same virtual MAC address configured on every leaf for a given VLAN/SVI. This means every leaf acts as the default gateway for hosts in that VLAN.

It's critical for VM mobility because when a VM moves from Leaf-1 to Leaf-3, it does NOT need to re-ARP for the gateway — the gateway IP and MAC are identical on both leaves. Traffic flows immediately without any convergence delay.

</details>

### Q8. What NX-OS command shows you all discovered VTEP peers?

<details><summary>Answer</summary>

`show nve peers` — shows all remote VTEPs discovered via BGP EVPN, their state (Up/Down), and the VNIs they share.

</details>

### Q9. What is the function of `ingress-replication protocol bgp` on an NVE member VNI?

<details><summary>Answer</summary>

It enables head-end replication for BUM (Broadcast, Unknown unicast, Multicast) traffic using BGP EVPN Type-3 routes to discover remote VTEPs. Instead of using multicast in the underlay, the ingress VTEP replicates BUM frames and sends a copy to each remote VTEP individually via unicast.

</details>

### Q10. What are Route Targets (RT) and Route Distinguishers (RD) in EVPN?

<details><summary>Answer</summary>

**Route Distinguisher (RD):** Makes EVPN routes globally unique. Each VTEP uses a different RD (typically `loopback:VNI-ID`). RD is for uniqueness, NOT for filtering.

**Route Target (RT):** Controls import/export of routes between VRFs/VNIs. If a VRF exports with RT `65000:50001`, only VRFs that import RT `65000:50001` will receive those routes. RT is for **policy**.

</details>

### Q11. What four components are required for an L3VNI on NX-OS?

<details><summary>Answer</summary>

1. **VRF vni assignment:** `vrf context X → vni 50001`
2. **Transit VLAN:** `vlan 999 → vn-segment 50001`
3. **Transit SVI:** `interface vlan 999 → vrf member X → ip forward`
4. **NVE association:** `interface nve1 → member vni 50001 associate-vrf`

All four must be present. Missing any one causes inter-subnet routing to fail across leaves.

</details>

### Q12. How does EVPN ARP suppression work, and why is it beneficial?

<details><summary>Answer</summary>

When a leaf learns a host's MAC-IP binding (via EVPN Type-2 route), it can respond to ARP requests on behalf of remote hosts locally, WITHOUT flooding the ARP request across the VXLAN fabric.

**Benefit:** Dramatically reduces BUM traffic (ARP broadcasts) in the overlay — particularly important at scale with thousands of hosts.

</details>

### Q13. What is the BGP `l2vpn evpn` address family, and why must it be explicitly configured?

<details><summary>Answer</summary>

BGP supports multiple address families (AFI/SAFI). The `l2vpn evpn` address family (AFI 25, SAFI 70) carries EVPN routes (Type 1-5). It must be explicitly activated on all BGP neighbors that need to exchange EVPN routes. A BGP session can be Established for IPv4 but carry zero EVPN routes if this AFI is not configured.

</details>

### Q14. What is the difference between `show l2route evpn mac all` and `show mac address-table`?

<details><summary>Answer</summary>

`show mac address-table` shows the traditional L2 forwarding table (locally learned + remote MACs).

`show l2route evpn mac all` shows the EVPN-specific MAC database — it includes the VNI, the VTEP source, and whether the MAC was learned locally or remotely via EVPN Type-2 routes. The EVPN table is the source of truth for the overlay.

</details>

### Q15. Draw or describe the packet flow when Host A (VLAN 100, Leaf-1) pings Host B (VLAN 200, Leaf-3) using Symmetric IRB.

<details><summary>Answer</summary>

```
1. Host A → Leaf-1: "ping 10.200.0.30" (regular Ethernet frame)
2. Leaf-1: Routes VLAN 100 → VRF TENANT-A → destination is in VLAN 200
3. Leaf-1: Looks up EVPN route for 10.200.0.30 → via Leaf-3 VTEP 10.255.1.3
4. Leaf-1: Encapsulates with VXLAN header, VNI = 50001 (L3VNI for VRF)
5. Leaf-1: Outer IP: src=10.255.1.1, dst=10.255.1.3, UDP 4789
6. Spine: Routes based on outer IP (OSPF underlay)
7. Leaf-3: Decapsulates VXLAN, sees VNI 50001 → VRF TENANT-A
8. Leaf-3: Routes VRF → VLAN 200 → resolves dest MAC for Host B
9. Leaf-3 → Host B: delivers the original ICMP echo request
```

Both Leaf-1 AND Leaf-3 performed a routing lookup (symmetric).

</details>
