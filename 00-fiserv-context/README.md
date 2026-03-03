# 🏢 Module 00: Fiserv Context

> Before diving into protocols and configs, understand the **environment** you'll be working in. Fiserv's technology choices, compliance requirements, and ongoing infrastructure consolidation directly impact every design decision.

---

## Why This Matters

You're not studying for an exam — you're preparing for a specific role at a specific company. Knowing Fiserv's stack means:

1. **You speak their language** — Reference Versa (not Viptela), Cisco Catalyst (not Meraki), PCI-DSS (not generic security)
2. **You understand constraints** — PCI-DSS compliance drives VRF segmentation, not just "best practice"
3. **You spot opportunities** — The First Data merger means active migration/consolidation work = job security

## Contents

| File                                     | Description                                              |
| ---------------------------------------- | -------------------------------------------------------- |
| [NETWORK_STACK.md](./NETWORK_STACK.md)   | Confirmed Fiserv technology stack with confidence levels |
| [PCI_DSS_IMPACT.md](./PCI_DSS_IMPACT.md) | How PCI-DSS v4.0 drives network design decisions         |
| [VERSA_SDWAN.md](./VERSA_SDWAN.md)       | Versa Networks primer — your primary WAN tool            |

## Key Takeaways

- **Versa Networks** is their SD-WAN — not Cisco Viptela. Versa uses EVPN/VXLAN natively.
- **Cisco Catalyst 9000** for campus/enterprise — 30+ year partnership
- **PCI-DSS drives EVERYTHING** — cardholder data isolation via VRFs, L3VNIs, firewall insertion
- **First Data merger** (2019, $22B) — active DC consolidation and migration work
