# Migration Runbook Template

## Change Information

| Field      | Value                    |
| ---------- | ------------------------ |
| Change ID  | CR-XXXX                  |
| Date       | YYYY-MM-DD               |
| Window     | HH:MM - HH:MM (timezone) |
| Engineer   | [Name]                   |
| Approver   | [Name]                   |
| Risk Level | Low / Medium / High      |

## Purpose

[One paragraph: what this change accomplishes]

## Scope

- Devices affected: [LIST]
- VRFs affected: [LIST]
- Sites affected: [LIST]

## Prerequisites

- [ ] Change request approved by CAB
- [ ] Rollback plan reviewed and approved
- [ ] Lab testing completed
- [ ] Maintenance window confirmed
- [ ] Communication sent to stakeholders

## Pre-Checks

Run on each device in scope:

```bash
show ip route vrf all | count
show bgp l2vpn evpn summary
show ip ospf neighbor
show nve peers
show nve vni
show interface counters errors
```

Save output to: `pre_check_CRXXXX_YYYYMMDD.txt`

## Procedure

### Step 1: [Description]

```
[exact CLI commands]
```

**Verify:**

```
[verification commands]
```

**Expected result:** [what you should see]

### Step 2: [Description]

```
[exact CLI commands]
```

**Verify:**

```
[verification commands]
```

### Step N: Final Verification

```
[comprehensive verification commands]
```

## Post-Checks

Run the same pre-check commands and compare:

```bash
show ip route vrf all | count
show bgp l2vpn evpn summary
show ip ospf neighbor
show nve peers
show nve vni
show interface counters errors
```

Save output to: `post_check_CRXXXX_YYYYMMDD.txt`

**Compare:** Diff pre-check vs post-check. Flag any unexpected changes.

## Rollback Plan

### Trigger Criteria

Rollback if:

- [ ] Any BGP session goes down unexpectedly
- [ ] Route count drops by more than 5%
- [ ] End-to-end connectivity lost for any critical path
- [ ] Change exceeds maintenance window

### Rollback Steps

```
[exact CLI commands to reverse this change]
```

### Rollback Verification

```
[verification commands to confirm rollback succeeded]
```

## Post-Implementation Review

- [ ] Change completed successfully
- [ ] All post-checks passed
- [ ] No unexpected side effects
- [ ] Documentation updated
- [ ] IPAM/NetBox updated
- [ ] Monitoring verified

**Notes:**
[Any observations, lessons learned, or follow-up items]
