# Breakfix Scenario 10: Underlay MTU Too Small for VXLAN

## Symptom

Small packets (ICMP echo, ARP) work fine across the VXLAN fabric. Large packets (file transfers, database replication, jumbo frames from applications) are silently dropped. No errors on interfaces. pings with size 1400 work; pings with size 8000 fail.

## Topology

```
[Leaf-1] ----spine---- [Leaf-3]
  ↕ VXLAN encap            ↕ VXLAN decap
  Host-A                    Host-B

Underlay MTU: 1500 on one spine link ← TOO SMALL
VXLAN overhead: ~50 bytes
Max payload through fabric: ~1450 bytes (1500 - 50) ← Silent drops above this
```

## Broken Config Snippet (Spine-1, one interface)

```
interface ethernet1/3
  description to-leaf-3
  ip router ospf 1 area 0
  ip ospf network point-to-point
  ! Missing: mtu 9214           ← Default MTU 1500 is too small!
```

## Hints

1. Small packets work, large packets fail → classic MTU black hole
2. The tricky part: the problematic link might not be the one you check first (it's one hop in the path)
3. Test with DF-bit set: `ping X.X.X.X size 8972 df-bit` — large frame + don't fragment
4. Check MTU on ALL underlay interfaces: `show interface | include "MTU|Ethernet"`
5. Check NVE interface: `show interface nve1` — what's the MTU there?

## Solution

```
! Fix the MTU on the affected spine interface
interface ethernet1/3
  mtu 9214
```

> Verify ALL underlay interfaces have consistent MTU:

```bash
show interface | include "MTU|Ethernet" | grep -v "9214"
# This should return NOTHING — every fabric interface should be 9214
```

## Root Cause Explanation

VXLAN encapsulation adds ~50 bytes of overhead (outer Ethernet header + outer IP header + UDP header + VXLAN header). If the underlay MTU is 1500, the maximum inner payload is ~1450 bytes. Any packet larger than this either:

1. Gets fragmented (if DF-bit is not set) — causes performance issues
2. Gets silently dropped (if DF-bit is set) — causes application failures

This is a "black hole" because there are no interface errors — the dropping happens silently when the encapsulated packet exceeds the underlay MTU. ICMP "packet too big" messages may not reach the source due to firewall policies.

## Key Takeaway

> Large packets fail, small packets work → MTU black hole. Check MTU on ALL underlay interfaces (not just the directly connected ones). Every fabric link must be 9214+ for VXLAN. Run `ping X.X.X.X size 8972 df-bit` to test end-to-end path MTU.
