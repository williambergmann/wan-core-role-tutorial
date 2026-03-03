# 🤖 AI Prompts for Network Engineering

> **The most unique part of this repo.** Ready-to-use prompt templates for accelerating your daily work as a WAN Core Engineer.

---

## How to Use AI Effectively in Network Engineering

### What AI Is Good At

| Task                               | Quality | Example                                           |
| ---------------------------------- | ------- | ------------------------------------------------- |
| **Config generation from intent**  | ★★★★☆   | "Generate BGP config for 3 sites with these ASNs" |
| **Config review / error checking** | ★★★★★   | "Review this config for common mistakes"          |
| **Documentation writing**          | ★★★★★   | "Turn this show output into a runbook section"    |
| **Troubleshooting guidance**       | ★★★★☆   | "Analyze this BGP output and suggest next steps"  |
| **Test plan generation**           | ★★★★☆   | "Generate a resiliency test plan for this fabric" |
| **Concept explanation**            | ★★★★★   | "Explain EVPN Type-5 routes in simple terms"      |

### What AI Is NOT Good At

| Task                                    | Risk                                          | Mitigation                            |
| --------------------------------------- | --------------------------------------------- | ------------------------------------- |
| **Generating production-ready configs** | May have wrong IPs, ASNs, or missing features | Always review in lab first            |
| **Knowing your specific environment**   | Doesn't know your actual topology             | Provide detailed context              |
| **Real-time troubleshooting**           | Can't see your actual device state            | Paste show output                     |
| **Compliance validation**               | May miss PCI-DSS edge cases                   | Always have a human compliance review |

### Tips for Better Results

1. **Specify the platform** — "Use Cisco NX-OS syntax" not just "configure BGP"
2. **Provide topology context** — Describe the environment, number of sites, VRFs
3. **State the purpose** — "This is for PCI-DSS CDE isolation" changes the output significantly
4. **Ask for verification commands** — Always ask "what commands should I run to verify?"
5. **Request inline comments** — "Add comments explaining each section"

---

## Prompt Library

### Configuration & Design

| Prompt                                       | When to Use                                           | Module        |
| -------------------------------------------- | ----------------------------------------------------- | ------------- |
| [config-generator.md](./config-generator.md) | Generate any network config from intent               | Cross-cutting |
| [config-reviewer.md](./config-reviewer.md)   | Review configs for errors, best practices, PCI issues | Cross-cutting |
| [design-reviewer.md](./design-reviewer.md)   | Critique a network design before implementation       | Cross-cutting |

### Operations

| Prompt                                               | When to Use                                    | Module       |
| ---------------------------------------------------- | ---------------------------------------------- | ------------ |
| [documentation-writer.md](./documentation-writer.md) | Turn show output into structured documentation | 06 Migration |
| [runbook-writer.md](./runbook-writer.md)             | Generate operational runbooks from procedures  | 06 Migration |
| [test-plan-writer.md](./test-plan-writer.md)         | Generate validation test plans                 | 05 Testing   |

### Troubleshooting & Learning

| Prompt                                                         | When to Use                                     | Module             |
| -------------------------------------------------------------- | ----------------------------------------------- | ------------------ |
| [troubleshooting-assistant.md](./troubleshooting-assistant.md) | Debug any networking issue with guided analysis | 07 Troubleshooting |
| [quiz-generator.md](./quiz-generator.md)                       | Generate study questions from your notes        | Cross-cutting      |

---

## Prompt Design Pattern

All prompts in this library follow the same structure:

```
1. ROLE: "You are an expert network engineer specializing in..."
2. CONTEXT: "The environment is a PCI-DSS compliant financial services..."
3. TASK: "Given the following [topology/config/show output]..."
4. INPUT: [PLACEHOLDER for your actual data]
5. OUTPUT FORMAT: "Provide [config/analysis/plan] in [specific format]"
6. CONSTRAINTS: "Ensure [PCI compliance/vendor syntax/etc.]"
```

This structure ensures consistent, high-quality output regardless of which AI model you use (Claude, ChatGPT, Gemini, etc.).
