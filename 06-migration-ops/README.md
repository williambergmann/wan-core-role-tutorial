# 📋 Module 06: Migration & Operations

> The JD explicitly calls out "migration planning and execution, including onboarding new fabrics." This module covers the fabric onboarding workflow, migration runbooks, rollback plans, and change management.

---

## Fabric Onboarding Workflow

This is what "onboarding a new fabric" means — a 4-phase process:

```
Phase 1: Design          Phase 2: Build           Phase 3: Validate        Phase 4: Migrate
┌─────────────────┐   ┌─────────────────────┐   ┌────────────────────┐   ┌────────────────┐
│ Addressing plan  │→  │ OSPF underlay config │→  │ Functional tests   │→  │ Cutover plan   │
│ VNI/VRF design   │   │ BGP overlay config   │   │ Scale tests        │   │ Rollback plan  │
│ AS assignment    │   │ VXLAN/EVPN config    │   │ Resiliency tests   │   │ Execute        │
│ Topology         │   │ Border GW peering    │   │ End-to-end verify  │   │ Validate       │
└─────────────────┘   └─────────────────────┘   └────────────────────┘   └────────────────┘
```

## Pre-Flight Checklist

```markdown
### Design Approved

- [ ] IP addressing scheme documented and approved
- [ ] ASN assigned (new or existing)
- [ ] VNI/VRF mapping defined
- [ ] Underlay routing design reviewed (OSPF areas)
- [ ] Overlay routing design reviewed (eBGP/iBGP EVPN)
- [ ] WAN core integration points identified
- [ ] MTU verified end-to-end (≥9214 for VXLAN)

### Build Complete

- [ ] All switches racked, cabled, and powered
- [ ] Management connectivity verified
- [ ] OSPF underlay configured and adjacencies formed
- [ ] Loopback addresses pingable from all fabric members
- [ ] BGP EVPN overlay configured
- [ ] VTEPs registered and VNIs configured
- [ ] IRB interfaces configured for required VLANs
- [ ] Border GW peering to WAN core established

### Validation Passed

- [ ] Functional test plan executed — all tests PASS
- [ ] Resiliency test plan executed — convergence within SLA
- [ ] Scale test plan executed — route table within limits
- [ ] End-to-end traffic verification complete
- [ ] Monitoring integrated (SNMP, syslog, streaming telemetry)

### Migration Approved

- [ ] Change request submitted and CAB-approved
- [ ] Maintenance window scheduled
- [ ] Rollback plan documented and reviewed
- [ ] Communication plan sent to stakeholders
- [ ] Pre-change state captured (baseline)
```

---

## Migration Methodology

### Application Onboarding

```
Step 1: Pre-Migration (T-7 days)
├── Verify application requirements (ports, protocols, latency)
├── Confirm VRF/VNI mapping for the application
├── Create firewall rules in new fabric
├── Test connectivity from new fabric to application dependencies
└── Schedule maintenance window

Step 2: Migration Day (T-0)
├── Pre-checks: capture routing tables, ARP, sessions
├── Announce change start on bridge call
├── Phase 1: Move test server to new fabric
│   ├── Verify connectivity
│   ├── Verify application functionality
│   └── Go/No-Go: proceed or rollback
├── Phase 2: Move remaining servers in batches
│   ├── 25% → validate → 50% → validate → 100%
│   └── Go/No-Go at each checkpoint
├── Post-checks: compare with pre-checks
├── Monitor for 30 minutes
└── Announce change complete

Step 3: Post-Migration (T+1 to T+7)
├── Monitor application performance
├── Decommission old fabric connections
├── Update documentation (NetBox, runbooks, diagrams)
└── Conduct post-implementation review
```

---

## Pre-Change State Capture

The most critical artifact. Before touching anything, capture:

```bash
# Run on every device in scope:
show ip route                    # Full routing table
show bgp l2vpn evpn summary     # EVPN peer state
show ip ospf neighbor            # OSPF adjacencies
show l2route evpn mac all        # EVPN MAC table
show nve peers                   # VXLAN tunnels
show ip arp vrf all              # ARP tables
show mac address-table           # MAC tables
show interface brief             # Interface status
show interface counters errors   # Error counters
show nve vni                     # VNI status
```

> **Automate this!** See `automation/state-snapshot.py` for a script that captures all of the above across all devices simultaneously.

---

## Templates

| Template                                                 | Purpose                          |
| -------------------------------------------------------- | -------------------------------- |
| [migration-runbook.md](./templates/migration-runbook.md) | Step-by-step migration execution |
| [rollback-plan.md](./templates/rollback-plan.md)         | Rollback with trigger criteria   |
| [change-request.md](./templates/change-request.md)       | CAB change request template      |
| [post-impl-review.md](./templates/post-impl-review.md)   | Post-implementation review       |

## Automation

| Script                  | Purpose                                  |
| ----------------------- | ---------------------------------------- |
| `state-snapshot.py`     | Capture full device state to JSON        |
| `state-diff.py`         | Compare two snapshots, highlight changes |
| `fabric-onboarding.yml` | Ansible: deploy a new fabric end-to-end  |

## AI-Assisted Workflows

| Prompt                                                         | Use Case                                   |
| -------------------------------------------------------------- | ------------------------------------------ |
| [runbook-generator.md](./ai-assist/runbook-generator.md)       | "Generate a runbook for onboarding Site X" |
| [change-risk-analyzer.md](./ai-assist/change-risk-analyzer.md) | "Assess the risk of this network change"   |
