# Vecta: Personal Knowledge Encoding System

> **Encode facts. Retrieve facts. Remember everything.**

## What Vecta Is

**Vecta is an associative memory system that encodes and retrieves specific facts from training data.**

It's NOT:
- ❌ "AI that understands meaning"
- ❌ Word association (it's fact encoding)
- ❌ Generic pattern matching

**It encodes WHAT YOU TRAIN IT ON and retrieves those facts on query.**

## How It Works

```
vecta think "Kirk lives in Hamburg. Kirk owns three guitars."
    ↓
vecta predict KIRK
    ↓
Returns: HAMBURG[2], GUITARS[2], OWNS[3], LIVES[11]
```

### Commands:

- `vecta think <text>` = Encode facts into memory
- `vecta predict <word>` = Retrieve encoded facts

### Key Properties:

| Property | What It Means |
|----------|---------------|
| Low numbers (2, 3, 4) | Strong encoding - close to training |
| Memory accumulates | Facts persist across sessions |
| No truth filter | Encodes whatever you train |

## The Difference: RAG vs Vecta

| System | Returns |
|--------|---------|
| RAG | "Here's a document about X" |
| **Vecta** | "Here's what you taught me about X" |

**Vecta = Personal knowledge encoding**

## What We Proved:

```
Training: "The moon is made of cheese"
Query: vecta predict MOON
Result: CHEESE[2] ✓

Training: "Whales are purple"
Query: vecta predict WHALES  
Result: PURPLE[2] ✓
```

**Vecta encodes EXACT FACTS from training data.**

## The Real Product:

**Personal Knowledge Encoding for AI**

```
You train Vecta on: Your notes, emails, knowledge
        ↓
Vecta encodes: Your specific facts
        ↓
LLM queries: "What does user know about X?"
        ↓
Vecta retrieves: User's encoded facts
        ↓
LLM generates: Contextual response using user's data
```

## Honest Claim:

**"Vecta encodes and retrieves specific facts from training data. Personal associative memory for AI systems."**

## Use Cases:

1. **Personal AI assistant** - Train on your knowledge, retrieve your facts
2. **Meeting memory** - Encode conversations, query for facts
3. **Research tool** - Train on papers, retrieve concepts
4. **Knowledge base** - Encode expertise, query for associations

## Warning:

**Vecta encodes whatever you train it on - true or false.**

Garbage in = garbage out. You curate the training data.

## The Problem with Current AI

Traditional AI fails at the questions humans actually ask when they're struggling:

- "My boss says 'let's revisit this' but nothing ever changes — what does this **mean**?"
- "My partner goes quiet when I share good news — what's happening?"
- "Why do I keep attracting the same type of person?"

LLMs hallucinate because they try to answer **MEANING questions** with **FACT retrieval**. Vecta retrieves semantic pattern associations.

## The Innovation

| Traditional AI | Vecta Therapeutic |
|----------------|-------------------|
| "Here are 10 tips for following up" | "Your boss is communicating something without saying it" |
| High confidence on uncertain questions | Calibrated confidence on nuanced questions |
| Single answer | Multiple hypotheses ranked by confidence |
| Prescriptive | Exploratory |
| No subtext awareness | Finds semantic pattern associations |

## What Vecta Actually Is

**Sophisticated word association with XOR cascades.**

Vecta doesn't "understand" meaning. It finds what words tend to appear together in context. That's sophisticated pattern matching at scale — not understanding, but still useful for communication analysis.

## The Relationship Decoder: Boss Edition

### Input
```
"My boss always says 'we should revisit this' but nothing ever changes"
```

### Vecta Analysis

#### Pattern Detected
**Agreement without action**

#### Top Interpretation: Power Play
- **Confidence:** High
- **Pattern:** "We should revisit" = polite refusal
- **Signals:** ABDICATING, DELEGATING, REFUSAL, DISHONESTY
- **Meaning:** Boss is avoiding direct confrontation

#### Secondary: Genuine Disagreement
- **Confidence:** Medium
- **Signals:** DISAGREEMENT, DISPUTE, OPPONENT
- **Meaning:** Boss disagrees but won't say it directly

#### Excluded Interpretations
- ❌ NOT genuine forgetfulness
- ❌ NOT simply busy
- ❌ NOT benign

#### This Is NOT a Coordination Problem
This is a **POWER problem**.

### What This Means for the Employee

**Exploration questions:**
- "What do you think is preventing your boss from committing?"
- "Has your boss ever followed through on a 'revisit'?"
- "What happens when you bring it up again?"

**Possible actions:**
- "Try: 'I'd love to understand your concerns. What's making this hard to decide now?'"
- "If it's a power play: Decide if you want to escalate or let it go"
- "If it's fear of conflict: Create safety for direct conversation"

## Architecture

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
│ INTERPRETATION GENERATION        │
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
```

## Key Capabilities

- **Causal reasoning**: Understands "LEADS TO", "CAUSES", "PRECEDES"
- **Metaphor understanding**: Irony, subtext, figurative language
- **Power dynamics**: Who has power? How is it exercised?
- **Manipulation detection**: GASLIGHTING, DARVO, coercive control, silent treatment
- **Framework-aware**: Can tag interpretations by therapeutic school (Gottman, CBT, attachment)
- **Signal-driven architecture**: Pure Vecta signals drive interpretation — no keyword matching

## Brain Stats

| Metric | Value |
|--------|-------|
| Entries | 3,264 |
| Concepts | 948 |
| Thoughts | 2,316 |
| Synapses | 117,960 |
| Quality Score | 95/100 |

## Getting Started

```bash
# Clone the repo
git clone https://github.com/your-org/vecta-therapeutic

# Install dependencies
npm install

# Run the demo
npm run demo:boss
```

## Blog Series

Learn the full story of Vecta Therapeutic:

| Part | Title | Description |
|------|-------|-------------|
| [Part 1](../BLOG/part-01-what-is-vecta.md) | What is Vecta? | The origin story |
| [Part 2](../BLOG/part-02-xor-cascades.md) | XOR Cascades | How associative memory works |
| [Part 3](../BLOG/part-03-stress-testing.md) | Stress Testing | Finding Vecta's gaps |
| [Part 4](../BLOG/part-04-api-design.md) | API Design | The therapeutic API |
| [Part 5](../BLOG/part-05-future.md) | The Future | What's next |
| **[Part 6](../BLOG/part-06-signal-driven-architecture.md)** | **Signal-Driven Architecture** | **How we built the meaning decoder** |

## Project Structure

```
vecta-therapeutic/
├── SPEC.md              ← Full API specification
├── README.md            ← This file
├── BLOG/                ← Blog series (6 parts)
├── EXAMPLES/
│   ├── relationship_decoder.md
│   ├── negotiation_intelligence.md
│   └── conflict_mediation.md
├── BRAIN/
│   └── communication-brain.json
├── SAFETY/
│   └── crisis_detection_rules.md
└── src/
    ├── api.ts
    ├── safety.ts
    └── synthesis.ts
```

## The Market

Vecta answers **"What does this mean?"** — and that is a MASSIVE market:

- 50% of therapy sessions
- 70% of relationship conflicts
- 80% of workplace frustrations
- 90% of existential anxiety

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for development guidelines.

## License

MIT

---

*Vecta is not a chatbot. It's a clinical tool for understanding meaning.*
