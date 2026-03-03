# 🌐 Versa Networks SD-WAN — Primer for WAN Core Engineers

> Versa Networks is Fiserv's confirmed SD-WAN platform. As a WAN Core Engineer, this is likely your primary tool. This primer covers Versa's architecture, how it relates to the EVPN/VXLAN concepts you already know, and what you need to learn.

---

## Why Versa (Not Cisco Viptela)?

Fiserv chose Versa over Cisco Viptela for their SD-WAN. Key reasons (from public sources):

1. **Integrated security** — Versa VOS includes FW, IPS, URL filtering, anti-malware built in
2. **Multi-tenancy** — Native VRF-based segmentation maps directly to PCI-DSS requirements
3. **EVPN/VXLAN support** — VOS devices act as VTEPs, using the same encapsulation as DC fabrics
4. **Flexible deployment** — Runs on x86 hardware, VMs, or cloud (AWS/Azure/GCP)
5. **Single-pass architecture** — All security functions processed in one pass through the packet

---

## Architecture Components

```
┌──────────────────────────────────────────────────────┐
│                  VERSA SD-WAN                        │
│                                                      │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────┐ │
│  │   Director   │  │  Controller  │  │  Analytics   │ │
│  │  (Management)│  │   (Policy)   │  │ (Monitoring) │ │
│  │  Templates,  │  │  Route dist, │  │  DPI, flow   │ │
│  │  provisioning│  │  path select │  │  reporting   │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
│         │                 │                  │         │
│         └─────────────────┼──────────────────┘         │
│                           │                            │
│                    Control Plane                        │
│  ═══════════════════════════════════════════════════   │
│                     Data Plane                         │
│                           │                            │
│    ┌──────────┐    ┌──────────┐    ┌──────────┐       │
│    │ VOS CPE  │    │ VOS CPE  │    │ VOS CPE  │       │
│    │ (Branch) │    │  (DC)    │    │ (Cloud)  │       │
│    │ FlexVNF  │    │ FlexVNF  │    │ FlexVNF  │       │
│    └──────────┘    └──────────┘    └──────────┘       │
│                                                        │
└──────────────────────────────────────────────────────┘
```

### Component Details

| Component            | Function                                                                 | Equivalent In...                   |
| -------------------- | ------------------------------------------------------------------------ | ---------------------------------- |
| **Versa Director**   | Centralized management, template-based provisioning, GUI/API             | Cisco vManage                      |
| **Versa Controller** | Policy distribution, overlay routing, SD-WAN path selection              | Cisco vSmart                       |
| **Versa Analytics**  | Traffic analytics, DPI, application visibility, reporting                | Cisco vAnalytics                   |
| **VOS (Versa OS)**   | Runs on CPE appliances at branches/DCs. Full networking + security stack | Cisco cEdge (IOS-XE)               |
| **FlexVNF**          | Virtual network functions on VOS — FW, routing, SD-WAN, all in one       | Individual VNFs on other platforms |

---

## How Your EVPN/VXLAN Knowledge Maps to Versa

This is the most important section. **Everything you've learned about EVPN/VXLAN applies directly:**

| DC Fabric Concept       | Versa SD-WAN Equivalent              | What's The Same                            |
| ----------------------- | ------------------------------------ | ------------------------------------------ |
| Leaf switch (VTEP)      | VOS CPE device (VTEP)                | Both encapsulate/decapsulate VXLAN         |
| Spine (Route Reflector) | Versa Controller                     | Both reflect EVPN routes to all endpoints  |
| iBGP EVPN overlay       | MP-BGP EVPN between VOS devices      | Same BGP address family (AFI 25/SAFI 70)   |
| L2VNI (VLAN extension)  | VOS VNI segments                     | Same VXLAN encapsulation                   |
| L3VNI (VRF transit)     | VOS routing instances / tenants      | Same VRF-based L3 isolation                |
| VRF                     | VOS tenant/routing-instance          | Same multi-tenancy model                   |
| Anycast Gateway         | VOS gateway per tenant               | Same distributed gateway concept           |
| OSPF underlay           | Underlay routing (or SD-WAN overlay) | Transport differs, but concept is the same |

### Key Differences from DC Fabric

