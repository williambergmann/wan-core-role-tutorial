# Decision Tree: BGP Not Established

## Starting Symptom

BGP session stuck in Idle, Active, Connect, or OpenSent — NOT reaching Established.

```mermaid
flowchart TD
    A["BGP Not Established"] --> B{"What state is it in?"}

    B --> |"Idle"| C["Check: Is the neighbor\nconfigured correctly?"]
    C --> C1["show bgp neighbor X.X.X.X"]
    C1 --> C2{"Neighbor exists?"}
    C2 --> |"No"| C3["FIX: Add neighbor config"]
    C2 --> |"Yes"| C4{"Admin shutdown?"}
    C4 --> |"Yes"| C5["FIX: no shutdown"]
    C4 --> |"No"| C6["Check: route to peer IP exists?"]

    B --> |"Active/Connect"| D["TCP connection failing"]
    D --> D1{"Can you ping\nthe peer IP?"}
    D1 --> |"No"| D2["Layer 3 issue:\n- Check routing to peer\n- Check update-source\n- Check loopback is up"]
    D1 --> |"Yes"| D3{"Is TCP 179 blocked?\nCheck ACLs/firewall"}
    D3 --> |"Yes"| D4["FIX: Allow TCP 179\nin both directions"]
    D3 --> |"No"| D5{"ebgp-multihop needed?\n(peers not directly connected)"}
    D5 --> |"Yes"| D6["FIX: Add ebgp-multihop N"]
    D5 --> |"No"| D7["Check: update-source\nconfigured for iBGP?"]

    B --> |"OpenSent/\nOpenConfirm"| E["TCP up but BGP\nOPEN message rejected"]
    E --> E1{"ASN mismatch?"}
    E1 --> |"Yes"| E2["FIX: Correct remote-as\non both sides"]
    E1 --> |"No"| E3{"Auth mismatch?\n(MD5 password)"}
    E3 --> |"Yes"| E4["FIX: Match password\non both sides"]
    E3 --> |"No"| E5{"Capability mismatch?\nCheck AFI/SAFI"}
    E5 --> E6["Check logs:\nshow logging | grep BGP"]
```

## Quick Checklist

```bash
# 1. What state are we in?
show bgp neighbor X.X.X.X | grep "BGP state"

# 2. Can we reach the peer?
ping X.X.X.X source Y.Y.Y.Y    # Y = your update-source

# 3. Is anything blocking TCP 179?
show ip access-lists

# 4. Check the OPEN message
show bgp neighbor X.X.X.X | grep -A5 "message statistics"

# 5. Check syslog for BGP errors
show logging | grep BGP
```
