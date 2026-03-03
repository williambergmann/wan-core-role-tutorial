# 📖 WAN Core Engineering — Glossary

> Every acronym and term you'll hear in the first week on the job.  
> Organized by domain. Ctrl+F is your friend.

---

## Routing — BGP

| Term                         | Meaning                                                                                                                  |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| **BGP**                      | Border Gateway Protocol — the inter-domain routing protocol of the internet and WAN cores                                |
| **eBGP**                     | External BGP — peering between different Autonomous Systems                                                              |
| **iBGP**                     | Internal BGP — peering within the same Autonomous System                                                                 |
| **AS / ASN**                 | Autonomous System (Number) — a routing domain under single administration. Private: 64512–65534, 4200000000–4294967294   |
| **MP-BGP**                   | Multi-Protocol BGP (RFC 4760) — extends BGP to carry multiple address families (IPv6, EVPN, VPNv4, etc.)                 |
| **AFI/SAFI**                 | Address Family Identifier / Subsequent AFI — how BGP signals what route types it can carry (e.g., AFI 25/SAFI 70 = EVPN) |
| **RR**                       | Route Reflector — device that re-advertises iBGP routes to avoid full mesh                                               |
| **Cluster ID**               | Identifies a route reflector cluster to prevent loops                                                                    |
| **LP / Local-Pref**          | Local Preference — iBGP attribute, higher = more preferred. Default 100                                                  |
| **MED**                      | Multi-Exit Discriminator — suggests to eBGP peers which entry point to prefer. Lower = better                            |
| **AS-Path**                  | List of ASNs a route has traversed. Shorter = more preferred (by default)                                                |
| **AS-Path Prepend**          | Artificially making a path look longer to discourage its use                                                             |
| **Community**                | BGP attribute (32-bit) to tag routes for policy. Format: `ASN:Value` (e.g., 65001:100)                                   |
| **Large Community**          | 96-bit community (RFC 8092). Format: `ASN:LocalData1:LocalData2`                                                         |
| **Extended Community**       | 64-bit community used for VPN route targets, EVPN, etc.                                                                  |
| **RT (Route Target)**        | Extended community that controls VRF route import/export                                                                 |
| **RD (Route Distinguisher)** | Makes VPN routes unique in BGP even if prefixes overlap. Format: `IP:ID` or `ASN:ID`                                     |
| **Next-Hop**                 | IP address traffic should be forwarded to. eBGP changes it; iBGP preserves it (unless next-hop-self)                     |
| **Next-Hop Self**            | iBGP speaker replaces the eBGP next-hop with its own address                                                             |
| **Prefix List**              | Ordered list of IP prefixes used for route filtering                                                                     |
| **Route Map**                | (Cisco/Arista) Policy applied to BGP routes — match + set                                                                |
| **Policy Statement**         | (Juniper) Equivalent of route-map                                                                                        |
| **Weight**                   | Cisco-only local BGP attribute. Highest wins. Never leaves the router                                                    |
| **BFD**                      | Bidirectional Forwarding Detection — sub-second link failure detection                                                   |

## Routing — OSPF

