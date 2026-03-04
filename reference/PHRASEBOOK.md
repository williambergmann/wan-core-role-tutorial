# 🎙️ Network Engineering Phrasebook

> How a 15-year veteran sounds in meetings vs. how a newcomer sounds.
> Your programming background gives you the thinking — this gives you the dialect.

---

## The Key Principle

Experienced network engineers are **casual, specific, and brief.** They:

- Drop unnecessary words ("BGP is up" not "the BGP session is in Established state")
- Use acronyms without explaining them (you're expected to know)
- Lead with the conclusion, then add detail if asked
- Never say "I think" when they mean "I checked" — confidence matters

---

## Meeting Scenario 1: Status Update

### ❌ How a newcomer sounds:

> _"So I checked the Border Gateway Protocol sessions and they appear to be functioning correctly. The Open Shortest Path First protocol neighbors are all in FULL state. I also verified that the Virtual Extensible LAN tunnels seem to be operational. I believe everything is working as expected."_

### ✅ How a 15-year vet sounds:

> _"Fabric's healthy. OSPF is full across the board, all BGP EVPN peers are up, VXLAN tunnels are formed. No issues."_

**What makes it different:**

- Acronyms only — never spells out what they stand for
- "Across the board" instead of "on all devices"
- Declarative statements, not hedging with "I believe" or "appears to be"
- Three facts, done. No filler.

---

## Meeting Scenario 2: Describing a Problem

### ❌ Newcomer:

> _"There seems to be some kind of connectivity issue between Site A and Site B. The users are reporting that they're unable to access resources. I'm going to look into the routing tables and the BGP configuration to see if I can determine what might be causing the issue."_

### ✅ Veteran:

> _"Dallas is unreachable from Atlanta. BGP to their border gateway is down — session's in Active, so it's a TCP layer issue. I'm checking if we can even ping the peer IP. Probably an underlay problem or something blocking port 179."_

**What makes it different:**

- Site names, not "Site A and Site B"
- Specific state ("Active") with immediate interpretation
- Already narrowed the problem before finishing the sentence
- "Probably" with a hypothesis — shows you're thinking ahead

---

## Meeting Scenario 3: Explaining Your Change

### ❌ Newcomer:

> _"What I'm planning to do is add configuration for OSPF and BGP on the new switch so that it can participate in the network fabric. I'll also configure the VXLAN Network Identifier mappings and the VRF instances for tenant segmentation."_

### ✅ Veteran:

> _"Standard leaf onboard — OSPF underlay, BGP EVPN overlay, two VRFs. Same build as every other leaf. Pre-checks captured, I'll diff after."_

**What makes it different:**

- "Standard leaf onboard" — implies you've done this a hundred times
- Listing the components without over-explaining
- "Same build as every other leaf" — shows you know the existing fabric
- Mentions pre/post workflow casually

---

## Meeting Scenario 4: Answering a Question You're Not Sure About

### ❌ Newcomer:

> _"I'm not really sure about that. Let me go research it and get back to you."_

### ✅ Veteran:

> _"Off the top of my head, I think it's set to 300 for the interval, but let me pull up the running config and confirm. I'll follow up on Slack in five minutes."_

**What makes it different:**

- Gives a best-guess answer first (shows competence)
- Specifies HOW they'll verify (not vague "research")
- Commits to a specific follow-up time and channel
- "Off the top of my head" = honest without sounding ignorant

---

## Meeting Scenario 5: Pushing Back on a Bad Idea

### ❌ Newcomer:

> _"I don't think that's a good idea because it could potentially cause issues with the routing."_

### ✅ Veteran:

> _"That'll work, but it'll bite us later. If we redistribute BGP into OSPF, every WAN route change triggers an SPF recalc across the whole site. We'd be better off keeping them separate and using a static default."_

**What makes it different:**

- Doesn't just say "no" — explains the specific consequence
- Uses the correct mechanism name ("SPF recalc")
- Offers an alternative immediately
- "That'll work, but it'll bite us later" — acknowledges the idea isn't wrong, just risky

---

## Meeting Scenario 6: During an Outage Bridge Call

### ❌ Newcomer:

> _"I'm currently investigating the issue. I'm looking at various show commands to determine the root cause."_

### ✅ Veteran:

> _"I'm on the box now. OSPF is up but BGP EVPN is bouncing — last reset says hold timer expired, and BFD isn't configured on this peer. I think we've got packet loss on the WAN link causing keepalive drops. I'm going to enable BFD and check the optics."_

**What makes it different:**

- "I'm on the box" = I'm already SSH'd in and working
- Specific findings, not "looking at things"
- Root cause hypothesis with evidence
- Next action stated immediately
- No one has to ask "what are you going to do next?"

---

## Meeting Scenario 7: Design Discussion

### ❌ Newcomer:

> _"I was thinking maybe we should use Virtual Routing and Forwarding to separate the different types of traffic for the PCI compliance requirements?"_

### ✅ Veteran:

> _"CDE traffic needs its own VRF with a dedicated L3VNI. Corporate and guest stay in separate VRFs. No route leaking between CDE and anything else — that's a PCI audit finding if we get it wrong. Cross-VRF traffic goes through the firewall."_

**What makes it different:**

- Doesn't ask if they should use VRFs — states the design decision
- Specific technical mechanism (L3VNI, not just "VRF")
- Mentions the compliance consequence ("audit finding")
- Complete design in three sentences

---

## Filler Phrases Vets Use

These buy you time while sounding natural:

| Phrase                                                      | When to use it                                  |
| ----------------------------------------------------------- | ----------------------------------------------- |
| _"Let me pull that up real quick"_                          | When you need to check something on the CLI     |
| _"That's a good question — let me sanity-check the config"_ | When you're not sure and need to verify         |
| _"Yeah, that tracks"_                                       | When someone's diagnosis makes sense            |
| _"That's consistent with what I'm seeing"_                  | When your findings match someone else's         |
| _"I need to dig into that a bit more"_                      | When you don't have an answer yet               |
| _"Let me run through the pre-checks real quick"_            | Before any change                               |
| _"I want to diff the state before and after"_               | Describing pre/post methodology                 |
| _"Let me trace the path"_                                   | When debugging connectivity                     |
| _"From a routing perspective..."_                           | When pivoting to routing analysis               |
| _"From a segmentation standpoint..."_                       | When discussing VRF/PCI isolation               |
| _"The concern here is..."_                                  | When raising a risk politely                    |
| _"I'll circle back on that"_                                | When you need to follow up later                |
| _"Quick sanity check —"_                                    | Before asking a verification question           |
| _"Just to confirm —"_                                       | Before double-checking an assumption            |
| _"For context..."_                                          | Before adding background someone might not have |

---

## Things To Never Say

| ❌ Never Say                           | Why                                                                       |
| -------------------------------------- | ------------------------------------------------------------------------- |
| "Virtual Extensible LAN"               | Nobody says the full name. Ever. Just say VXLAN.                          |
| "Border Gateway Protocol"              | Just say BGP.                                                             |
| "What does that acronym mean?"         | Google it after the meeting. Asking on a call outs you.                   |
| "I'm not familiar with that"           | Instead: "I haven't worked with that recently — can you send me the doc?" |
| "Let me Google that"                   | Instead: "Let me check the documentation"                                 |
| "The server" (meaning a switch)        | Servers are compute. Switches are switches. Routers are routers.          |
| "The internet" (meaning the WAN)       | The WAN is private. The internet is public. Big difference.               |
| "IP address" when you mean "prefix"    | A prefix is a network (10.1.0.0/16). An IP is a host (10.1.0.1).          |
| "Bandwidth" when you mean "throughput" | Bandwidth = link capacity. Throughput = actual data rate.                 |
| "Latency" when you mean "jitter"       | Latency = delay. Jitter = variation in delay.                             |

---

## Your Software Background — Translation Table

You already know these concepts from programming. Here's the network equivalent:

| Programming Concept     | Network Equivalent           | How to say it                                                |
| ----------------------- | ---------------------------- | ------------------------------------------------------------ |
| API endpoint            | BGP neighbor / peering       | _"We're peered with Dallas"_                                 |
| Load balancer           | ECMP / anycast               | _"Traffic is ECMP'd across both spines"_                     |
| Environment variables   | Route communities            | _"We tag with communities for policy"_                       |
| Microservices isolation | VRF segmentation             | _"Each tenant is in its own VRF"_                            |
| CI/CD pipeline          | Change management / CAB      | _"It goes through CAB Thursday"_                             |
| Unit tests              | Pre/post checks              | _"I'll diff the state before and after"_                     |
| Git rollback            | Config rollback / checkpoint | _"Roll it back to the checkpoint"_                           |
| Pub/sub topics          | BGP address families         | _"We're exchanging routes in the l2vpn evpn address family"_ |
| Container networking    | VXLAN overlay                | _"The overlay handles forwarding across the fabric"_         |
| DNS resolution          | Route lookup / FIB           | _"Let me check the FIB for that prefix"_                     |
| Firewall rules          | ACLs / route-maps            | _"There's a route-map filtering the exports"_                |
| Health check endpoint   | BFD                          | _"BFD runs a heartbeat every 300ms"_                         |
| Database sharding       | Route summarization          | _"We summarize at the border to keep the tables small"_      |
| Dependency injection    | Route redistribution         | _"We don't redistribute — we keep OSPF and BGP separate"_    |
