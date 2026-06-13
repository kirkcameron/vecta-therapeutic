#!/usr/bin/env python3
"""
Vecta Client: Personal Knowledge Encoding System

Usage:
    from vecta_client import VectaClient
    
    vc = VectaClient()
    vc.think("Kirk lives in Hamburg")
    facts = vc.predict("KIRK")
    print(facts)
"""

import subprocess
import re
from typing import Optional


class VectaClient:
    """Client for Vecta associative memory system."""
    
    def __init__(self, vecta_path: str = None):
        """
        Initialize Vecta client.
        
        Args:
            vecta_path: Path to vecta.sh. Defaults to ~/GIT/business/erlang/vecta/vecta.sh
        """
        self.vecta_path = vecta_path or "/Users/kraemere/GIT/business/erlang/vecta/vecta.sh"
    
    def _run(self, command: str) -> str:
        """Run vecta command and return output."""
        try:
            result = subprocess.run(
                [self.vecta_path] + command.split(),
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            raise TimeoutError("Vecta command timed out")
        except FileNotFoundError:
            raise FileNotFoundError(f"Vecta not found at {self.vecta_path}")
    
    def think(self, text: str) -> str:
        """
        Train: Encode facts into memory.
        
        Args:
            text: Text to encode into Vecta memory
            
        Returns:
            XOR hash result
            
        Example:
            >>> vc.think("The moon is made of cheese")
            '1234567890...'
        """
        # Wrap text in quotes if it contains spaces
        if ' ' in text:
            result = self._run(f'think "{text}"')
        else:
            result = self._run(f"think {text}")
        
        # Extract hash from output (format: "= 123456789...")
        match = re.search(r'=\s*(\d+)', result)
        if match:
            return match.group(1)
        return result.strip()
    
    def predict(self, query: str) -> dict:
        """
        Query: Retrieve facts from memory.
        
        Args:
            query: Word/concept to query
            
        Returns:
            Dict with 'concepts' (list of [word, score]) and 'raw' (raw output)
            
        Example:
            >>> vc.predict("MOON")
            {
                'concepts': [['CHEESE', 2], ['IS', 180], ...],
                'raw': '...'
            }
        """
        result = self._run(f"predict {query.upper()}")
        
        concepts = []
        # Parse @ section for concepts
        # Format: [CONCEPT[score], ...]
        match = re.search(r'\[IN\]\s*\|.*?\n(.*?)(?:\[SIMILAR\]|$)', result, re.DOTALL)
        if match:
            in_section = match.group(1)
            # Find all CONCEPT[number] patterns
            for concept_match in re.finditer(r'([A-Z0-9ÄÖÜß]+)\[(\d+)\]', in_section):
                word = concept_match.group(1)
                score = int(concept_match.group(2))
                concepts.append([word, score])
        
        return {
            'query': query.upper(),
            'concepts': concepts,
            'count': len(concepts),
            'raw': result
        }
    
    def predict_top(self, query: str, n: int = 10) -> list:
        """
        Query and return top N facts.
        
        Args:
            query: Word/concept to query
            n: Number of top facts to return
            
        Returns:
            List of [word, score] tuples, sorted by score (low = strong)
        """
        result = self.predict(query)
        # Sort by score (low = strong encoding)
        sorted_concepts = sorted(result['concepts'], key=lambda x: x[1])
        return sorted_concepts[:n]
    
    def learn(self, word: str) -> str:
        """
        Learn a single concept/word.
        
        Args:
            word: Word to learn
            
        Returns:
            'ok' on success
        """
        return self._run(f"learn {word}").strip()
    
    def reset(self) -> str:
        """
        Reset Vecta memory.
        
        Returns:
            'reset' on success
        """
        return self._run("reset").strip()
    
    def status(self) -> dict:
        """
        Get Vecta status.
        
        Returns:
            Status dict
        """
        result = self._run("status")
        return {'raw': result}


def demo():
    """Demo of Vecta client."""
    print("=== Vecta Client Demo ===\n")
    
    vc = VectaClient()
    
    # Demo training
    print("Training: 'The moon is made of cheese'")
    hash_result = vc.think("The moon is made of cheese")
    print(f"  Hash: {hash_result}\n")
    
    # Demo query
    print("Querying: MOON")
    facts = vc.predict("MOON")
    print(f"  Found {facts['count']} concepts:")
    for word, score in facts['predict_top'](10) if hasattr(facts, 'predict_top') else facts['concepts'][:10]:
        print(f"    {word}: {score}")


if __name__ == "__main__":
    demo()
