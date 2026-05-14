# 🗼 Tower of Hanoi — RISC-V Mentorship Coding Challenge

> **Challenge:** Broadening the RISC-V High Precision Code Base and Reach  
> **Submission:** Tower of Hanoi — Recursive & Iterative approaches with live ASCII simulation  
> **Language:** Python 3.8+  

---

## 📌 About This Submission

This script demonstrates the **Tower of Hanoi** puzzle using two distinct algorithmic approaches — **Recursive** and **Iterative** — with a real-time ASCII terminal simulation.

Both approaches are clearly sectioned and commented inside the code, making it easy to identify where recursion ends and iteration begins. This directly satisfies the challenge requirement of identifying and commenting on recursion and/or iteration sections.

The iterative solution is of particular relevance to **RISC-V embedded environments**: it uses **O(1) auxiliary stack space**, avoiding deep call stacks that can be problematic on resource-constrained RISC-V processors where stack memory is limited.

---

## 🖥️ Demo Preview

```
   [A]       [B]       [C]
   ===        |         |
    =          |         |
  =====     =====     =====

  Move   1: Disk 1 — A → B
  Optimal moves: 7
```

Each move is animated live in the terminal with a 0.5s delay between frames.

---

## ⚙️ How to Run

**Requirements:** Python 3.8 or higher. No external libraries needed.

```bash
# Clone the repo
git clone https://github.com/<your-username>/risc-v-hanoi.git
cd risc-v-hanoi

# Run the script
python3 tower_of_hanoi.py
```

You will be prompted to:
1. Enter the number of disks (1–10)
2. Choose an algorithm: `R` for Recursive, `I` for Iterative

---

## 🧠 Algorithm Overview

### 🔁 Recursive Approach
```
solve(n, source → target via auxiliary)
  ├─ solve(n-1, source → auxiliary)   # Move top n-1 disks out of the way
  ├─ move disk n (source → target)    # Place the largest disk
  └─ solve(n-1, auxiliary → target)   # Rebuild on top
```

| Property | Value |
|---|---|
| Time Complexity | O(2ⁿ) |
| Space Complexity | O(n) — call stack depth |
| Comment marker in code | `── RECURSIVE SECTION ──` |

---

### 🔄 Iterative Approach
Uses a **mathematical parity rule** — no recursion, no call stack:

- **Odd moves** → Move the smallest disk (disk 1) cyclically in a fixed direction
- **Even moves** → Make the only other legal move between the remaining two rods

This alternation guarantees the optimal **2ⁿ − 1** total moves.

| Property | Value |
|---|---|
| Time Complexity | O(2ⁿ) |
| Space Complexity | **O(1)** — constant auxiliary space |
| Comment marker in code | `── ITERATIVE SECTION ──` |

> **RISC-V relevance:** The iterative solution avoids stack overflow risks on deeply embedded RISC-V targets where stack memory is minimal. It is the preferred approach for bare-metal or RTOS deployments.

---

## 📁 File Structure

```
risc-v-hanoi/
│
├── tower_of_hanoi.py   # Main script — all logic, visualiser, solvers
└── README.md           # This file
```

---

## ✅ Features

- [x] Two algorithm implementations — Recursive & Iterative
- [x] Clearly marked recursion and iteration sections in comments
- [x] Real-time ASCII terminal animation (0.5s delay per move)
- [x] Error handling — invalid input prompts re-entry instead of crashing
- [x] Professional docstrings on every class and method
- [x] PEP 8 compliant code style
- [x] `if __name__ == "__main__"` guarded entry point
- [x] Zero external dependencies

---

## 🔗 RISC-V Connection

| Concept | Relevance |
|---|---|
| O(1) iterative stack | Safe on RISC-V bare-metal targets with limited RAM |
| Recursive depth = n | Maps directly to RISC-V call stack frame analysis |
| Optimal move count (2ⁿ−1) | Useful benchmark for instruction-count profiling on RISC-V simulators |
| Pure Python, no deps | Runs on MicroPython ports targeting RISC-V MCUs |

---

## 👩‍💻 Author

**Unnati**  
First-Year B.Tech — Artificial Intelligence & Machine Learning  
Founder, [ELYX](https://elyx-ai.github.io) — AI-powered accountability mentor app  

*Submitted for the RISC-V Mentorship Program — Coding Challenge*