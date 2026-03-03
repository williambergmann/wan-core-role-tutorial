# 🗂️ EVPN Route Types — Visual Reference

> One-page visual reference for all EVPN route types. Print this out.

---

## Route Type Summary

```
╔══════════════════════════════════════════════════════════════════╗
║                    EVPN ROUTE TYPES                             ║
╠══════╦══════════════════╦═══════════════════════════════════════╣
║ Type ║ Name             ║ What It Does                         ║
╠══════╬══════════════════╬═══════════════════════════════════════╣
║  1   ║ Ethernet         ║ Multi-homing: signals ESI membership ║
║      ║ Auto-Discovery   ║ and DF election. Used for MLAG/ESI   ║
╠══════╬══════════════════╬═══════════════════════════════════════╣
║  2   ║ MAC/IP           ║ HOST LEARNING — the most important   ║
║      ║ Advertisement    ║ type. Advertises MAC + optional IP.   ║
║      ║                  ║ Replaces flood-and-learn.             ║
╠══════╬══════════════════╬═══════════════════════════════════════╣
║  3   ║ Inclusive         ║ BUM traffic: establishes flooding    ║
║      ║ Multicast        ║ tree between VTEPs. One per VNI/VTEP ║
╠══════╬══════════════════╬═══════════════════════════════════════╣
║  4   ║ Ethernet Segment ║ ESI multi-homing: DF election for    ║
║      ║                  ║ which VTEP forwards BUM for an ESI   ║
╠══════╬══════════════════╬═══════════════════════════════════════╣
║  5   ║ IP Prefix        ║ L3 ROUTING — advertises IP prefixes  ║
║      ║ Route            ║ in EVPN. Used for inter-site routing  ║
║      ║                  ║ and VRF route exchange.               ║
╚══════╩══════════════════╩═══════════════════════════════════════╝
```

## Type 2: MAC/IP Advertisement (Most Common)

```
Fields:
┌──────────────┬──────────────────────────────────────────┐
│ RD           │ Route Distinguisher (per-VTEP unique)     │
│ ESI          │ Ethernet Segment ID (0 if single-homed)   │
│ Ethernet Tag │ Usually 0                                 │
│ MAC Length   │ 48 (always)                               │
│ MAC Address  │ The learned host MAC                      │
│ IP Length    │ 0, 32, or 128                             │
│ IP Address   │ Host IP (optional but common)             │
│ MPLS Label 1 │ L2VNI (for MAC forwarding)                │
│ MPLS Label 2 │ L3VNI (for IP routing — Symmetric IRB)    │
└──────────────┴──────────────────────────────────────────┘

How to read it:
  "VTEP 10.255.1.1 learned MAC aa:bb:cc:dd:ee:ff with IP 10.100.0.50
   on VNI 10100 (L2) and VNI 50001 (L3 for VRF Tenant-A)"
```

## Type 5: IP Prefix Route (WAN Core Primary)

```
Fields:
┌──────────────┬──────────────────────────────────────────┐
│ RD           │ Route Distinguisher                       │
│ ESI          │ Usually 0 for Type-5                      │
│ Ethernet Tag │ 0                                         │
│ IP Prefix Len│ /8, /16, /24, etc.                        │
│ IP Prefix    │ The subnet being advertised               │
│ GW IP        │ Gateway IP                                │
│ MPLS Label   │ L3VNI (VRF routing)                       │
└──────────────┴──────────────────────────────────────────┘

How to read it:
  "Site A is advertising 10.1.0.0/16 via L3VNI 50001 (VRF Tenant-A)"
```

## When Each Type Is Used

```
Host connects to Leaf       → Type 2 (MAC/IP) generated
Leaf joins a VNI             → Type 3 (Inclusive Multicast) generated
Host moves to new Leaf       → New Type 2, old withdrawn
Inter-site routing           → Type 5 (IP Prefix) at border gateway
Dual-homed server            → Type 1 + Type 4 for ESI/DF
```

## Verification

```bash
# NX-OS
show bgp l2vpn evpn route-type 2     # All Type-2 (MAC/IP) routes
show bgp l2vpn evpn route-type 5     # All Type-5 (IP prefix) routes
show bgp l2vpn evpn                   # All EVPN routes (all types)

# Junos
show evpn database                    # Type-2 MAC/IP entries
show route table bgp.evpn.0           # All EVPN routes
show route table VRF.evpn.0 evpn-ip-prefix  # Type-5 routes
```
