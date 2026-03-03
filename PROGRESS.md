# 📊 Progress Tracker

> Check off each item as you complete it. Be honest — partial understanding counts as incomplete.

---

## Module 00: Fiserv Context

- [ ] Read NETWORK_STACK.md — understand the confirmed tech stack
- [ ] Read PCI_DSS_IMPACT.md — understand how PCI drives network design
- [ ] Read VERSA_SDWAN.md — understand Versa architecture and how it maps to DC fabric concepts

## Module 01: Core Routing (BGP + OSPF)

- [ ] Read README — BGP design patterns and OSPF underlay
- [ ] Lab: BGP fundamentals (eBGP + iBGP peering)
- [ ] Lab: BGP policy (communities, local-pref, MED)
- [ ] Lab: OSPF underlay (P2P links, BFD, loopbacks)
- [ ] Complete quiz (≥80%)
- [ ] Try AI prompt: config-from-intent
- [ ] Try AI prompt: bgp-troubleshooter

## Module 02: EVPN/VXLAN Fabric

- [ ] Read README — VXLAN encap, EVPN route types, Symmetric IRB
- [ ] Lab: Build single-site fabric (2-spine, 3-leaf)
- [ ] Lab: Verify L2VNI and L3VNI connectivity
- [ ] Lab: Test Symmetric IRB (cross-VLAN, cross-leaf)
- [ ] Complete quiz (≥80%)
- [ ] Try AI prompt: evpn-explainer
- [ ] Try AI prompt: fabric-designer

## Module 03: WAN DCI

- [ ] Read README — Multi-site EVPN, border gateway design
- [ ] Lab: Two-site DCI with eBGP EVPN peering
- [ ] Lab: Exchange Type-5 routes between sites
- [ ] Lab: Test resiliency (kill WAN link, verify reconvergence)
- [ ] Complete quiz (≥80%)
- [ ] Try AI prompt: dci-design-reviewer

## Module 04: Segmentation

- [ ] Read README — Multi-VRF, route leaking, PCI-DSS zones
- [ ] Lab: Create 3 VRFs with L3VNI isolation
- [ ] Lab: Configure route leaking (Prod ↔ Mgmt)
- [ ] Lab: Verify VRF isolation (Dev cannot reach Prod)
- [ ] Complete quiz (≥80%)
- [ ] Try AI prompt: vrf-designer
- [ ] Try AI prompt: pci-compliance-checker

## Module 05: Validation & Testing

- [ ] Read README — 3-pillar testing framework
- [ ] Practice: Write a functional test plan
- [ ] Practice: Execute resiliency tests in lab
- [ ] Practice: Run pre/post check automation
- [ ] Try AI prompt: test-plan-generator

## Module 06: Migration & Operations

- [ ] Read README — Fabric onboarding, migration methodology
- [ ] Practice: Simulate a fabric onboarding migration
- [ ] Practice: Write a migration runbook
- [ ] Practice: Execute and verify a rollback
- [ ] Try AI prompt: runbook-generator

## Module 07: Troubleshooting

- [ ] Read README — Systematic troubleshooting methodology
- [ ] Practice: Complete all 10 breakfix scenarios
- [ ] Review: All 5 decision tree flowcharts
- [ ] Try AI prompt: troubleshooting-copilot

## Automation

- [ ] Set up Python environment (`pip install -r automation/python/requirements.txt`)
- [ ] Run an Ansible health check playbook
- [ ] Run a Python state capture script
- [ ] Use 3+ AI prompts in a real work scenario

## Interview Prep

- [ ] Review all 30 interview questions
- [ ] Practice 3 whiteboard scenarios (time yourself)
- [ ] Finalize Day-1 playbook

---

## Summary

| Module             | Status         | Confidence |
| ------------------ | -------------- | ---------- |
| 00 Fiserv Context  | ⬜ Not Started | —          |
| 01 Core Routing    | ⬜ Not Started | —          |
| 02 EVPN/VXLAN      | ⬜ Not Started | —          |
| 03 WAN DCI         | ⬜ Not Started | —          |
| 04 Segmentation    | ⬜ Not Started | —          |
| 05 Validation      | ⬜ Not Started | —          |
| 06 Migration       | ⬜ Not Started | —          |
| 07 Troubleshooting | ⬜ Not Started | —          |
| Automation         | ⬜ Not Started | —          |
| Interview Prep     | ⬜ Not Started | —          |
