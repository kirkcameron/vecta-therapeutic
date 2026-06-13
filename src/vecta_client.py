#!/usr/bin/env python3
"""
Vecta Client — Real integration with Vecta's CLI

Usage:
    from vecta_client import VectaClient
    client = VectaClient()
    result = client.predict("my boss always says we should revisit this")
"""

import os
import subprocess
import re
from dataclasses import dataclass

@dataclass
class VectaSignal:
    word: str
    score: int

@dataclass
class VectaPrediction:
    query: str
    present: list  # list of (word, score)
    absent: list   # list of (word, score)
    raw: str

class VectaClient:
    """Client for Vecta CLI"""
    
    VECTA_PATH = os.environ.get("VECTA_PATH", "~/GIT/business/erlang/vecta/vecta")
    
    def predict(self, query: str) -> VectaPrediction:
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
            raise Exception(f"Vecta not found at {vecta_cmd}. Set VECTA_PATH or install from: https://github.com/kirkcameron/vecta")
        
        return self._parse(query, output)
    
    def _parse(self, query: str, output: str) -> VectaPrediction:
        """Parse Vecta's output format"""
        present = []
        absent = []
        
        # Format: WORD[score] or WORD[-score]
        for match in re.finditer(r'([A-Z_-]+)\[(-?\d+)\]', output):
            word = match.group(1)
            score = int(match.group(2))
            if score > 0:
                present.append((word, score))
            else:
                absent.append((word, score))
        
        return VectaPrediction(query=query, present=present, absent=absent, raw=output)


if __name__ == "__main__":
    # Demo
    client = VectaClient()
    
    query = "my boss always says we should revisit this"
    print(f"\n🔮 Vecta: '{query}'\n")
    
    try:
        pred = client.predict(query)
        print("📊 PRESENT SIGNALS:")
        for w, s in sorted(pred.present, key=lambda x: -x[1])[:15]:
            print(f"   {w}[{s}]")
        print("\n📊 ABSENT SIGNALS (excluded):")
        for w, s in sorted(pred.absent, key=lambda x: x[1])[:10]:
            print(f"   {w}[{s}]")
    except Exception as e:
        print(f"❌ {e}")
