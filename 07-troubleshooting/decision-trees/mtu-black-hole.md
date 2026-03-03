# Decision Tree: MTU Black Hole

## Starting Symptom

Small packets (ICMP, ARP, small HTTP requests) work fine. Large packets (file transfers, database queries, jumbo frames) fail silently. No interface errors reported.

```mermaid
flowchart TD
    A["MTU Black Hole\n(Large packets fail,\nsmall work)"] --> B{"Test: ping with\nlarge size + DF bit"}

    B --> |"ping X size 1400\ndf-bit → SUCCESS"| C["Below MTU threshold"]
    B --> |"ping X size 8000\ndf-bit → FAIL"| D["Confirmed: MTU issue\nin the path"]

    D --> E{"Where in the path\nis the break?"}
    E --> E1["Binary search:\nping size 4000 → ?\nping size 6000 → ?\nNarrow down the exact\nbreakpoint"]

    E1 --> F{"Breakpoint found\nat ~1500?"}
    F --> |"Yes"| G["One or more links\nhave MTU 1500\n(no jumbo frames)"]
    G --> G1["Check ALL underlay\ninterfaces"]
    G1 --> G2["show interface | include\n'MTU|Ethernet'"]
    G2 --> G3["FIX: mtu 9214 on\nthe offending interface(s)"]

    F --> |"No (~9000)"| H["One link has\nsmaller jumbo MTU"]
    H --> H1["Some switches default\nto 9000 vs 9216"]
    H1 --> H2["FIX: Standardize to\nmtu 9214 everywhere"]

    D --> I{"Is this across\nthe WAN?"}
    I --> |"Yes"| J["WAN/ISP may not\nsupport jumbo frames"]
    J --> J1["Options:\n1. Request jumbo MTU from ISP\n2. Use VXLAN with DF-bit clear\n   (allow fragmentation)\n3. Reduce inner MTU to 1400\n   at the border gateway"]

    I --> |"No (within fabric)"| K["Check EVERY hop\nin the underlay path"]
    K --> K1["traceroute X source Y\nThen check MTU on\neach hop's egress interface"]
```

## Quick Checklist

```bash
# 1. Test end-to-end with large frame
ping <remote-host> size 8972 df-bit
ping <remote-host> size 1400 df-bit

# 2. Test underlay loopback-to-loopback
ping <remote-vtep-lo0> source loopback0 size 8972 df-bit

# 3. Check all fabric interface MTUs
show interface | include "MTU|Ethernet"

# 4. Check NVE interface MTU
show interface nve1 | include MTU

# 5. Look for fragmentation counters
show ip traffic | include "fragment"

# 6. Check specific interface
show interface ethX/Y | include "MTU|input error|output error"
```

## Prevention

```
Standard: ALL underlay fabric interfaces = MTU 9214
Verification: After every new device deployment, run:
  show interface | include "MTU|Ethernet" | grep -v 9214
  → This should return NOTHING
```
