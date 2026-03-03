# AI Prompt: Troubleshooting Assistant

## When to Use

You have a networking issue and want step-by-step guided troubleshooting.

## The Prompt

```
You are an expert network engineer troubleshooting an issue in a
WAN core / EVPN/VXLAN fabric environment. Guide me through
systematic troubleshooting.

Symptom: [DESCRIBE what's broken — be specific]
Scope: [One host / one VLAN / one site / widespread]
Recent changes: [Any recent changes? What was changed?]
Platform: [Cisco NX-OS / Junos / Versa VOS]

Show command output I have so far:
```

[PASTE any output you've already collected]

```

Please:
1. Identify which layer the problem is likely at (physical →
   switching → underlay → overlay → application)
2. List the top 3 most likely root causes
3. For each, give me the exact show command to confirm/deny
4. After I run those commands and provide output, narrow down
   to the root cause
5. Provide the exact fix
6. Suggest how to verify the fix worked
7. Suggest how to prevent this in the future
```

## Caveats

- AI is walking you through a process, not seeing your actual devices
- Always verify AI's suggestions against actual device output
- If security-sensitive, scrub IPs/hostnames before using public AI
