# Decision Tree: EVPN Routes Missing

## Starting Symptom

BGP EVPN session is Established, but expected routes (Type-2 MAC/IP or Type-5 IP Prefix) are not appearing in the EVPN table.

```mermaid
flowchart TD
    A["EVPN Routes Missing"] --> B{"Which routes\nare missing?"}

    B --> |"Type-2 MAC/IP"| C["Host MAC not learned\nin EVPN database"]
    C --> C1{"Is the host's MAC in\nthe local MAC table?"}
    C1 --> |"No"| C2["Layer 2 issue:\n- Host link down?\n- Wrong VLAN?\n- Port security?"]
    C1 --> |"Yes"| C3{"Is the VLAN mapped\nto a VNI?"}
    C3 --> |"No"| C4["FIX: Add vn-segment\nto VLAN config"]
    C3 --> |"Yes"| C5{"Is NVE interface UP?"}
    C5 --> |"No"| C6["FIX: no shutdown on\ninterface nve1\nCheck source-interface"]
    C5 --> |"Yes"| C7{"Are VTEP peers\ndiscovered?"}
    C7 --> |"No"| C8["Underlay issue:\n- Loopback not reachable?\n- OSPF problem?\n- BGP EVPN not configured?"]
    C7 --> |"Yes"| C9["Check: send-community\nboth configured?"]

    B --> |"Type-5 IP Prefix"| D["IP prefix routes\nnot in EVPN"]
    D --> D1{"Is the prefix in the\nVRF routing table?"}
    D1 --> |"No"| D2["Route not originated:\n- Connected? Static? BGP?\n- Check VRF membership"]
    D1 --> |"Yes"| D3{"Is the L3VNI\nconfigured?"}
    D3 --> |"No"| D4["FIX: Add L3VNI:\n- VRF vni XXXXX\n- Transit VLAN + SVI\n- member vni associate-vrf"]
    D3 --> |"Yes"| D5{"Are Route Targets\ncorrect?"}
    D5 --> |"No"| D6["FIX: Match RT import/export\non both sides"]
    D5 --> |"Yes"| D7{"Is route-map\nblocking export?"}
    D7 --> |"Yes"| D8["FIX: Adjust route-map\nto permit the prefix"]
    D7 --> |"No"| D9["Check: advertise-pip,\nrouter bgp VRF config"]
```

## Quick Checklist

```bash
# 1. Check EVPN database
show bgp l2vpn evpn summary          # How many routes?
show bgp l2vpn evpn route-type 2     # Type-2 hosts
show bgp l2vpn evpn route-type 5     # Type-5 prefixes

# 2. Check NVE/VXLAN
show nve peers                        # VTEP peers discovered?
show nve vni                          # VNIs operational?

# 3. Check VRF / L3VNI
show vrf                              # L3VNI assigned?
show ip route vrf X                   # Prefix in VRF?

# 4. Check communities
show bgp neighbor X.X.X.X            # send-community configured?

# 5. Check route maps
show route-map                        # Any deny statements?
```
