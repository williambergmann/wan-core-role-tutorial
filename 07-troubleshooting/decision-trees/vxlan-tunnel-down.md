# Decision Tree: VXLAN Tunnel Not Forming

## Starting Symptom

`show nve peers` shows no peers, or specific VTEPs are missing. BGP EVPN may or may not be established.

```mermaid
flowchart TD
    A["VXLAN Tunnel Not Forming"] --> B{"Is BGP EVPN\nEstablished?"}

    B --> |"No"| C["Fix BGP first.\nSee: bgp-not-established\ndecision tree"]

    B --> |"Yes"| D{"Is NVE interface UP?"}
    D --> |"No"| E["Check NVE config"]
    E --> E1{"source-interface\nconfigured?"}
    E1 --> |"No"| E2["FIX: interface nve1\nsource-interface loopback0"]
    E1 --> |"Yes"| E3{"Is the source\nloopback UP?"}
    E3 --> |"No"| E4["FIX: no shutdown\non loopback"]
    E3 --> |"Yes"| E5["FIX: no shutdown\non interface nve1"]

    D --> |"Yes"| F{"Can you ping the\nremote VTEP loopback?"}
    F --> |"No"| G["Underlay problem"]
    G --> G1{"OSPF adjacency\nFULL?"}
    G1 --> |"No"| G2["Fix OSPF first.\nSee: ospf-stuck\ndecision tree"]
    G1 --> |"Yes"| G3{"Route to remote\nloopback exists?"}
    G3 --> |"No"| G4["FIX: Remote loopback\nnot in OSPF or route\nfiltered"]
    G3 --> |"Yes"| G5["Check: ACL blocking\nUDP 4789?"]

    F --> |"Yes"| H{"Are VNIs\nconfigured?"}
    H --> |"No"| I["FIX: Add member vni\nunder interface nve1"]
    H --> |"Yes"| J{"Do VNI IDs match\non both sides?"}
    J --> |"No"| K["FIX: VNI must be\nidentical on both VTEPs"]
    J --> |"Yes"| L{"Is ingress-replication\nconfigured?"}
    L --> |"No"| M["FIX: Add ingress-replication\nprotocol bgp under member vni"]
    L --> |"Yes"| N["Check: nv overlay evpn\nenabled globally?"]
```

## Quick Checklist

```bash
# 1. NVE interface status
show interface nve1

# 2. NVE peers
show nve peers

# 3. VNI status
show nve vni

# 4. Underlay reachability
ping <remote-vtep-loopback> source <local-loopback>

# 5. BGP EVPN routes
show bgp l2vpn evpn summary
show bgp l2vpn evpn route-type 3   # Inclusive multicast (one per VNI/VTEP)

# 6. Feature check
show feature | include "nv overlay|vn-segment"
```
