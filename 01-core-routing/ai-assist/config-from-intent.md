# AI Prompt: Generate BGP Config from Intent

## When to Use

You need to create BGP configuration for a new site, a new peering, or a design change — and you want a first draft generated from high-level intent instead of writing from scratch.

## How to Use

1. Copy the prompt below
2. Replace the `[PLACEHOLDERS]` with your actual design parameters
3. Paste into Claude or ChatGPT
4. **Review the output critically** — verify ASNs, IPs, communities, and policy logic

## The Prompt

```
You are an expert network engineer specializing in WAN core routing
and EVPN/VXLAN data center fabrics. You work with Cisco NX-OS,
Juniper Junos, and Versa SD-WAN in a PCI-DSS compliant financial
services environment.

Generate BGP configuration for the following design:

Topology:
- [DESCRIBE: e.g., "Site A (AS 65001) peering with Site B (AS 65002)
   via two border gateways per site"]

Parameters:
- Local ASN: [VALUE]
- Remote ASN: [VALUE]
- Local border GW1 loopback: [IP]
- Local border GW2 loopback: [IP]
- Remote border GW1 IP: [IP]
- Remote border GW2 IP: [IP]
- Link subnet(s): [SUBNET(s)]
- Address families: [ipv4 unicast, l2vpn evpn, or both]
- BFD: [yes/no, interval, multiplier]

Policy requirements:
- Communities to apply: [e.g., "tag all exports with 65001:100:1"]
- Local preference: [e.g., "GW1 = primary (LP 200), GW2 = backup (LP 100)"]
- Route summarization: [e.g., "advertise 10.1.0.0/16 aggregate only"]
- Route filtering: [e.g., "only accept /16 or shorter from remote"]

Output format:
- Provide configs for BOTH local border gateways
- Use [Junos / NX-OS / both] syntax
- Include verification commands to run after applying
- Add inline comments explaining each section
```

## Example

**Input:** "Site A (AS 65001) has two border GWs (lo0: 10.1.255.1 and 10.1.255.2) peering with Site B (AS 65002, remote GWs at 10.2.255.1 and 10.2.255.2). Use link-local peering on 10.0.0.0/30 subnets. Tag exports with community 65001:100:1. Primary path via GW1 (LP 200)."

**Expected output:** Complete NX-OS configs for both GW1 and GW2 with BGP, route-maps, community lists, and verification commands.

## Caveats

- **Always verify ASNs and IPs** — AI can transpose numbers
- **Check community format** — standard vs. extended vs. large communities have different syntax
- **Validate policy logic** — ensure import/export route-maps do what you intend
- **Test in lab first** — never paste AI-generated config directly into production
