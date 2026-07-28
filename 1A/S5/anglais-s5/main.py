"""Projet: Anglais S5
1AS5 - ENSEM NRJ (FISA)
Remise a niveau, vocabulaire de base, grammaire fondamentale"""

GRAMMAR_BASICS = {
    "Verb to be": "I am, you are, he/she/it is, we are, they are",
    "Present Simple": "I work, he works (habits, facts)",
    "Articles": "a/an (indefinite), the (definite)",
    "Plurals": "book -> books, box -> boxes, baby -> babies",
    "Prepositions": "in, on, at, for, by, with, from, to",
    "Question words": "what, where, when, why, who, how",
    "Possessives": "my, your, his/her/its, our, their",
}

BASIC_VOCABULARY = {
    "Numbers": ["zero", "one", "two", "three", "four", "five", "ten", "hundred", "thousand"],
    "Colors": ["red", "blue", "green", "black", "white", "yellow"],
    "School": ["teacher", "student", "classroom", "lesson", "homework", "exam"],
    "Time": ["Monday", "Tuesday", "January", "February", "spring", "summer"],
    "Science basics": ["energy", "force", "power", "heat", "light", "motion"],
}

def verb_to_be_exercise():
    print("\nVERB TO BE - Complete:")
    print("  1. I ___ a student.")
    print("  2. She ___ an engineer.")
    print("  3. We ___ from France.")
    print("  4. They ___ in the classroom.")
    print("  5. He ___ twenty years old.")
    print("  (Answers: am, is, are, are, is)")

def vocabulary_lists():
    print("\nBASIC VOCABULARY")
    print("-" * 40)
    for category, words in BASIC_VOCABULARY.items():
        print(f"  {category}: {', '.join(words)}")

def numbers_exercise():
    print("\nNUMBERS PRACTICE")
    print("-" * 40)
    numbers = {
        1: "one", 2: "two", 3: "three", 10: "ten",
        15: "fifteen", 20: "twenty", 50: "fifty",
        100: "one hundred", 1000: "one thousand"
    }
    for num, word in numbers.items():
        print(f"  {num:5d} -> {word}")

def simple_questions():
    print("\nSIMPLE QUESTIONS")
    print("-" * 40)
    questions = [
        "What is your name?",
        "Where are you from?",
        "How old are you?",
        "What is your favorite subject?",
        "Why did you choose engineering?",
        "When is your birthday?",
        "Who is your role model?",
    ]
    for q in questions:
        print(f"  - {q}")

def reading_passage():
    print("\nREADING - My Daily Routine")
    print("-" * 40)
    text = """Every day, I wake up at 7 o'clock. I have breakfast and then I go to 
school. The lessons start at 8:30. I study mathematics, physics, and 
computer science. At noon, I have lunch with my friends. In the afternoon, 
I attend laboratory sessions. I go home at 5 PM. In the evening, I do my 
homework and review the lessons. I go to bed at 10:30."""
    print(f"\n{text}\n")
    print("Questions:")
    print("  1. What time does the person wake up?")
    print("  2. What subjects does the person study?")
    print("  3. What does the person do in the evening?")

def main():
    print("=" * 60)
    print("Anglais S5")
    print("1AS5 - ENSEM NRJ (FISA)")
    print("=" * 60)

    print("\n--- 1. Grammar basics ---")
    for rule, desc in GRAMMAR_BASICS.items():
        print(f"  {rule}: {desc}")

    verb_to_be_exercise()
    vocabulary_lists()
    numbers_exercise()
    simple_questions()
    reading_passage()

    print("\n--- DELIVERABLES ---")
    items = [
        "Complete grammar exercises (10 sentences)",
        "Learn vocabulary list (30 words)",
        "Write a short introduction (50 words)",
        "Read and summarize a short text",
    ]
    for i, item in enumerate(items, 1):
        print(f"  {i}. {item}")

if __name__ == '__main__':
    main()
