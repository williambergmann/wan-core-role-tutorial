# 🖧 Fiserv — Confirmed Network Stack

> Research-based intelligence from public sources.  
> **Confidence levels:** 🟢 Confirmed | 🟡 Likely | 🔴 Uncertain  
> **Last updated:** 2026-03-03

---

## Company Overview

- **Industry:** Financial technology (fintech) — debit/credit card processing, payments, banking
- **Scale:** One of the world's largest fintech companies (~$17B+ revenue)
- **Merged with First Data** in 2019 (~$22B deal) — still integrating infrastructure
- **Data centers:** Consolidated from many legacy DCs into fewer Tier IV facilities
  - Known facility: 25,000 sq ft Tier IV in Johns Creek, Georgia
  - Modernization initiative: "One Fiserv" — common platform strategy
- **Compliance:** PCI-DSS (Payment Card Industry) is a HUGE driver for network segmentation

---

## WAN / SD-WAN

| Component            | Details                                                      | Confidence   |
| -------------------- | ------------------------------------------------------------ | ------------ |
| **SD-WAN Vendor**    | **Versa Networks** (Secure SD-WAN)                           | 🟢 Confirmed |
| **WAN Transport**    | Moving from legacy MPLS to SD-WAN + internet                 | 🟢 Confirmed |
| **DMVPN**            | Meshed DMVPN for client-facing "Sentry" managed network      | 🟢 Confirmed |
| **WAN Architecture** | Multi-DC, global footprint, direct cloud access via SD-WAN   | 🟢 Confirmed |
| **Versa EVPN/VXLAN** | Versa VOS supports EVPN/VXLAN overlay natively               | 🟢 Confirmed |
| **Versa Components** | Director (mgmt), Controller (policy), Analytics (monitoring) | 🟢 Confirmed |

## Campus / Enterprise

| Component           | Details                                               | Confidence   |
| ------------------- | ----------------------------------------------------- | ------------ |
| **Primary Vendor**  | **Cisco** — 30+ year partnership                      | 🟢 Confirmed |
| **Management**      | **Cisco Catalyst Center** (formerly DNA Center)       | 🟢 Confirmed |
| **Switches**        | **Cisco Catalyst 9000 series** (950 series mentioned) | 🟢 Confirmed |
| **Wireless**        | Cisco (Wi-Fi in branches)                             | 🟢 Confirmed |
| **Network Refresh** | Enterprise Cisco refresh initiated ~2023              | 🟢 Confirmed |

## Data Center

| Component          | Details                                             | Confidence   |
| ------------------ | --------------------------------------------------- | ------------ |
| **Virtualization** | VMware vSphere, vCenter, VDI                        | 🟢 Confirmed |
| **Containers**     | Kubernetes + Portworx (75% storage reduction)       | 🟢 Confirmed |
| **Cloud**          | IBM Cloud (OpenShift, Power10), hybrid cloud        | 🟢 Confirmed |
| **DC Fabric**      | Likely EVPN/VXLAN (via Versa SD-WAN + Cisco campus) | 🟡 Likely    |
| **DC Switches**    | Likely Cisco Nexus or Catalyst 9000 for DC          | 🟡 Likely    |
| **Load Balancers** | F5 or similar (financial services standard)         | 🟡 Likely    |
| **DC Tier**        | Tier IV (2N+1 electrical, N+1 mechanical)           | 🟢 Confirmed |

## Security

| Component            | Details                                                    | Confidence   |
| -------------------- | ---------------------------------------------------------- | ------------ |
| **Firewalls**        | Layered approach — likely Palo Alto and/or Cisco Firepower | 🟡 Likely    |
| **IPS**              | Intrusion Prevention Systems                               | 🟢 Confirmed |
| **Segmentation**     | PCI-DSS compliance = heavy micro-segmentation              | 🟢 Confirmed |
| **Threat Detection** | 24/7 SOC, real-time detection, managed hunting             | 🟢 Confirmed |
| **MFA**              | Multi-factor authentication across the board               | 🟢 Confirmed |

---

## WAN Core Engineer — Role Mapping

### What You'll Touch Daily

1. **Versa SD-WAN** — Director, Controller, Analytics, VOS on CPE
2. **Cisco Catalyst infrastructure** — Catalyst 9000, Catalyst Center
3. **BGP/OSPF routing** — MP-BGP for SD-WAN overlay and EVPN fabric
4. **VRF segmentation** — Critical for PCI-DSS CDE isolation
5. **Multi-DC / DCI** — First Data merger DC consolidation, EVPN Multi-Site

### How Your Skills Map

| Your Knowledge         | Fiserv Application                       |
| ---------------------- | ---------------------------------------- |
| EVPN/VXLAN fabric      | DC fabric + Versa SD-WAN overlay         |
| BGP design patterns    | WAN core eBGP between sites              |
| OSPF underlay          | Intra-site fabric routing                |
| VRF/L3VNI segmentation | PCI-DSS CDE isolation                    |
| Validation testing     | Fabric onboarding pre-production testing |
| Migration runbooks     | First Data consolidation work            |
