# 🎤 WAN Core Engineer — Interview Preparation

> **30 interview questions** you're likely to face, with strong answers. Organized by the JD's three pillars: Design & Build, Testing & Validation, Migration & Documentation.

---

## Part 1: WAN Design & Build (12 Questions)

### Q1. Walk me through how you'd design the routing for a new WAN core.

**Strong Answer:**

> "I'd start by defining the routing domains. For the WAN core, I'd use **eBGP between autonomous systems** — each site or region gets its own ASN. Inside each site, **OSPF Area 0** serves as the underlay IGP, distributing loopback addresses for VTEP reachability and BGP peering.
>
> For the overlay, **iBGP with route reflectors** within each site distributes EVPN routes between leaves. At the WAN boundary, border gateways peer via eBGP and exchange both IPv4 unicast and EVPN address families.
>
> I'd apply summarization at each boundary — sites advertise aggregates, not specifics. BGP communities tag routes by source site for downstream policy control. BFD on all peering sessions gives us sub-second failure detection."

---

### Q2. Why eBGP between sites and OSPF inside?

**Strong Answer:**

> "OSPF is excellent within a site because it converges fast, distributes loopbacks efficiently for VTEP reachability, and doesn't require complex policy. But OSPF doesn't scale across a WAN with many sites — the link-state database would become enormous and SPF calculations unpredictable.
>
> eBGP excels at inter-domain routing — it provides policy control through communities and local-preference, natural isolation between sites (each AS is independent), and scales to thousands of prefixes without flooding. So you get the best of both: OSPF's speed inside, BGP's policy and scale outside."

---

### Q3. Explain EVPN/VXLAN to me.

**Strong Answer:**

> "EVPN/VXLAN solves the problem of extending Layer 2 and Layer 3 services across a routed network.
>
> **VXLAN** is the data plane — it encapsulates Layer 2 frames inside UDP packets, so you can send Ethernet traffic across an IP-routed underlay. It adds about 50 bytes of overhead, which is why we need jumbo MTU on the underlay.
>
> **EVPN** is the control plane — it uses BGP to advertise MAC and IP address bindings, replacing traditional flood-and-learn. Instead of broadcasting ARP requests everywhere, the local leaf switch can proxy-respond using information learned via EVPN.
>
> Together, they give you scalable L2 extension without STP, efficient L3 routing with Symmetric IRB, and multi-tenancy via VNIs and VRFs."

---

### Q4. What is Symmetric IRB and why does it matter?

**Strong Answer:**

> "Symmetric IRB means **both the ingress and egress leaf perform routing**. When a host on VLAN 100 at Leaf-1 wants to reach a host on VLAN 200 at Leaf-3:
>
> 1. Leaf-1 routes from VLAN 100 → L3VNI (tenant VRF)
> 2. Traffic travels through the VXLAN tunnel to Leaf-3
> 3. Leaf-3 routes from L3VNI → VLAN 200
>
> This is important because it means **each leaf only needs the VLANs it locally hosts**. With asymmetric IRB, every VLAN would need to exist on every leaf — that doesn't scale. Symmetric IRB is the standard for any production EVPN deployment."

---

### Q5. How does OSPF interact with BGP in a WAN core?

**Strong Answer:**

> "They're intentionally separate. OSPF handles intra-site routing — loopback distribution, VTEP reachability, and fast convergence within a site. BGP handles inter-site routing — application prefixes, EVPN routes, and policy between sites.
>
> The key design rule is **minimal redistribution**. We don't redistribute BGP into OSPF or vice versa. The border gateway is the boundary — it participates in both protocols but keeps them isolated. BGP next-hops are resolved via OSPF if using iBGP internally, but the route content stays separate."

---

### Q6. What's the difference between L2VNI and L3VNI?

**Strong Answer:**

> "**L2VNI** maps to a VLAN — it extends a single broadcast domain. Traffic between hosts on the same VLAN uses the L2VNI tunnel.
>
> **L3VNI** maps to a VRF — it enables inter-subnet routing. When traffic needs to cross subnets (different VLANs), the leaf routes it through the L3VNI. This is the 'transit VNI' that makes Symmetric IRB work.
>
> In practice: L2VNI 10100 maps to VLAN 100, L2VNI 10200 maps to VLAN 200, and L3VNI 50001 maps to VRF-TenantA. Traffic from VLAN 100 → VLAN 200 goes through the L3VNI."

