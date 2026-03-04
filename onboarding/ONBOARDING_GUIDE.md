# Network Engineer Onboarding Guide

> Northstar Technologies contractor onboarding playbook — rules, procedures, soft skills, and operational best practices for network engineering engagements.

---

## Most Important Rules

| Rule | Detail |
|------|--------|
| **No Unauthorized Changes** | Never make changes on production network devices without support team approval. |
| **Change Control** | Always have a change control before modifying network devices. |
| **Documentation Review** | Review your transcribed interview and resume with the support team. |

---

## Enterprise Networks: Reality vs Training

### Etherchannels

- **Training:** Etherchannels are only switch-to-switch.
- **Production:** Servers often connect to switches via etherchannels using multiple NICs.

### Trunking

- **Training:** Trunking is only switch-to-switch or router-on-a-stick.
- **Production:** VMware servers may have trunks of many VLANs, supporting virtual switching for VMs.

---

## Basic Network Concepts

| Concept | Description |
|---------|-------------|
| **Active Directory** | Centralized domain management system. |
| **DNS** | Domain Name System for translating domain names to IP addresses. |
| **Ping & Traceroute** | Tools for network diagnostics and path tracing. |

---

## Network Diagnostic Tools

### 1. NS Lookup

Query DNS servers for domain name or IP address mapping information.

### 2. Continuous Ping

Monitor network connectivity over time.

### 3. SNMP

Simple Network Management Protocol for collecting and organizing information about managed devices.

---

## Monitoring Tools Overview

**Solarwinds** and **Logic Monitor** are comprehensive IT management software suites used for network monitoring, troubleshooting, and performance optimization.

---

## Email Tools: Outlook Essentials

1. **Signature Setup** — Create a professional email signature for consistent branding.
2. **Spell Check** — Ensure error-free communication with built-in spell check features.
3. **Rules Configuration** — Set up rules to automate email organization and management.

---

## Customizing Your Desktop

- **Software Installation** — Use the Software Center to install approved applications.
- **Bookmark Important Sites** — Add key URLs to your browser bookmarks bar.
- **Putty Configuration** — Configure Putty to save session output to file for documentation.

---

## Sharing Information with Support

1. **Draft in Gmail** — Use Gmail drafts to save and access information across devices.
2. **Share with Northstar** — Access the draft on your personal machine to share with the support team.
3. **Post on Northstar Teams Chat** — So support can easily access and assist.

---

## Timesheet Management

Timesheets are crucial for contractors. Consistent completion is key to client satisfaction.

### Northstar Timecards

- Submit your timecards through the **Northstar Timecard App**.
- You've been added to the **NST Timesheets** group for questions on Teams.
- **Timecards are due every Monday by 10 AM**, regardless of approval status.
- Attach a screenshot of your MDS-approved timecard for each submission to Northstar for verification.

### Timecard Approval

- Ensure a copy of your approved timecards is uploaded into the app by **12 PM CST on Tuesdays** for verification.
- If approval is delayed, include a note explaining the reason (e.g., the manager is on vacation).

> For timecard questions, contact **Megan Patterson** at Timecards@northstar-tek.com.

---

## Essential Account Registrations

| # | Account | Purpose |
|---|---------|---------|
| 1 | **Cisco CCO Account** | Higher access and TAC case management. |
| 2 | **F5 Registered Account** | Access Dev Central for valuable resources. |
| 3 | **Vendor Accounts** | Register for Juniper and Aruba accounts. |

---

## Perception Management

| Area | Guidance |
|------|----------|
| **Online Presence** | Be active during working hours, plus 30 minutes before and after your shift. |
| **Meeting Participation** | Speak up in every meeting, even for simple questions or reiterations. |
| **Note-Taking** | Take thorough, understandable notes during all sessions. |

---

## Day-to-Day Work Best Practices

1. **Initiative** — Ask for more work weekly, both verbally and via email.
2. **Documentation** — Create detailed network documentation and "big picture" diagrams.
3. **Auditing** — Regularly audit network devices and configurations, providing feedback on discrepancies.

---

## Personal Background Preparation

### If asked "So what'd you do before this?"

> "Yeah, I was just wrapping a long-term contract over at [previous staffing company] and it was a pretty standard route/switch, firewall, [relevant technology] — similar to what we do around here. This role came up and I'm super glad to be here and look forward to helping out."

### Follow-up: "Who was the end client?"

