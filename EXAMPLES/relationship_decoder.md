# Relationship Decoder Examples

> Real-world examples demonstrating the Vecta Relationship Decoder.

---

## Example 1: Boss Edition (Hero Example)

### Input
```
"My boss always says 'we should revisit this' but nothing ever changes"
```

### Vecta Analysis

#### Pattern Detected
**Agreement without action**

#### Top Interpretation: Power Play
- **Confidence:** HIGH (85%)
- **Pattern:** "We should revisit" = polite refusal
- **Signals:** ABDICATING, DELEGATING, REFUSAL, DISHONESTY
- **Meaning:** Boss is avoiding direct confrontation
- **Framework:** Negotiation

#### Secondary: Genuine Disagreement
- **Confidence:** MEDIUM (45%)
- **Signals:** DISAGREEMENT, DISPUTE, OPPONENT
- **Meaning:** Boss disagrees but won't say it directly

#### Excluded Interpretations
- ❌ NOT genuine forgetfulness
- ❌ NOT simply busy
- ❌ NOT benign

#### What This Means for the Employee

**Exploration questions:**
- "What do you think is preventing your boss from committing?"
- "Has your boss ever followed through on a 'revisit'?"
- "What happens when you bring it up again?"

**Possible actions:**
- "Try: 'I'd love to understand your concerns. What's making this hard to decide now?'"
- "If it's a power play: Decide if you want to escalate or let it go"
- "If it's fear of conflict: Create safety for direct conversation"

---

## Example 2: Partner Edition

### Input
```
"After I share good news, my partner gets quiet. Sometimes they change the subject."
```

### Vecta Analysis

#### Pattern Detected
**Positive announcement → Withdrawal**

#### Primary Interpretation: Differential Processing
- **Confidence:** HIGH (80%)
- **Pattern:** Partner processes positive emotions internally
- **Signals:** SILENCE, REFLECTION, INTERNAL_PROCESSING
- **Meaning:** This isn't rejection — it's a different communication style
- **Framework:** Gottman

#### Secondary: Unconscious Competition
- **Confidence:** MEDIUM (40%)
- **Signals:** COMPARISON, INADEQUACY, AVOIDANCE
- **Meaning:** Partner may feel inadequate when comparing themselves

#### Secondary: Avoidance of Vulnerability
- **Confidence:** LOW (25%)
- **Signals:** VULNERABILITY, CELEBRATION, RISK
- **Meaning:** Celebrating together requires emotional intimacy

#### What This Means

**This is NOT:**
- Rejection of you
- Envy
- A red flag (necessarily)

**This IS:**
- An opportunity to understand different communication styles
- A bid for connection that missed

#### What to Do Next

1. **Ask, don't assume:** "I noticed you went quiet. What were you thinking?"
2. **Create space:** Don't pressure for immediate response
3. **Explore patterns:** Is there unspoken competition in your relationship?

---

## Example 3: Friend Edition

### Input
```
"My best friend has been canceling plans at the last minute. They always have an excuse."
```

### Vecta Analysis

#### Pattern Detected
**Cancellation pattern**

#### Primary Interpretation: Avoidance Behavior
- **Confidence:** HIGH (75%)
- **Pattern:** Repeated cancellation = something they're avoiding
- **Signals:** AVOIDANCE, EXCUSES, ESCAPE, DISCOMFORT
- **Meaning:** Something about the friendship (or their life) feels heavy
- **Framework:** Attachment

#### Secondary: Overcommitment
- **Confidence:** MEDIUM (35%)
- **Signals:** BURNOUT, SPREAD_THIN, YES_HABIT
- **Meaning:** Friend says yes but can't follow through

#### Secondary: Passive Disengagement
- **Confidence:** LOW (25%)
- **Signals:** GRADUAL_WITHDRAWAL, DIFFICULT_CONVERSATION
- **Meaning:** Friend wants out but won't initiate hard conversation

#### What This Means

**This is NOT:**
- Something you did (necessarily)
- A reflection of your worth

**This IS:**
- A pattern that needs direct conversation
- A sign something has shifted in the friendship

#### What to Do Next

1. **Direct conversation:** "I've noticed plans keep falling through. Is everything okay?"
2. **Check in, not out:** Don't assume the worst — ask with curiosity
3. **Set boundaries:** If this continues, decide what you can accept

---

## Example 4: Family Edition

### Input
```
"My parent criticizes everything I do, even when they're 'just joking.'"
```

### Vecta Analysis

#### Pattern Detected
**Masked criticism**

#### Primary Interpretation: Passive-Aggressive Pattern
- **Confidence:** HIGH (85%)
- **Pattern:** Criticism disguised as humor
- **Signals:** MASKING, SUPERIORITY, DISGUISE, HOSTILITY
- **Meaning:** Criticism feels safer when packaged as a joke
- **Framework:** Family Systems

#### Secondary: Unconscious Transmission
- **Confidence:** MEDIUM (40%)
- **Signals:** LEARNED_BEHAVIOR, UNCONSCIOUS, REPEATING
- **Meaning:** This is how they were raised — they may not realize it's harmful

#### Secondary: Maintaining Control
- **Confidence:** MEDIUM (35%)
- **Signals:** POWER, SUPERIORITY, INFERIORITY
- **Meaning:** Criticism keeps you in a subordinate position

#### What This Means

**This is NOT:**
- Harmless
- Just their personality
- Something you should accept

**This IS:**
- A pattern that affects your self-esteem
- Worth addressing directly

#### What to Do Next

1. **Name the pattern:** "When you say things like that, even joking, it hurts."
2. **Set consequences:** "If it continues, I'll need to limit our conversations."
3. **Protect yourself:** You don't have to convince them to change.

---

## Example 5: Escalation Edition

### Input
```
"My partner and I had a huge fight. They said things they can't take back."
```

### Vecta Analysis

#### Pattern Detected
**Relationship crisis**

#### Primary Interpretation: Emotional Flooding
- **Confidence:** HIGH (80%)
- **Pattern:** Hurtful words during high-emotion state
- **Signals:** FLOODING, REACTIVITY, DEFENSIVENESS, CRITICISM
- **Meaning:** Words said in anger often don't reflect true feelings
- **Framework:** Gottman

#### Safety Check
- ⚠️ **ESCALATION PATTERN DETECTED**
- This is a high-stakes situation

#### What This Means

**Before interpretation, consider:**
- Is everyone physically safe?
- Is this part of a pattern or a one-time event?
- What was the trigger?

**If this is a one-time flooding event:**
- Apology and repair are possible
- Cool-down period needed
- Address the underlying issue

**If this is a pattern:**
- This may indicate deeper problems
- Consider couple's therapy
- Your safety matters most

#### What to Do Next

1. **Immediate:** Ensure physical safety
2. **Short-term:** Take space to cool down
3. **When ready:** "I need to talk about what happened. Can we do that calmly?"
4. **If pattern:** "This keeps happening. We need help."

---

## Running These Examples

```bash
# Run all examples
python relationship_decoder.py

# Run specific example
python relationship_decoder.py "My boss always says 'we should revisit this'..."

# Interactive mode
python relationship_decoder.py --interactive
```

---

*These examples are for demonstration purposes. Real clinical use requires proper safety protocols and professional oversight.*