---

### Q7. How do you handle MTU in a VXLAN environment?

**Strong Answer:**

> "VXLAN adds 50 bytes of overhead — outer Ethernet (14), outer IP (20), UDP (8), and VXLAN header (8). If the inner frame is 1500 bytes, the outer frame is 1550 bytes.
>
> The underlay — spine switches and any WAN transit — must support at least **9214 MTU** (standard jumbo). We set this on all fabric-facing and WAN-facing interfaces. If any hop in the path has a smaller MTU, we get silent packet drops or fragmentation, which cripples VXLAN performance.
>
> I always include **MTU verification** in my validation test plan — both `ping -s 8972 -M do` tests and checking interface MTU configs end-to-end."

---

### Q8. Describe a leaf-spine topology. Why not traditional three-tier?

**Strong Answer:**

> "Leaf-spine is a two-tier Clos topology. Every leaf connects to every spine. Every server/host connects to a leaf. Spines never connect to other spines, and leaves never connect to other leaves (except MLAG pairs).
>
> The advantage over three-tier: **every path has the same number of hops** (leaf → spine → leaf), which gives predictable latency. ECMP across all spines means no wasted bandwidth — no blocked paths like STP. And it scales horizontally — need more ports? Add a leaf. Need more bandwidth? Add a spine.
>
> Three-tier had aggregation/core creating bottlenecks and STP blocking half the links. Leaf-spine eliminates both problems."

---

### Q9. What BGP attributes do you use most in WAN design?

**Strong Answer:**

> "**Local Preference** — to prefer the primary WAN path over backup within my AS. Primary gets LP 200, backup gets LP 100.
>
> **AS-Path Prepending** — to influence inbound traffic from external peers. I prepend my AS 2–3 times on the backup link to make it less attractive.
>
> **Communities** — to tag routes by source (site, region, tier) so downstream policies can make decisions without looking at individual prefixes. I use RFC 8092 large communities for the three-field flexibility.
>
> **MED** — to suggest to an eBGP peer which entry point to use when there are multiple peering points.
>
> I try to avoid relying on AS-path length for policy — communities and local-pref are more explicit and easier to maintain."

---

### Q10. What is a route reflector and when do you need one?

**Strong Answer:**

> "In iBGP, every peer must have a session with every other peer — that's O(n²) sessions. With 50 routers, that's 1,225 sessions. A **route reflector** breaks this requirement — clients peer with the RR, and the RR reflects routes to all clients.
>
> I deploy RRs when I have more than ~5 iBGP peers. In a WAN core, I'd place RR functionality on dedicated devices or on the spine switches. Always deploy them in pairs for redundancy. The RR adds Cluster-ID and Originator-ID attributes to prevent loops but **never modifies the AS-Path** — so routing decisions remain consistent."

---

### Q11. How would you troubleshoot a WAN connectivity issue between two sites?

**Strong Answer:**

> "I follow a structured, layer-by-layer approach:
>
> 1. **Verify the symptom** — Confirm the issue, scope it (complete outage vs. partial)
> 2. **Check Layer 1** — Interface status, light levels on optics, CRC errors
> 3. **Check OSPF** — Are all adjacencies FULL? Any recent SPF events?
> 4. **Check BGP** — Is the eBGP session Established? Are routes being received?
> 5. **Check EVPN** — Are the relevant Type-2/Type-5 routes present on both sides?
> 6. **Check VXLAN** — Is the VTEP tunnel up? Can I ping the remote VTEP?
> 7. **Check MTU** — Can I send jumbo frames end-to-end?
> 8. **Check policy** — Is a route-map or community filter dropping the routes?
>
> At each step, I'm comparing against the pre-change baseline. If something changed, that's likely the root cause."

---

### Q12. How do you ensure routing symmetry across the WAN?

**Strong Answer:**

