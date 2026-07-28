"""Projet: Informatique 1
1AS5 - ENSEM NRJ (FISA)
Introduction a la programmation Python, variables, boucles, fonctions"""

import math
import random

def afficher_bienvenue():
    print("Bienvenue dans le module Informatique 1")
    print("Introduction a la programmation avec Python")

class VariablesTypes:
    @staticmethod
    def decrire(variable):
        return type(variable).__name__

    @staticmethod
    def conversions():
        return [
            ("entier -> float", float(42)),
            ("float -> entier", int(3.14)),
            ("nombre -> str", str(123)),
            ("str -> nombre", int("456")),
        ]

class StructuresControle:
    @staticmethod
    def parite(n):
        return "pair" if n % 2 == 0 else "impair"

    @staticmethod
    def note_lettre(note):
        if note >= 16: return 'A'
        elif note >= 14: return 'B'
        elif note >= 12: return 'C'
        elif note >= 10: return 'D'
        else: return 'E'

    @staticmethod
    def est_premier(n):
        if n < 2: return False
        for i in range(2, int(math.sqrt(n))+1):
            if n % i == 0:
                return False
        return True

class FonctionsUtilisateur:
    @staticmethod
    def factorielle(n):
        if n <= 1: return 1
        return n * FonctionsUtilisateur.factorielle(n-1)

    @staticmethod
    def fibonacci(n):
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a+b
        return a

    @staticmethod
    def somme_liste(lst):
        s = 0
        for x in lst:
            s += x
        return s

class ManipulationListes:
    @staticmethod
    def max_liste(lst):
        m = lst[0]
        for x in lst[1:]:
            if x > m: m = x
        return m

    @staticmethod
    def moyenne(lst):
        return sum(lst) / len(lst) if lst else 0

    @staticmethod
    def filtrer_pairs(lst):
        return [x for x in lst if x % 2 == 0]

class ChainesCaracteres:
    @staticmethod
    def palindrome(mot):
        mot = mot.lower()
        return mot == mot[::-1]

    @staticmethod
    def compter_voyelles(mot):
        return sum(1 for c in mot.lower() if c in 'aeiouy')

def main():
    print("=" * 60)
    print("Informatique 1 - Introduction a la programmation")
    print("1AS5 - ENSEM NRJ (FISA)")
    print("=" * 60)

    afficher_bienvenue()

    print("\n--- 1. Variables et types ---")
    vt = VariablesTypes()
    for val in [42, 3.14, "hello", True, [1,2,3]]:
        print(f"  {repr(val):<15} type: {vt.decrire(val)}")
    print("\n  Conversions:")
    for desc, res in vt.conversions():
        print(f"    {desc}: {res} ({type(res).__name__})")

    print("\n--- 2. Structures de controle ---")
    sc = StructuresControle()
    for n in [7, 12, 23, 42]:
        print(f"  {n}: {sc.parite(n)}, premier={sc.est_premier(n)}")
    for note in [8, 11, 13, 16, 19]:
        print(f"  Note {note}: {sc.note_lettre(note)}")

    print("\n--- 3. Fonctions ---")
    fu = FonctionsUtilisateur()
    for n in [5, 10]:
        print(f"  factorielle({n}) = {fu.factorielle(n)}")
    for n in [5, 10, 20]:
        print(f"  fibonacci({n}) = {fu.fibonacci(n)}")
    lst = [3, 7, 2, 9, 1, 8]
    print(f"  somme({lst}) = {fu.somme_liste(lst)}")

    print("\n--- 4. Listes ---")
    ml = ManipulationListes()
    notes = [12, 15, 8, 19, 10, 14, 17]
    print(f"  Notes: {notes}")
    print(f"  Max: {ml.max_liste(notes)}")
    print(f"  Moyenne: {ml.moyenne(notes):.1f}")
    print(f"  Notes paires: {ml.filtrer_pairs(notes)}")

    print("\n--- 5. Chaines de caracteres ---")
    cc = ChainesCaracteres()
    for mot in ["radar", "python", "level", "hello"]:
        print(f"  '{mot}': palindrome={cc.palindrome(mot)}, voyelles={cc.compter_voyelles(mot)}")

    print("\n--- 6. Exercice synthese - Analyse de donnees ---")
    data = [random.randint(1, 100) for _ in range(20)]
    print(f"  Donnees ({len(data)}): {data}")
    print(f"  Max: {max(data)}, Min: {min(data)}")
    print(f"  Somme: {sum(data)}, Moyenne: {sum(data)/len(data):.1f}")
    print(f"  Pairs: {[x for x in data if x%2==0]}")

if __name__ == '__main__':
    main()
