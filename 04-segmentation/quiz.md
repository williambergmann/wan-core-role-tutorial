# Module 04 Quiz — Segmentation (VRF, L3VNI, PCI-DSS)

> 10 questions. Target: ≥80% (8/10). PCI-DSS awareness is a differentiator for this role.

---

### Q1. What is a VRF and how does it provide network segmentation?

<details><summary>Answer</summary>

A VRF (Virtual Routing and Forwarding) creates an isolated routing table on a device. Each VRF has its own RIB, FIB, and interfaces. Traffic in one VRF cannot reach another VRF unless explicitly leaked (via route-target import or firewall). This provides Layer 3 isolation at the network level — essential for PCI-DSS compliance.

</details>

### Q2. Name the minimum VRFs you would deploy in a Fiserv environment and why.

<details><summary>Answer</summary>

1. **CDE (Cardholder Data Environment)** — Payment processing, credit card data. Highest security.
2. **Corporate** — User workstations, office apps. Must be isolated from CDE.
3. **DMZ** — Internet-facing services. Must NEVER have direct access to CDE.
4. **Management** — NOC monitoring, SNMP collectors. Needs to reach CDE for monitoring, but ONLY through a firewall.

Optionally: **Development** (isolated dev/test).

</details>

### Q3. What is route leaking and when is it acceptable in PCI-DSS?

<details><summary>Answer</summary>

Route leaking imports routes from one VRF into another, enabling cross-VRF communication. In PCI-DSS:

**Acceptable:** Management VRF leaking CDE routes for monitoring purposes — BUT all actual traffic must traverse an inspecting firewall (route leaking alone is NOT sufficient for compliance).

**NOT acceptable:** Direct route leaking between CDE and Corporate or CDE and DMZ without firewall inspection. PCI-DSS requires all traffic to/from the CDE to be inspected.

</details>

### Q4. How do you configure route leaking using Route Targets in EVPN?

<details><summary>Answer</summary>

By importing the remote VRF's Route Target:

```
vrf context MANAGEMENT
  vni 50004
  address-family ipv4 unicast
    route-target import 65000:50004      ← own routes
    route-target import 65000:50004 evpn
    route-target export 65000:50004
    route-target export 65000:50004 evpn
    route-target import 65000:50001      ← leak CDE routes IN
    route-target import 65000:50001 evpn
```

This makes CDE routes visible in the Management VRF routing table.

</details>

### Q5. Why is route leaking alone NOT sufficient for PCI-DSS compliance?

<details><summary>Answer</summary>

Route leaking provides routing-level connectivity, but PCI-DSS requires **traffic inspection** between zones. Route leaking creates the path, but doesn't enforce:

- Stateful firewall inspection
- IDS/IPS monitoring
- Logging and audit trails
- Access control lists

You must combine route leaking with firewall service insertion (service leaf or VRF-aware inline firewall) to meet PCI-DSS requirements.

</details>

### Q6. What is a "service leaf" in a firewall insertion design?

<details><summary>Answer</summary>

A service leaf is a leaf switch dedicated to connecting shared services like firewalls, load balancers, and IDS/IPS. The firewall has interfaces in multiple VRFs (e.g., one in CDE, one in Management). All cross-VRF traffic is routed through the service leaf → firewall → back to the fabric.

**Advantage:** Centralizes service insertion without requiring every leaf to have firewall connectivity.

</details>

### Q7. How would you verify that VRF isolation is working correctly?

<details><summary>Answer</summary>

```bash
# 1. Verify routing tables are separate
show ip route vrf CDE
show ip route vrf CORPORATE
# Each should only contain its own routes (+ explicitly leaked routes)

# 2. Test isolation — from a host in CDE:
ping 10.102.0.10    # Corporate IP → should FAIL
ping 10.103.0.10    # DMZ IP → should FAIL

# 3. Verify VRF membership
show vrf
show vrf interface

# 4. Verify RT import/export
show bgp l2vpn evpn | grep RT
```

</details>

### Q8. What is the relationship between an L3VNI and a VRF?

<details><summary>Answer</summary>

Each VRF has exactly one L3VNI assigned. The L3VNI acts as the "transit VNI" for that VRF — it carries inter-subnet routed traffic for that VRF across the VXLAN fabric. When Leaf-1 routes traffic to a remote subnet in VRF TENANT-A, it encapsulates the packet with the L3VNI (e.g., 50001) assigned to that VRF. The receiving leaf decapsulates and routes it into the correct local VLAN.

**VRF ↔ L3VNI is a 1:1 mapping.**

</details>

### Q9. What PCI-DSS requirements directly impact network design? Name 3.

<details><summary>Answer</summary>

1. **Requirement 1 (Network Security Controls):** Install and maintain network security controls (firewalls) to protect the CDE. → VRF segmentation + firewall insertion.

2. **Requirement 4 (Strong Cryptography):** Encrypt cardholder data during transmission over open, public networks. → IPsec/MACsec on WAN links carrying CDE traffic.

3. **Requirement 10 (Logging & Monitoring):** Log and monitor all access to network resources and cardholder data. → sFlow/NetFlow on all CDE interfaces, syslog forwarding, SIEM integration.

</details>

### Q10. You're asked to add a new VRF for a development team. Walk through the steps.

<details><summary>Answer</summary>

1. **Assign L3VNI:** Pick an unused VNI (e.g., 50005)
2. **Assign transit VLAN:** Pick an unused VLAN (e.g., 905)
3. **Design RT:** `65000:50005` (import and export)
4. **Assign IP space:** e.g., 10.105.0.0/16
5. **PCI-DSS classification:** Is this zone PCI-scoped? If no → no CDE route leaking allowed
6. **Configure on all relevant leaves:**

   ```
   vrf context DEV
     vni 50005
     rd auto
     address-family ipv4 unicast
       route-target import 65000:50005
       route-target export 65000:50005

   vlan 905
     vn-segment 50005

   interface vlan 905
     vrf member DEV
     ip forward

   interface nve1
     member vni 50005 associate-vrf
   ```

7. **Test isolation:** Verify DEV VRF cannot reach CDE, Corporate, or DMZ
8. **Update documentation:** IPAM, design docs, runbooks

</details>
