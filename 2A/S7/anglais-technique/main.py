"""Projet: Anglais technique
2AS7 - ENSEM NRJ (FISA)
Technical vocabulary, reading comprehension, scientific writing"""

import random

TECHNICAL_VOCABULARY = {
    "Electrical Engineering": {
        "voltage": "Difference in electric potential",
        "current": "Flow of electric charge",
        "impedance": "Total opposition to AC current",
        "power factor": "Ratio of real to apparent power",
        "transformer": "Device for voltage conversion",
        "rectifier": "Converts AC to DC",
        "inverter": "Converts DC to AC",
        "harmonic": "Frequency multiple of fundamental",
        "grid": "Network for power distribution",
        "load flow": "Analysis of power system steady-state",
    },
    "Thermodynamics": {
        "enthalpy": "Total heat content of a system",
        "entropy": "Measure of disorder or randomness",
        "isentropic": "Reversible adiabatic process",
        "efficiency": "Ratio of useful output to input",
        "turbine": "Rotary engine extracting energy from fluid",
        "compressor": "Device that increases fluid pressure",
        "condenser": "Heat exchanger for condensation",
        "rankine cycle": "Steam power plant cycle",
        "cogeneration": "Simultaneous heat and power production",
    },
    "Fluid Mechanics": {
        "Reynolds number": "Ratio of inertial to viscous forces",
        "laminar flow": "Smooth, orderly fluid motion",
        "turbulent flow": "Chaotic, irregular fluid motion",
        "boundary layer": "Thin region near a surface",
        "Bernoulli": "Pressure-velocity relationship in flow",
        "head loss": "Pressure drop due to friction",
        "cavitation": "Vapor bubble formation in liquid",
        "NPSH": "Net Positive Suction Head",
        "hydraulic grade line": "Pressure head along a pipeline",
    },
    "Control Systems": {
        "feedback": "Output signal returned to input",
        "transfer function": "Input-output relationship in s-domain",
        "PID controller": "Proportional-Integral-Derivative control",
        "stability": "System's ability to return to equilibrium",
        "root locus": "Plot of pole locations vs gain",
        "Bode plot": "Frequency response magnitude/phase",
        "overshoot": "Exceeding the setpoint value",
        "steady-state error": "Difference after transients decay",
        "bandwidth": "Frequency range of effective response",
    },
}

COMPREHENSION_TEXTS = [
    {
        "title": "Smart Grids and Renewable Integration",
        "text": ("Smart grids are electrical networks that use digital technology to "
                 "monitor and manage the transport of electricity. They integrate "
                 "renewable energy sources, improve efficiency, and enable demand-side "
                 "management. The increasing penetration of intermittent sources like "
                 "wind and solar requires advanced forecasting, energy storage solutions, "
                 "and grid flexibility. Power electronics play a crucial role in converting "
                 "and controlling electricity from renewable sources to match grid requirements."),
        "questions": [
            "What is a smart grid?",
            "Why are energy storage solutions needed?",
            "What role do power electronics play?",
        ],
    },
    {
        "title": "Combined Cycle Gas Turbines",
        "text": ("A combined cycle gas turbine (CCGT) plant uses both a gas turbine and "
                 "a steam turbine to generate electricity. The gas turbine operates on the "
                 "Brayton cycle, while the steam turbine operates on the Rankine cycle using "
                 "waste heat from the gas turbine exhaust. This configuration can achieve "
                 "thermal efficiencies above 60%, significantly higher than conventional "
                 "power plants. The heat recovery steam generator (HRSG) is a critical "
                 "component that captures exhaust heat without supplementary firing."),
        "questions": [
            "What two cycles are combined in a CCGT?",
            "What efficiency can a CCGT achieve?",
            "What is the role of the HRSG?",
        ],
    },
]

def vocabulary_quiz():
    print("VOCABULARY QUIZ")
    print("-" * 40)
    domain = random.choice(list(TECHNICAL_VOCABULARY.keys()))
    term, definition = random.choice(list(TECHNICAL_VOCABULARY[domain].items()))
    print(f"Domain: {domain}")
    options = [definition]
    others = [d for d_list in TECHNICAL_VOCABULARY.values() for d in d_list.values()]
    others = [d for d in others if d != definition]
    options.extend(random.sample(others, min(3, len(others))))
    random.shuffle(options)
    print(f"Term: '{term}'")
    print("Choose the correct definition:")
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")

def reading_comprehension():
    print("READING COMPREHENSION")
    print("-" * 40)
    passage = random.choice(COMPREHENSION_TEXTS)
    print(f"\nTitle: {passage['title']}")
    print(f"\n{passage['text']}\n")
    print("Questions:")
    for i, q in enumerate(passage['questions'], 1):
        print(f"  {i}. {q}")

def technical_writing():
    print("TECHNICAL WRITING TIPS")
    print("-" * 40)
    tips = [
        "Use passive voice for procedures: 'The valve is opened...'",
        "Define acronyms on first use: 'Heat Recovery Steam Generator (HRSG)'",
        "Use present tense for facts: 'The system operates at 50 Hz'",
        "Write short, clear sentences (15-20 words max)",
        "Use bullet points for lists and specifications",
        "Include units for all measurements",
        "Label all figures and tables with captions",
    ]
    for tip in tips:
        print(f"  * {tip}")

    print("\nEXAMPLE SENTENCES:")
    examples = [
        "The efficiency of the proposed system is 47.3%.",
        "Figure 2 shows the temperature profile along the heat exchanger.",
        "The PID controller was tuned using the Ziegler-Nichols method.",
        "A 10% increase in pressure results in a 3.2% efficiency gain.",
        "All measurements were recorded at steady-state conditions.",
    ]
    for ex in examples:
        print(f"  - {ex}")

def main():
    print("=" * 60)
    print("Anglais technique")
    print("2AS7 - ENSEM NRJ (FISA)")
    print("=" * 60)

    print("\n--- 1. Vocabulary domains ---")
    for domain, terms in TECHNICAL_VOCABULARY.items():
        sample = random.sample(list(terms.keys()), min(5, len(terms)))
        print(f"\n{domain}:")
        for term in sample:
            print(f"  - {term}: {terms[term]}")

    print("\n--- 2. Vocabulary quiz ---")
    print()
    vocabulary_quiz()

    print("\n\n--- 3. Reading comprehension ---")
    print()
    reading_comprehension()

    print("\n--- 4. Technical writing ---")
    print()
    technical_writing()

    print("\n" + "=" * 60)
    print("DELIVERABLES")
    print("=" * 60)
    print("1. Domain-specific vocabulary list (20 terms)")
    print("2. Reading summary (150 words)")
    print("3. Technical description (200 words)")
    print("4. Oral presentation on energy topic")

if __name__ == '__main__':
    main()
