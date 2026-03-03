# ✅ Module 05: Validation & Testing

> The JD explicitly calls out "scale, resiliency, and functional testing." This is what you'll do before any fabric goes to production. This module covers the 3-pillar testing framework, reusable templates, and automation for pre/post checks.

---

## The Three Testing Pillars

### Pillar 1: Functional Testing

> "Does each feature work as designed?"

| Test ID | Test            | Steps                               | Expected Result         |
| ------- | --------------- | ----------------------------------- | ----------------------- |
| F-001   | OSPF adjacency  | `show ip ospf neighbor`             | All neighbors FULL      |
| F-002   | BGP peering     | `show bgp l2vpn evpn summary`       | All peers Established   |
| F-003   | VXLAN tunnel    | `show nve peers`                    | All VTEPs discovered    |
| F-004   | EVPN Type-2     | Learn MAC on Leaf-1, check Leaf-3   | MAC in EVPN table       |
| F-005   | Symmetric IRB   | Ping between hosts, different VLANs | ICMP success, <5ms RTT  |
| F-006   | L3VNI routing   | Traceroute between VRFs             | Expected path           |
| F-007   | ARP suppression | ARP from host, check remote leaf    | No flood to remote      |
| F-008   | Anycast GW      | Check GW MAC on all leaves          | Identical MAC           |
| F-009   | BFD             | `show bfd neighbors`                | All sessions UP         |
| F-010   | WAN eBGP        | Inter-site route exchange           | Remote prefixes learned |

### Pillar 2: Scale Testing

> "How many routes/MACs/VNIs can the fabric handle?"

| Test ID | Test              | Method                           | Expected              |
| ------- | ----------------- | -------------------------------- | --------------------- |
| S-001   | Route scale       | Inject 10K/50K/100K routes       | All in FIB            |
| S-002   | MAC scale         | Generate 1K/5K/10K MACs per leaf | All learned           |
| S-003   | VNI scale         | Configure 100/500/1000 VNIs      | All operational       |
| S-004   | BGP session scale | Add 10/50/100 peers              | All Established       |
| S-005   | ECMP paths        | Verify across all spines         | Balanced distribution |

### Pillar 3: Resiliency Testing

> "What happens when component X fails?"

| Test ID | Test                  | Method                        | Expected              |
| ------- | --------------------- | ----------------------------- | --------------------- |
| R-001   | Single spine failure  | Shut spine-1                  | Reconverge <1s        |
| R-002   | Single leaf failure   | Shut leaf-1                   | MLAG failover         |
| R-003   | WAN link failure      | Shut primary WAN link         | Failover <3s          |
| R-004   | BGP peer loss         | Kill BGP process on border GW | Reroute via secondary |
| R-005   | OSPF reconvergence    | Shut inter-switch link        | SPF recalc <1s        |
| R-006   | Power failure         | Power off a leaf              | Fabric self-heals     |
| R-007   | Control plane restart | Restart routing process       | Graceful restart      |
| R-008   | MTU black hole        | Misconfigure MTU              | Detect via PMTUD      |

---

## Templates

Reusable templates in [`templates/`](./templates/):

| Template                                                       | Purpose                        |
| -------------------------------------------------------------- | ------------------------------ |
| [functional-test-plan.md](./templates/functional-test-plan.md) | Full functional test plan      |
| [resiliency-test-plan.md](./templates/resiliency-test-plan.md) | Resiliency test plan           |
| [scale-test-plan.md](./templates/scale-test-plan.md)           | Scale test plan                |
| [test-report.md](./templates/test-report.md)                   | Post-test report with sign-off |

## Automation

Scripts in [`automation/`](./automation/):

| Script                 | Purpose                                              |
| ---------------------- | ---------------------------------------------------- |
| `pre-post-check.py`    | Capture state before/after change, auto-diff         |
| `convergence-timer.py` | Measure failover convergence during resiliency tests |
| `fabric-health.yml`    | Ansible playbook for comprehensive health check      |

## AI-Assisted Workflows

| Prompt                                                         | Use Case                                 |
| -------------------------------------------------------------- | ---------------------------------------- |
| [test-plan-generator.md](./ai-assist/test-plan-generator.md)   | "Generate a test plan for this topology" |
| [test-result-analyzer.md](./ai-assist/test-result-analyzer.md) | "Analyze these test results for issues"  |
