import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import sys
import os
import io
import math
import random
import time
import webbrowser
import json as json_mod

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

SEMESTERS = [
    ("1AS5", "1A/S5", "1ère année - Semestre 5"),
    ("1AS6", "1A/S6", "1ère année - Semestre 6"),
    ("2AS7", "2A/S7", "2ème année - Semestre 7"),
    ("2AS8", "2A/S8", "2ème année - Semestre 8"),
    ("3AS9", "3A/S9", "3ème année - Semestre 9"),
    ("3AS10", "3A/S10", "3ème année - Semestre 10"),
]


# ─── Project Discovery ─────────────────────────────────────────────────

def discover_projects():
    projects = []
    for sid, rel_path, label in SEMESTERS:
        abs_path = os.path.join(ROOT, rel_path)
        if not os.path.isdir(abs_path):
            continue
        entries = sorted(os.listdir(abs_path))
        for entry in entries:
            entry_path = os.path.join(abs_path, entry)
            if not os.path.isdir(entry_path):
                continue
            main_py = os.path.join(entry_path, "main.py")
            if os.path.isfile(main_py):
                projects.append({
                    "semester_id": sid,
                    "semester_label": label,
                    "course": entry,
                    "path": entry_path,
                    "type": "python",
                    "file": main_py,
                })
            elif entry == "assembly-kernel-os":
                projects.append({
                    "semester_id": sid,
                    "semester_label": label,
                    "course": entry,
                    "path": entry_path,
                    "type": "asm",
                    "file": os.path.join(entry_path, "run.bat"),
                })
    return projects


