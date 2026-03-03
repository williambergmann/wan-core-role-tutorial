# Resiliency Test Plan Template

## Test Plan Information

| Field      | Value                       |
| ---------- | --------------------------- |
| Project    | [Fabric name / site]        |
| Author     | [Your name]                 |
| Date       | YYYY-MM-DD                  |
| SLA Target | Reconvergence < [X] seconds |

## Test Cases

| ID    | Test                  | Failure Simulated        | Steps                               | Expected Convergence        | Actual | P/F |
| ----- | --------------------- | ------------------------ | ----------------------------------- | --------------------------- | ------ | --- |
| R-001 | Single spine failure  | `shutdown` spine-1       | Continuous ping during shutdown     | < 1s (BFD + ECMP)           |        |     |
| R-002 | Single leaf failure   | `shutdown` leaf-1        | Continuous ping from affected hosts | MLAG failover < 3s          |        |     |
| R-003 | WAN link failure      | `shutdown` WAN interface | Continuous ping between sites       | < 3s (BFD on eBGP)          |        |     |
| R-004 | Border GW failure     | `shutdown` border-GW1    | Inter-site traffic                  | Reroute via GW2 < 5s        |        |     |
| R-005 | BGP process restart   | `restart bgp`            | Monitor peer state                  | Graceful restart, no drops  |        |     |
| R-006 | Link flap (5x in 60s) | Bounce interface 5 times | Monitor routing stability           | No loops, clean reconverge  |        |     |
| R-007 | OSPF reconvergence    | Shut inter-switch link   | `show ip ospf neighbor`             | SPF < 1s                    |        |     |
| R-008 | Full power loss       | Power off leaf switch    | Host connectivity                   | Dual-homed hosts unaffected |        |     |

## Procedure for Each Test

1. **Pre-check:** Capture baseline state (`python state_capture.py`)
2. **Start monitoring:** Begin continuous ping + packet capture
3. **Inject failure:** Execute the failure scenario
4. **Measure:** Count packet drops, measure time to recovery
5. **Recover:** Restore the failed component
6. **Verify:** Confirm full recovery, no stale routes
7. **Post-check:** Capture state, diff against baseline

## Sign-Off

| Role          | Name | Date | Signature |
| ------------- | ---- | ---- | --------- |
| Test Engineer |      |      |           |
| Design Lead   |      |      |           |
