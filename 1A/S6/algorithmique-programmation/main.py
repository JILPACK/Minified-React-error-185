"""Projet: Algorithmique et programmation
1AS6 - ENSEM NRJ (FISA)
Algorithmes de tri, recherche, structures de donnees, complexite"""

import time
import random
import math

class Tris:
    @staticmethod
    def bulle(arr):
        n = len(arr)
        arr = arr.copy()
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr

    @staticmethod
    def selection(arr):
        arr = arr.copy()
        n = len(arr)
        for i in range(n):
            min_idx = i
            for j in range(i+1, n):
                if arr[j] < arr[min_idx]:
                    min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        return arr

    @staticmethod
    def insertion(arr):
        arr = arr.copy()
        for i in range(1, len(arr)):
            key = arr[i]
            j = i-1
            while j >= 0 and arr[j] > key:
                arr[j+1] = arr[j]
                j -= 1
            arr[j+1] = key
        return arr

    @staticmethod
    def rapide(arr):
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr)//2]
        gauche = [x for x in arr if x < pivot]
        milieu = [x for x in arr if x == pivot]
        droite = [x for x in arr if x > pivot]
        return Tris.rapide(gauche) + milieu + Tris.rapide(droite)

class Recherche:
    @staticmethod
    def lineaire(arr, x):
        for i, v in enumerate(arr):
            if v == x:
                return i
        return -1

    @staticmethod
    def binaire(arr, x):
        g, d = 0, len(arr)-1
        while g <= d:
            m = (g+d)//2
            if arr[m] == x:
                return m
            elif arr[m] < x:
                g = m+1
            else:
                d = m-1
        return -1

class StructuresDonnees:
    class Pile:
        def __init__(self):
            self.elements = []
        def empiler(self, x):
            self.elements.append(x)
        def depiler(self):
            return self.elements.pop() if self.elements else None
        def est_vide(self):
            return len(self.elements) == 0

    class File:
        def __init__(self):
            self.elements = []
        def enfiler(self, x):
            self.elements.append(x)
        def defiler(self):
            return self.elements.pop(0) if self.elements else None

    class Noeud:
        def __init__(self, val):
            self.val = val
            self.gauche = None
            self.droite = None

    class ArbreBinaire:
        def __init__(self):
            self.racine = None

        def inserer(self, val):
            if not self.racine:
                self.racine = StructuresDonnees.Noeud(val)
                return
            cur = self.racine
            while True:
                if val < cur.val:
                    if cur.gauche:
                        cur = cur.gauche
                    else:
                        cur.gauche = StructuresDonnees.Noeud(val)
                        break
                else:
                    if cur.droite:
                        cur = cur.droite
                    else:
                        cur.droite = StructuresDonnees.Noeud(val)
                        break

        def parcours_infixe(self, noeud=None, res=None):
            if res is None: res = []
            if noeud is not None:
                self.parcours_infixe(noeud.gauche, res)
                res.append(noeud.val)
                self.parcours_infixe(noeud.droite, res)
            return res

class Complexite:
    @staticmethod
    def mesurer(fonction, arr):
        debut = time.time()
        resultat = fonction(arr)
        return time.time() - debut

def main():
    print("=" * 60)
    print("Algorithmique et programmation")
    print("1AS6 - ENSEM NRJ (FISA)")
    print("=" * 60)

    data = [64, 34, 25, 12, 22, 11, 90, 5, 78, 45]
    print(f"Tableau initial: {data}")

    print("\n--- 1. Algorithmes de tri ---")
    print(f"  Tri bulle:     {Tris.bulle(data)}")
    print(f"  Tri selection: {Tris.selection(data)}")
    print(f"  Tri insertion: {Tris.insertion(data)}")
    print(f"  Tri rapide:    {Tris.rapide(data)}")

    print("\n--- 2. Performance des tris (n=1000) ---")
    big = [random.randint(0, 10000) for _ in range(1000)]
    t_bulle = Complexite.mesurer(Tris.bulle, big)
    t_rapide = Complexite.mesurer(Tris.rapide, big)
    print(f"  Tri bulle:  {t_bulle*1000:.1f} ms")
    print(f"  Tri rapide: {t_rapide*1000:.1f} ms")

    print("\n--- 3. Algorithmes de recherche ---")
    trie = sorted(data)
    print(f"Tableau trie: {trie}")
    for x in [12, 99]:
        idx_l = Recherche.lineaire(trie, x)
        idx_b = Recherche.binaire(trie, x)
        print(f"  Recherche de {x}: lineaire={idx_l}, binaire={idx_b}")

    print("\n--- 4. Structures de donnees ---")
    pile = StructuresDonnees.Pile()
    for x in [1, 2, 3]:
        pile.empiler(x)
    print(f"  Pile (LIFO): empiler 1,2,3 -> depiler: {pile.depiler()}, {pile.depiler()}")

    file = StructuresDonnees.File()
    for x in [1, 2, 3]:
        file.enfiler(x)
    print(f"  File (FIFO): enfiler 1,2,3 -> defiler: {file.defiler()}, {file.defiler()}")

    print("\n--- 5. Arbre binaire de recherche ---")
    arbre = StructuresDonnees.ArbreBinaire()
    for v in [5, 3, 7, 2, 4, 8]:
        arbre.inserer(v)
    print(f"  Insertion: 5,3,7,2,4,8")
    print(f"  Parcours infixe: {arbre.parcours_infixe(arbre.racine)}")

    print("\n--- 6. Complexite algorithmique ---")
    tailles = [100, 500, 1000]
    for n in tailles:
        arr = [random.randint(0, 10000) for _ in range(n)]
        t_b = Complexite.mesurer(Tris.bulle, arr)
        t_r = Complexite.mesurer(Tris.rapide, arr)
        print(f"  n={n:5d}: bulle={t_b*1000:7.1f}ms, rapide={t_r*1000:5.1f}ms")

if __name__ == '__main__':
    main()
