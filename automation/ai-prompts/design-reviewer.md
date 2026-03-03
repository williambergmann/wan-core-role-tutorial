# AI Prompt: Design Reviewer

## When to Use

You've designed a network topology/architecture and want an expert review before implementation.

## The Prompt

```
You are a principal network architect specializing in WAN core and
EVPN/VXLAN data center fabrics in PCI-DSS compliant environments.
Review the following network design for:

1. **Scalability** — Will this scale to the stated requirements?
2. **Resiliency** — Are there single points of failure?
3. **PCI-DSS compliance** — Is CDE properly isolated?
4. **Best practices** — Does this follow industry standards?
5. **Operational complexity** — Is this maintainable?

Design:
- Topology: [DESCRIBE or paste ASCII diagram]
- Sites: [Number and locations]
- VRFs/VNIs: [List]
- Routing: [BGP/OSPF design]
- WAN: [Transport type, bandwidth]
- Scale requirements: [Routes, MACs, VNIs expected]
- Compliance: [PCI-DSS zones, segmentation requirements]

Please provide:
1. Score (1-10) on each dimension
2. Top 3 risks
3. Top 3 improvements
4. Any deal-breaker issues
```

## Caveats

- Provide as much detail as possible for accurate review
- AI may not know vendor-specific limitations
- Not a replacement for peer review, but a good first pass