| Term                  | Meaning                                                                          |
| --------------------- | -------------------------------------------------------------------------------- |
| **OSPF**              | Open Shortest Path First — link-state IGP, used as underlay in WAN/fabric        |
| **Area 0**            | Backbone area — all other areas must connect to it                               |
| **ABR**               | Area Border Router — connects two OSPF areas                                     |
| **ASBR**              | Autonomous System Boundary Router — redistributes external routes into OSPF      |
| **SPF**               | Shortest Path First (Dijkstra's algorithm) — how OSPF computes best paths        |
| **LSA**               | Link-State Advertisement — OSPF routing information unit                         |
| **LSDB**              | Link-State Database — each router's view of the network topology                 |
| **DR/BDR**            | Designated Router / Backup DR — used on broadcast networks (not on P2P links)    |
| **P2P**               | Point-to-Point — OSPF network type for fabric links. No DR/BDR election          |
| **Passive Interface** | OSPF interface that advertises its subnet but doesn't send hellos                |
| **Stub Area**         | OSPF area that doesn't accept external routes (Type 5 LSAs)                      |
| **NSSA**              | Not-So-Stubby Area — stub area that allows limited external routes (Type 7 LSAs) |
| **Hello Timer**       | Default 10s (broadcast/P2P). How often OSPF sends hello packets                  |
| **Dead Timer**        | Default 40s. Neighbor declared dead if no hello received in this time            |
| **Router-ID**         | 32-bit identifier for each OSPF router. Usually set to loopback IP               |

## Data Plane — EVPN / VXLAN

| Term                    | Meaning                                                                                                           |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------- |
| **EVPN**                | Ethernet VPN (RFC 7432) — BGP-based control plane for L2/L3 VPN services                                          |
| **VXLAN**               | Virtual Extensible LAN (RFC 7348) — tunneling protocol that encapsulates L2 frames in UDP                         |
| **VNI**                 | VXLAN Network Identifier — 24-bit ID that identifies a VXLAN segment (like VLAN but 16M scale)                    |
| **VTEP**                | VXLAN Tunnel Endpoint — device that encaps/decaps VXLAN. Usually a leaf switch                                    |
| **NVE**                 | Network Virtualization Edge — Cisco term for VTEP interface                                                       |
| **L2VNI**               | Layer 2 VNI — extends a single VLAN/broadcast domain across the fabric                                            |
| **L3VNI**               | Layer 3 VNI — enables inter-subnet routing within a VRF across the fabric (transit VNI)                           |
| **Symmetric IRB**       | Integrated Routing and Bridging where both ingress and egress leaves perform routing. The standard for production |
| **Asymmetric IRB**      | Routing only at ingress leaf. Requires all VLANs on all leaves. Doesn't scale                                     |
| **Anycast Gateway**     | Same IP + same MAC on every leaf for a given VLAN. Enables seamless host mobility                                 |
| **ARP Suppression**     | Leaf responds to ARP locally using EVPN-learned data. Reduces broadcast flooding                                  |
| **BUM Traffic**         | Broadcast, Unknown unicast, Multicast — the traffic that must be flooded                                          |
| **Ingress Replication** | Each VTEP sends BUM traffic individually to every other VTEP (no multicast needed)                                |
| **Type 2 Route**        | EVPN MAC/IP Advertisement — the primary host learning mechanism                                                   |
| **Type 3 Route**        | Inclusive Multicast Ethernet Tag — establishes BUM flooding trees                                                 |
| **Type 5 Route**        | IP Prefix Route — advertises IP prefixes (like traditional routing, but in EVPN)                                  |
| **DCI**                 | Data Center Interconnect — extending L2/L3 between data centers or sites                                          |
| **Multi-Site**          | EVPN architecture where border gateways re-originate routes between sites                                         |
| **IRB**                 | Integrated Routing and Bridging — a virtual L3 interface on a VLAN (SVI equivalent in Junos)                      |
| **SVI**                 | Switch Virtual Interface — Cisco/Arista term for an L3 VLAN interface                                             |

## Network Architecture

| Term                 | Meaning                                                                                     |
| -------------------- | ------------------------------------------------------------------------------------------- |
| **Leaf-Spine**       | Two-tier Clos fabric. Leaves connect to all spines. Every path has equal hops               |
| **Leaf**             | Access/ToR switch — hosts connect here                                                      |
| **Spine**            | Aggregation switch — provides interconnectivity between all leaves                          |
| **Border Leaf / GW** | Leaf that connects the fabric to external networks (WAN, firewall, etc.)                    |
| **Clos Topology**    | Non-blocking switch fabric invented by Charles Clos (1952). Leaf-spine is a folded Clos     |
| **Underlay**         | The physical/routed network (OSPF/eBGP) that provides IP reachability between VTEPs         |
| **Overlay**          | The virtual/tunneled network (EVPN/VXLAN) built on top of the underlay                      |
| **WAN Core**         | Backbone routers that interconnect multiple sites across a wide area                        |
| **P Router**         | Provider/transit router — forwards traffic, doesn't terminate VPNs                          |
| **PE Router**        | Provider Edge — terminates VPNs, peers with CEs. Equivalent to border leaf                  |
| **CE Router**        | Customer Edge — connects customer network to the provider/WAN                               |
| **VRF**              | Virtual Routing and Forwarding — isolated routing table on a single device                  |
| **ECMP**             | Equal-Cost Multi-Path — load balancing across multiple equal-metric paths                   |
| **MLAG / MC-LAG**    | Multi-Chassis Link Aggregation — LAG across two physical switches for redundancy            |
| **ESI**              | Ethernet Segment Identifier — EVPN's multi-homing mechanism (replaces MLAG in some designs) |
| **Fabric**           | The collection of leaf + spine switches + overlay forming a single logical network          |
| **Pod**              | A self-contained fabric unit within a larger data center (multiple pods = multi-pod)        |

## Operations & Process

| Term                       | Meaning                                                                       |
| -------------------------- | ----------------------------------------------------------------------------- |
| **CAB**                    | Change Advisory Board — approves production changes                           |
| **MOP**                    | Method of Procedure — step-by-step execution plan for a change                |
| **RCA**                    | Root Cause Analysis — post-incident document explaining what happened and why |
| **P1 / P2 / P3**           | Incident priority levels. P1 = complete outage, P2 = degraded, P3 = minor     |
| **SLA**                    | Service Level Agreement — measurable performance targets                      |
| **MTTR**                   | Mean Time To Repair — average time to fix an incident                         |
| **Runbook**                | Step-by-step operational guide for common tasks and troubleshooting           |
| **Rollback**               | Reverting a change to the previous state                                      |
| **Pre-check / Post-check** | Capturing network state before and after a change for comparison              |
| **OOB**                    | Out-of-Band — management network separate from production data path           |
| **IPAM**                   | IP Address Management — system tracking all IP allocations (e.g., NetBox)     |
| **DCIM**                   | Data Center Infrastructure Management — physical infrastructure tracking      |
| **NMS**                    | Network Management System — monitoring and alerting platform                  |
| **SNMP**                   | Simple Network Management Protocol — legacy but still widely used for polling |
| **Streaming Telemetry**    | Push-based, real-time data export from devices (replaces SNMP polling)        |
| **gRPC / gNMI**            | Google RPC / gRPC Network Management Interface — modern telemetry transport   |
| **NetFlow / sFlow**        | Traffic flow sampling and analysis protocols                                  |

## Security & Segmentation

| Term           | Meaning                                                                      |
| -------------- | ---------------------------------------------------------------------------- |
| **SGT**        | Security Group Tag — Cisco TrustSec identity-based tag                       |
| **ISE**        | Identity Services Engine — Cisco's NAC platform                              |
| **802.1X**     | Port-based network access control standard                                   |
| **CoA**        | Change of Authorization (RFC 5176) — ISE tells switch to re-auth a session   |
| **NAC**        | Network Access Control — authentication and authorization for network access |
| **NSX-T DFW**  | VMware NSX-T Distributed Firewall — micro-segmentation at hypervisor level   |
| **Zero Trust** | Security model: never trust, always verify, least-privilege access           |
| **NGFW**       | Next-Generation Firewall (Palo Alto, etc.)                                   |
| **App-ID**     | Palo Alto's application identification technology                            |
| **User-ID**    | Palo Alto's user-to-IP mapping (integrates with AD)                          |

## WAN Technologies

| Term                     | Meaning                                                                       |
| ------------------------ | ----------------------------------------------------------------------------- |
| **MPLS**                 | Multi-Protocol Label Switching — label-based forwarding in SP/WAN cores       |
| **SD-WAN**               | Software-Defined WAN — overlay WAN with centralized policy and path selection |
| **OMP**                  | Overlay Management Protocol — Viptela's SD-WAN routing protocol               |
| **TLOC**                 | Transport Location — SD-WAN identifier for a transport interface              |
| **AAR**                  | Application-Aware Routing — SD-WAN feature to steer apps by SLA               |
| **DMVPN**                | Dynamic Multipoint VPN — legacy WAN overlay technology                        |
| **GRE**                  | Generic Routing Encapsulation — simple tunneling protocol                     |
| **IPsec**                | IP Security — encryption for WAN traffic                                      |
| **SR / Segment Routing** | Modern label-based forwarding replacing RSVP-TE in some WAN cores             |
| **SR-MPLS**              | Segment Routing over MPLS data plane                                          |
| **SRv6**                 | Segment Routing over IPv6 data plane                                          |
