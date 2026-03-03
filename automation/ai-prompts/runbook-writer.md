# AI Prompt: Runbook Writer

## When to Use

You need to create an operational runbook for a procedure (fabric onboarding, migration, failover, etc.).

## The Prompt

```
You are a network operations engineer writing a runbook for a team
that operates WAN core and EVPN/VXLAN fabrics in a PCI-DSS
compliant financial services environment.

Create a detailed runbook for: [DESCRIBE THE PROCEDURE]

Context:
- Environment: [DESCRIBE topology, platforms]
- Devices involved: [LIST]
- Expected duration: [TIME]
- Risk level: [Low / Medium / High]

The runbook must include:
1. **Purpose** — One paragraph describing what this procedure does
2. **Prerequisites** — What must be true before starting
3. **Pre-checks** — Exact commands to verify state before changes
4. **Step-by-step procedure** — Numbered steps with exact CLI commands
5. **Verification** — Commands to verify each step succeeded
6. **Rollback plan** — How to undo if something goes wrong
7. **Post-checks** — Commands to verify overall success
8. **Troubleshooting** — Common issues during this procedure

Format: Use markdown with code blocks for all CLI commands.
```

## Caveats

- Review all CLI commands for your specific platform version
- Add your company's change management requirements
- Test the runbook in lab before using in production
