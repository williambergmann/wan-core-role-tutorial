# AI Prompt: Test Plan Writer

## When to Use

You need to create a validation test plan for a new fabric build, migration, or change.

## The Prompt

```
You are a network validation engineer creating a test plan for a
WAN core / EVPN/VXLAN fabric in a PCI-DSS compliant environment.

Create a comprehensive test plan for: [DESCRIBE WHAT YOU'RE TESTING]

Topology:
[DESCRIBE or paste ASCII diagram]

The test plan must cover three pillars:

1. **Functional Tests** — Does each feature work as designed?
2. **Scale Tests** — Can the fabric handle the expected load?
3. **Resiliency Tests** — What happens when components fail?

For each test case include:
- Test ID (e.g., F-001, S-001, R-001)
- Test name
- Preconditions
- Steps (with exact CLI commands)
- Expected result
- Actual result (blank — to fill in during testing)
- Pass/Fail criteria

Also include:
- Test environment requirements
- Test execution schedule
- Sign-off section
```

## Caveats

- Add test cases specific to your environment
- Include PCI-DSS specific tests (VRF isolation, encryption)
- Test plan should be reviewed by the team before execution
