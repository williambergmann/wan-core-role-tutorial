# AI Prompt: BGP Troubleshooter

## When to Use

You have a BGP issue — sessions not establishing, routes missing, unexpected path selection — and you want AI-guided troubleshooting.

## How to Use

1. Capture the relevant `show` command output from your devices
2. Copy the prompt below and paste your output into the placeholders
3. AI will walk you through a structured diagnosis

## The Prompt

```
You are an expert network engineer troubleshooting a BGP issue in a
WAN core environment. The environment uses eBGP between sites and
iBGP within sites, with OSPF as the underlay IGP and EVPN/VXLAN
overlay.

I have a BGP issue. Here is the information:

Symptom:
[DESCRIBE: e.g., "BGP session between border GW1 and remote site is
stuck in Active state" or "Routes from Site B are not appearing at
Site A"]

Show command output:
```

[PASTE: show bgp summary output]

```

```

[PASTE: show bgp neighbor X.X.X.X output (for the problematic peer)]

```

```

[PASTE: any additional show output — routes, logs, interfaces]

```

Environment context:
- Platform: [Cisco NX-OS / Junos / Versa VOS]
- Was anything changed recently? [yes/no, what]
- Is BFD enabled? [yes/no]
- Is the peering eBGP or iBGP?

Please:
1. Analyze the show output for anomalies
2. Identify the most likely root cause
3. Suggest 3 specific commands to confirm the diagnosis
4. Provide the fix (exact CLI commands)
5. Suggest verification commands to confirm the fix worked
```

## Caveats

- **AI can't see your actual devices** — always verify its suggestions against real output
- **Provide as much output as possible** — more data = better diagnosis
- **Don't blindly apply fixes** — understand WHY the fix works before applying
- **Security-sensitive data** — scrub IPs/hostnames if using a public AI service
