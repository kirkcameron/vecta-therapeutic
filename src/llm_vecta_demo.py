#!/usr/bin/env python3
"""
Vecta Memory Query Demo

Query Vecta's associative memory.

Usage:
    python llm_vecta_demo.py
    
    > gravity
    > einstein
    > mass
    > quantum
"""

from vecta_client import VectaClient


def main():
    """Interactive Vecta query demo."""
    print("=== Vecta Memory Query ===\n")
    print("Query the trained associative memory")
    print("Type 'quit' to exit\n")
    
    vecta = VectaClient()
    
    while True:
        query = input("Query: ").strip().upper()
        if query.lower() in ['quit', 'exit', 'q']:
            break
        if not query:
            continue
        
        try:
            result = vecta.predict(query)
            print(f"\nFacts for '{query}' (top 15):\n")
            for word, score in result['concepts'][:15]:
                if score <= 100:
                    print(f"  {word}: [{score}]")
            print()
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