> "Routing symmetry means traffic follows the same path in both directions — critical for stateful firewalls. I ensure it by:
>
> 1. **Consistent local-preference and MED** — If I set LP 200 on the primary path inbound, I set lower MED on the same path outbound
> 2. **Same active border gateway** in both directions — using VRRP or anycast gateway
> 3. **Avoiding asymmetric ECMP** — If ECMP is used, ensure both directions hash to the same path set
> 4. **Firewall clustering** with state sync if firewalls are in the path
>
> In my test plan, I always include a traceroute in both directions to verify symmetry."

---

## Part 2: Testing & Validation (10 Questions)

### Q13. How do you structure a network validation test plan?

**Strong Answer:**

> "I organize tests into three pillars: **functional, scale, and resiliency**.
>
> Functional tests verify each feature works — OSPF adjacencies, BGP peering, VXLAN tunnels, EVPN route learning, Symmetric IRB routing.
>
> Scale tests push limits — how many routes, MACs, VNIs before the fabric degrades? I inject routes using a route generator and monitor FIB utilization.
>
> Resiliency tests break things intentionally — kill a spine, kill a BGP session, pull a cable. I measure convergence time and verify zero packet loss (or within SLA).
>
> Each test has an ID, description, exact steps, expected result, and pass/fail. The results go into a formal report with sign-off before production promotion."

---

### Q14. You're onboarding a new fabric. What tests do you run before it goes live?

**Strong Answer:**

> "In order:
>
> 1. **Underlay verification** — All OSPF adjacencies FULL, all loopbacks pingable end-to-end
> 2. **Overlay verification** — BGP EVPN sessions Established, VTEP discovery complete
> 3. **Host connectivity** — Hosts on same VLAN can ping (L2VNI), hosts on different VLANs can ping (L3VNI/Symmetric IRB)
> 4. **ARP suppression** — Verify ARP isn't flooding to remote leaves
> 5. **Anycast gateway** — Verify same MAC on all leaves, host can move between leaves without losing connectivity
> 6. **WAN integration** — Routes from this fabric appear at remote sites, and vice versa
> 7. **Resiliency** — Kill each spine, kill each leaf one at a time, verify convergence
> 8. **MTU** — Jumbo frame test end-to-end
> 9. **Monitoring** — Verify SNMP traps, syslog, telemetry are received by monitoring stack
> 10. **End-to-end application test** — Run the actual application workload through the new fabric"

---

### Q15. What does a resiliency test look like?

**Strong Answer:**

> "I test each failure scenario independently. For example, 'Single Spine Failure':
>
> 1. **Baseline:** Capture routing table, session count, traffic flow. Start continuous ping/iperf.
> 2. **Execute:** Shut down spine-1 (or pull power for a more realistic test)
> 3. **Observe:** How long until traffic reconverges? How many pings were lost?
> 4. **Expected:** Reconvergence under 1 second with BFD, 0–2 pings lost
> 5. **Verify:** All routes re-converge via remaining spine(s), no black holes
> 6. **Restore:** Bring spine-1 back, verify it re-joins cleanly
> 7. **Document:** Record actual convergence time, packet loss, any anomalies
>
> I repeat this for every critical component: each spine, leaf MLAG failover, WAN link, BGP session, OSPF adjacency."

---

### Q16. You run a scale test and hit the FIB limit on a leaf switch. What do you do?

**Strong Answer:**

> "First, I document the exact number where we hit the limit — that becomes our capacity ceiling for this hardware.
>
> Then I look at options:
>
> 1. **Route summarization** — Are we carrying specifics that could be aggregated?
> 2. **Route filtering** — Are we learning routes we don't need on this leaf?
> 3. **Host-route suppression** — Can we suppress /32 host routes and rely on aggregates?
> 4. **Hardware upgrade** — If we genuinely need more FIB, we need a different switch (deeper TCAM)
> 5. **Design change** — Maybe this leaf doesn't need all routes — use a default route to the spine
>
> I report this as a finding with a recommendation in the test report."

---

### Q17. How do you validate that EVPN is working correctly after a change?

**Strong Answer:**

