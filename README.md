# 🌐 WAN Core Engineer — AI-Augmented Tutorial

> **Role:** WAN Core Engineer @ Fiserv (12-month contract)  
> **Start Date:** March 9, 2026  
> **Stack:** Versa SD-WAN · Cisco Catalyst 9000 · EVPN/VXLAN · MP-BGP · OSPF · PCI-DSS  
> **Philosophy:** Learn → Practice → Operationalize with AI & Automation

---

## 🎯 What Is This?

A focused, AI-augmented learning toolkit that prepares you for the WAN Core Engineer role. Every module has three layers:

| Layer                 | Purpose                      | Example                                                 |
| --------------------- | ---------------------------- | ------------------------------------------------------- |
| **📖 Learn**          | Master WAN core concepts     | Tutorials, visual references, quizzes                   |
| **⌨️ Practice**       | Build muscle memory in lab   | Containerlab topologies, hands-on configs               |
| **🤖 Operationalize** | Use AI/automation on the job | Prompt templates, Ansible playbooks, validation scripts |

> **This is not just study material** — it's a toolkit you'll use on Day 1 and beyond.

---

## 📂 Module Map

| #                              | Module              | What You'll Learn                      | AI/Automation                         |
| ------------------------------ | ------------------- | -------------------------------------- | ------------------------------------- |
| [00](./00-fiserv-context/)     | **Fiserv Context**  | Company stack, PCI-DSS, Versa SD-WAN   | —                                     |
| [01](./01-core-routing/)       | **Core Routing**    | BGP design patterns, OSPF underlay     | Config generator, BGP troubleshooter  |
| [02](./02-evpn-vxlan/)         | **EVPN/VXLAN**      | Fabric architecture, route types, IRB  | EVPN explainer, fabric designer       |
| [03](./03-wan-dci/)            | **WAN DCI**         | Multi-site EVPN, border gateway design | DCI design reviewer                   |
| [04](./04-segmentation/)       | **Segmentation**    | VRF, L3VNI, PCI-DSS zones              | VRF designer, PCI compliance checker  |
| [05](./05-validation-testing/) | **Validation**      | Test methodology, 3-pillar framework   | Pre/post checks, convergence timer    |
| [06](./06-migration-ops/)      | **Migration & Ops** | Runbooks, rollback plans, onboarding   | State capture/diff, runbook generator |
| [07](./07-troubleshooting/)    | **Troubleshooting** | Decision trees, breakfix scenarios     | Troubleshooting copilot               |

### Cross-Cutting Resources

| Directory                            | Contents                                                 |
| ------------------------------------ | -------------------------------------------------------- |
| [automation/](./automation/)         | Ansible playbooks, Python scripts, **AI prompt library** |
| [reference/](./reference/)           | CLI cheatsheets, glossary, vendor comparison             |
| [interview-prep/](./interview-prep/) | 30 Q&A, scenario practice, Day-1 playbook                |
| [onboarding/](./onboarding/)         | Northstar contractor onboarding guide, learning resources |

---

## 🚀 Quickstart

### 1. Clone & Setup

```bash
git clone git@github.com:williambergmann/wan-core-role-tutorial.git
cd wan-core-role-tutorial
./scripts/setup.sh
```

### 2. Follow the Roadmap

See [`ROADMAP.md`](./ROADMAP.md) for the recommended learning path — 7-day pre-start ramp + ongoing Day 1+ plan.

### 3. Track Your Progress

Check off completed modules in [`PROGRESS.md`](./PROGRESS.md).

### 4. Use AI Prompts On The Job

Browse [`automation/ai-prompts/`](./automation/ai-prompts/) for ready-to-use prompt templates that accelerate your daily work:

- **Generate configs** from high-level intent
- **Review configs** for errors and best practices
- **Troubleshoot issues** with guided step-by-step analysis
- **Write runbooks** from show command output
- **Create test plans** for validation testing

---

## 🏢 Fiserv Technology Stack

| Domain          | Technology                                       | Confidence   |
| --------------- | ------------------------------------------------ | ------------ |
| **SD-WAN**      | Versa Networks (Director, Controller, Analytics) | 🟢 Confirmed |
| **Campus**      | Cisco Catalyst 9000 + Catalyst Center            | 🟢 Confirmed |
| **Data Center** | VMware vSphere + Kubernetes/Portworx             | 🟢 Confirmed |
| **Compliance**  | PCI-DSS v4.0 (heavy network segmentation)        | 🟢 Confirmed |
| **DC Fabric**   | EVPN/VXLAN (Versa VOS + likely Cisco Nexus)      | 🟡 Likely    |
| **Security**    | Layered firewalls, IPS, micro-segmentation       | 🟢 Confirmed |

> Full deep dive: [`00-fiserv-context/NETWORK_STACK.md`](./00-fiserv-context/NETWORK_STACK.md)

---

## 🛠️ Tools Required

| Tool          | Purpose                  | Install                          |
| ------------- | ------------------------ | -------------------------------- |
| Python 3.10+  | Automation scripts       | `brew install python`            |
| Ansible 2.15+ | Network playbooks        | `pip install ansible`            |
| Containerlab  | Lab topologies           | `brew install containerlab`      |
| Docker        | Container runtime        | [docker.com](https://docker.com) |
| Netmiko       | SSH to network devices   | `pip install netmiko`            |
| NAPALM        | Multi-vendor abstraction | `pip install napalm`             |

---

## 📝 License

Private learning repository. Not for distribution.
