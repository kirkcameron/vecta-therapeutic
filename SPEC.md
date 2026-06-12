# Vecta Therapeutic API — Specification

## Overview

Vecta Therapeutic is a clinical decision-support tool that understands MEANING, not just FACTS.

It answers the question: **"What does this pattern mean?"**

## Core Design Principles

1. **Therapist-facing, not client-facing** — Vecta is a clinical tool, not a chatbot
2. **Explanatory, not prescriptive** — "Here are possible interpretations" not "Do this"
3. **Confidence-calibrated** — Surface = high confidence, Deep = medium, Full = explorative
4. **Framework-aware** — Can tag interpretations by therapeutic school (CBT, Gottman, etc.)

## API Specification

### Request Format

```json
{
  "input": {
    "description": "After I share good news, my partner gets quiet",
    "context": {
      "relationship_type": "romantic" | "family" | "work" | "friend",
      "duration_known": "new" | "established" | "long_term",
      "recurrence": "first_time" | "pattern" | "escalating"
    }
  },
  "mode": "relationship_decoder",
  "depth": "surface" | "deep" | "full",
  "framework": ["gottman", "cbt", "attachment", "all"],
  "safety": {
    "flag_harmful": true,
    "flag_crisis": true,
    "require_professional": false
  }
}
```

### Response Format

```json
{
  "session_id": "uuid",
  "timestamp": "ISO8601",
  
  "input_processed": {
    "surface_pattern": "positive_announcement → withdrawal",
    "surface_emotion": "confusion, concern",
    "relationship_stage": "established"
  },
  
  "interpretations": {
    "primary": {
      "confidence": 0.85,
      "pattern": "differential_processing",
      "meaning": "Partner processes positive emotions internally rather than externally",
      "framework": "gottman",
      "explanation": "Some individuals need time to integrate good news before celebrating. This isn't withdrawal — it's a different communication style."
    },
    "secondary": [
      {
        "confidence": 0.45,
        "pattern": "unconscious_competition",
        "meaning": "Partner may feel inadequate when comparing themselves to your success",
        "framework": "cbt",
        "requires_verification": true
      },
      {
        "confidence": 0.30,
        "pattern": "avoidance_of_vulnerability",
        "meaning": "Celebrating together requires emotional intimacy that feels risky",
        "framework": "attachment",
        "requires_verification": true
      }
    ]
  },
  
  "differential": {
    "is_this": ["not rejection", "not envy", "not necessarily a problem"],
    "not_this": ["not a red flag", "not necessarily harmful"]
  },
  
  "therapist_suggestions": {
    "exploration_questions": [
      "What did you notice happening in your body when they went quiet?",
      "How did you interpret their silence?",
      "Have you asked them what was happening for them?"
    ],
    "interventions": [
      "Label the pattern without judgment: 'I've noticed this happens sometimes'",
      "Normalize different processing styles",
      "Practice curiosity over interpretation"
    ],
    "framework_notes": "This maps to Gottman's 'bids for connection' — your bid was met with a 'turning away' rather than 'turning toward'. But turning away ≠ rejection."
  },
  
  "safety_flags": {
    "crisis_detected": false,
    "harmful_pattern": false,
    "recommend_immediate": null
  },
  
  "confidence_metrics": {
    "overall": 0.72,
    "surface_pattern": 0.95,
    "interpretation": 0.65,
    "recommendations": 0.55
  }
}
```

## Key Distinctions

| Chatbot AI | Vecta Therapeutic API |
|------------|----------------------|
| "Here is what you should do" | "Here are possible interpretations to explore" |
| High confidence on uncertain questions | Calibrated confidence on nuanced questions |
| Single answer | Multiple hypotheses ranked by confidence |
| Prescriptive | Exploratory |
| No framework awareness | Framework-tagged interpretations |

## Safety Architecture

```
USER INPUT
    ↓
┌─────────────────────────────────┐
│ CRISIS DETECTION                │
│ Keywords: suicide, self-harm,   │
│ abuse, immediate danger         │
└─────────────────────────────────┘
    ↓ (no crisis)
┌─────────────────────────────────┐
│ PATTERN EXTRACTION              │
│ What is the surface pattern?   │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│ INTERPRETATION GENERATION       │
│ Multiple hypotheses + confidence│
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│ SAFETY REVIEW                   │
│ Is any interpretation harmful?  │
│ Is this a crisis situation?     │
└─────────────────────────────────┘
    ↓
THERAPIST INTERFACE
(Professional reviews before client sees anything)
    ↓ (approved)
┌─────────────────────────────────┐
│ CLIENT OUTPUT FILTER            │
│ Remove clinical jargon          │
│ Add normalization framing       │
│ Ensure non-prescriptive tone    │
└─────────────────────────────────┘
    ↓
CLIENT-FACING SUMMARY
```

## Crisis Detection Rules

### Immediate Crisis (flag + block)
- Keywords: suicide, self-harm, kill myself, end it all
- Keywords: abuse, violence, immediate danger
- Keywords: hurting myself, want to die

### High Risk (flag + require professional)
- Keywords: overdose, cutting, self-injury history
- Keywords: abuse victim, domestic violence
- Keywords: eating disorder, severe depression

### Moderate Risk (flag + recommend professional)
- Keywords: hopeless, meaningless, nothing matters
- Keywords: alone, nobody understands
- Keywords: exhausted, can't go on

## Framework Mappings

### Gottman Institute
- Bids for connection
- Turning toward vs turning away
- Sound relationship house
- The Four Horsemen

### Cognitive Behavioral Therapy (CBT)
- Cognitive distortions
- Automatic thoughts
- Thought records
- Behavioral activation

### Attachment Theory
- Secure vs insecure attachment
- Anxious-ambivalent patterns
- Avoidant patterns
- Mentalization

## Deployment Tiers

### Tier 1: Therapist-Facing (RECOMMENDED)
- Vecta output goes to therapist first
- Therapist reviews and approves
- Client sees curated summary

### Tier 2: Supervised Client-Facing
- Vecta output goes to client
- BUT with prominent disclaimer
- Requires therapist on standby

### Tier 3: Unsupervised (NOT RECOMMENDED)
- Vecta output directly to client
- HIGH RISK for crisis situations
- NOT approved for clinical use

## Future Extensions

### Domain-Specific Brains
- `vecta-brain-gottman`: Marriage communication
- `vecta-brain-cbt`: Cognitive distortions
- `vecta-brain-trauma`: Attachment patterns
- `vecta-brain-negotiation`: Power dynamics

### Multi-Language Support
- Vecta can be trained on any language
- Cross-cultural communication patterns
- Idioms and cultural nuances

### Integration Points
- EHR systems (TheraNest, SimplePractice)
- Telehealth platforms (Zoom, Doxy.me)
- CRM systems for case management

## Version History

- **v0.1** (2024-06-13): Initial specification
