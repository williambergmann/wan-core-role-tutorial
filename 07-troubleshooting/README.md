# 🔧 Module 07: Troubleshooting

> Systematic troubleshooting is what separates a senior engineer from a junior one. This module covers a structured methodology, 5 decision tree flowcharts, and 10 breakfix scenarios you'll practice in lab.

---

## Troubleshooting Methodology

### The Layer-by-Layer Approach

Always work bottom-up through the stack:

```
Layer 1: Physical
├── Interface up/up? Light levels OK? CRC errors?
│
Layer 2: Switching / VXLAN Data Plane
├── MAC table populated? VXLAN tunnel up? VNI correct?
│
Layer 3: Underlay Routing (OSPF)
├── All OSPF neighbors FULL? Loopbacks reachable? BFD up?
│
Layer 4: Overlay Routing (BGP EVPN)
├── BGP sessions Established? Routes received? Communities correct?
│
Layer 5: Overlay Data Plane (EVPN)
├── EVPN database populated? Type-2/Type-5 routes present?
│
Layer 6: Application
├── End-to-end connectivity? MTU? Firewall rules?
└── Compare against pre-change baseline at each layer
```

### First Triage Questions

When you get a ticket or an alert, ask these FIRST:

1. **What changed?** — Was there a recent change? Check the change log.
2. **What's the scope?** — One host, one VLAN, one site, or everything?
3. **When did it start?** — Correlate with any change or event.
4. **Is it intermittent or constant?** — Intermittent = often physical or load-related.

---

## Decision Trees

Visual troubleshooting guides in [`decision-trees/`](./decision-trees/):

| Decision Tree                                                     | Starting Symptom               |
| ----------------------------------------------------------------- | ------------------------------ |
| [bgp-not-established.md](./decision-trees/bgp-not-established.md) | BGP session not coming up      |
| [ospf-stuck.md](./decision-trees/ospf-stuck.md)                   | OSPF neighbor stuck (not FULL) |
| [evpn-routes-missing.md](./decision-trees/evpn-routes-missing.md) | EVPN routes not appearing      |
| [vxlan-tunnel-down.md](./decision-trees/vxlan-tunnel-down.md)     | VXLAN tunnel not forming       |
| [mtu-black-hole.md](./decision-trees/mtu-black-hole.md)           | Large packets dropped silently |

---

## 10 Breakfix Scenarios

Practice these in your lab. Each scenario has a broken config and a symptom — diagnose and fix without looking at the answer first.

| #   | Scenario                                                                             | Symptom                           | Key Commands                                       |
| --- | ------------------------------------------------------------------------------------ | --------------------------------- | -------------------------------------------------- |
| 1   | [OSPF area mismatch](./breakfix-scenarios/scenario-01-ospf-area-mismatch.md)         | Neighbor stuck in INIT            | `show ip ospf neighbor`, `show ip ospf interface`  |
| 2   | [MTU mismatch](./breakfix-scenarios/scenario-02-mtu-mismatch.md)                     | OSPF stuck in EXSTART             | `show ip ospf neighbor detail`, `show interface`   |
| 3   | [Wrong BGP peer-AS](./breakfix-scenarios/scenario-03-bgp-wrong-peer-as.md)           | BGP in ACTIVE/OPENSENT            | `show bgp neighbor`, syslog                        |
| 4   | [Missing EVPN AFI](./breakfix-scenarios/scenario-04-missing-evpn-afi.md)             | BGP up, no EVPN routes            | `show bgp l2vpn evpn summary` (0 prefixes)         |
| 5   | [Wrong VNI](./breakfix-scenarios/scenario-05-wrong-vni.md)                           | L2 connectivity broken for VLAN   | `show nve vni`, `show vlan`                        |
| 6   | [Missing L3VNI](./breakfix-scenarios/scenario-06-missing-l3vni.md)                   | Inter-VLAN routing broken         | `show bgp l2vpn evpn route-type 5`, `show vrf`     |
| 7   | [BFD not enabled](./breakfix-scenarios/scenario-07-no-bfd.md)                        | Slow failover on failure          | `show bfd neighbors`, measure convergence          |
| 8   | [Route-map deny](./breakfix-scenarios/scenario-08-route-map-deny.md)                 | Routes not advertised to WAN      | `show route-map`, `show bgp neighbor X advertised` |
| 9   | [Duplicate router-id](./breakfix-scenarios/scenario-09-duplicate-router-id.md)       | Weird routing instability         | `show ip ospf`, syslog                             |
| 10  | [Underlay MTU too small](./breakfix-scenarios/scenario-10-underlay-mtu-too-small.md) | Large packets dropped, ICMP works | `ping X.X.X.X size 8972 df-bit`, counters          |

### Breakfix Scenario Format

Each scenario file contains:

```markdown
## Symptom

[What the user/monitoring reports]

## Broken Config Snippet

[The misconfigured section — load this into your lab]

## Hints

1. [First hint — which layer to look at]
2. [Second hint — which show command reveals it]
3. [Third hint — the specific field to look at]

## Solution

[The fix — exact commands]

## Root Cause Explanation

[Why this broke things and how to prevent it]

## Key Takeaway

[One sentence you should remember]
```

---

## AI-Assisted Workflows

| Prompt                                                               | Use Case                                                        |
| -------------------------------------------------------------------- | --------------------------------------------------------------- |
| [troubleshooting-copilot.md](./ai-assist/troubleshooting-copilot.md) | "Here's my show output — walk me through diagnosing this issue" |

---

## Top 10 Show Commands for Troubleshooting

| #   | Command (NX-OS)                  | What It Tells You                       |
| --- | -------------------------------- | --------------------------------------- |
| 1   | `show ip ospf neighbor`          | Underlay health — all neighbors FULL?   |
| 2   | `show bgp l2vpn evpn summary`    | Overlay health — all peers Established? |
| 3   | `show nve peers`                 | VXLAN tunnels — all VTEPs discovered?   |
| 4   | `show nve vni`                   | VNI status — all VNIs up?               |
| 5   | `show l2route evpn mac all`      | EVPN MAC table — hosts learned?         |
| 6   | `show ip route vrf X`            | VRF routing — routes present?           |
| 7   | `show interface brief`           | Physical — any down interfaces?         |
| 8   | `show interface counters errors` | Errors — CRC, input, output errors?     |
| 9   | `show bfd neighbors`             | BFD — all sessions up?                  |
| 10  | `show logging last 50`           | Syslog — any recent errors?             |
