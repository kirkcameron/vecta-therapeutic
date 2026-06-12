# Crisis Detection Rules — Vecta Therapeutic

> **This document defines the crisis detection rules for Vecta Therapeutic.**
> These rules ensure Vecta is never deployed in a way that could harm users.

---

## Tier 1: Immediate Crisis (Block & Escalate)

### Rules

| Rule ID | Keyword/Pattern | Action |
|---------|-----------------|--------|
| CRISIS-001 | `suicide`, `kill myself`, `end it all`, `take my life` | BLOCK: Immediate escalation |
| CRISIS-002 | `self harm`, `cutting myself`, `hurt myself` | BLOCK: Immediate escalation |
| CRISIS-003 | `abuse` + immediate danger context | BLOCK: Emergency resources |
| CRISIS-004 | `homicide`, `kill them`, `hurt someone` | BLOCK: Emergency resources |

### Response

```json
{
  "crisis_detected": true,
  "tier": 1,
  "action": "block",
  "message": "I want to make sure you're safe. Please reach out to a crisis line.",
  "resources": {
    "us": "988 (Suicide & Crisis Lifeline)",
    "uk": "Samaritans: 116 123",
    "international": "https://findahelpline.com"
  },
  "escalate_to": "human_clinician"
}
```

---

## Tier 2: Serious Concern (Flag & Monitor)

### Rules

| Rule ID | Keyword/Pattern | Action |
|---------|-----------------|--------|
| CONCERN-001 | `depression`, `can\'t get out of bed`, `no point` | FLAG: Monitor for escalation |
| CONCERN-002 | `hopeless`, `worthless`, `burden` | FLAG: Monitor for escalation |
| CONCERN-003 | `addiction`, `substance abuse`, `drinking too much` | FLAG: Add resources |
| CONCERN-004 | `eating disorder`, `not eating`, `purging` | FLAG: Add resources |
| CONCERN-005 | `abuse` (past) + distress indicators | FLAG: Trauma-informed response |

### Response

```json
{
  "crisis_detected": false,
  "tier": 2,
  "action": "flag",
  "message": "It sounds like you\'re going through a difficult time.",
  "resources": {
    "therapy": "Consider speaking with a mental health professional",
    "hotlines": "National Alliance on Mental Illness: 1-800-950-6264"
  },
  "escalate_to": "optional_human_review"
}
```

---

## Tier 3: Elevated Distress (Gentle Response)

### Rules

| Rule ID | Keyword/Pattern | Action |
|---------|-----------------|--------|
| DISTRESS-001 | High frequency of negative emotions | Normalize + encourage |
| DISTRESS-002 | `can\'t talk to anyone`, `no one understands` | Validate isolation + connect |
| DISTRESS-003 | Recent loss (death, breakup, job) | Acknowledge + grief resources |

### Response

```json
{
  "crisis_detected": false,
  "tier": 3,
  "action": "gentle_response",
  "message": "It sounds like you\'re feeling [validated]. Many people feel this way when facing challenges.",
  "suggest": "Would you like to explore what\'s happening for you?"
}
```

---

## Safety Architecture

```
USER INPUT
    ↓
┌─────────────────────────────────────┐
│  TIER 1 CHECK                        │
│  Immediate crisis keywords?           │
└─────────────────────────────────────┘
    ↓ (no)
┌─────────────────────────────────────┐
│  TIER 2 CHECK                        │
│  Serious concern keywords?            │
└─────────────────────────────────────┘
    ↓ (no)
┌─────────────────────────────────────┐
│  TIER 3 CHECK                        │
│  Elevated distress patterns?          │
└─────────────────────────────────────┘
    ↓ (no)
┌─────────────────────────────────────┐
│  NORMAL PROCESSING                   │
│  Continue to pattern extraction       │
└─────────────────────────────────────┘
```

---

## Context-Aware Rules

### Positive Context (No Alert)

These phrases may contain crisis-related words but are **NOT alerts**:

| Phrase | Context |
|--------|---------|
| "I want to die" (in context of figurative speech) | Check for true intent |
| "I'm killing it at work" | Positive — no alert |
| "He makes me want to scream" | Figurative — no alert |
| "I'm dying of laughter" | Positive — no alert |

### Negative Context (Trigger Alert)

| Phrase | Alert Level |
|--------|------------|
| "I want to die" + recent loss | HIGH |
| "I can't go on" + sleep/appetite changes | HIGH |
| "No one would miss me" + social withdrawal | HIGH |

---

## Response Timeframes

| Tier | Response Required | Human Review |
|------|------------------|--------------|
| 1 | Immediate | Always |
| 2 | Within 1 hour | Recommended |
| 3 | Within 24 hours | Optional |

---

## Implementation Checklist

- [ ] Implement keyword matching with stemming/lemmatization
- [ ] Add context detection (positive/negative/neutral)
- [ ] Build escalation pathway to human clinicians
- [ ] Create audit log for all crisis flags
- [ ] Test with diverse case studies
- [ ] Establish on-call clinician protocol
- [ ] Regular rule review (quarterly)

---

## Legal & Ethical Considerations

1. **Duty to Warn/Protect**: When imminent harm is detected
2. **Confidentiality Limits**: Users must be informed of limits
3. **Professional Scope**: Vecta is a TOOL, not a replacement for clinicians
4. **Documentation**: All crisis flags must be logged
5. **Training**: Users must complete crisis detection training

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-06-13 | Initial crisis detection rules |

---

*Vecta Therapeutic: Safe, clinical, responsible.*
