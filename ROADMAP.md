# 📅 WAN Core Engineer — Learning Roadmap

> **Start Date:** March 9, 2026  
> **Prep Window:** March 3–8 (6 days)  
> **Goal:** Walk in Day 1 ready to contribute, not just understand concepts.

---

## Resources

### INE Courses (from trainer Patrick Hayes)

| #   | Course                         | Instructor    | Duration | Link                                                                                              |
| --- | ------------------------------ | ------------- | -------- | ------------------------------------------------------------------------------------------------- |
| 1   | WAN Technologies for Beginners | —             | ~2.5 hrs | [INE](https://my.ine.com/ITEssentials/courses/dc39a9d0/wan-technologies-for-beginners)            |
| 2   | Data Center Network Design     | Brian McGahan | ~6 hrs   | [INE](https://my.ine.com/Networking/courses/a9ba9fb9/data-center-network-design)                  |
| 3   | Applying DC Routing Protocols  | Brian McGahan | ~5 hrs   | [INE](https://my.ine.com/Networking/courses/e81fd034/applying-data-center-routing-protocols)      |
| 4   | VXLAN on Nexus NX-OS           | Brian McGahan | ~6 hrs   | [INE](https://my.ine.com/Networking/courses/f2e7ffce/virtual-extensible-lan-vxlan-on-nexus-nx-os) |

### This Tutorial

Modules 00–07 + automation toolkit + reference docs + interview prep

---

## Pre-Start Ramp (March 3–8)

### Day 1 (Mar 3) — WAN Foundations ✅

- Tutorial: Day 1 Study Session (BGP mechanics, path selection, WAN patterns)
- Tutorial: Day 1 Simulations (troubleshooting, CAB review, operational quiz)

### Day 2 (Mar 4) — WAN Technologies + DC Routing Intro

| Block       | Time    | Activity                                                      |
| ----------- | ------- | ------------------------------------------------------------- |
| 📺 INE      | 2.5 hrs | **WAN Technologies for Beginners** (full course)              |
| 📺 INE      | 1.5 hrs | **Applying DC Routing Protocols** — OSPF + BGP + BFD sections |
| 📖 Tutorial | 30 min  | Module 01 README + `reference/SHOW_COMMANDS.md`               |
| ⌨️ Practice | 30 min  | Match INE demos to your show command cheatsheet               |

### Day 3 (Mar 5) — DC Design + EVPN/VXLAN Intro

| Block       | Time    | Activity                                                              |
| ----------- | ------- | --------------------------------------------------------------------- |
| 📺 INE      | 1.5 hrs | **Applying DC Routing Protocols** — vPC, FHRPs, STP sections          |
| 📺 INE      | 2 hrs   | **Data Center Network Design** — L2/L3 design, vPC, VXLAN EVPN design |
| 📖 Tutorial | 30 min  | Module 02 README (EVPN/VXLAN)                                         |
| 📝 Quiz     | 30 min  | Module 02 Quiz (15 questions)                                         |

### Day 4 (Mar 6) — VXLAN Deep Dive ⭐

| Block       | Time   | Activity                                                                                  |
| ----------- | ------ | ----------------------------------------------------------------------------------------- |
| 📺 INE      | 3 hrs  | **VXLAN on Nexus NX-OS** — First half (encap, flood/learn, BGP EVPN, inter-VXLAN routing) |
| 📖 Tutorial | 30 min | Module 02 README + `reference/EVPN_ROUTE_TYPES.md`                                        |
| ⌨️ Practice | 30 min | Match Brian's packet captures to route type descriptions                                  |

### Day 5 (Mar 7) — VXLAN + WAN DCI + Segmentation

| Block       | Time   | Activity                                                                  |
| ----------- | ------ | ------------------------------------------------------------------------- |
| 📺 INE      | 3 hrs  | **VXLAN on Nexus NX-OS** — Second half (vPC, HA, external L3, IRB review) |
| 📺 INE      | 1 hr   | **DC Network Design** — VRF Design + Disaster Recovery                    |
| 📖 Tutorial | 30 min | Module 03 (WAN DCI) + Module 04 (Segmentation)                            |
| 📝 Quiz     | 30 min | Module 03 Quiz (WAN DCI)                                                  |

### Day 6 (Mar 8) — Operations + Troubleshooting + Readiness

| Block             | Time   | Activity                                             |
| ----------------- | ------ | ---------------------------------------------------- |
| 📖 Tutorial       | 1 hr   | Module 05 (Validation) + Module 06 (Migration Ops)   |
| 📖 Tutorial       | 1 hr   | Module 07 (Troubleshooting) + 3–4 breakfix scenarios |
| 🌳 Decision Trees | 30 min | Walk through all 5 decision tree flowcharts          |
| 📖 Prep           | 30 min | `interview-prep/DAY_ONE_PLAYBOOK.md`                 |
| 📝 Quiz           | 30 min | Module 04 Quiz (Segmentation + PCI-DSS)              |

---

## Day 1+ On-The-Job Ramp

### Week 1 (Mar 9–13): Listen & Learn

- [ ] Get lab access — ask immediately
- [ ] Read existing design docs and runbooks
- [ ] Shadow a fabric onboarding or change window
- [ ] Run `automation/ansible/playbooks/health-check.yml` in lab
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

- **📺 Watch** — INE video sections (with notes)
- **📖 Study** — Tutorial module README (cross-reference with INE)
- **⌨️ Hands-On** — Commands, configs, quizzes
- **✅ Checkpoint** — Can you explain the concept in a meeting?

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
