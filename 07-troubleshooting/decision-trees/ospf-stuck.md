# Decision Tree: OSPF Neighbor Stuck (Not FULL)

## Starting Symptom

OSPF neighbor is visible but stuck in a state other than FULL.

```mermaid
flowchart TD
    A["OSPF Neighbor Not FULL"] --> B{"What state is it in?"}

    B --> |"INIT"| C["One-way communication:\nReceiving hellos but not\nbeing listed in neighbor's hello"]
    C --> C1{"Can you ping\nthe neighbor?"}
    C1 --> |"No"| C2["Layer 1/2 issue:\n- Cable? Interface down?\n- VLAN mismatch?"]
    C1 --> |"Yes"| C3{"Area ID match\non both sides?"}
    C3 --> |"No"| C4["FIX: Match area IDs"]
    C3 --> |"Yes"| C5{"Hello/Dead timers\nmatch?"}
    C5 --> |"No"| C6["FIX: Match timers"]
    C5 --> |"Yes"| C7{"Network type match?\n(P2P vs Broadcast)"}
    C7 --> |"No"| C8["FIX: Match network types"]
    C7 --> |"Yes"| C9["Check: Authentication\nmismatch?"]

    B --> |"2-WAY"| D["DR/BDR issue:\nOnly happens on\nbroadcast networks"]
    D --> D1["On P2P links?\nShould never be 2-WAY"]
    D1 --> D2["FIX: Set ip ospf\nnetwork point-to-point"]

    B --> |"EXSTART/\nEXCHANGE"| E["Database exchange\nfailing"]
    E --> E1{"MTU match on\nboth sides?"}
    E1 --> |"No"| E2["FIX: Match MTU\n(9214 for VXLAN fabric)"]
    E1 --> |"Yes"| E3{"Is one side overloaded?\n(CPU, memory)"}
    E3 --> |"Yes"| E4["Reduce OSPF scale\nor increase resources"]
    E3 --> |"No"| E5["Check: Duplicate\nrouter-id?"]

    B --> |"LOADING"| F["Full database not\nreceived yet"]
    F --> F1["Usually transient.\nWait 60 seconds.\nIf persistent → large LSDB\nor congestion"]
```

## Quick Checklist

```bash
# 1. What state?
show ip ospf neighbor

# 2. Interface details on both sides
show ip ospf interface ethX/Y
# Must match: area, network type, hello/dead timers, authentication

# 3. MTU check
show interface ethX/Y | include MTU

# 4. Timer check
show ip ospf interface ethX/Y | include "Timer|Hello|Dead"

# 5. Authentication
show ip ospf interface ethX/Y | include "Authentication"
```
