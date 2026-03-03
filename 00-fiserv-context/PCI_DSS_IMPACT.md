# 🔒 PCI-DSS v4.0 — Network Design Impact

> Fiserv processes billions of card transactions. PCI-DSS compliance is not optional — it drives nearly every network design decision. As a WAN Core Engineer, you must understand how PCI requirements translate to VRF segmentation, firewall insertion, and traffic isolation.

---

## What Is PCI-DSS?

**Payment Card Industry Data Security Standard** — a set of security requirements for any organization that stores, processes, or transmits cardholder data. Fiserv is a **Level 1 Service Provider** (highest tier), meaning the strictest requirements apply.

---

## Requirements That Impact Network Design

| PCI-DSS Req | Requirement Summary                | Network Impact                              | Implementation                                     |
| ----------- | ---------------------------------- | ------------------------------------------- | -------------------------------------------------- |
| **1.1**     | Firewall at CDE boundary           | Every CDE↔non-CDE path traverses a firewall | Service leaf + PBR or VRF-based firewall insertion |
| **1.2**     | Restrict CDE traffic               | Only authorized connections to CDE          | ACLs, security groups, VRF isolation               |
| **1.3**     | No direct internet to CDE          | DMZ required                                | Separate VRF for DMZ, firewall between             |
| **2.1**     | Change defaults                    | No default passwords/communities            | SNMP v3, unique credentials per device             |
| **4.1**     | Encrypt cardholder data in transit | All CDE transport encrypted                 | IPsec, MACsec, TLS on WAN links                    |
| **10.1**    | Audit trail                        | Log all CDE network access                  | sFlow/NetFlow, SIEM integration                    |
| **11.1**    | Quarterly scans                    | Network vulnerability scanning              | Nessus/Qualys on CDE segments                      |

---

## How This Maps to EVPN/VXLAN

The EVPN/VXLAN fabric provides the segmentation primitives that make PCI-DSS compliance achievable:

```
┌─────────────────────────────────────────────────────────┐
│                   EVPN/VXLAN FABRIC                     │
│                                                         │
│  ┌───── VRF: CDE ──────┐   ┌──── VRF: Corporate ───┐  │
│  │ L2VNI 10100          │   │ L2VNI 10300           │  │
│  │ Payment Servers      │   │ User Workstations     │  │
│  │ L3VNI 50001          │   │ L3VNI 50002           │  │
│  └─────────┬────────────┘   └─────────┬─────────────┘  │
│            │                          │                  │
│            └──────── Firewall ────────┘                  │
│             (Service Leaf / PBR)                         │
│             PCI-DSS Req 1.1 ✓                            │
│                                                         │
│  ┌───── VRF: DMZ ──────┐   ┌──── VRF: Management ──┐  │
│  │ L2VNI 10500          │   │ L2VNI 10600           │  │
│  │ Internet-facing      │   │ NOC, jump hosts       │  │
│  │ L3VNI 50003          │   │ L3VNI 50004           │  │
│  │ No direct CDE access │   │ Leaks to/from CDE     │  │
│  │ PCI-DSS Req 1.3 ✓    │   │ (through firewall)    │  │
│  └──────────────────────┘   └───────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### VRF-to-PCI Zone Mapping

| VRF        | L3VNI | PCI Zone            | Purpose                     | Route Leaking              |
| ---------- | ----- | ------------------- | --------------------------- | -------------------------- |
| CDE        | 50001 | Cardholder Data Env | Payment processing servers  | To/from Mgmt (via FW only) |
| Corporate  | 50002 | Corporate           | User workstations, email    | Isolated from CDE          |
| DMZ        | 50003 | DMZ                 | Internet-facing services    | No CDE access ever         |
| Management | 50004 | Management          | NOC, monitoring, jump hosts | To/from CDE (via FW only)  |

### Key Design Principles

1. **VRF isolation is the foundation** — CDE traffic never shares a routing table with corporate traffic
2. **Firewall at every boundary** — VRF route leaking alone is NOT sufficient; traffic must be inspected
3. **L3VNI per zone** — Each PCI zone gets its own L3VNI for fabric-wide routing isolation
4. **Audit everything** — NetFlow/sFlow on all CDE-facing interfaces feeds into SIEM
5. **Encrypt WAN traffic** — CDE data crossing the WAN must be encrypted (IPsec or MACsec)

---

## What This Means for Your Role

As a WAN Core Engineer at Fiserv:

- **Every VRF design must consider PCI zones** — You can't just create VRFs for convenience
- **Firewall insertion is mandatory** — Know how to integrate firewalls into EVPN fabrics (service leaf, PBR)
- **WAN links carrying CDE traffic need encryption** — IPsec tunnels or MACsec on DCI links
- **Documentation must include PCI mapping** — Your design docs must show which VRFs/VNIs are CDE scoped
- **Changes to CDE segments require extra scrutiny** — More rigorous change management for CDE-touching changes
