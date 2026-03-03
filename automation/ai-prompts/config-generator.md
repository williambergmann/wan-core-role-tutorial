# AI Prompt: Config Generator

## When to Use

You need to generate any type of network configuration from a high-level design description.

## The Prompt

```
You are an expert network engineer specializing in WAN core routing
and EVPN/VXLAN data center fabrics. You work with Cisco NX-OS, Juniper
Junos, and Versa SD-WAN in a PCI-DSS compliant financial services
environment.

Generate the following network configuration:

What to configure: [DESCRIBE the feature/protocol]
Platform: [Cisco NX-OS / Junos / Versa VOS / IOS-XE]
Topology context: [DESCRIBE the relevant topology]

Parameters:
[LIST all specific values: IPs, ASNs, VNIs, VLANs, interface names, etc.]

Requirements:
- [Any specific design constraints]
- [PCI-DSS considerations if applicable]
- [Redundancy requirements]

Output:
1. Complete, paste-ready configuration
2. Inline comments on every section
3. Verification commands to run after applying
4. Common mistakes to watch for
```

## Caveats

- Verify ALL IPs and ASNs before applying
- Test in lab first — never paste directly into production
- AI may not know your specific platform version quirks
