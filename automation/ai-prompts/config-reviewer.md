# AI Prompt: Config Reviewer

## When to Use

You've written or generated a config and want it reviewed for errors, best practices violations, and PCI-DSS compliance issues before applying.

## The Prompt

```
You are a senior network engineer conducting a config review in a
PCI-DSS compliant financial services environment. Review the following
network configuration for:

1. **Syntax errors** — typos, missing keywords, incorrect format
2. **Best practice violations** — missing BFD, no authentication,
   suboptimal timers, missing logging
3. **Security issues** — default credentials, SNMP v2, missing ACLs,
   PCI-DSS violations
4. **Design issues** — scalability concerns, single points of failure,
   route leaking risks
5. **Missing configuration** — features that should be enabled but aren't

Platform: [Cisco NX-OS / Junos / Versa VOS]
Context: [DESCRIBE: what this device does in the topology]

Configuration to review:
```

[PASTE YOUR CONFIG HERE]

```

For each issue found:
- Severity: CRITICAL / WARNING / INFO
- Line(s) affected
- What's wrong
- How to fix it (exact CLI)
- Why it matters
```

## Caveats

- AI doesn't know your full topology — it may flag things that are intentional
- Always cross-reference security findings with your company's security policy
- Not a replacement for a human CAB review
