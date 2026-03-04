# 🎤 Intro Scripts & Talking Points

> Polished scripts for team introductions, capability discussions, and topic-specific talking points.
> Memorize the **General Intro** and the **Quick Overall Intro**. Keep the rest as reference for when those topics come up.

---

## General Intro — Use This Day 1

> _"Hey everyone, I'm William. I've been working in network engineering for about 10 years, mostly across enterprise campus, data center, and WAN environments. A lot of my background has been around building and supporting modern routing fabrics — things like EVPN/VXLAN overlays, MP-BGP routing, and integrating those environments with WAN and SD-WAN edge networks._
>
> _I've spent quite a bit of time working on greenfield builds and large migrations, helping transition legacy Layer-2 environments into routed fabrics and validating those designs through lab testing and staged production cutovers. Most of my work tends to sit around the core routing and fabric side of the network, making sure routing, segmentation, and traffic flows behave predictably across campus, data center, and WAN domains._
>
> _Looking forward to working with everyone and getting up to speed on the environment here."_

---

## Quick Overall Intro — Shorter Version

> _"Most of my background has been around designing and supporting WAN and fabric routing environments across campus and data center networks. I've worked a lot with EVPN-VXLAN fabrics, MP-BGP routing, and SD-WAN edge integration, helping migrate legacy networks into routed overlay architectures and validating those designs through lab testing and staged production migrations._
>
> _A lot of my work tends to sit around the intersection of routing architecture, fabric overlays, and WAN connectivity — making sure those pieces integrate cleanly and behave predictably at scale."_

---

## Topic-Specific Talking Points

Use these when the conversation naturally goes to a specific area. Don't volunteer all of it — wait for the topic to come up and deploy the relevant piece.

### WAN Design & Build Support

> _"My background is mostly around designing and building core routing and fabric environments across campus, data center, and WAN networks. A lot of my work has involved building EVPN/VXLAN fabrics and integrating them with WAN routing and SD-WAN environments._
>
> _On the routing side I've spent quite a bit of time designing MP-BGP based routing architectures, using EVPN for overlay control planes and OSPF or eye-ess eye-ess for underlay reachability between VTEPs. That typically involved building out L2VNI and L3VNI segmentation models, Anycast gateway routing, and ECMP spine-leaf forwarding paths so traffic stays deterministic across the fabric._
>
> _On the WAN side I've designed and supported multi-homed BGP edge environments with multiple carriers, building routing policy frameworks with prefix filtering, BGP community tagging, and path manipulation so failover and path selection behave predictably across MPLS, DIA, and internet transports."_

### EVPN/VXLAN & Core Routing Architecture

> _"A big focus of my recent work has been helping transition legacy campus and data center environments into EVPN-VXLAN based routing fabrics. That usually means moving away from large L2 domains and STP-based designs and replacing them with routed access models where leaf switches act as distributed gateways using Anycast gateway with symmetric IRB routing._
>
> _From the control plane perspective that's driven by MP-BGP EVPN, handling MAC/IP route advertisement, ARP suppression, and host mobility events across VTEPs. I've spent a lot of time validating how those EVPN route types propagate across fabrics and making sure the overlay routing behavior stays consistent with the underlay IGP topology._
>
> _That overlay architecture also ties into the WAN core, where we establish BGP peering between fabric border nodes and WAN edge routers, ensuring route leaking, aggregation boundaries, and policy enforcement are clean between the fabric and external routing domains."_

### Testing & Validation

> _"One thing I've spent a lot of time doing is validating network designs before they hit production. That usually happens in a lab or staging environment where we test the behavior of routing and overlay protocols under different conditions._
>
> _For EVPN fabrics specifically we'll validate things like route scale in the EVPN control plane, ECMP distribution across spines, BGP convergence during link or node failures, and VTEP reachability across the underlay._
>
> _We also simulate failure scenarios — shutting down uplinks, isolating VTEPs, or forcing routing reconvergence — to confirm the architecture behaves the way we expect before rolling it into production. Once it moves to production we monitor control-plane behavior and forwarding state to make sure the network converges the same way it did in the lab."_

