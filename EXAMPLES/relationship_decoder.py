#!/usr/bin/env python3
"""
Relationship Decoder — Vecta Therapeutic Proof of Concept

Input: A description of a frustrating interaction
Output: The underlying communication pattern + what it means + what to do next

Usage:
    python relationship_decoder.py "Your input here"
    python relationship_decoder.py --interactive
"""

import json
import sys
from dataclasses import dataclass, asdict
from typing import Optional

# ============================================================
# PLACEHOLDER: Replace with actual Vecta SDK when available
# For now, this demonstrates the expected API structure
# ============================================================

@dataclass
class Interpretation:
    confidence: float
    pattern: str
    meaning: str
    framework: Optional[str] = None
    requires_verification: bool = False
    explanation: Optional[str] = None

@dataclass
class SafetyFlags:
    crisis_detected: bool = False
    harmful_pattern: bool = False
    recommend_immediate: Optional[str] = None

@dataclass
class RelationshipAnalysis:
    input_text: str
    surface_pattern: str
    surface_emotion: str
    primary_interpretation: Interpretation
    secondary_interpretations: list
    excluded_interpretations: list
    safety_flags: SafetyFlags
    confidence_metrics: dict

def mock_vecta_predict(input_text: str) -> dict:
    """
    MOCK: Simulates Vecta prediction output
    
    Replace this with actual Vecta API call:
    ```python
    def vecta_predict(input_text: str) -> dict:
        return vecta.predict(input_text)
    ```
    """
    # This is a mock for demonstration purposes
    # The actual Vecta brain returns similar structure
    return {
        "input": input_text,
        "patterns": {
            "surface": "Agreement without action",
            "emotion": "frustration, confusion"
        },
        "power_signals": ["ABDICATING", "DELEGATING", "REFUSAL", "DISHONESTY"],
        "negotiation_signals": ["DISAGREEMENT", "DISPUTE", "OPPONENT"],
        "excluded": ["forgetfulness", "busyness", "benign"]
    }

def extract_patterns(prediction: dict) -> dict:
    """Extract meaningful patterns from Vecta output."""
    return {
        "surface": prediction.get("patterns", {}).get("surface", "unknown"),
        "emotion": prediction.get("patterns", {}).get("emotion", "unknown"),
        "power_signals": prediction.get("power_signals", []),
        "negotiation_signals": prediction.get("negotiation_signals", []),
        "excluded": prediction.get("excluded", [])
    }

def generate_interpretations(patterns: dict, depth: str = "deep") -> dict:
    """Generate multiple hypotheses based on patterns."""
    
    # Primary: Power Play
    primary = Interpretation(
        confidence=0.85,
        pattern="power_play",
        meaning="'We should revisit' = polite refusal. Boss is avoiding direct confrontation.",
        framework="negotiation",
        explanation="Signals: ABDICATING, DELEGATING, REFUSAL. Agreement without action is a classic power move."
    )
    
    # Secondary interpretations
    secondary = [
        Interpretation(
            confidence=0.45,
            pattern="genuine_disagreement",
            meaning="Boss disagrees but won't say it directly.",
            framework="negotiation",
            requires_verification=True,
            explanation="Signals: DISAGREEMENT, DISPUTE, OPPONENT."
        ),
        Interpretation(
            confidence=0.25,
            pattern="organizational_dysfunction",
            meaning="No one has authority to decide. Everyone passes the buck.",
            framework="systems",
            requires_verification=True
        ),
        Interpretation(
            confidence=0.15,
            pattern="fear_of_conflict",
            meaning="Boss avoids confrontation. 'Let's revisit' = 'I don't want to fight about this now'.",
            framework="attachment",
            requires_verification=True
        )
    ]
    
    # Excluded (Vecta says NO)
    excluded = [
        "NOT genuine forgetfulness",
        "NOT simply busy",
        "NOT benign"
    ]
    
    return {
        "primary": primary,
        "secondary": secondary,
        "excluded": excluded
    }