> "I check three things specifically:
>
> 1. **EVPN database** — `show evpn database` or `show bgp evpn` — verify MAC/IP routes are present for local and remote hosts
> 2. **VXLAN tunnel** — `show vxlan vtep` — verify all remote VTEPs are discovered
> 3. **Data plane** — Ping between hosts across leaves, across VLANs, and across sites. Not just ICMP — run actual application traffic if possible
>
> I also compare the EVPN route count before and after the change. If the count dropped unexpectedly, something was lost."

---

### Q18. What tools do you use for network validation?

**Strong Answer:**

> "For verification commands: `show` commands on the devices themselves — OSPF neighbors, BGP summary, EVPN database, VXLAN VTEP table, interface counters.
>
> For traffic testing: **iperf3** for throughput, **ping/traceroute** for connectivity, **mtr** for path analysis with loss/jitter stats.
>
> For packet capture: **Wireshark** to verify VXLAN encapsulation, EVPN route content, and troubleshoot at the packet level.
>
> For automation: **Ansible** or **Python/Netmiko** to run pre/post-check scripts across all devices simultaneously and generate diff reports.
>
> For monitoring: **Grafana + Prometheus** for real-time dashboards, **LibreNMS** for SNMP-based monitoring."

---

### Q19. Tell me about a time you found an issue during validation.

**Strong Answer Template:**

> "During a fabric build, I was running resiliency tests and noticed that when I shut down one spine, convergence took 12 seconds instead of the expected sub-second. I checked BFD and found it wasn't enabled on the OSPF adjacencies between leaves and spines — only on the BGP sessions. Without BFD, OSPF had to wait for its dead timer (40 seconds, but the adjacency went down after the 3× hello miss at 30 seconds — it happened to reconverge faster due to other triggers).
>
> The fix was simple — enable BFD on all OSPF P2P links. After that, convergence dropped to ~300ms. I added BFD verification to the standard validation checklist so we wouldn't miss it again on future fabrics."

---

### Q20–Q22: Rapid Fire

**Q20.** What is BFD and why do we need it on WAN links?

> "Bidirectional Forwarding Detection. It detects link failures in 150–300ms vs. BGP's 180-second holdtime. Essential for meeting sub-second failover SLAs on WAN links."

**Q21.** What's the difference between pre-production and production validation?

> "Pre-production is in the lab with synthetic traffic — you can break things freely. Production validation uses the same test plan but with real traffic and a maintenance window. You're more cautious and have rollback plans ready."

**Q22.** How do you confirm no packet loss during a resiliency test?

> "Continuous ping (1-second interval) or iperf3 stream during the failure event. Count the lost packets. For sub-second convergence, you should see 0–1 lost pings. I also check interface error counters before and after."

---

## Part 3: Migration & Documentation (8 Questions)

### Q23. How do you plan a network migration?

**Strong Answer:**

> "Six phases:
>
> 1. **Discovery** — Document the existing network completely
> 2. **Design** — Create the target state architecture and the transition plan
> 3. **Lab** — Build the target state in lab, test all scenarios
> 4. **Stage** — Pre-configure production equipment, pre-validate configs
> 5. **Migrate** — Execute the cutover during the maintenance window, with rollback ready
> 6. **Validate** — Post-change checks against pre-change baseline, monitor for 24–48 hours
>
> I treat each phase as a gate — you don't proceed to the next until the current one passes."

---

### Q24. What goes into a rollback plan?

**Strong Answer:**

> "A rollback plan must be specific to each step of the migration:
>
> - **Trigger criteria** — When do you invoke the rollback? (measurable conditions, not gut feel)
> - **Step-by-step reversal** — Exact commands to undo each change, in reverse order
> - **Verification** — What to check after each rollback step
> - **Time estimate** — How long the full rollback takes
> - **Owner** — Who executes each rollback step
>
> I always test the rollback in the lab before the production migration. A rollback plan that hasn't been tested is just a hope."

---

### Q25. Describe how you'd create an operational runbook for a WAN fabric.

**Strong Answer:**

