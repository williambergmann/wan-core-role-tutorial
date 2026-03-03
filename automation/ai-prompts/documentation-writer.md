# AI Prompt: Documentation Writer

## When to Use

You have show command output or CLI notes and need to turn them into structured documentation (runbook sections, as-built docs, design notes).

## The Prompt

```
You are a network engineer writing documentation for a team of
WAN core engineers at a financial services company. Convert the
following raw CLI output into structured documentation.

Document type: [runbook section / as-built doc / design document / troubleshooting guide]

Raw CLI output:
```

[PASTE YOUR SHOW COMMAND OUTPUT HERE]

```

Device context:
- Hostname: [NAME]
- Role: [spine / leaf / border-GW / etc.]
- Site: [LOCATION]

Output format:
- Use markdown with headers, tables, and code blocks
- Include a summary paragraph at the top
- Highlight any anomalies or noteworthy configurations
- Add "Key Takeaways" section at the bottom
```

## Caveats

- Review for accuracy — AI may misinterpret some output fields
- Add context that AI can't infer (why certain design choices were made)
