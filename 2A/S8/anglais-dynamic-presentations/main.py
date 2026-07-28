"""Projet: Anglais - Dynamic Presentations
2AS8 - ENSEM NRJ (FISA)
Technical presentation skills for energy engineering"""

PRESENTATION_STRUCTURE = """
DYNAMIC PRESENTATION STRUCTURE
==============================
1. HOOK (30s) - Attention grabber
   - Startling statistic, question, or short story

2. CONTEXT (1 min) - Why this matters
   - Background, problem statement, stakes

3. MAIN CONTENT (3-4 min) - Core message
   - Technical explanation with visuals
   - Key data and results
   - 3 main points max

4. DEMONSTRATION (2 min) - Show, don't just tell
   - Live demo, simulation results, or case study

5. CONCLUSION (1 min) - Call to action
   - Summary, implications, next steps
   - Memorable closing statement

6. Q&A (2 min) - Handle questions confidently
"""

TOPICS_TECHNICAL = [
    "How a Combined Cycle Gas Turbine (CCGT) achieves 60%+ efficiency",
    "The role of Power Electronics in Smart Grid integration",
    "Battery Energy Storage Systems: grid-scale applications",
    "Condition Monitoring of rotating machinery using vibration analysis",
    "Power-to-Gas: converting renewable electricity to hydrogen",
    "High Voltage DC (HVDC) transmission for offshore wind farms",
    "Digital Twins for predictive maintenance in power plants",
]

EVALUATION_CRITERIA = """
EVALUATION RUBRIC
=================
Content (40%):
  - Technical accuracy and depth
  - Clear explanation of complex concepts
  - Relevant examples and data

Delivery (30%):
  - Eye contact and body language
  - Voice modulation and pacing
  - Minimal reading from slides

Visuals (20%):
  - Clear, uncluttered slides
  - Effective diagrams and graphs
  - Appropriate use of animations

Q&A Handling (10%):
  - Understanding of questions
  - Confident, concise answers
  - Honest about limitations
"""

def structure_presentation():
    print("PRESENTATION WORKSHOP - Dynamic Presentations")
    print("=" * 50)
    topic = "Smart Grids and Renewable Integration"
    print(f"\nPractice topic: {topic}")
    print(PRESENTATION_STRUCTURE)

def vocabulary_boost():
    print("\nPRESENTATION VOCABULARY")
    print("=" * 50)
    phrases = {
        "Opening": [
            "Let me start by asking you a question...",
            "Did you know that...",
            "The topic I'd like to discuss today is..."
        ],
        "Transitions": [
            "This brings me to my next point...",
            "Let's now turn to...",
            "Building on that idea..."
        ],
        "Visuals": [
            "As you can see from this graph...",
            "This diagram illustrates...",
            "The key takeaway here is..."
        ],
        "Closing": [
            "To sum up, we've seen that...",
            "In conclusion, I'd like to emphasize...",
            "Thank you for your attention. I'm happy to take questions."
        ]
    }
    for category, examples in phrases.items():
        print(f"\n{category}:")
        for ex in examples:
            print(f"  • {ex}")

def impromptu_speech():
    import random
    print("\nIMPROMPTU SPEECH PRACTICE")
    print("=" * 50)
    topics = [
        "Why energy efficiency is the 'first fuel'",
        "The future of nuclear power",
        "Electric vehicles vs hydrogen: which will win?",
        "The most important skill for an energy engineer",
        "How I would explain a power grid to a child"
    ]
    topic = random.choice(topics)
    print(f"Topic: {topic}")
    print("Time: 2 minutes (30s preparation)")
    print("Structure: Opinion → Reason → Example → Conclusion")

def peer_review_guide():
    print("\nPEER REVIEW GUIDE")
    print("=" * 50)
    print("For each presentation, note:")
    print("  1. What was the main message?")
    print("  2. What was the strongest part?")
    print("  3. What could be improved?")
    print("  4. Rate 1-5: Content / Delivery / Visuals")
    print(EVALUATION_CRITERIA)

def main():
    print("=" * 60)
    print("English - Dynamic Presentations")
    print("2AS8 - ENSEM NRJ (FISA)")
    print("=" * 60)

    structure_presentation()
    vocabulary_boost()
    impromptu_speech()
    peer_review_guide()

    print("\n" + "=" * 60)
    print("DELIVERABLES")
    print("=" * 60)
    print("1. 5-minute technical presentation (slides + demo)")
    print("2. Presentation script (500-700 words)")
    print("3. Peer review of 2 classmates")
    print("4. Self-assessment using rubric")

if __name__ == '__main__':
    main()
