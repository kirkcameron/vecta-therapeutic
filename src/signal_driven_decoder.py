#!/usr/bin/env python3
"""
Signal-Driven Relationship Decoder — Vecta Therapeutic

100% signal-driven. 0% keyword text matching.

Vecta signals → Interpretation

No `if "boss" in text` checks. Pure pattern recognition.
"""

from dataclasses import dataclass, field
from typing import Optional
import os
import subprocess
import re


class VectaClient:
    """Client for Vecta CLI"""
    
    VECTA_PATH = os.environ.get("VECTA_PATH", "~/GIT/business/erlang/vecta/vecta")
    
    def predict(self, query: str):
        """Run prediction query against Vecta's brain"""
        vecta_cmd = os.path.expanduser(self.VECTA_PATH)
        try:
            result = subprocess.run(
                [vecta_cmd, "predict"] + query.split(),
                capture_output=True,
                text=True,
                timeout=10
            )
            output = result.stdout + result.stderr
        except FileNotFoundError:
            raise Exception(f"Vecta not found at {vecta_cmd}")
        
        return self._parse(query, output)
    
    def _parse(self, query: str, output: str):
        """Parse Vecta's output format"""
        present = {}
        absent = {}
        
        for match in re.finditer(r'([A-Z_-]+)\[(-?\d+)\]', output):
            word = match.group(1)
            score = int(match.group(2))
            if score > 0:
                present[word] = score
            else:
                absent[word] = score
        
        return type('Result', (), {
            'present': present,
            'absent': absent,
            'raw': output
        })()

# ============================================================
# SIGNAL CATEGORIES
# ============================================================

SIGNAL_CATEGORIES = {
    "power_dynamics": {
        "signals": ["POWER", "ABDICAT", "DELEGAT", "RIVAL", "OPPONENT", "AUTHORITY", 
                    "DEFIANCE", "CONTROL", "SUBMISSION", "BOSS", "MANAGER", "LEADER"],
        "exclude_signals": ["FORGET", "BUSY", "CALENDAR", "SCHEDULE"],
        "meaning": "Power play or authority avoidance detected",
        "framework": "negotiation",
        "description": "One party is avoiding direct confrontation or responsibility"
    },
    "avoidance": {
        "signals": ["AVOID", "DISINTEREST", "CANCEL", "REFUSE", "ESCAPE", 
                    "DEFLECT", "DELAY", "STALL", "CIRCLE", "REVISIT"],
        "exclude_signals": ["ENTHUSIASM", "EXCITED", "EAGER"],
        "meaning": "Active avoidance or disengagement detected",
        "framework": "attachment",
        "description": "One party is actively avoiding engagement or commitment"
    },
    "withdrawal": {
        "signals": ["SILENCE", "WITHDRAW", "QUIET", "STONEWALL", "SHUTDOWN", 
                    "DISENGAGE", "SPACE", "THINK", "PAUSE"],
        "exclude_signals": ["ATTACK", "AGGRESS", "CONFRONT"],
        "meaning": "Emotional withdrawal or overwhelm detected",
        "framework": "gottman",
        "description": "One party is withdrawing from emotional engagement"
    },
    "criticism": {
        "signals": ["CRITICISM", "INVALIDAT", "DEHUMAN", "SENSITIVE", "OVERREACT", 
                    "MASQUERADES", "DISGUISE", "LECTURE", "INSULT"],
        "exclude_signals": ["CONSTRUCTIVE", "HELPFUL", "SUPPORT"],
        "meaning": "Invalidation disguised as feedback detected",
        "framework": "cbt",
        "description": "Criticism is being delivered as if it were helpful feedback"
    },
    "trust_issue": {
        "signals": ["TRUST", "DISTRUST", "BETRAY", "HONEST", "SECRET", "LIE", 
                    "HIDING", "CONCEAL", "DECEPTION"],
        "exclude_signals": ["SECURE", "CONFIDENT", "OPEN"],
        "meaning": "Trust violation or betrayal detected",
        "framework": "attachment",
        "description": "A trust issue is present in the relationship"
    },
    "miscommunication": {
        "signals": ["MISUNDERSTAND", "CONFUSION", "UNCLEAR", "AMBIGUOUS", 
                    "MISCOMMUNICATION", "MISREAD"],
        "exclude_signals": ["CLEAR", "EXPLICIT"],
        "meaning": "Misalignment in communication detected",
        "framework": "general",
        "description": "The parties are talking past each other"
    },
    "quick_acceptance": {
        "signals": ["REGRET", "ENTHUSIASM", "FEAR", "DOUBT", "EASY", 
                    "ACCEPTANCE", "AGREEMENT", "IMMEDIATE", "QUICK"],
        "exclude_signals": ["HESITATION", "CAUTION"],
        "meaning": "Quick acceptance needs deeper analysis",
        "framework": "negotiation",
        "description": "Quick agreement may indicate enthusiasm, regret potential, or strategy"
    },
    "manipulation": {
        "signals": ["MANIPULAT", "GASLIGHT", "CONTROL", "DARVO", "DEFLECT", 
                    "PROJECT", "BLAME", "EXCUSE"],
        "exclude_signals": ["HONEST", "OPEN", "TRANSPARENT"],
        "meaning": "Manipulation or control pattern detected",
        "framework": "abuse",
        "description": "One party may be manipulating or controlling the other"
    },
    "emotional_abuse": {
        "signals": ["SILENT", "STONEWALL", "ABUSE", "CRUELTY", "DEHUMANIZE", 
                    "INVALIDATE", "MINIMIZE", "GASLIGHT"],
        "exclude_signals": ["RESPECT", "SUPPORT", "CARE"],
        "meaning": "Emotional abuse pattern detected",
        "framework": "abuse",
        "description": "Potentially harmful emotional patterns present"
    }
}


