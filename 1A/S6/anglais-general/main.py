"""Projet: Anglais general
1AS6 - ENSEM NRJ (FISA)
Grammar, vocabulary, reading comprehension, writing skills"""

import random

GRAMMAR_RULES = {
    "Present Simple": "Used for habits, facts: 'The system operates at 50 Hz.'",
    "Present Continuous": "Used for ongoing actions: 'The turbine is rotating.'",
    "Present Perfect": "Used for past actions with present relevance: 'The voltage has dropped.'",
    "Past Simple": "Used for completed past actions: 'The test finished at 3 PM.'",
    "Passive Voice": "Used when the action is more important: 'The valve was opened.'",
    "Conditionals": "Type 0/1/2/3 for different probability levels.",
    "Modals": "can, could, may, might, must, should for ability/permission/obligation.",
}

TECHNICAL_VOCAB_S6 = {
    "Energy": ["power", "energy", "efficiency", "consumption", "generation"],
    "Electricity": ["voltage", "current", "resistance", "circuit", "frequency"],
    "Materials": ["strength", "stress", "strain", "elasticity", "hardness"],
    "Measurement": ["accuracy", "precision", "calibration", "tolerance", "range"],
}

def grammar_exercise():
    print("GRAMMAR EXERCISES")
    print("-" * 40)
    print("\nChoose the correct form:")
    exercises = [
        ("The turbine ______ at 3000 rpm.", ["rotate", "rotates", "is rotating"]),
        ("The voltage ______ by the transformer.", ["steps up", "is stepped up", "stepping up"]),
        ("If the pressure ______ too high, the valve opens.", ["will rise", "rises", "would rise"]),
        ("The engineer ______ the measurements yesterday.", ["takes", "has taken", "took"]),
        ("You ______ wear safety glasses in the lab.", ["must", "can", "might"]),
    ]
    for i, (sentence, options) in enumerate(exercises, 1):
        print(f"  {i}. {sentence}")
        for j, opt in enumerate(options, 1):
            print(f"     {j}. {opt}")

def vocabulary_builder():
    print("\nTECHNICAL VOCABULARY - Domains")
    print("-" * 40)
    for domain, words in TECHNICAL_VOCAB_S6.items():
        print(f"\n  {domain}:")
        for word in words:
            print(f"    - {word}")

def reading_comprehension():
    print("\nREADING COMPREHENSION")
    print("-" * 40)
    texts = [
        {
            "title": "Electrical Power Systems",
            "text": "An electrical power system consists of generation, transmission, and distribution. Power plants generate electricity at medium voltage. Transformers step up the voltage for efficient long-distance transmission. At substations, the voltage is stepped down for distribution to consumers. The frequency is maintained at 50 Hz in Europe. Power systems must balance supply and demand in real time.",
            "questions": [
                "What are the three main parts of a power system?",
                "Why is voltage stepped up for transmission?",
                "What frequency is used in Europe?",
            ]
        },
        {
            "title": "Renewable Energy Sources",
            "text": "Renewable energy comes from natural sources that are constantly replenished. Solar energy is captured by photovoltaic panels. Wind turbines convert kinetic energy from the wind into electricity. Hydropower uses the energy of moving water. Each source has advantages and limitations. Solar and wind are intermittent, while hydropower can provide consistent baseload power.",
            "questions": [
                "What are three types of renewable energy mentioned?",
                "What is the main limitation of solar and wind?",
                "Why is hydropower considered reliable?",
            ]
        },
    ]
    passage = random.choice(texts)
    print(f"\nTitle: {passage['title']}")
    print(f"\n{passage['text']}\n")
    for i, q in enumerate(passage['questions'], 1):
        print(f"  Q{i}: {q}")

def writing_prompts():
    print("\nWRITING PRACTICE")
    print("-" * 40)
    prompts = [
        "Describe a simple electrical circuit (100 words). Use passive voice.",
        "Explain how a transformer works. Use present simple.",
        "Write a safety instruction for a laboratory. Use modals (must, should).",
        "Summarize the advantages of renewable energy (150 words).",
    ]
    for i, prompt in enumerate(prompts, 1):
        print(f"  {i}. {prompt}")

def communication_phrases():
    print("\nUSEFUL PHRASES")
    print("-" * 40)
    phrases = {
        "Asking for clarification": [
            "Could you explain that again?",
            "What do you mean by...?",
            "I'm not sure I follow.",
        ],
        "Expressing agreement": [
            "I agree with you.",
            "That's a good point.",
            "You're absolutely right.",
        ],
        "Expressing disagreement": [
            "I see it differently.",
            "I'm not sure I agree.",
            "That's one way to look at it, but...",
        ],
        "Making suggestions": [
            "What if we tried...?",
            "I suggest that we...",
            "One option would be to...",
        ],
    }
    for category, examples in phrases.items():
        print(f"\n  {category}:")
        for ex in examples:
            print(f"    - {ex}")

def main():
    print("=" * 60)
    print("Anglais general")
    print("1AS6 - ENSEM NRJ (FISA)")
    print("=" * 60)

    print("\n--- 1. Grammar review ---")
    for rule, desc in GRAMMAR_RULES.items():
        print(f"  {rule}: {desc}")

    print()
    grammar_exercise()
    vocabulary_builder()
    reading_comprehension()
    writing_prompts()
    communication_phrases()

    print("\n" + "=" * 60)
    print("DELIVERABLES")
    print("=" * 60)
    print("1. Grammar exercises (10 sentences)")
    print("2. Vocabulary list (20 technical terms)")
    print("3. Reading summary (150 words)")
    print("4. Short technical description (200 words)")
    print("5. Oral presentation (5 min)")

if __name__ == '__main__':
    main()