| Aspect             | DC Fabric                         | Versa SD-WAN                           |
| ------------------ | --------------------------------- | -------------------------------------- |
| **Transport**      | Dedicated fabric links (25G/100G) | Internet, MPLS, LTE (variable quality) |
| **Path selection** | ECMP across spines                | Application-aware routing (SLA-based)  |
| **Security**       | Separate firewall appliances      | Integrated in VOS (single-pass)        |
| **Scale**          | Hundreds of leaves per fabric     | Thousands of CPE devices globally      |
| **Provisioning**   | Manual or Ansible                 | Zero Touch Provisioning (ZTP)          |
| **Encryption**     | Optional (MACsec)                 | Always-on IPsec                        |

---

## Versa-Specific Concepts to Learn

### 1. Application-Aware Routing (AAR)

Unlike DC fabrics where all paths are equal (ECMP), SD-WAN must choose between paths of different quality:

```
Branch VOS CPE
├── Transport 1: MPLS (low latency, expensive)
├── Transport 2: Internet (variable latency, cheap)
└── Transport 3: LTE (high latency, backup)

Application SLA Policy:
  Voice/Video → MPLS only (latency < 50ms, jitter < 10ms)
  Business Apps → MPLS preferred, Internet fallback
  Internet Traffic → Direct internet breakout
```

### 2. Zero Touch Provisioning (ZTP)

New branch deployments are automated:

1. Ship VOS appliance to branch
2. Appliance contacts Director via staging URL
3. Director pushes full config template
4. Branch is operational in minutes — no engineer on-site

### 3. Multi-Tenancy for PCI-DSS

Versa's VRF model maps directly to PCI zones:

```
VOS CPE (Branch)
├── Tenant: CDE        → VRF with PCI cardholder data
│   └── VNI 50001, strict isolation, encrypted transport
├── Tenant: Corporate   → VRF for user traffic
│   └── VNI 50002, internet breakout allowed
└── Tenant: Management  → VRF for NOC/monitoring
    └── VNI 50004, route leak to CDE via firewall
```

### 4. Versa Director Templates

Configuration is template-driven (similar to Ansible roles):

- **Device Template** — Base system config (hostname, DNS, NTP)
- **WAN Template** — Transport interfaces, IPsec, routing
- **LAN Template** — VLANs, VRFs, IRB interfaces
- **Security Template** — FW rules, IPS policy, URL filtering
- **Application Template** — SLA classes, steering policy

---

## CLI Comparison: Versa VOS vs. Cisco

| Task                     | Versa VOS CLI                     | Cisco IOS-XE                 |
| ------------------------ | --------------------------------- | ---------------------------- |
| Show BGP peers           | `show bgp neighbors`              | `show bgp summary`           |
| Show SD-WAN tunnels      | `show sdwan tunnel statistics`    | `show sdwan bfd sessions`    |
| Show application routing | `show sdwan app-route statistics` | `show sdwan app-route stats` |
| Show VRF routes          | `show ip route vrf TENANT-A`      | `show ip route vrf TENANT-A` |
| Show interfaces          | `show interfaces`                 | `show interfaces`            |
| Show VXLAN tunnels       | `show vxlan tunnel`               | `show nve peers`             |
| Enter config mode        | `configure`                       | `configure terminal`         |
| Commit changes           | `commit`                          | N/A (direct apply)           |

> **Note:** VOS CLI is Junos-influenced (candidate config + commit model), which is good news if you know Junos.

---

## What to Study First

1. **Versa Architecture Overview** — Understand Director/Controller/Analytics relationship
2. **VOS VRF/Tenant Model** — How multi-tenancy works (same as your VRF/L3VNI knowledge)
3. **EVPN on Versa** — Confirm the MP-BGP EVPN implementation matches what you know
4. **Application Steering** — New concept vs. DC fabric ECMP (SLA-based path selection)
5. **Director Templates** — How config management works at scale

### Resources

- [Versa Networks Documentation](https://docs.versa-networks.com/)
- [Versa SD-WAN Architecture Guide](https://versa-networks.com/resources/)
- Versa Director GUI — ask for lab access on Day 1
- Versa VOS CLI Reference — available in Director documentation