> "A good runbook is written for the on-call engineer at 2 AM who might not have designed the network:
>
> 1. **Architecture overview** — One-page diagram with key IPs, ASNs, VRFs
> 2. **Common tasks** — Step-by-step for BAU operations (add VLAN, add BGP peer, replace switch)
> 3. **Troubleshooting guides** — Decision trees for common symptoms (BGP down, VTEP not forming, packet loss)
> 4. **Emergency procedures** — How to roll back a failed change, who to escalate to
> 5. **Reference** — IP addressing tables, VNI mappings, community definitions, contact list
>
> Every procedure has **exact commands**, **expected output**, and **decision points**. I version-control it in Git and require periodic review."

---

### Q26. What's the most important pre-migration artifact?

**Strong Answer:**

> "The **pre-change state capture**. Before touching anything:
>
> - Full routing tables (all AFIs)
> - BGP neighbor state and received routes
> - OSPF neighbor state and LSDB summary
> - EVPN route count
> - ARP/ND tables
> - MAC address tables
> - Interface status and error counters
> - Active firewall sessions
> - Application health checks
>
> I script this and run it on every device simultaneously. After the change, I run the same script and diff the outputs. Any unexpected difference is investigated before closing the window."

---

### Q27. How do you handle continuous improvement of network standards?

**Strong Answer:**

> "After every deployment, I conduct a **post-implementation review**:
>
> - What worked well?
> - What didn't work? What was the root cause?
> - What should we do differently next time?
>
> I document these as lessons learned and update our standards:
>
> - Add new checks to the validation test plan
> - Update configuration templates with discovered best practices
> - Improve runbooks with newly discovered troubleshooting steps
>
> I also review vendor release notes and industry best practices quarterly to keep standards current."

---

### Q28. How do you approach documentation for a WAN environment?

**Strong Answer:**

> "I organize documentation into four tiers:
>
> 1. **Architecture docs** — High-level design, topology diagrams, ASN/IP plan (updated quarterly)
> 2. **Configuration standards** — Template configs, naming conventions, community schemes (version-controlled in Git)
> 3. **Operational runbooks** — Step-by-step procedures for BAU and emergency operations (reviewed monthly)
> 4. **As-built records** — What was actually deployed, including any deviations from the design (updated after every change)
>
> Source of truth for IP/VRF/VNI is **NetBox** (IPAM/DCIM), not spreadsheets. Everything else is in Markdown, version-controlled in Git."

---

### Q29–Q30: Behavioral Questions

**Q29.** Tell me about a time you worked in both a lab and production environment.

**Template:**

> "In a recent EVPN/VXLAN deployment, I built the complete fabric in [EVE-NG/GNS3/CML] first. I tested the OSPF underlay, eBGP overlay, and all EVPN route types. I discovered an MTU issue in lab — the WAN transit links were configured for 1500 MTU instead of 9214, causing VXLAN fragmentation.
>
> After fixing it in lab, I updated the config template so the same mistake wouldn't happen in production. When we deployed to production, the fabric came up cleanly because we'd already caught and fixed the issues in lab."

**Q30.** How do you handle pushback when a migration doesn't go as planned?

**Template:**

> "During a migration, if step X fails validation, I don't push forward. I calmly assess: Can we fix it quickly (under 10 minutes)? If yes, attempt the fix. If not, invoke the rollback.
>
> When stakeholders push to 'just finish it,' I explain the risk quantitatively: 'If we proceed without fixing this, there's a high probability of a P1 outage affecting X users for Y hours. Rollback takes 20 minutes and we can reschedule for next week with a fix.'
>
> I've never regretted rolling back. I have regretted pushing forward."

---

## 💡 Final Tips

1. **Use the JD's language** — Say "design, build, and validate" not just "configure"
2. **Show your process** — They want structured thinking, not just technical answers
3. **Lab and production** — Make sure to mention experience in both
4. **Documentation is a first-class skill** — They mention it repeatedly
5. **Be honest about gaps** — "I haven't worked with X, but I've worked with the equivalent Y and I'm confident I can ramp up quickly"
6. **Ask good questions** — "What vendor platforms make up your current WAN core?" "How many sites are in scope for the fabric build?" "What's your change management process?"
