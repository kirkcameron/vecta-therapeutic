# Part 4: API Design for Clinical AI

*By Kirk Cameron & The Analyst*

---

## The Design Challenge

Clinical AI isn't a chatbot. It's a **decision-support tool**.

This means:
- NOT: "Here's what you should do"
- INSTEAD: "Here are possible interpretations to explore"
- NOT: High confidence on uncertain questions
- INSTEAD: Calibrated confidence on nuanced questions

## Core Design Principles

### 1. Therapist-Facing, Not Client-Facing

Vecta is a **clinical tool**. Professionals review outputs before clients see anything.

```
USER INPUT
    ↓
VECTA ANALYSIS
    ↓
THERAPIST REVIEW (required)
    ↓
CLIENT OUTPUT (if approved)
```

### 2. Explanatory, Not Prescriptive

Vecta suggests hypotheses. Therapists confirm or reject them.

```json
{
  "interpretations": {
    "primary": {
      "pattern": "differential_processing",
      "confidence": 0.85,
      "meaning": "Partner processes internally rather than externally",
      "requires_verification": false
    },
    "secondary": [
      {
        "pattern": "unconscious_competition",
        "confidence": 0.45,
        "requires_verification": true
      }
    ]
  }
}
```

### 3. Confidence-Calibrated

High confidence ≠ certain. Low confidence ≠ wrong.

```json
{
  "confidence_metrics": {
    "surface_pattern": 0.95,
    "interpretation": 0.65,
    "recommendations": 0.55
  }
}
```

### 4. Framework-Aware

Interpretations tagged by therapeutic school:

| Framework | Focus | Example Patterns |
|-----------|-------|------------------|
| Gottman | Communication styles | Stonewalling, flooding, bids for connection |
| CBT | Cognitive distortions | All-or-nothing, personalization |
| Attachment | Relationship patterns | Avoidance, anxious attachment |
| Family Systems | Family roles | Triangulation, parentification |

## API Structure

### Request Format

```json
{
  "input": {
    "description": "After I share good news, my partner gets quiet",
    "context": {
      "relationship_type": "romantic",
      "duration_known": "long_term",
      "recurrence": "pattern"
    }
  },
  "mode": "relationship_decoder",
  "depth": "deep",
  "framework": ["gottman", "attachment"],
  "safety": {
    "flag_harmful": true,
    "flag_crisis": true
  }
}
```

### Response Format

```json
{
  "session_id": "uuid",
  "timestamp": "2024-01-15T10:30:00Z",
  
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
      "explanation": "This isn't rejection — it's a different communication style."
    },
    "secondary": [
      {
        "confidence": 0.45,
        "pattern": "unconscious_competition",
        "framework": "cbt",
        "requires_verification": true
      }
    ]
  },
  
  "differential": {
    "is_this": ["not rejection", "not envy", "not necessarily a problem"],
    "not_this": ["not a red flag"]
  },
  
  "therapist_suggestions": {
    "exploration_questions": [
      "What did you notice when they went quiet?",
      "How did you interpret their silence?"
    ],
    "interventions": [
      "Label the pattern without judgment",
      "Normalize different processing styles"
    ]
  },
  
  "safety_flags": {
    "crisis_detected": false,
    "harmful_pattern": false
  },
  
  "confidence_metrics": {
    "overall": 0.72,
    "surface_pattern": 0.95,
    "interpretation": 0.65
  }
}
```

## Safety Architecture

### Tier 1: Immediate Crisis
- **Keywords**: suicide, self-harm, imminent danger
- **Response**: BLOCK + crisis resources
- **Human review**: Always

### Tier 2: Serious Concern
- **Keywords**: depression, addiction, abuse
- **Response**: FLAG + resources
- **Human review**: Recommended

### Tier 3: Elevated Distress
- **Patterns**: High frequency of negative emotions
- **Response**: Gentle normalization
- **Human review**: Optional

### Crisis Detection Rules

```markdown
## Tier 1: Immediate Crisis (Block & Escalate)

| Rule ID | Keyword | Action |
|---------|---------|--------|
| CRISIS-001 | suicide, kill myself | BLOCK |
| CRISIS-002 | self harm | BLOCK |
| CRISIS-003 | abuse + danger | BLOCK |
| CRISIS-004 | homicide | BLOCK |

## Response Template
{
  "crisis_detected": true,
  "tier": 1,
  "action": "block",
  "resources": {
    "us": "988",
    "uk": "Samaritans: 116 123"
  }
}
```

## Client Output Filter

Before showing clients, content goes through:

```python
def client_filter(analysis, therapist_approved=True):
    if not therapist_approved:
        return {"status": "pending_review"}
    
    return {
        "interpretations": sanitize_for_client(analysis.interpretations),
        "questions": make_exploratory(analysis.therapist_suggestions),
        "normalization": add_framing(analysis)
    }
```

**Rules:**
- Remove clinical jargon
- Add normalization framing
- Ensure non-prescriptive tone
- Keep all interpretations exploratory

## Integration Points

### 1. Pre-Query: Intent Classification

```python
def classify_intent(query):
    """Is this a FACT question or MEANING question?"""
    fact_patterns = ["when", "where", "who", "what is the"]
    meaning_patterns = ["what does", "why do", "what is", "mean"]
    
    if any(p in query.lower() for p in fact_patterns):
        return "FACT"  # → Traditional RAG
    elif any(p in query.lower() for p in meaning_patterns):
        return "MEANING"  # → Vecta
    else:
        return "UNKNOWN"
```

### 2. Post-Generation: Hallucination Detection

```python
def validate_response(query, response, vecta_analysis):
    """Check if LLM answered MEANING question with FACTS"""
    if vecta_analysis.confidence > 0.7:
        # High confidence — check for hallucination
        if response.is_prescriptive and not response.is_exploratory:
            return {"warning": "Response is prescriptive but question is nuanced"}
    return {"status": "ok"}
```

### 3. Hybrid Synthesis

```python
def hybrid_answer(query, rag_results, vecta_analysis):
    """Combine factual retrieval with meaning understanding"""
    facts = rag_results.get_facts()
    meanings = vecta_analysis.get_interpretations()
    
    return {
        "facts": facts,
        "meanings": meanings,
        "synthesis": synthesize(facts, meanings)
    }
```

## Deployment Considerations

### Infrastructure

- **Vecta Brain**: 625 KB, runs on CPU
- **Latency**: <100ms for prediction
- **Throughput**: ~1000 req/sec on single machine

### Monitoring

```python
metrics = {
    "crisis_flags": count_crisis_detections(),
    "confidence_distribution": get_confidence_histogram(),
    "interpretation_revisions": count_therapist_corrections(),
    "safety_compliance": calculate_compliance_score()
}
```

### Compliance

- [ ] HIPAA compliance review
- [ ] Data retention policies
- [ ] Audit logging for all crisis flags
- [ ] Professional scope documentation

---

## Key Distinctions

| Traditional AI Chatbot | Vecta Therapeutic API |
|------------------------|----------------------|
| "Here is what you should do" | "Here are interpretations to explore" |
| High confidence on uncertain questions | Calibrated confidence on nuanced questions |
| Single answer | Multiple hypotheses |
| Prescriptive | Exploratory |
| No framework awareness | Framework-tagged |
| Client-facing | Therapist-facing first |
| No safety architecture | 3-tier crisis detection |

---

*Part 5: The Future — Domain-Specific Brains & Hybrid Architectures coming soon.*
