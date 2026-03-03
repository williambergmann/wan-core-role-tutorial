# 📅 Day One Playbook

> Your guide for the first week on the job. Priorities, questions to ask, and how to make a strong first impression.

---

## Day 1: Listen & Orient

### Morning (First 4 Hours)

1. **Get credentials** — VPN, email, Slack/Teams, ticketing system
2. **Meet the team** — Names, roles, who owns what
3. **Get lab access** — This is priority #1. Ask immediately.
4. **Get documentation access** — SharePoint, Confluence, Wiki — wherever design docs live
5. **Ask:** "What's the current state of the fabric buildout / migration?"

### Afternoon

6. **Read existing design documents** — Get the topology in your head
7. **Read existing runbooks** — Understand how the team operates
8. **Set up your local environment** — VPN, SSH keys, terminal tools, configs
9. **Ask:** "What's the change management process? How do I get changes approved?"

### Day 1 Questions to Ask

| Question                                             | Why You Ask It                 |
| ---------------------------------------------------- | ------------------------------ |
| "What vendor platforms make up the WAN core?"        | Verify the Versa/Cisco intel   |
| "What's the current fabric onboarding process?"      | Understand your primary work   |
| "Is there a lab environment I should get access to?" | Start practicing ASAP          |
| "What's the change management process?"              | Know the CAB workflow          |
| "Are there existing runbooks I should review?"       | Build on existing work         |
| "What's the state of the First Data migration?"      | Understand the biggest project |
| "How is PCI-DSS segmentation implemented?"           | Understand segmentation design |
| "What monitoring/alerting is in place?"              | Know the ops tools             |

---

## Day 2–3: Deep Dive into the Environment

- [ ] Map the actual topology (sites, ASNs, VRFs, VNIs)
- [ ] Identify the vendors/platforms in use (confirm your research)
- [ ] Review the IP addressing scheme (IPAM/NetBox access)
- [ ] Read the most recent change requests to understand current work
- [ ] Shadow a colleague during a change window or lab session
- [ ] Run health check commands on a lab device to build muscle memory

---

## Day 4–5: Start Contributing

- [ ] Offer to help with documentation — great way to learn the environment
- [ ] Run pre/post checks during a scheduled change (use your `state_capture.py` script)
- [ ] Review a pending configuration change (use your `config-reviewer.md` AI prompt)
- [ ] Set up your personal lab environment mirroring production
- [ ] Ask: "What's the most painful operational task? Can I help automate it?"

---

## Week 2+ Targets

- [ ] Own a validation test execution
- [ ] Write or update a migration runbook
- [ ] Propose an automation improvement
- [ ] Present a topic to the team (show your value early)

---

## First Impression Tips

1. **Be curious, not critical** — Ask "why" questions, don't suggest changes yet
2. **Document everything** — Take notes in your personal docs, not just in your head
3. **Offer to help** — Documentation, testing, lab work — any contribution matters
4. **Show your automation skills** — But only after understanding the environment
5. **Be reliable** — Show up prepared, follow through on commitments
