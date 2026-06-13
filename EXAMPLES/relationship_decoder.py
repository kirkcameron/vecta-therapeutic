#!/usr/bin/env python3
"""
Relationship Decoder — Vecta Therapeutic Proof of Concept

INPUT: A description of a frustrating interaction
OUTPUT: The underlying communication pattern + what it means + what to do next

USAGE:
    python relationship_decoder.py "Your input here"
    python relationship_decoder.py --interactive
    python relationship_decoder.py --demo boss

NOTE: Works with mock data if Vecta CLI is not available.
"""

import json
import os
import sys
import subprocess
import re
from dataclasses import dataclass, field
from typing import Optional

# ============================================================
# VECTA CONFIGURATION
# ============================================================

VECTA_PATH = os.path.expanduser("~/GIT/business/erlang/vecta/vecta")  # or full path

@dataclass
class VectaSignal:
    word: str
    score: int
    is_present: bool

def run_vecta_predict(query: str) -> dict:
    """Run real Vecta prediction or fall back to mock"""
    try:
        result = subprocess.run(
            [VECTA_PATH, "predict"] + query.split(),
            capture_output=True,
            text=True,
            timeout=10
        )
        output = result.stdout + result.stderr
        
        # Parse output: WORD[score] for present, WORD[-score] for absent
        present = []
        absent = []
        
        for match in re.finditer(r'([A-Z_-]+)\[(-?\d+)\]', output):
            word = match.group(1)
            score = int(match.group(2))
            signal = VectaSignal(word=word, score=score, is_present=score > 0)
            if score > 0:
                present.append((word, score))
            else:
                absent.append((word, score))
        
        return {
            "signals": present,
            "absent": absent,
            "raw": output,
            "real": True
        }
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return mock_vecta_predict(query)


def mock_vecta_predict(input_text: str) -> dict:
    """Mock Vecta output for demo"""
    lower = input_text.lower()
    
    if "boss" in lower or "revisit" in lower:
        return {
            "signals": [
                ("OPPONENT", 2), ("RIVAL", 2), ("AUTHORITY", 2),
                ("DELEGATE", 3), ("OPPOSITE", 3), ("WAY", 3)
            ],
            "absent": [
                ("RENOUNCES", -352), ("DISRESPECT", -353), ("DISAGREEMENT", -352)
            ],
            "raw": "[MOCK OUTPUT - Install Vecta for real data]",
            "real": False
        }
    elif "partner" in lower or "quiet" in lower:
        return {
            "signals": [
                ("SILENCE", 24), ("WITHDRAWAL", 3), ("TRUST", 16),
                ("LISTENING", 30), ("PROCESSING", 4)
            ],
            "absent": [],
            "raw": "[MOCK OUTPUT]",
            "real": False
        }
    else:
        return {
            "signals": [],
            "absent": [],
            "raw": "[MOCK OUTPUT]",
            "real": False
        }


@dataclass
class Interpretation:
    confidence: float
    pattern: str
    meaning: str
    framework: Optional[str] = None
    signals: list = field(default_factory=list)

@dataclass
class SafetyFlags:
    crisis_detected: bool = False
    recommend_immediate: Optional[str] = None

@dataclass
class RelationshipAnalysis:
    input_text: str
    surface_pattern: str
    primary: Interpretation
    secondary: list
    excluded: list
    signals: list
    real_vecta: bool
    confidence: float


def check_crisis(text: str) -> SafetyFlags:
    keywords = ["suicide", "kill myself", "self harm"]
    for kw in keywords:
        if kw in text.lower():
            return SafetyFlags(crisis_detected=True, recommend_immediate="Please call 988")
    return SafetyFlags()