def get_description(proj):
    desc_file = os.path.join(proj["path"], "main.py")
    if not os.path.isfile(desc_file):
        return ""
    try:
        with open(desc_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith('"""') or line.startswith("'''"):
                    parts = []
                    for inner in f:
                        inner_s = inner.strip()
                        if inner_s.endswith('"""') or inner_s.endswith("'''"):
                            parts.append(inner_s.rstrip('"').rstrip("'"))
                            break
                        parts.append(inner_s)
                    return " ".join(p.strip('" ').strip("' ") for p in parts).strip()
                if line and not line.startswith("#"):
                    break
    except Exception:
        pass
    return ""


# ─── FluxLang Integration ──────────────────────────────────────────────

def run_fluxlang(source):
    from fluxlang.lexer import Lexer, FluxLexerError
    from fluxlang.parser import Parser, ParseError
    from fluxlang.interpreter import Interpreter

    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    parser = Parser(tokens)
    ast = parser.parse()
    interp = Interpreter()

    output_lines = []

    def capture(v):
        s = str(v)
        if isinstance(v, bool):
            s = "true" if v else "false"
        elif v is None:
            s = "nil"
        elif isinstance(v, float):
            s = f"{v:.10f}".rstrip("0").rstrip(".")
            if s == "":
                s = "0"
        output_lines.append(s)

    interp._output = capture
    interp.interpret(ast)
    return "\n".join(output_lines)


# ─── FluxLang Example Programs ──────────────────────────────────────────

FLUXLANG_EXAMPLES = {
    "Hello World": """\
// Premier programme en FluxLang
print "Hello, FluxLang!";
print "Bienvenue dans le langage ENSEM NRJ";
""",
    "Variables & Maths": """\
// Variables et operations mathematiques
let x = 42;
let y = 3.14;
let nom = "Flux";
print x;
print y;
print "La reponse est:";
print x + y;
print sqrt(x);
print abs(-10);
print sin(3.14159 / 2);
""",
    "Conditions": """\
// Structures conditionnelles
let note = 15;

if note >= 16 {
    print "Excellent";
} else if note >= 14 {
    print "Tres bien";
} else if note >= 12 {
    print "Bien";
} else if note >= 10 {
    print "Passable";
} else {
    print "Insuffisant";
}

// Sans parentheses
let age = 20;
if age >= 18 {
    print "Majeur";
} else {
    print "Mineur";
}
""",
    "Boucles": """\
// Boucle while
let i = 0;
while i < 5 {
    print i;
    i = i + 1;
}

print "---";

// Boucle for (style C)
for (let j = 0; j < 5; j = j + 1) {
    print j * 2;
}

print "---";

// Listes
let nums = [10, 20, 30, 40, 50];
print len(nums);
print nums[0];
print nums[2];
""",
    "Fonctions": """\
// Fonctions et recursion
fun factorielle(n) {
    if n <= 1 {
        return 1;
    }
    return n * factorielle(n - 1);
}

fun fibonacci(n) {
    if n <= 1 {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

print "factorielle(5) =";
print factorielle(5);
print "fibonacci(10) =";
print fibonacci(10);

// Fonction sans return
fun saluer(nom) {
    print "Bonjour";
    print nom;
}
saluer("Alice");
""",
    "Simulation physique": """\
// Simulation de chute libre
let g = 9.81;
let h0 = 100;
let t = 0;
let dt = 0.5;

print "Chute libre depuis";
print h0;
print "metres:";

while t <= 5 {
    let h = h0 - 0.5 * g * t * t;
    if h < 0 {
        h = 0;
    }
    print t;
    print h;
    t = t + dt;
}

print "Impact au sol!";
""",
    "Analyse de notes": """\
// Analyse de notes etudiantes
let notes = [12, 15, 8, 19, 10, 14, 17, 6, 13, 11];

fun moyenne(liste) {
    let somme = 0;
    let i = 0;
    while i < len(liste) {
        somme = somme + liste[i];
        i = i + 1;
    }
    return somme / len(liste);
}

fun max(liste) {
    let m = liste[0];
    let i = 1;
    while i < len(liste) {
        if liste[i] > m {
            m = liste[i];
        }
        i = i + 1;
    }
    return m;
}

print "Notes:";
print notes;
print "Moyenne:";
print moyenne(notes);
print "Maximum:";
print max(notes);

// Compte les admis
let admis = 0;
let i = 0;
while i < len(notes) {
    if notes[i] >= 10 {
        admis = admis + 1;
    }
    i = i + 1;
}
print "Admis:";
print admis;
print "Taux de reussite:";
print (admis * 100) / len(notes);
""",
}


# ─── Visualizations ────────────────────────────────────────────────────

class SortingVisualization:
    """Animated bubble sort with step-by-step explanation."""

    def __init__(self, canvas):
        self.canvas = canvas
        self.array = []
        self.steps = []
        self.current_step = 0
        self.step_explanations = []
        self.running = False
        self.timer_id = None

    def generate(self, size=12):
        self.array = [random.randint(5, 95) for _ in range(size)]
        self.steps = []
        self.step_explanations = []
        self.current_step = 0
        arr = self.array.copy()
        n = len(arr)
        self.steps.append((arr.copy(), [], [], "État initial du tableau"))
        self.step_explanations.append(
            "On commence avec un tableau non trié. "
            "Le tri à bulles compare chaque paire d'éléments adjacents."
        )
        for i in range(n):
            swapped = False
            for j in range(n - i - 1):
                cmp = (arr.copy(), [j, j + 1], [], f"Comparaison de {arr[j]} et {arr[j + 1]}")
                self.steps.append((arr.copy(), [j, j + 1], [], f"Comparaison: arr[{j}]={arr[j]}, arr[{j+1}]={arr[j+1]}"))
                self.step_explanations.append(
                    f"On compare les éléments aux positions {j} et {j+1} : {arr[j]} et {arr[j+1]}."
                )
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swapped = True
                    self.steps.append((arr.copy(), [], [j, j + 1], f"Échange de {arr[j+1]} et {arr[j]}"))
                    self.step_explanations.append(
                        f"{arr[j+1]} > {arr[j]} ? Oui ! On échange les éléments aux positions {j} et {j+1}."
                    )
                else:
                    self.step_explanations.append(
                        f"{arr[j]} <= {arr[j+1]} ? Pas besoin d'échanger."
                    )
            if not swapped:
                self.steps.append((arr.copy(), [], list(range(n - i)), "Tri terminé !"))
                self.step_explanations.append(
                    "Aucun échange lors de ce passage : le tableau est déjà trié !"
                )
                break
            self.steps.append((arr.copy(), [], [n - i - 1], f"Élément {arr[n-i-1]} en place"))
            self.step_explanations.append(
                f"Le plus grand élément ({arr[n-i-1]}) a 'bulé' jusqu'à sa position finale."
            )
        self.steps.append((arr.copy(), [], list(range(n)), "✓ Tableau trié !"))
        self.step_explanations.append(
            "Le tableau est complètement trié en ordre croissant !"
        )
        self.draw_step(0)

    def draw_step(self, idx):
        self.canvas.delete("all")
        if idx >= len(self.steps):
            idx = len(self.steps) - 1
        arr, comparing, swapping, msg = self.steps[idx]
        w = self.canvas.winfo_width() or 600
        h = self.canvas.winfo_height() or 350
        n = len(arr)
        bar_w = min(40, (w - 40) // n)
        max_val = max(arr) if arr else 1
        self.canvas.create_text(w // 2, 20, text=msg, fill="#d4d4d4", font=("Consolas", 10))
        for i, val in enumerate(arr):
            x0 = 20 + i * bar_w
            bar_h = (val / max_val) * (h - 100)
            y0 = h - 40 - bar_h
            x1 = x0 + bar_w - 2
            y1 = h - 40
            color = "#4ec9b0"
            if i in comparing:
                color = "#dcdcaa"
            if i in swapping:
                color = "#f44747"
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="#1e1e1e")
            self.canvas.create_text((x0 + x1) // 2, y1 + 12, text=str(val), fill="#d4d4d4", font=("Consolas", 8))

    def next_step(self):
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.draw_step(self.current_step)
            return self.step_explanations[self.current_step] if self.current_step < len(self.step_explanations) else ""
        return ""

    def prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.draw_step(self.current_step)
            return self.step_explanations[self.current_step] if self.current_step < len(self.step_explanations) else ""
        return ""


class RecursionVisualization:
    """Animated recursion tree for fibonacci."""

    def __init__(self, canvas):
        self.canvas = canvas
        self.tree = {}
        self.current_nodes = []
        self.steps = []
        self.current_step = 0
        self.fib_calls = []
        self.explanations = []

    def generate(self, n=6):
        self.fib_calls = []
        self.explanations = []
        self.steps = []
        self.current_step = 0
        self._simulate_fib(n)
        self._build_steps()
        self.draw_step(0)

    def _simulate_fib(self, n):
        self._fib_trace(n, 0, [])

    def _fib_trace(self, n, depth, path):
        indent = "  " * depth
        self.fib_calls.append((depth, n, path))
        if n <= 1:
            return n
        left_path = path + [0]
        right_path = path + [1]
        left = self._fib_trace(n - 1, depth + 1, left_path)
        right = self._fib_trace(n - 2, depth + 1, right_path)
        return left + right

    def _build_steps(self):
        max_depth = max(d for d, _, _ in self.fib_calls) if self.fib_calls else 0
        step_map = {}
        for depth, n, path in self.fib_calls:
            key = tuple(path)
            if n <= 1:
                step_map[key] = f"fib({n}) = {n} (cas de base)"
            else:
                step_map[key] = f"fib({n}) = fib({n-1}) + fib({n-2})"
        visited = set()
        for depth, n, path in self.fib_calls:
            key = tuple(path)
            if key in visited:
                continue
            visited.add(key)
            text = f"fib({n})"
            if n <= 1:
                text += f" = {n} (base)"
            self.steps.append((depth, n, path, text))
            explanation = f"Appel fibonacci({n}). "
            if n <= 1:
                explanation += f"Cas de base atteint : retourne {n}."
            else:
                explanation += f"Décomposition en fib({n-1}) + fib({n-2})."
            self.explanations.append(explanation)
        self.steps.append((0, "done", [], "✓ Calcul terminé"))
        self.explanations.append("Tous les appels récursifs sont résolus !")

    def draw_step(self, idx):
        self.canvas.delete("all")
        if idx >= len(self.steps):
            idx = len(self.steps) - 1
        w = self.canvas.winfo_width() or 600
        h = self.canvas.winfo_height() or 350
        mx = w // 2
        depth, n, path, text = self.steps[idx]
        max_d = max(s[0] for s in self.steps[:-1]) if len(self.steps) > 1 else 1
        if isinstance(n, int):
            self.canvas.create_text(mx, 25, text=f"fibonacci({n})", fill="#569cd6",
                                    font=("Consolas", 14, "bold"))
            self.canvas.create_text(mx, 50, text=text, fill="#d4d4d4", font=("Consolas", 10))
        else:
            self.canvas.create_text(mx, 25, text="Terminé !", fill="#4ec9b0",
                                    font=("Consolas", 14, "bold"))
        self.canvas.create_text(mx, h - 20, text=f"Étape {idx + 1}/{len(self.steps)}",
                                fill="#808080", font=("Consolas", 9))
        self._draw_tree()
        self._highlight_path(path)

    def _draw_tree(self):
        w = self.canvas.winfo_width() or 600
        h = self.canvas.winfo_height() or 350
        self.canvas.create_text(w // 2, h - 55, text="Arbre d'appels récursifs (fibonacci)",
                                fill="#dcdcaa", font=("Consolas", 9, "italic"))
        for d, nn, p, _ in self.steps[:-1]:
            px, py = self._node_pos(p, w, h)
            for child_idx in [0, 1]:
                child_path = list(p) + [child_idx]
                for cd, cnn, cp, _ in self.steps[:-1]:
                    if list(cp) == child_path:
                        cx, cy = self._node_pos(cp, w, h)
                        self.canvas.create_line(px, py + 15, cx, cy - 15,
                                                fill="#404040", width=1)
                        break

    def _highlight_path(self, path):
        w = self.canvas.winfo_width() or 600
        h = self.canvas.winfo_height() or 350
        for idx in range(len(path) + 1):
            sub = path[:idx]
            px, py = self._node_pos(sub, w, h)
            for d, nn, p, _ in self.steps[:-1]:
                if list(p) == sub:
                    label = f"fib({nn})"
                    color = "#4ec9b0" if idx == len(path) else "#569cd6"
                    r = 25 - d * 3
                    self.canvas.create_oval(px - r, py - r, px + r, py + r,
                                            fill=color, outline="white", width=1)
                    self.canvas.create_text(px, py, text=label, fill="#1e1e1e",
                                            font=("Consolas", 8, "bold"))
                    break

    def _node_pos(self, path, w, h):
        depth = len(path)
        spread = max(30, 250 / (2 ** max(depth, 1)))
        x = w // 2 + sum((1 if p == 1 else -1) * spread / (2 ** i) for i, p in enumerate(path))
        y = 80 + depth * 50
        return x, y

    def next_step(self):
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.draw_step(self.current_step)
            return self.explanations[self.current_step] if self.current_step < len(self.explanations) else ""
        return ""

    def prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.draw_step(self.current_step)
            return self.explanations[self.current_step] if self.current_step < len(self.explanations) else ""
        return ""


class PhysicsVisualization:
    """Animated projectile motion with step-by-step explanation."""

    def __init__(self, canvas):
        self.canvas = canvas
        self.trajectory = []
        self.current_point = 0
        self.running = False
        self.timer_id = None
        self.explanations = []
        self.params = {}

    def generate(self, v0=30, angle_deg=45):
        self.canvas.delete("all")
        g = 9.81
        angle = math.radians(angle_deg)
        vx = v0 * math.cos(angle)
        vy0 = v0 * math.sin(angle)
        t_total = 2 * vy0 / g
        dt = 0.05
        t = 0
        self.trajectory = []
        self.explanations = []
        self.current_point = 0
        self.params = {"v0": v0, "angle": angle_deg, "vx": vx, "vy0": vy0, "g": g, "t_total": t_total}
        step = 0
        while t <= t_total + dt:
            x = vx * t
            y = vy0 * t - 0.5 * g * t * t
            self.trajectory.append((x, y, t))
            if step == 0:
                self.explanations.append(
                    f"Lancement : vitesse initiale V₀={v0} m/s à {angle_deg}°.\n"
                    f"Composantes : Vx = {vx:.1f} m/s, Vy₀ = {vy0:.1f} m/s"
                )
            elif abs(y - self.trajectory[step - 1][1]) > 1e-6:
                max_h = (vy0 ** 2) / (2 * g)
                if y >= max_h * 0.99:
                    self.explanations.append(
                        f"Point culminant ! t={t:.2f}s, hauteur max={y:.1f}m.\n"
                        f"Vy = 0 m/s, seule la composante horizontale Vx={vx:.1f} m/s agit."
                    )
                elif y < 0.5 and y >= 0:
                    self.explanations.append(
                        f"Impact au sol ! t={t:.2f}s. Portée = {x:.1f} m.\n"
                        f"Durée totale du vol : {t:.2f}s"
                    )
                else:
                    self.explanations.append(
                        f"t={t:.2f}s : x={x:.1f}m, y={y:.1f}m.\n"
                        f"La parabole décrit la trajectoire du projectile."
                    )
            else:
                step += 1
                t += dt
                continue
            step += 1
            t += dt
        self.explanations.append(
            "Le mouvement parabolique est la composition de deux mouvements :\n"
            "- Uniforme selon l'axe horizontal (Vx constant)\n"
            "- Uniformément accéléré selon l'axe vertical (due à la gravité)"
        )
        self.draw_step(0)

    def draw_step(self, idx):
        self.canvas.delete("all")
        if idx >= len(self.trajectory):
            idx = len(self.trajectory) - 1
        w = self.canvas.winfo_width() or 600
        h = self.canvas.winfo_height() or 400
        pad = 40
        plot_w = w - pad * 2
        plot_h = h - pad * 2
        if not self.trajectory:
            return
        xs = [p[0] for p in self.trajectory]
        ys = [p[1] for p in self.trajectory]
        max_x = max(xs) if xs else 1
        max_y = max(ys) if ys else 1
        # grid
        for i in range(6):
            gx = pad + (i / 5) * plot_w
            gy = pad + (i / 5) * plot_h
            self.canvas.create_line(gx, h - pad, gx, pad, fill="#2a2a2a")
            self.canvas.create_line(pad, gy, w - pad, gy, fill="#2a2a2a")
            val_x = int(i / 5 * max_x)
            val_y = int(i / 5 * max_y)
            self.canvas.create_text(gx, h - pad + 12, text=f"{val_x}", fill="#606060", font=("Consolas", 8))
            self.canvas.create_text(pad - 25, gy, text=f"{val_y}", fill="#606060", font=("Consolas", 8))
        # axis labels
        self.canvas.create_text(w // 2, h - 5, text="x (m)", fill="#808080", font=("Consolas", 9))
        self.canvas.create_text(12, pad + plot_h // 2, text="y (m)", fill="#808080", font=("Consolas", 9))
        # draw full trajectory
        px, py = None, None
        for x, y, _ in self.trajectory:
            sx = pad + (x / max_x) * plot_w
            sy = h - pad - (y / max_y) * plot_h
            if px is not None:
                self.canvas.create_line(px, py, sx, sy, fill="#569cd6", width=2)
            px, sy = sx, sy
            px, py = sx, sy
        # draw current point
        cx = pad + (self.trajectory[idx][0] / max_x) * plot_w
        cy = h - pad - (self.trajectory[idx][1] / max_y) * plot_h
        self.canvas.create_oval(cx - 5, cy - 5, cx + 5, cy + 5, fill="#f44747", outline="white")
        # info
        p = self.trajectory[idx]
        info = f"t={p[2]:.2f}s  x={p[0]:.1f}m  y={p[1]:.1f}m"
        self.canvas.create_text(w // 2, 18, text=info, fill="#d4d4d4", font=("Consolas", 11, "bold"))
        self.canvas.create_text(w // 2, h - pad + 28,
                                text=f"Étape {idx + 1}/{len(self.trajectory)}",
                                fill="#808080", font=("Consolas", 9))

    def next_step(self):
        if self.current_point < len(self.trajectory) - 1:
            self.current_point += 1
            self.draw_step(self.current_point)
            if self.current_point < len(self.explanations):
                return self.explanations[self.current_point]
        return ""

    def prev_step(self):
        if self.current_point > 0:
            self.current_point -= 1
            self.draw_step(self.current_point)
            if self.current_point < len(self.explanations):
                return self.explanations[self.current_point]
        return ""

    def auto_play(self, callback, interval=100):
        if self.current_point >= len(self.trajectory) - 1:
            self.current_point = 0
        self.running = True

        def _play():
            if not self.running:
                return
            if self.current_point < len(self.trajectory) - 1:
                self.current_point += 1
                self.draw_step(self.current_point)
                if self.current_point < len(self.explanations):
                    callback(self.explanations[self.current_point])
                self.timer_id = self.canvas.after(interval, _play)
            else:
                self.running = False
                callback("✓ Animation terminée !")

        _play()

    def stop(self):
        self.running = False
        if self.timer_id:
            self.canvas.after_cancel(self.timer_id)
            self.timer_id = None


# ─── FluxGUI Main Application ──────────────────────────────────────────

class FluxGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("FLUX - ENSEM NRJ (FISA)")
        self.root.geometry("1200x800")
        self.root.minsize(900, 600)

        style = ttk.Style()
        style.theme_use("clam" if "clam" in style.theme_names() else "default")
        style.configure("TNotebook", background="#252526")
        style.configure("TNotebook.Tab", background="#2d2d2d", foreground="#cccccc",
                        padding=[10, 4], font=("Segoe UI", 10))
        style.map("TNotebook.Tab", background=[("selected", "#1e1e1e")],
                  foreground=[("selected", "#ffffff")])

        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, padx=12, pady=(10, 2))
        ttk.Label(header_frame, text="⚡ FLUX", font=("Segoe UI", 20, "bold"),
                  foreground="#4ec9b0").pack(side=tk.LEFT)
        ttk.Label(header_frame, text="ENSEM NRJ (FISA) — Lanceur intelligent",
                  font=("Segoe UI", 10), foreground="#888888").pack(side=tk.LEFT, padx=12, pady=6)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=8, pady=(2, 8))

        self._build_projects_tab()
        self._build_fluxlang_tab()
        self._build_visuals_tab()
        self._build_worker_tab()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    # ── Tab 1: Projects ──────────────────────────────────────────────────

    def _build_projects_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=" Projets ")
        panes = ttk.PanedWindow(frame, orient=tk.HORIZONTAL)
        panes.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        left = ttk.Frame(panes, width=360)
        panes.add(left, weight=1)
        ttk.Label(left, text="Projets par semestre", font=("Segoe UI", 10, "bold"),
                  foreground="#cccccc").pack(anchor=tk.W, pady=(0, 4))
        tf = ttk.Frame(left)
        tf.pack(fill=tk.BOTH, expand=True)
        self.tree = ttk.Treeview(tf, columns=("sem",), selectmode="browse",
                                 show="tree headings", height=20)
        self.tree.heading("#0", text="Projet")
        self.tree.heading("sem", text="Semestre")
        self.tree.column("#0", width=240, minwidth=180)
        self.tree.column("sem", width=80, minwidth=60)
        ts = ttk.Scrollbar(tf, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=ts.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        ts.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.bind("<<TreeviewSelect>>", self._on_project_select)
        right = ttk.Frame(panes, width=600)
        panes.add(right, weight=2)
        ttk.Label(right, text="Sortie", font=("Segoe UI", 10, "bold"),
                  foreground="#cccccc").pack(anchor=tk.W, pady=(0, 4))
        of = ttk.Frame(right)
        of.pack(fill=tk.BOTH, expand=True)
        self.output = tk.Text(of, wrap=tk.WORD, font=("Consolas", 10),
                              bg="#1e1e1e", fg="#d4d4d4", insertbackground="white",
                              state=tk.DISABLED)
        os_ = ttk.Scrollbar(of, orient=tk.VERTICAL, command=self.output.yview)
        self.output.configure(yscrollcommand=os_.set)
        self.output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        os_.pack(side=tk.RIGHT, fill=tk.Y)
        self.output.tag_configure("green", foreground="#4ec9b0")
        self.output.tag_configure("yellow", foreground="#dcdcaa")
        self.output.tag_configure("red", foreground="#f44747")
        self.output.tag_configure("white", foreground="#d4d4d4")
        self.output.tag_configure("blue", foreground="#569cd6")
        bf = ttk.Frame(frame)
        bf.pack(fill=tk.X, padx=6, pady=(0, 6))
        self.p_status = tk.StringVar(value="Prêt")
        ttk.Label(bf, textvariable=self.p_status, font=("Segoe UI", 9),
                  foreground="#888888").pack(side=tk.LEFT)
        ttk.Button(bf, text="Effacer", command=self._clear_output).pack(side=tk.RIGHT, padx=(4, 0))
        self.p_run_btn = ttk.Button(bf, text="▶ Lancer", command=self._run_project)
        self.p_run_btn.pack(side=tk.RIGHT, padx=(4, 0))
        ttk.Button(bf, text="Description", command=self._show_description).pack(side=tk.RIGHT, padx=(4, 0))
        self.projects = discover_projects()
        self.selected_project = None
        self.p_running = False
        self._populate_tree()

    def _populate_tree(self):
        sem_nodes = {}
        for sid, _, slabel in SEMESTERS:
            node = self.tree.insert("", tk.END, iid=sid, text=slabel,
                                    open=True, values=(sid,))
            sem_nodes[sid] = node
        for p in self.projects:
            sid = p["semester_id"]
            parent = sem_nodes.get(sid)
            if parent:
                icon = "🐍" if p["type"] == "python" else "⚙"
                self.tree.insert(parent, tk.END,
                                 iid=p["course"] + "@" + sid,
                                 text=f"  {icon} {p['course']}",
                                 values=(sid,))

    def _on_project_select(self, event):
        sel = self.tree.selection()
        if not sel:
            self.selected_project = None
            return
        iid = sel[0]
        if "@" not in iid:
            self.selected_project = None
            return
        parts = iid.split("@")
        if len(parts) != 2:
            self.selected_project = None
            return
        course, sid = parts
        for p in self.projects:
            if p["course"] == course and p["semester_id"] == sid:
                self.selected_project = p
                return
        self.selected_project = None

    def _show_description(self):
        p = self.selected_project
        if not p:
            messagebox.showinfo("Info", "Sélectionnez un projet.")
            return
        desc = get_description(p)
        if desc:
            messagebox.showinfo(f"{p['semester_id']} / {p['course']}", desc)
        else:
            messagebox.showinfo(f"{p['semester_id']} / {p['course']}",
                                f"Chemin : {p['path']}\nType : {p['type']}")

    def _write_output(self, text, tag="white"):
        self.output.configure(state=tk.NORMAL)
        self.output.insert(tk.END, text, tag)
        self.output.see(tk.END)
        self.output.configure(state=tk.DISABLED)
        self.root.update_idletasks()

    def _clear_output(self):
        self.output.configure(state=tk.NORMAL)
        self.output.delete(1.0, tk.END)
        self.output.configure(state=tk.DISABLED)

    def _run_project(self):
        if self.p_running:
            return
        p = self.selected_project
        if not p:
            messagebox.showinfo("Info", "Sélectionnez un projet dans l'arbre.")
            return
        self.p_running = True
        self.p_run_btn.configure(state=tk.DISABLED)
        self._clear_output()
        self._write_output(f"▶ {p['semester_id']} / {p['course']}\n", "blue")
        desc = get_description(p)
        if desc:
            self._write_output(f"  {desc}\n", "yellow")
        self._write_output("─" * 70 + "\n", "white")
        self.p_status.set(f"Exécution : {p['course']}...")
        t = threading.Thread(target=self._run_thread, args=(p,), daemon=True)
        t.start()

    def _run_thread(self, p):
        try:
            if p["type"] == "python":
                env = os.environ.copy()
                env["PYTHONIOENCODING"] = "utf-8"
                proc = subprocess.Popen(
                    [sys.executable, "-u", "main.py"],
                    cwd=p["path"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    env=env, bufsize=1, text=True, encoding="utf-8", errors="replace",
                )
                for line in proc.stdout:
                    self.root.after(0, self._write_output, line)
                proc.wait()
                if proc.returncode != 0:
                    self.root.after(0, self._write_output,
                                    f"\n⚠ Code de retour : {proc.returncode}\n", "red")
                else:
                    self.root.after(0, self._write_output, "\n✅ Terminé\n", "green")
            elif p["type"] == "asm":
                run_bat = p.get("file", "")
                if os.path.isfile(run_bat):
                    self.root.after(0, self._write_output,
                                    "Lancement OS assembleur (QEMU)...\n", "yellow")
                    proc = subprocess.Popen(
                        ["cmd", "/c", "run.bat"], cwd=p["path"],
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                        bufsize=1, text=True, encoding="utf-8", errors="replace",
                    )
                    for line in proc.stdout:
                        self.root.after(0, self._write_output, line)
                    proc.wait()
                else:
                    self.root.after(0, self._write_output,
                                    "⚠ run.bat introuvable\n", "red")
        finally:
            self.root.after(0, self._project_done)

    def _project_done(self):
        self.p_running = False
        self.p_run_btn.configure(state=tk.NORMAL)
        self.p_status.set("Prêt")

    # ── Tab 2: FluxLang Playground ──────────────────────────────────────

    def _build_fluxlang_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="  FluxLang  ")

        panes = ttk.PanedWindow(frame, orient=tk.HORIZONTAL)
        panes.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        left = ttk.Frame(panes, width=500)
        panes.add(left, weight=1)

        topbar = ttk.Frame(left)
        topbar.pack(fill=tk.X)
        ttk.Label(topbar, text="Éditeur FluxLang", font=("Segoe UI", 10, "bold"),
                  foreground="#cccccc").pack(side=tk.LEFT)
        self.lang_example_var = tk.StringVar()
        ex_combo = ttk.Combobox(topbar, textvariable=self.lang_example_var,
                                values=list(FLUXLANG_EXAMPLES.keys()),
                                state="readonly", width=25)
        ex_combo.pack(side=tk.RIGHT)
        ex_combo.bind("<<ComboboxSelected>>", self._load_example)
        ttk.Label(topbar, text="Exemple :", foreground="#888888").pack(side=tk.RIGHT, padx=(0, 4))

        ef = ttk.Frame(left)
        ef.pack(fill=tk.BOTH, expand=True, pady=(4, 0))
        self.lang_editor = tk.Text(ef, wrap=tk.WORD, font=("Consolas", 11),
                                   bg="#1e1e1e", fg="#d4d4d4", insertbackground="white",
                                   relief=tk.FLAT, border=4, padx=8, pady=8)
        ed_scroll = ttk.Scrollbar(ef, orient=tk.VERTICAL, command=self.lang_editor.yview)
        self.lang_editor.configure(yscrollcommand=ed_scroll.set)
        self.lang_editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        ed_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.lang_editor.tag_configure("keyword", foreground="#569cd6")
        self.lang_editor.tag_configure("string", foreground="#ce9178")
        self.lang_editor.tag_configure("number", foreground="#b5cea8")
        self.lang_editor.tag_configure("comment", foreground="#6a9955")

        lang_bf = ttk.Frame(left)
        lang_bf.pack(fill=tk.X, pady=(4, 0))
        self.lang_status = tk.StringVar(value="Prêt")
        ttk.Label(lang_bf, textvariable=self.lang_status, foreground="#888888",
                  font=("Segoe UI", 9)).pack(side=tk.LEFT)
        ttk.Button(lang_bf, text="Tout effacer", command=lambda: self.lang_editor.delete(1.0, tk.END)
                   ).pack(side=tk.RIGHT, padx=(4, 0))
        self.lang_run_btn = ttk.Button(lang_bf, text="▶ Exécuter",
                                       command=self._run_fluxlang)
        self.lang_run_btn.pack(side=tk.RIGHT, padx=(4, 0))

        right = ttk.Frame(panes, width=500)
        panes.add(right, weight=1)

        ttk.Label(right, text="Sortie", font=("Segoe UI", 10, "bold"),
                  foreground="#cccccc").pack(anchor=tk.W)
        of = ttk.Frame(right)
        of.pack(fill=tk.BOTH, expand=True, pady=(4, 0))
        self.lang_output = tk.Text(of, wrap=tk.WORD, font=("Consolas", 11),
                                   bg="#0e0e0e", fg="#d4d4d4", state=tk.DISABLED)
        lo_scroll = ttk.Scrollbar(of, orient=tk.VERTICAL, command=self.lang_output.yview)
        self.lang_output.configure(yscrollcommand=lo_scroll.set)
        self.lang_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        lo_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.lang_output.tag_configure("out", foreground="#d4d4d4")
        self.lang_output.tag_configure("err", foreground="#f44747")

        # Load default example
        first_ex = list(FLUXLANG_EXAMPLES.keys())[0]
        self.lang_example_var.set(first_ex)
        self._load_example()

    def _load_example(self, event=None):
        name = self.lang_example_var.get()
        code = FLUXLANG_EXAMPLES.get(name, "")
        self.lang_editor.delete(1.0, tk.END)
        self.lang_editor.insert(1.0, code)

    def _run_fluxlang(self):
        if self.lang_status.get() == "Exécution...":
            return
        code = self.lang_editor.get(1.0, tk.END).strip()
        if not code:
            return
        self.lang_run_btn.configure(state=tk.DISABLED)
        self.lang_status.set("Exécution...")
        self.lang_output.configure(state=tk.NORMAL)
        self.lang_output.delete(1.0, tk.END)
        self.lang_output.configure(state=tk.DISABLED)
        t = threading.Thread(target=self._fluxlang_thread, args=(code,), daemon=True)
        t.start()

    def _fluxlang_thread(self, code):
        try:
            result = run_fluxlang(code)
            self.root.after(0, self._fluxlang_output, result, None)
        except Exception as e:
            self.root.after(0, self._fluxlang_output, None, str(e))

    def _fluxlang_output(self, result, error):
        self.lang_output.configure(state=tk.NORMAL)
        if error:
            self.lang_output.insert(1.0, f"⚠ Erreur :\n{error}", "err")
        else:
            self.lang_output.insert(1.0, result if result else "(aucune sortie)", "out")
        self.lang_output.configure(state=tk.DISABLED)
        self.lang_run_btn.configure(state=tk.NORMAL)
        self.lang_status.set("Prêt")

    # ── Tab 3: Visualizations ───────────────────────────────────────────

    def _build_visuals_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="  Animations  ")

        panes = ttk.PanedWindow(frame, orient=tk.HORIZONTAL)
        panes.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        left = ttk.Frame(panes, width=700)
        panes.add(left, weight=2)

        self.viz_notebook = ttk.Notebook(left)
        self.viz_notebook.pack(fill=tk.BOTH, expand=True)

        # Sort tab
        sort_f = ttk.Frame(self.viz_notebook)
        self.viz_notebook.add(sort_f, text=" Tri à bulles ")
        self.sort_canvas = tk.Canvas(sort_f, bg="#1e1e1e", highlightthickness=0)
        self.sort_canvas.pack(fill=tk.BOTH, expand=True)
        sort_bf = ttk.Frame(sort_f)
        sort_bf.pack(fill=tk.X, padx=4, pady=4)
        self.sort_explanation = tk.StringVar(value="Cliquez sur 'Générer' pour commencer")
        ttk.Label(sort_bf, textvariable=self.sort_explanation, foreground="#dcdcaa",
                  font=("Segoe UI", 9), wraplength=500).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(sort_bf, text="◀", width=3, command=self._sort_prev).pack(side=tk.RIGHT, padx=1)
        ttk.Button(sort_bf, text="▶", width=3, command=self._sort_next).pack(side=tk.RIGHT, padx=1)
        ttk.Button(sort_bf, text="Générer", command=self._sort_generate).pack(side=tk.RIGHT, padx=4)

        # Recursion tab
        rec_f = ttk.Frame(self.viz_notebook)
        self.viz_notebook.add(rec_f, text=" Récursion ")
        self.rec_canvas = tk.Canvas(rec_f, bg="#1e1e1e", highlightthickness=0)
        self.rec_canvas.pack(fill=tk.BOTH, expand=True)
        rec_bf = ttk.Frame(rec_f)
        rec_bf.pack(fill=tk.X, padx=4, pady=4)
        self.rec_explanation = tk.StringVar(value="Cliquez sur 'Générer' pour voir l'arbre d'appels")
        ttk.Label(rec_bf, textvariable=self.rec_explanation, foreground="#dcdcaa",
                  font=("Segoe UI", 9), wraplength=500).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(rec_bf, text="◀", width=3, command=self._rec_prev).pack(side=tk.RIGHT, padx=1)
        ttk.Button(rec_bf, text="▶", width=3, command=self._rec_next).pack(side=tk.RIGHT, padx=1)
        ttk.Button(rec_bf, text="Générer (n=6)", command=self._rec_generate).pack(side=tk.RIGHT, padx=4)

        # Physics tab
        phys_f = ttk.Frame(self.viz_notebook)
        self.viz_notebook.add(phys_f, text=" Physique ")
        self.phys_canvas = tk.Canvas(phys_f, bg="#1e1e1e", highlightthickness=0)
        self.phys_canvas.pack(fill=tk.BOTH, expand=True)
        phys_bf = ttk.Frame(phys_f)
        phys_bf.pack(fill=tk.X, padx=4, pady=4)
        self.phys_explanation = tk.StringVar(value="Cliquez sur 'Lancer' pour simuler un tir parabolique")
        ttk.Label(phys_bf, textvariable=self.phys_explanation, foreground="#dcdcaa",
                  font=("Segoe UI", 9), wraplength=500).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(phys_bf, text="◀", width=3, command=self._phys_prev).pack(side=tk.RIGHT, padx=1)
        ttk.Button(phys_bf, text="▶", width=3, command=self._phys_next).pack(side=tk.RIGHT, padx=1)
        ttk.Button(phys_bf, text="▶ Auto", command=self._phys_auto).pack(side=tk.RIGHT, padx=1)
        ttk.Button(phys_bf, text="Lancer 30m/s 45°", command=self._phys_generate).pack(side=tk.RIGHT, padx=4)

        # Right panel: explanation detail
        right = ttk.Frame(panes, width=350)
        panes.add(right, weight=1)
        ttk.Label(right, text="Explication pas à pas", font=("Segoe UI", 10, "bold"),
                  foreground="#cccccc").pack(anchor=tk.W)
        self.viz_explain = tk.Text(right, wrap=tk.WORD, font=("Segoe UI", 10),
                                   bg="#252526", fg="#d4d4d4", state=tk.DISABLED,
                                   relief=tk.FLAT, padx=6, pady=6)
        ve_scroll = ttk.Scrollbar(right, orient=tk.VERTICAL, command=self.viz_explain.yview)
        self.viz_explain.configure(yscrollcommand=ve_scroll.set)
        self.viz_explain.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        ve_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.viz_explain.tag_configure("title", foreground="#569cd6", font=("Segoe UI", 10, "bold"))
        self.viz_explain.tag_configure("body", foreground="#d4d4d4", font=("Segoe UI", 10))
        self.viz_explain.tag_configure("highlight", foreground="#dcdcaa", font=("Segoe UI", 10))
        self.viz_explain.tag_configure("green", foreground="#4ec9b0", font=("Segoe UI", 10))

        self.sort_viz = SortingVisualization(self.sort_canvas)
        self.rec_viz = RecursionVisualization(self.rec_canvas)
        self.phys_viz = PhysicsVisualization(self.phys_canvas)

        self.viz_notebook.bind("<<NotebookTabChanged>>", self._on_viz_tab_change)
        self._update_viz_explain("Choisissez une animation et cliquez sur Générer.")

    def _on_viz_tab_change(self, event=None):
        self._update_viz_explain("")

    def _update_viz_explain(self, text):
        self.viz_explain.configure(state=tk.NORMAL)
        self.viz_explain.delete(1.0, tk.END)
        if text:
            lines = text.split("\n")
            for i, line in enumerate(lines):
                tag = "body"
                if line.startswith("✓") or line.startswith("✅"):
                    tag = "green"
                elif line.startswith("•") or line.startswith("Lancement"):
                    tag = "title"
                self.viz_explain.insert(tk.END, line + "\n", tag)
        else:
            self.viz_explain.insert(tk.END,
                "Utilisez les boutons ◀ ▶ pour parcourir\n"
                "chaque étape de l'animation pas à pas.\n\n"
                "Chaque étape est expliquée en détail pour\n"
                "comprendre le concept en profondeur.",
                "body")
        self.viz_explain.configure(state=tk.DISABLED)

    # Sort callbacks
    def _sort_generate(self):
        self.sort_viz.generate(10)
        self._update_viz_explain(self.sort_viz.step_explanations[0])
        self.sort_explanation.set(self.sort_viz.step_explanations[0])

    def _sort_next(self):
        exp = self.sort_viz.next_step()
        if exp:
            self._update_viz_explain(exp)
            self.sort_explanation.set(exp)

    def _sort_prev(self):
        exp = self.sort_viz.prev_step()
        if exp:
            self._update_viz_explain(exp)
            self.sort_explanation.set(exp)

    # Recursion callbacks
    def _rec_generate(self):
        self.rec_viz.generate(6)
        self._update_viz_explain(self.rec_viz.explanations[0])
        self.rec_explanation.set(self.rec_viz.explanations[0])

    def _rec_next(self):
        exp = self.rec_viz.next_step()
        if exp:
            self._update_viz_explain(exp)
            self.rec_explanation.set(exp)

    def _rec_prev(self):
        exp = self.rec_viz.prev_step()
        if exp:
            self._update_viz_explain(exp)
            self.rec_explanation.set(exp)

    # Physics callbacks
    def _phys_generate(self):
        self.phys_viz.generate(30, 45)
        self.phys_viz.current_point = 0
        self.phys_viz.draw_step(0)
        if self.phys_viz.explanations:
            self._update_viz_explain(self.phys_viz.explanations[0])
            self.phys_explanation.set(self.phys_viz.explanations[0])

    def _phys_next(self):
        exp = self.phys_viz.next_step()
        if exp:
            self._update_viz_explain(exp)
            self.phys_explanation.set(exp)

    def _phys_prev(self):
        exp = self.phys_viz.prev_step()
        if exp:
            self._update_viz_explain(exp)
            self.phys_explanation.set(exp)

    def _phys_auto(self):
        self._update_viz_explain("▶ Lecture automatique...")
        self.phys_viz.auto_play(lambda t: (
            self._update_viz_explain(t),
            self.phys_explanation.set(t)
        ), 80)

    # ── Tab 4: Worker Mini ────────────────────────────────────────────────

    def _build_worker_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="  Worker IA  ")

        panes = ttk.PanedWindow(frame, orient=tk.HORIZONTAL)
        panes.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        left = ttk.Frame(panes, width=500)
        panes.add(left, weight=1)

        # Control bar
        ctrl = ttk.Frame(left)
        ctrl.pack(fill=tk.X)
        ttk.Label(ctrl, text="Ministral 3.3B — Worker IA", font=("Segoe UI", 10, "bold"),
                  foreground="#cccccc").pack(side=tk.LEFT)
        self.worker_status_lbl = ttk.Label(ctrl, text="🔴 Arrêté", foreground="#f44747",
                                           font=("Segoe UI", 9, "bold"))
        self.worker_status_lbl.pack(side=tk.RIGHT, padx=(8, 0))
        self.w_start_btn = ttk.Button(ctrl, text="▶ Lancer", command=self._worker_toggle)
        self.w_start_btn.pack(side=tk.RIGHT, padx=2)
        ttk.Button(ctrl, text="🔄 Health", command=self._worker_health).pack(side=tk.RIGHT, padx=2)

        # Chat area
        chat_label = ttk.Label(left, text="Chat avec le modèle (API locale)",
                               font=("Segoe UI", 9), foreground="#888888")
        chat_label.pack(anchor=tk.W, pady=(8, 2))

        chat_f = ttk.Frame(left)
        chat_f.pack(fill=tk.BOTH, expand=True)
        self.w_chat = tk.Text(chat_f, wrap=tk.WORD, font=("Consolas", 10),
                              bg="#0e0e0e", fg="#d4d4d4", state=tk.DISABLED,
                              relief=tk.FLAT, padx=6, pady=6)
        wc_s = ttk.Scrollbar(chat_f, orient=tk.VERTICAL, command=self.w_chat.yview)
        self.w_chat.configure(yscrollcommand=wc_s.set)
        self.w_chat.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        wc_s.pack(side=tk.RIGHT, fill=tk.Y)
        self.w_chat.tag_configure("user", foreground="#569cd6", font=("Consolas", 10, "bold"))
        self.w_chat.tag_configure("assistant", foreground="#4ec9b0", font=("Consolas", 10, "bold"))
        self.w_chat.tag_configure("body", foreground="#d4d4d4", font=("Consolas", 10))
        self.w_chat.tag_configure("err", foreground="#f44747")
        self.w_chat.tag_configure("sys", foreground="#dcdcaa", font=("Consolas", 9, "italic"))

        self._chat_append("système", "Bienvenue ! Lancez le worker puis échangez.", "sys")

        # Input area
        inp_f = ttk.Frame(left)
        inp_f.pack(fill=tk.X, pady=(4, 0))
        self.w_input = tk.Text(inp_f, height=3, wrap=tk.WORD, font=("Consolas", 10),
                               bg="#252526", fg="#d4d4d4", insertbackground="white",
                               relief=tk.FLAT, padx=4, pady=4)
        self.w_input.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.w_input.bind("<Control-Return>", lambda e: self._worker_send())
        self.w_send_btn = ttk.Button(inp_f, text="Envoyer", command=self._worker_send)
        self.w_send_btn.pack(side=tk.RIGHT, padx=(4, 0))

        # Right: status panel
        right = ttk.Frame(panes, width=350)
        panes.add(right, weight=1)
        ttk.Label(right, text="Infos worker", font=("Segoe UI", 10, "bold"),
                  foreground="#cccccc").pack(anchor=tk.W)
        self.w_info = tk.Text(right, wrap=tk.WORD, font=("Consolas", 9),
                              bg="#252526", fg="#d4d4d4", state=tk.DISABLED,
                              relief=tk.FLAT, padx=6, pady=6)
        wi_s = ttk.Scrollbar(right, orient=tk.VERTICAL, command=self.w_info.yview)
        self.w_info.configure(yscrollcommand=wi_s.set)
        self.w_info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        wi_s.pack(side=tk.RIGHT, fill=tk.Y)
        self._worker_info("Worker non lancé.\n\nLancez avec le bouton ▶\npour démarrer le serveur\nAPI local.\n\nModèle : Ministral 3 3B\nNécessite : transformers,\nmistral-common, torch\n\npip install -r worker-mini/requirements.txt")
        self.worker_proc = None
        self.worker_running = False
        self.w_history = []

    def _worker_info(self, text):
        self.w_info.configure(state=tk.NORMAL)
        self.w_info.delete(1.0, tk.END)
        self.w_info.insert(1.0, text)
        self.w_info.configure(state=tk.DISABLED)

    def _chat_append(self, role, text, tag="body"):
        self.w_chat.configure(state=tk.NORMAL)
        prefix = {"user": "🧑 Vous", "assistant": "🤖 Worker", "système": "⚙ Système"}.get(role, role)
        label = self.w_chat.tag_names()
        self.w_chat.insert(tk.END, f"{prefix}:\n", tag)
        self.w_chat.insert(tk.END, f"{text}\n\n", "body")
        self.w_chat.see(tk.END)
        self.w_chat.configure(state=tk.DISABLED)

    def _worker_toggle(self):
        if self.worker_running:
            self._worker_stop()
        else:
            self._worker_start()

    def _worker_start(self):
        import subprocess as sp
        worker_script = os.path.join(ROOT, "worker-mini", "model_worker.py")
        if not os.path.isfile(worker_script):
            self._chat_append("système", "worker-mini/model_worker.py introuvable", "err")
            return
        self._chat_append("système", "Démarrage du worker...", "sys")
        self._worker_info("Démarrage...\n\nLe chargement du modèle\npeut prendre 1-2 minutes\nlors de la première exécution.")
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        self.worker_proc = sp.Popen(
            [sys.executable, worker_script],
            stdout=sp.PIPE, stderr=sp.STDOUT,
            env=env, bufsize=1, text=True, encoding="utf-8", errors="replace",
        )
        self.worker_running = True
        self.w_start_btn.configure(text="■ Arrêter")
        self.worker_status_lbl.configure(text="🟡 Démarrage...", foreground="#dcdcaa")

        def _monitor():
            for line in self.worker_proc.stdout:
                self.root.after(0, self._worker_log, line.rstrip())
            self.worker_proc.wait()
            self.root.after(0, self._worker_stopped)

        t = threading.Thread(target=_monitor, daemon=True)
        t.start()

        def _check_ready():
            import urllib.request
            try:
                resp = urllib.request.urlopen("http://localhost:8742/health", timeout=2)
                if resp.status == 200:
                    self.root.after(0, lambda: self.worker_status_lbl.configure(
                        text="🟢 Prêt", foreground="#4ec9b0"))
                    self.root.after(0, lambda: self._chat_append(
                        "système", "Worker prêt ! Vous pouvez envoyer des messages.", "sys"))
                    self.root.after(0, self._worker_health)
            except Exception:
                self.root.after(2000, _check_ready)

        self.root.after(3000, _check_ready)

    def _worker_log(self, line):
        self._worker_info(self.w_info.get(1.0, tk.END).strip() + "\n" + line)

    def _worker_stop(self):
        if self.worker_proc:
            self.worker_proc.terminate()
            try:
                self.worker_proc.wait(timeout=5)
            except Exception:
                self.worker_proc.kill()
        self._worker_stopped()

    def _worker_stopped(self):
        self.worker_running = False
        self.worker_proc = None
        self.w_start_btn.configure(text="▶ Lancer")
        self.worker_status_lbl.configure(text="🔴 Arrêté", foreground="#f44747")
        self._chat_append("système", "Worker arrêté.", "sys")
        self._worker_info("Worker arrêté.")

    def _worker_health(self):
        import urllib.request
        try:
            resp = urllib.request.urlopen("http://localhost:8742/health", timeout=3)
            data = json_mod.loads(resp.read())
            info = (
                f"Statut  : {data.get('status', '?')}\n"
                f"Modèle  : {data.get('model', '?')}\n"
                f"GPU     : {data.get('gpu', '?')}\n"
                f"Device  : {data.get('device', '?')}\n"
            )
            self._worker_info(info)
            self.worker_status_lbl.configure(text="🟢 Prêt", foreground="#4ec9b0")
        except Exception as e:
            self._worker_info(f"Worker injoignable\n\n{e}")
            if self.worker_running:
                self.worker_status_lbl.configure(text="🟡 Démarrage...", foreground="#dcdcaa")

    def _worker_send(self):
        if not self.worker_running:
            self._chat_append("système", "Worker non lancé. Cliquez sur ▶ Lancer d'abord.", "err")
            return
        text = self.w_input.get(1.0, tk.END).strip()
        if not text:
            return
        self.w_input.delete(1.0, tk.END)
        self._chat_append("user", text, "user")
        self.w_send_btn.configure(state=tk.DISABLED)

        def _query():
            try:
                import urllib.request
                payload = json_mod.dumps({
                    "messages": self.w_history + [{"role": "user", "content": text}],
                    "temperature": 0.1,
                    "max_tokens": 2048,
                }).encode()
                req = urllib.request.Request(
                    "http://localhost:8742/v1/chat/completions",
                    data=payload,
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                resp = urllib.request.urlopen(req, timeout=120)
                data = json_mod.loads(resp.read())
                reply = data["choices"][0]["message"]["content"]
                self.root.after(0, self._chat_append, "assistant", reply, "assistant")
                self.w_history.append({"role": "user", "content": text})
                self.w_history.append({"role": "assistant", "content": reply})
                if len(self.w_history) > 20:
                    self.w_history = self.w_history[-20:]
            except Exception as e:
                self.root.after(0, self._chat_append, "système", f"Erreur : {e}", "err")
            finally:
                self.root.after(0, lambda: self.w_send_btn.configure(state=tk.NORMAL))

        t = threading.Thread(target=_query, daemon=True)
        t.start()

    def on_close(self):
        if self.worker_proc:
            self.worker_proc.terminate()
            try:
                self.worker_proc.wait(timeout=3)
            except Exception:
                self.worker_proc.kill()
        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    FluxGUI().run()