> "It was a large medical insurance company, but due to NDA I can't really disclose the end client."

### "What certs do you have?"

> "I had my CCNP but it expired."

---

## Staffing Company Relationships

| Audience | Approach |
|----------|----------|
| **End Customer** | Present yourself as a contractor from the staffing agency, without mentioning Northstar. |
| **Staffing Agency** | Acknowledge your work with Northstar when interacting with the staffing agency. |

---

## Elevator Pitch: Key Questions to Ask

### 1. VPN and Remote Access Setup

1. What VPN client does the team use for remote access?
2. Will I be issued a corporate laptop or use VDI for access?
3. How do I obtain TACACS credentials for network device access?

### 2. Documentation and Resources

5. Where is the team documentation hosted — SharePoint or Confluence?
6. What network design documents and runbooks are available for reference?
7. Which monitoring tools are used for network management?

### 3. Operational Processes

8. What is the support rotation schedule?
9. How many branch sites are we responsible for?
10. What is the change control process and schedule?
11. Who are the key contacts on the system/security teams we work with?

---

## Handling Employment Offers

- **Remember Your Commitment** — You have a 2-year agreement with Northstar. It takes about that long to become fully self-sufficient.
- **Polite Declination** — Express appreciation but prefer contracting work currently. Mention potential future consideration.
- **Communicate with Northstar** — Discuss all employment offers with your Northstar team.

---

## Navigating Controversial Topics

1. **Maintain Neutrality** — As a contractor, remain neutral on potentially divisive topics.
2. **Polite Deflection** — Use phrases like "I don't talk about politics/religion/money" to avoid discussions.
3. **Seek Support** — Contact Northstar support if pressured into uncomfortable conversations.

### Non-Committal Responses

| Strategy | Example |
|----------|---------|
| **Neutral Acknowledgment** | "Hmm, interesting." / "I'll have to think about that." |
| **Polite Deflection** | "I'm not the best person to ask about that." / "I don't talk about that as a contractor." |
| **Respectful Boundary Setting** | "I respect your right to an opinion, but I'd rather not share mine." |

---

## Meeting Best Practices

- **Detailed Note-Taking** — Make comprehensive notes during meetings, focusing on discussions and follow-up tasks.
- **Recording for Accuracy** — Consider recording sessions to review later for thorough understanding.
- **Clear Communication** — Ensure accurate relay of environment details, ongoing work, and expectations to the team.

### Critical Points

- **Terms are really important** — Don't generalize when relaying messages to support about something a co-worker told you.
- **Side-car support** — Try to put your work laptop on speaker and have the support team hear calls on NST Webex or Teams so they can side-car you with questions/answers.

---

## Ticketing and Change Control

### Ticketing System

Learn and promptly respond to the company's specific ticketing system.

### Change Control Process

Understand and strictly follow the end client's change control procedures for production environment modifications.

### Change Advisory Board (CAB)

1. **Approval Process** — Submit changes for CAB approval before implementation.
2. **Timing Specification** — Clearly define the time to initiate the change.
3. **Backout Plan** — Always include a detailed plan for reverting changes if needed.

---

## Troubleshooting Scenario Questions

### 1. Timing and Symptoms

Ask about issue occurrence time and user-experienced symptoms.

### 2. Scope and Reproducibility

Inquire about affected sites and issue reproducibility.

### 3. Technical Details

Request source/destination IPs, ports, and any recent changes made.

---

## Prioritization and Communication

| Area | Action |
|------|--------|
| **Priority Level** | Determine if the issue is P1 or P2. Assess need for emergency change control. |
| **Key Contacts** | Identify main points of contact for updates. |
| **Previous Investigations** | Ask who has already looked into the issue details. |

---

## Continuous Learning and Adaptation

1. **Stay Updated** — Continuously learn about new technologies and industry trends.
2. **Seek Feedback** — Regularly ask for feedback from colleagues and supervisors.
3. **Adapt Quickly** — Be ready to adapt to new tools, processes, and environments.

---

## Spiel Practice

Schedule a 1-hour meeting with Pat, Jeremy, and Adrian to practice "soft skills" (talking to the customer). Use Outlook calendar and the scheduling assistant to make sure everyone is free.

**Topics:**

1. Rehearsing the "so what did you do before this?" question.
2. Rehearsing a spiel where you explain — using industry terms — what material you went over for project prep, including labs, YouTube videos, etc.
