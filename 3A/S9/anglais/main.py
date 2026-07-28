"""Projet: Anglais - Interacting Professionally
3AS9 - ENSEM NRJ (FISA)
Technical English for Energy Engineering"""

PROJECT_TOPICS = [
    "Smart Grids and the Future of Electricity Distribution",
    "Nuclear Energy: Safety and Sustainability Challenges",
    "Offshore Wind Energy: Technological Innovations",
    "Hydrogen Economy: Production, Storage, and Applications",
    "Electric Vehicles: Battery Technology and Charging Infrastructure",
    "Energy Efficiency in Industrial Processes",
    "Carbon Capture and Storage (CCS) Technologies",
    "Internet of Things (IoT) for Energy Management",
    "Power Electronics in Renewable Energy Systems",
    "Condition Monitoring and Predictive Maintenance"
]

PRESENTATION_OUTLINE = """
TECHNICAL PRESENTATION OUTLINE
==============================
Topic: {topic}

1. Introduction (2-3 slides)
   - Context and motivation
   - Key challenges

2. Technical Background (3-4 slides)
   - Fundamental principles
   - Current state of the art

3. Case Study / Application (2-3 slides)
   - Real-world example
   - Technical specifications

4. Analysis and Discussion (2-3 slides)
   - Advantages and limitations
   - Comparison with alternatives

5. Conclusion (1-2 slides)
   - Key takeaways
   - Future perspectives
"""

VOCABULARY_ENERGY = {
    "Smart Grid": "An electricity network that uses digital technology to monitor and manage electricity transport",
    "Load Shedding": "Deliberate shutdown of electric power to avoid grid collapse",
    "Power Factor": "Ratio of real power to apparent power in an AC circuit",
    "Cogeneration": "Simultaneous production of electricity and heat from one fuel source",
    "Levelized Cost": "Average cost of electricity generation over a plant's lifetime",
    "Baseload": "Minimum amount of power that must be supplied to the grid at all times",
    "Inertia": "Resistance of rotating masses in generators to changes in frequency",
    "Harmonics": "Voltage or current components at multiples of the fundamental frequency",
    "Fault Ride-Through": "Ability of equipment to remain connected during grid disturbances",
    "State of Charge": "Available capacity of a battery expressed as a percentage of rated capacity"
}

def presentation_preparation():
    from random import choice
    topic = choice(PROJECT_TOPICS)
    print("TECHNICAL PRESENTATION - Preparation Guide")
    print("=" * 50)
    print(f"\nRecommended topic: {topic}")
    print(PRESENTATION_OUTLINE.format(topic=topic))
    return topic

def technical_writing_exercise():
    print("\nTECHNICAL WRITING - Abstract Exercise")
    print("=" * 50)
    print("Write a 150-200 word abstract on one of these topics:")
    for i, topic in enumerate(PROJECT_TOPICS[:5], 1):
        print(f"  {i}. {topic}")
    print("\nStructure: Background → Problem → Method → Results → Conclusion")

def vocabulary_quiz():
    print("\nTECHNICAL VOCABULARY QUIZ")
    print("=" * 50)
    score = 0
    terms = list(VOCABULARY_ENERGY.items())
    from random import sample
    for term, definition in sample(terms, 5):
        print(f"\nDefine: '{term}'")
        print(f"  Answer: {definition}")
    print("\nStudy these terms for the next session.")

def meeting_roleplay():
    print("\nPROFESSIONAL MEETING - Role Play Scenario")
    print("=" * 50)
    print("Scenario: Project Review Meeting - Renewable Energy Integration")
    print("\nRoles:")
    print("  1. Project Manager - Leads the meeting")
    print("  2. Technical Lead - Presents technical progress")
    print("  3. Financial Analyst - Reviews budget and timeline")
    print("  4. Client Representative - Asks questions")
    print("\nKey phrases to use:")
    print("  - 'Let's review the milestones...'")
    print("  - 'The main challenge we're facing is...'")
    print("  - 'According to our analysis...'")
    print("  - 'I'd like to suggest an alternative approach...'")
    print("  - 'Could you elaborate on that point?'")

def main():
    print("=" * 60)
    print("English - Interacting Professionally")
    print("3AS9 - ENSEM NRJ (FISA)")
    print("=" * 60)

    topic = presentation_preparation()
    technical_writing_exercise()
    vocabulary_quiz()
    meeting_roleplay()

    print("\n" + "=" * 60)
    print("DELIVERABLES")
    print("=" * 60)
    print("1. Technical presentation (10-12 slides) on: " + topic)
    print("2. Written abstract (150-200 words)")
    print("3. Technical glossary (20 terms with definitions)")
    print("4. Meeting simulation (15 min recorded)")

if __name__ == '__main__':
    main()