@dataclass
class PatternScore:
    name: str
    confidence: float
    signal_count: int
    total_score: int
    signals: list
    meaning: str
    framework: str
    description: str


@dataclass
class Interpretation:
    pattern: str
    confidence: float
    meaning: str
    framework: str
    description: str
    signals: list = field(default_factory=list)


@dataclass
class RelationshipAnalysis:
    input_text: str
    primary: Interpretation
    secondary: list
    excluded: list
    signals: list
    absent: list
    real_vecta: bool
    confidence: float


def extract_signals_by_category(signals: list, category_signals: list) -> list:
    """Extract signals that match a category"""
    return [(w, s) for w, s in signals 
            if any(cat in w for cat in category_signals)]


def check_absent_signals(absent: list, check_signals: list) -> int:
    """Count how many exclusion signals are absent (good!)"""
    return sum(1 for w, _ in absent 
               if any(cat in w for cat in check_signals))


def score_pattern(signals: list, absent: list, category: dict) -> PatternScore:
    """Score how well signals match a pattern"""
    category_signals = extract_signals_by_category(signals, category["signals"])
    exclude_signals = extract_signals_by_category(absent, category["exclude_signals"])
    
    signal_count = len(category_signals)
    total_score = sum(s for _, s in category_signals) if category_signals else 0
    
    # Bonus for exclusion signals being absent
    exclusion_bonus = len(exclude_signals) * 0.05
    
    # Calculate confidence
    if signal_count == 0:
        confidence = 0.0
    else:
        signal_confidence = min(0.7, (signal_count * 0.15) + (total_score / 1000))
        confidence = min(0.95, signal_confidence + exclusion_bonus)
    
    return PatternScore(
        name=category["meaning"].split()[0] if category["meaning"] else "unknown",
        confidence=confidence,
        signal_count=signal_count,
        total_score=total_score,
        signals=category_signals,
        meaning=category["meaning"],
        framework=category["framework"],
        description=category["description"]
    )


def extract_exclusions(absent: list) -> list:
    """Extract meaningful exclusions from absent signals"""
    exclusions = []
    
    exclusion_meanings = {
        "FORGET": "NOT forgetfulness",
        "BUSY": "NOT simple busyness",
        "CALENDAR": "NOT scheduling conflict",
        "MALICE": "NOT intentional harm",
        "DANGER": "NOT dangerous",
        "FORGET": "NOT a memory issue",
        "CONSTRUCTIVE": "NOT helpful feedback",
        "SUPPORT": "NOT supportive",
        "ENTHUSIASM": "NOT genuine enthusiasm",
        "CLEAR": "NOT clear communication",
        "SECURE": "NOT secure attachment"
    }
    
    for word, score in absent[:10]:  # Top 10 absent signals
        for key, meaning in exclusion_meanings.items():
            if key in word:
                exclusions.append(meaning)
                break
    
    return list(set(exclusions))  # Deduplicate