def relationship_decoder(input_text: str) -> RelationshipAnalysis:
    """Main analysis function"""
    
    # Safety check
    safety = check_crisis(input_text)
    if safety.crisis_detected:
        return RelationshipAnalysis(
            input_text=input_text,
            surface_pattern="CRISIS DETECTED",
            primary=Interpretation(0, "crisis", safety.recommend_immediate),
            secondary=[],
            excluded=[],
            signals=[],
            real_vecta=False,
            confidence=1.0
        )
    
    # Get Vecta prediction
    result = run_vecta_predict(input_text)
    signals = result["signals"]
    absent = result["absent"]
    
    # Interpret
    lower = input_text.lower()
    
    if "boss" in lower or "revisit" in lower or "work" in lower:
        # Power play interpretation
        power_signals = [(w, s) for w, s in signals if any(x in w for x in ["OPPONENT", "DELEGATE", "AUTHORITY", "RIVAL"])]
        confidence = 0.85 if len(power_signals) > 2 else 0.6
        
        primary = Interpretation(
            confidence=confidence,
            pattern="power_play",
            meaning="'We should revisit' = polite refusal. Boss avoids direct confrontation.",
            framework="negotiation",
            signals=power_signals[:5]
        )
        
        secondary = [
            Interpretation(0.45, "genuine_disagreement", "Boss disagrees but won't say it directly.", "negotiation"),
            Interpretation(0.25, "dysfunction", "No one has authority to decide.", "systems")
        ]
        
        excluded = ["NOT genuine forgetfulness", "NOT simply busy", "NOT benign"]
        
    elif "partner" in lower or "quiet" in lower:
        # Withdrawal interpretation
        primary = Interpretation(
            confidence=0.80,
            pattern="differential_processing",
            meaning="Partner processes internally. Not rejection — different communication style.",
            framework="gottman",
            signals=[(w, s) for w, s in signals if w in ["SILENCE", "WITHDRAWAL", "TRUST"]]
        )
        secondary = [
            Interpretation(0.40, "unconscious_competition", "Partner may feel inadequate.", "cbt"),
            Interpretation(0.25, "avoidance", "Celebrating requires vulnerability.", "attachment")
        ]
        excluded = ["NOT rejection", "NOT envy"]
        
    elif "cancel" in lower or "repeats" in lower or "repeated" in lower:
        # Cancellation/avoidance interpretation
        avoidance_signals = [(w, s) for w, s in signals if any(x in w for x in ["AVOID", "DISINTEREST", "REPEATED", "WRONG"])]
        confidence = 0.75 if len(avoidance_signals) > 2 else 0.5
        
        primary = Interpretation(
            confidence=confidence,
            pattern="avoidance_pattern",
            meaning="Repeatedly canceling shows disinterest or avoidance. Something is wrong.",
            framework="attachment",
            signals=avoidance_signals[:5]
        )
        secondary = [
            Interpretation(0.35, "schedule_conflict", "May have genuine scheduling issues.", "practical"),
            Interpretation(0.30, "loss_of_interest", "May have lost interest in the relationship.", "attachment")
        ]
        excluded = ["NOT simply forgetful", "NOT random"]
        
    elif "sensitive" in lower or "overreact" in lower or "dramatic" in lower:
        # Criticism/invalidation interpretation
        criticism_signals = [(w, s) for w, s in signals if any(x in w for x in ["CRITICISM", "INVALIDATE", "DEHUMANIZE", "INSULT", "LECTURE"])]
        confidence = 0.80 if len(criticism_signals) > 2 else 0.6
        
        primary = Interpretation(
            confidence=confidence,
            pattern="criticism_invalidation",
            meaning="'You're too sensitive' is a form of criticism that invalidates feelings.",
            framework="cbt",
            signals=criticism_signals[:5]
        )
        secondary = [
            Interpretation(0.40, "deflection", "Partner avoids taking responsibility.", "cbt"),
            Interpretation(0.30, "communication_mismatch", "Different emotional expression norms.", "attachment")
        ]
        excluded = ["NOT helpful advice", "NOT constructive feedback"]
        
    elif "accept" in lower and ("immediately" in lower or "right away" in lower or "too quick" in lower):
        # Quick acceptance interpretation
        negotiation_signals = [(w, s) for w, s in signals if any(x in w for x in ["REGRET", "ENTHUSIASM", "FEAR", "DOUBT", "EASY"])]
        confidence = 0.70 if len(negotiation_signals) > 2 else 0.5
        
        primary = Interpretation(
            confidence=confidence,
            pattern="quick_acceptance",
            meaning="Quick acceptance may mean regret potential or genuine fit. Either way, probe deeper.",
            framework="negotiation",
            signals=negotiation_signals[:5]
        )
        secondary = [
            Interpretation(0.40, "genuine_enthusiasm", "They genuinely want the deal.", "negotiation"),
            Interpretation(0.35, "fear_of_losing", "They may regret later if they felt pressured.", "negotiation"),
            Interpretation(0.25, "over_eager", "May indicate you left money on the table.", "negotiation")
        ]
        excluded = ["NOT a mistake", "NOT random"]
        
    else:
        primary = Interpretation(0.5, "general", "Pattern detected. Explore further.", "general", signals[:3])
        secondary = []
        excluded = []
    
    return RelationshipAnalysis(
        input_text=input_text,
        surface_pattern="Agreement without action" if "boss" in lower else "Communication pattern",
        primary=primary,
        secondary=secondary,
        excluded=excluded,
        signals=signals,
        real_vecta=result["real"],
        confidence=primary.confidence
    )


def print_analysis(analysis: RelationshipAnalysis):
    """Print analysis results"""
    print("\n" + "=" * 60)
    print("🔮 VECTA RELATIONSHIP DECODER")
    print("=" * 60)
    
    print(f"\n📥 INPUT: \"{analysis.input_text}\"")
    print(f"🔍 PATTERN: {analysis.surface_pattern}")
    
    p = analysis.primary
    print(f"\n🎯 PRIMARY [{p.confidence:.0%}]: {p.pattern}")
    print(f"   {p.meaning}")
    if p.signals:
        print(f"   Signals: {', '.join(f'{w}[{s}]' for w, s in p.signals[:5])}")
    
    if analysis.secondary:
        print(f"\n📊 SECONDARY:")
        for s in analysis.secondary:
            print(f"   [{s.confidence:.0%}] {s.pattern}: {s.meaning}")
    
    if analysis.excluded:
        print(f"\n❌ EXCLUDED:")
        for e in analysis.excluded:
            print(f"   • {e}")
    
    if analysis.signals and analysis.real_vecta:
        print(f"\n📈 TOP SIGNALS (from Vecta):")
        for w, s in sorted(analysis.signals, key=lambda x: -x[1])[:10]:
            print(f"   {w}[{s}]")
    
    if not analysis.real_vecta:
        print(f"\n⚠️  Using mock data. Install Vecta for real analysis.")
    
    print("\n" + "=" * 60)


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] in ["-i", "--interactive"]:
            print("\n🔮 Interactive mode. Type 'quit' to exit.")
            while True:
                try:
                    text = input("\n📝 Situation: ").strip()
                    if text.lower() in ["quit", "q"]:
                        break
                    if text:
                        print_analysis(relationship_decoder(text))
                except KeyboardInterrupt:
                    break
        else:
            text = " ".join(sys.argv[1:])
            print_analysis(relationship_decoder(text))
    else:
        # Run boss example
        demo = "My boss always says we should revisit this but nothing changes"
        print(f"🎯 Demo: {demo}")
        print_analysis(relationship_decoder(demo))


if __name__ == "__main__":
    main()
