# 📅 WAN Core Engineer — Learning Roadmap

> **Start Date:** March 9, 2026  
> **Prep Window:** March 3–8 (6 days)  
> **Goal:** Walk in Day 1 ready to contribute, not just understand concepts.

---

## Pre-Start Ramp (March 3–8)

### Days 1–2: Core Protocols

| Day           | Module                                | Focus                                | Time    |
| ------------- | ------------------------------------- | ------------------------------------ | ------- |
| Day 1 (Mar 3) | [01 Core Routing](./01-core-routing/) | BGP fundamentals + policy            | 4-5 hrs |
| Day 2 (Mar 4) | [01 Core Routing](./01-core-routing/) | OSPF underlay + BGP+OSPF interaction | 4-5 hrs |

### Days 3–4: Fabric & WAN

| Day           | Module                                                              | Focus                                        | Time    |
| ------------- | ------------------------------------------------------------------- | -------------------------------------------- | ------- |
| Day 3 (Mar 5) | [02 EVPN/VXLAN](./02-evpn-vxlan/)                                   | VXLAN encap, EVPN route types, Symmetric IRB | 4-5 hrs |
| Day 4 (Mar 6) | [03 WAN DCI](./03-wan-dci/) + [04 Segmentation](./04-segmentation/) | Multi-site DCI + VRF/PCI-DSS segmentation    | 4-5 hrs |

### Days 5–6: Operations & Readiness

| Day           | Module                                                                            | Focus                                 | Time    |
| ------------- | --------------------------------------------------------------------------------- | ------------------------------------- | ------- |
| Day 5 (Mar 7) | [05 Validation](./05-validation-testing/) + [06 Migration](./06-migration-ops/)   | Test plans, runbooks, pre/post checks | 4-5 hrs |
| Day 6 (Mar 8) | [07 Troubleshooting](./07-troubleshooting/) + [Interview Prep](./interview-prep/) | Breakfix practice + Day 1 prep        | 3-4 hrs |

---

## Day 1+ On-The-Job Ramp

### Week 1 (Mar 9–13): Listen & Learn

- [ ] Get lab access — ask immediately
- [ ] Read existing design docs and runbooks
- [ ] Shadow a fabric onboarding or change window
- [ ] Run `automation/ansible/playbooks/health-check.yml` in lab to learn the environment
- [ ] Start using AI prompts for documentation tasks

### Week 2 (Mar 16–20): Contribute

- [ ] Assist with validation testing on a lab fabric
- [ ] Write or update documentation using `ai-prompts/documentation-writer.md`
- [ ] Run pre/post checks during a change window
- [ ] Set up your personal lab environment mirroring production topology

### Week 3+ (Mar 23+): Own

- [ ] Own a validation test execution for a fabric build
- [ ] Create or improve a migration runbook
- [ ] Propose an automation improvement
- [ ] Deepen Versa SD-WAN expertise (Module 00)

---

## Daily Study Format

Each study day has:

- **🎯 Objective** — What you'll be able to DO by end of day
- **📖 Study** — Read the module README (1–2 hours)
- **⌨️ Hands-On** — Lab work with actual CLI (2–3 hours)
- **📝 Deliverable** — Something tangible you produce
- **✅ Checkpoint** — How you know you're ready to move on

---

## Questions for Day 1

Bring these to your first meeting:

1. "What vendor platforms make up the WAN core?"
2. "What's the current fabric onboarding process?"
3. "Is there a lab environment I should get access to?"
4. "What's the change management process?"
5. "Are there existing runbooks or documentation I should review?"
6. "What's the current state of the First Data migration/consolidation?"
7. "How is PCI-DSS segmentation implemented in the fabric?"