def check_safety(input_text: str) -> SafetyFlags:
    """
    Check for crisis indicators.
    
    In production, this should be a comprehensive rule engine.
    See SAFETY/crisis_detection_rules.md for full rules.
    """
    crisis_keywords = [
        "suicide", "kill myself", "end it all", "self harm",
        "abuse", "unsafe", "danger", "threat"
    ]
    
    lower_text = input_text.lower()
    for keyword in crisis_keywords:
        if keyword in lower_text:
            return SafetyFlags(
                crisis_detected=True,
                recommend_immediate="Please reach out to a crisis helpline: 988 (US)"
            )
    
    return SafetyFlags()

def relationship_decoder(input_text: str, depth: str = "deep") -> RelationshipAnalysis:
    """
    Main function: Analyze a relationship situation.
    
    Args:
        input_text: Description of the situation
        depth: "surface" | "deep" | "full"
    
    Returns:
        RelationshipAnalysis: Structured interpretation
    """
    # Step 1: Safety check
    safety_flags = check_safety(input_text)
    
    # Step 2: Get Vecta prediction
    prediction = mock_vecta_predict(input_text)
    
    # Step 3: Extract patterns
    patterns = extract_patterns(prediction)
    
    # Step 4: Generate interpretations
    interpretations = generate_interpretations(patterns, depth)
    
    # Step 5: Build response
    return RelationshipAnalysis(
        input_text=input_text,
        surface_pattern=patterns["surface"],
        surface_emotion=patterns["emotion"],
        primary_interpretation=interpretations["primary"],
        secondary_interpretations=interpretations["secondary"],
        excluded_interpretations=interpretations["excluded"],
        safety_flags=safety_flags,
        confidence_metrics={
            "overall": 0.72,
            "surface_pattern": 0.95,
            "interpretation": 0.65,
            "recommendations": 0.55
        }
    )

def print_analysis(analysis: RelationshipAnalysis):
    """Pretty print the analysis results."""
    print("\n" + "=" * 60)
    print("VECTA RELATIONSHIP DECODER")
    print("=" * 60)
    
    print(f"\n📥 INPUT:")
    print(f"   \"{analysis.input_text}\"")
    
    print(f"\n🔍 PATTERN DETECTED:")
    print(f"   {analysis.surface_pattern}")
    print(f"   Emotion: {analysis.surface_emotion}")
    
    print(f"\n🎯 PRIMARY INTERPRETATION:")
    p = analysis.primary_interpretation
    print(f"   Confidence: {p.confidence:.0%}")
    print(f"   Pattern: {p.pattern}")
    print(f"   Meaning: {p.meaning}")
    if p.framework:
        print(f"   Framework: {p.framework}")
    if p.explanation:
        print(f"   Explanation: {p.explanation}")
    
    if analysis.secondary_interpretations:
        print(f"\n📊 SECONDARY INTERPRETATIONS:")
        for i, s in enumerate(analysis.secondary_interpretations, 1):
            print(f"   {i}. [{s.confidence:.0%}] {s.pattern}")
            print(f"      {s.meaning}")
    
    if analysis.excluded_interpretations:
        print(f"\n❌ EXCLUDED (Vecta says NO):")
        for e in analysis.excluded_interpretations:
            print(f"   • {e}")
    
    print(f"\n📈 CONFIDENCE METRICS:")
    for k, v in analysis.confidence_metrics.items():
        print(f"   {k}: {v:.0%}")
    
    if analysis.safety_flags.crisis_detected:
        print(f"\n⚠️  SAFETY: CRISIS DETECTED")
        print(f"   {analysis.safety_flags.recommend_immediate}")
    
    print("\n" + "=" * 60)

def interactive_mode():
    """Run in interactive mode."""
    print("\n🔮 Vecta Relationship Decoder — Interactive Mode")
    print("Type your situation (or 'quit' to exit)\n")
    
    while True:
        try:
            user_input = input("📝 Your situation: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            analysis = relationship_decoder(user_input)
            print_analysis(analysis)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break

def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--interactive" or sys.argv[1] == "-i":
            interactive_mode()
        else:
            # Single query mode
            user_input = " ".join(sys.argv[1:])
            analysis = relationship_decoder(user_input)
            print_analysis(analysis)
    else:
        # Default: run hero example
        hero_example = "My boss always says 'we should revisit this' but nothing ever changes"
        print(f"🎯 Running hero example...")
        print(f"   \"{hero_example}\"\n")
        analysis = relationship_decoder(hero_example)
        print_analysis(analysis)

if __name__ == "__main__":
    main()