class SignalDrivenDecoder:
    """
    100% signal-driven relationship decoder.
    
    NO keyword text matching. Pure pattern recognition from Vecta signals.
    """
    
    def __init__(self):
        self.vecta = VectaClient()
    
    def decode(self, input_text: str) -> RelationshipAnalysis:
        """
        Decode relationship dynamics from text.
        
        Pure signal-driven: Vecta signals → Interpretation
        """
        # Safety check only
        if self._check_crisis(input_text):
            return self._crisis_response(input_text)
        
        # Get real Vecta signals
        result = self.vecta.predict(input_text)
        signals = list(result.present.items())
        absent = list(result.absent.items())
        
        # Score each category
        patterns = {}
        for name, category in SIGNAL_CATEGORIES.items():
            patterns[name] = score_pattern(signals, absent, category)
        
        # Rank patterns by confidence
        ranked = sorted(patterns.items(), key=lambda x: x[1].confidence, reverse=True)
        
        # Filter out zero-confidence patterns
        ranked = [(n, p) for n, p in ranked if p.confidence > 0.1]
        
        # Build interpretations
        if ranked:
            primary = Interpretation(
                pattern=ranked[0][0],
                confidence=ranked[0][1].confidence,
                meaning=ranked[0][1].meaning,
                framework=ranked[0][1].framework,
                description=ranked[0][1].description,
                signals=ranked[0][1].signals[:5]
            )
            
            secondary = [
                Interpretation(
                    pattern=ranked[i][0],
                    confidence=ranked[i][1].confidence,
                    meaning=ranked[i][1].meaning,
                    framework=ranked[i][1].framework,
                    description=ranked[i][1].description,
                    signals=ranked[i][1].signals[:3]
                )
                for i in range(1, min(3, len(ranked)))
            ]
        else:
            # No strong patterns detected
            primary = Interpretation(
                pattern="general",
                confidence=0.3,
                meaning="No strong patterns detected",
                framework="general",
                description="Pattern unclear. More context needed.",
                signals=[]
            )
            secondary = []
        
        # Extract exclusions
        exclusions = extract_exclusions(absent)
        
        return RelationshipAnalysis(
            input_text=input_text,
            primary=primary,
            secondary=secondary,
            excluded=exclusions,
            signals=signals,
            absent=absent,
            real_vecta=True,
            confidence=primary.confidence
        )
    
    def _check_crisis(self, text: str) -> bool:
        """Safety check only"""
        crisis_keywords = ["suicide", "kill myself", "self harm", "end it all"]
        return any(kw in text.lower() for kw in crisis_keywords)
    
    def _crisis_response(self, text: str) -> RelationshipAnalysis:
        """Crisis response"""
        return RelationshipAnalysis(
            input_text=text,
            primary=Interpretation(
                pattern="crisis",
                confidence=1.0,
                meaning="Please contact 988 (Suicide & Crisis Lifeline)",
                framework="safety",
                description="Crisis detected. Immediate support recommended."
            ),
            secondary=[],
            excluded=[],
            signals=[],
            absent=[],
            real_vecta=False,
            confidence=1.0
        )


def print_analysis(analysis: RelationshipAnalysis):
    """Print analysis results"""
    print("\n" + "=" * 60)
    print("🔮 VECTA SIGNAL-DRIVEN DECODER")
    print("=" * 60)
    
    print(f"\n📥 INPUT: \"{analysis.input_text}\"")
    
    p = analysis.primary
    print(f"\n🎯 PRIMARY [{p.confidence:.0%}]: {p.pattern}")
    print(f"   📝 {p.description}")
    print(f"   🔗 {p.meaning}")
    if p.signals:
        print(f"   📡 Signals: {', '.join(f'{w}[{s}]' for w, s in p.signals)}")
    
    if analysis.secondary:
        print(f"\n📊 SECONDARY PATTERNS:")
        for i, s in enumerate(analysis.secondary, 1):
            print(f"   [{i}] [{s.confidence:.0%}] {s.pattern}: {s.meaning}")
            if s.signals:
                print(f"       Signals: {', '.join(f'{w}[{s}]' for w, s in s.signals)}")
    
    if analysis.excluded:
        print(f"\n❌ EXCLUDED (NOT these):")
        for ex in analysis.excluded[:5]:
            print(f"   • {ex}")
    
    print(f"\n📈 TOP SIGNALS: {', '.join(f'{w}[{s}]' for w, s in analysis.signals[:10])}")
    print(f"🔇 ABSENT: {', '.join(f'{w}[{s}]' for w, s in analysis.absent[:5])}")
    print("=" * 60)


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":
    import sys
    
    decoder = SignalDrivenDecoder()
    
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
        analysis = decoder.decode(text)
        print_analysis(analysis)
    else:
        # Demo
        test_cases = [
            "My boss always says we should revisit this",
            "My friend keeps canceling plans",
            "My spouse says I am too sensitive",
            "They accepted our offer immediately",
            "My teenager won't talk to me"
        ]
        
        print("\n🧪 SIGNAL-DRIVEN DECODER DEMO\n")
        
        for text in test_cases:
            analysis = decoder.decode(text)
            print_analysis(analysis)