### Migration & Fabric Onboarding

> _"A lot of the projects I've worked on have involved migrating older network environments into newer routing fabrics. One of the bigger efforts involved transitioning traditional campus networks into EVPN routed access architectures, where we moved gateway functions into the leaf layer and migrated VLAN segmentation into L3VNI VRF models._
>
> _Those migrations were usually done in phases, where we maintain both the legacy routing environment and the new fabric in parallel while gradually shifting traffic paths. That requires carefully controlling route advertisements and gateway behavior so traffic remains symmetric during the transition._
>
> _I've also worked on onboarding new application environments into those fabrics by establishing routing boundaries between the fabric and the WAN edge and making sure prefix filtering and policy enforcement keep routes from leaking in unintended ways."_

### Documentation & Runbooks

> _"I also spend a fair amount of time documenting the environments we build. For most of the networks I've worked on we've created architecture standards, routing design documentation, and operational runbooks that describe how the fabric and WAN routing environments are structured._
>
> _That usually includes things like EVPN segmentation models, WAN routing policies, firewall insertion points, and routing failover behavior. Those documents become the reference point for operations teams when they're doing maintenance work or troubleshooting routing behavior."_

### Troubleshooting & Network Stability

> _"My troubleshooting background is mostly around routing and control-plane behavior in larger networks. When something breaks the first thing I usually do is validate the routing state — checking BGP neighbor health, route propagation between EVPN nodes, and next-hop reachability across the underlay._
>
> _From there I'll validate forwarding behavior by checking the RIB and FIB tables and confirming traffic is being hashed across the expected ECMP paths. If the routing state looks correct but traffic still isn't behaving properly, that's when I start digging into packet flows using telemetry or packet capture tools to see where the forwarding path diverges from the routing design."_

---

## Key Phrases to Internalize

These phrases appear across the scripts above. They're the building blocks — you can remix them in real-time:

| Phrase                                                    | What it signals                                      |
| --------------------------------------------------------- | ---------------------------------------------------- |
| _"routing architecture"_                                  | You think at the design level, not just CLI          |
| _"overlay control plane"_                                 | You understand the EVPN abstraction                  |
| _"underlay reachability"_                                 | You know the two-tier model                          |
| _"deterministic forwarding"_                              | You care about predictability, not just connectivity |
| _"route propagation"_                                     | You think about how routes move through the network  |
| _"aggregation boundaries"_                                | You know where to summarize                          |
| _"policy enforcement"_                                    | You think about security and compliance              |
| _"behave predictably at scale"_                           | You've dealt with large environments                 |
| _"staged production cutovers"_                            | You don't yolo changes                               |
| _"validate the routing state"_                            | Your troubleshooting is systematic                   |
| _"routing and control-plane behavior"_                    | You distinguish data plane from control plane        |
| _"the forwarding path diverges from the routing design"_  | You understand the RIB/FIB distinction               |
| _"clean between the fabric and external routing domains"_ | You think about domain boundaries                    |

---

## Pronunciation Reminders for These Scripts

| Term in the scripts | How to say it                             |
| ------------------- | ----------------------------------------- |
| EVPN/VXLAN          | "ee-vee-pee-en / vee-ex-lan"              |
| MP-BGP              | "em-pee-bee-jee-pee" (Multi-Protocol BGP) |
| IS-IS               | "eye-ess eye-ess"                         |
| L2VNI / L3VNI       | "el-two-vee-en-eye / el-three-vee-en-eye" |
| VTEP                | "vee-tep" (rhymes with step)              |
| IRB                 | "eye-are-bee"                             |
| ECMP                | "ee-see-em-pee"                           |
| STP                 | "ess-tee-pee"                             |
| DIA                 | "dee-eye-ay" (Direct Internet Access)     |
| MPLS                | "em-pee-el-ess"                           |
| IGP                 | "eye-jee-pee" (Interior Gateway Protocol) |
| RIB                 | "rib" (rhymes with bib)                   |
| FIB                 | "fib" (rhymes with rib)                   |
| ARP                 | "arp" (say it as a word)                  |
