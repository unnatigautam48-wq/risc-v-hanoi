"""
Tower of Hanoi — Recursive & Iterative Approaches
===================================================
Author  : Unnati
Purpose : RISC-V Mentorship Challenge Submission
Python  : 3.8+

Demonstrates two classic algorithms for solving the Tower of Hanoi puzzle,
complete with a real-time ASCII terminal simulation, professional docstrings,
PEP 8 compliance, and robust input error handling.
"""

import time
import os
import sys


# ─────────────────────────────────────────────
#  CONFIGURATION
# ─────────────────────────────────────────────

DISK_CHAR = "="          # Character used to draw disk bodies
ROD_CHAR = "|"           # Character used to draw the rod
DELAY = 0.5              # Seconds between each animated move
ROD_NAMES = ["A", "B", "C"]


# ─────────────────────────────────────────────
#  VISUALISER CLASS
# ─────────────────────────────────────────────

class HanoiVisualiser:
    """
    Manages the ASCII terminal visualisation for the Tower of Hanoi simulation.

    Attributes
    ----------
    num_disks : int
        Total number of disks in the puzzle.
    rods : dict[str, list[int]]
        Maps rod names ('A', 'B', 'C') to their current stacks of disk sizes.
    move_count : int
        Running total of moves made so far.
    """

    def __init__(self, num_disks: int) -> None:
        """
        Initialise the visualiser with all disks stacked on rod A.

        Parameters
        ----------
        num_disks : int
            The number of disks to use in the puzzle (must be >= 1).
        """
        self.num_disks = num_disks
        self.move_count = 0
        # Rod A starts with disks in descending order (largest at bottom)
        self.rods: dict[str, list[int]] = {
            "A": list(range(num_disks, 0, -1)),
            "B": [],
            "C": [],
        }

    def move_disk(self, source: str, target: str) -> None:
        """
        Move the top disk from the source rod to the target rod and refresh display.

        Parameters
        ----------
        source : str
            Name of the rod to move a disk from ('A', 'B', or 'C').
        target : str
            Name of the rod to move a disk to ('A', 'B', or 'C').
        """
        disk = self.rods[source].pop()
        self.rods[target].append(disk)
        self.move_count += 1
        self._render(f"Move {self.move_count:>3}: Disk {disk} — {source} → {target}")
        time.sleep(DELAY)

    def _render(self, status_line: str = "") -> None:
        """
        Clear the terminal and redraw the current state of all three rods.

        Parameters
        ----------
        status_line : str, optional
            A description of the last move, displayed below the rods.
        """
        os.system("cls" if os.name == "nt" else "clear")

        col_width = self.num_disks * 2 + 3   # Width of each rod column
        total_rows = self.num_disks + 2       # Disk rows + base row + label row

        # Build a 2-D grid of strings (top row = row 0)
        grid: list[list[str]] = [
            [" " * col_width for _ in ROD_NAMES]
            for _ in range(total_rows)
        ]

        for col_idx, rod_name in enumerate(ROD_NAMES):
            stack = self.rods[rod_name]

            # Draw each disk from the bottom of the rod upward
            for row_from_bottom, disk_size in enumerate(stack):
                row = self.num_disks - row_from_bottom   # Convert to grid row
                disk_str = self._disk_repr(disk_size, col_width)
                grid[row][col_idx] = disk_str

            # Draw the empty rod segments above the disks
            filled_rows = len(stack)
            for row in range(1, self.num_disks - filled_rows + 1):
                grid[row][col_idx] = self._empty_rod_repr(col_width)

            # Draw the base
            grid[0][col_idx] = self._disk_repr(self.num_disks + 1, col_width)

            # Draw the rod label
            grid[total_rows - 1][col_idx] = f"  [{rod_name}]  ".center(col_width)

        # Print the grid (row 0 = top of rods visually, so we reverse)
        print()
        for row in reversed(range(total_rows)):
            print("   ".join(grid[row]))

        # Print status line
        print()
        print(f"  {status_line}")
        print(f"  Optimal moves: {2 ** self.num_disks - 1}")
        print()

    def _disk_repr(self, size: int, col_width: int) -> str:
        """
        Return an ASCII string representing a disk of the given size.

        Parameters
        ----------
        size : int
            The size of the disk (larger value = wider disk).
        col_width : int
            The total character width of the column.

        Returns
        -------
        str
            A centered string of '=' characters padded to col_width.
        """
        body = DISK_CHAR * (size * 2 - 1)
        return body.center(col_width)

    def _empty_rod_repr(self, col_width: int) -> str:
        """
        Return an ASCII string representing an empty rod segment (no disk).

        Parameters
        ----------
        col_width : int
            The total character width of the column.

        Returns
        -------
        str
            A centered '|' character padded to col_width.
        """
        return ROD_CHAR.center(col_width)


# ─────────────────────────────────────────────
#  TOWER OF HANOI — SOLVER CLASSES
# ─────────────────────────────────────────────

class RecursiveSolver:
    """
    Solves the Tower of Hanoi puzzle using the classic recursive algorithm.

    The recursive approach works by reducing the problem:
      1. Move the top (n-1) disks from source → auxiliary.
      2. Move the nth (largest) disk from source → target.
      3. Move the (n-1) disks from auxiliary → target.

    Time Complexity  : O(2ⁿ)
    Space Complexity : O(n)  — call stack depth
    """

    def __init__(self, visualiser: HanoiVisualiser) -> None:
        """
        Parameters
        ----------
        visualiser : HanoiVisualiser
            The shared visualiser instance used to animate each move.
        """
        self.vis = visualiser

    # ── RECURSIVE SECTION ──────────────────────────────────────────────────
    def solve(self, n: int, source: str, target: str, auxiliary: str) -> None:
        """
        Recursively move `n` disks from `source` to `target` via `auxiliary`.

        Parameters
        ----------
        n : int
            Number of disks to move in this recursive call.
        source : str
            The rod from which disks are moved.
        target : str
            The rod to which disks are moved.
        auxiliary : str
            The rod used as a temporary buffer.
        """
        # ── BASE CASE ──────────────────────────────────────────────────────
        if n == 1:
            # Only one disk: move it directly from source to target
            self.vis.move_disk(source, target)
            return

        # ── RECURSIVE CASE ─────────────────────────────────────────────────
        # Step 1: Move the top (n-1) disks out of the way
        self.solve(n - 1, source, auxiliary, target)

        # Step 2: Move the largest remaining disk to its final position
        self.vis.move_disk(source, target)

        # Step 3: Move the (n-1) disks from auxiliary onto the largest disk
        self.solve(n - 1, auxiliary, target, source)
    # ── END RECURSIVE SECTION ──────────────────────────────────────────────


class IterativeSolver:
    """
    Solves the Tower of Hanoi puzzle using an iterative (non-recursive) algorithm.

    The iterative approach uses a mathematical property of the puzzle:
    - For an even number of disks, the cyclic move order is A → B → C → A.
    - For an odd number of disks, the cyclic move order is A → C → B → A.
    On each step, either:
      (a) Make the 'legal small-disk move' (the smallest disk, cyclically), or
      (b) Make the only other legal move between the remaining two rods.
    This alternation guarantees the optimal 2ⁿ − 1 total moves.

    Time Complexity  : O(2ⁿ)
    Space Complexity : O(1)  — no call stack overhead
    """

    def __init__(self, visualiser: HanoiVisualiser) -> None:
        """
        Parameters
        ----------
        visualiser : HanoiVisualiser
            The shared visualiser instance used to animate each move.
        """
        self.vis = visualiser

    # ── ITERATIVE SECTION ──────────────────────────────────────────────────
    def solve(self, n: int) -> None:
        """
        Iteratively solve the Tower of Hanoi for `n` disks.

        Parameters
        ----------
        n : int
            Total number of disks to move from rod A to rod C.
        """
        total_moves = (2 ** n) - 1
        rods = self.vis.rods

        # Determine cyclic movement direction based on parity of n
        if n % 2 == 0:
            rod_order = ["A", "B", "C"]   # Even: cycle A → B → C
        else:
            rod_order = ["A", "C", "B"]   # Odd:  cycle A → C → B

        # ── ITERATIVE LOOP ─────────────────────────────────────────────────
        for move_num in range(1, total_moves + 1):
            if move_num % 2 == 1:
                # Odd move: make the smallest-disk (legal cyclic) move
                self._move_smallest_disk_cyclically(rods, rod_order)
            else:
                # Even move: make the only other legal move between
                # the two rods NOT currently holding the smallest disk
                self._move_non_smallest_disk(rods, rod_order)
        # ── END ITERATIVE LOOP ─────────────────────────────────────────────

    def _move_smallest_disk_cyclically(
        self, rods: dict, rod_order: list[str]
    ) -> None:
        """
        Move the smallest disk (size 1) to the next rod in the cyclic order.

        Parameters
        ----------
        rods : dict
            Current state mapping rod names to their disk stacks.
        rod_order : list[str]
            The ordered list of rods defining legal cyclic moves.
        """
        # Find which rod currently holds disk 1
        for rod in rod_order:
            if rods[rod] and rods[rod][-1] == 1:
                current_idx = rod_order.index(rod)
                break

        # Move to the next rod in the cycle
        next_rod = rod_order[(current_idx + 1) % 3]
        self.vis.move_disk(rod, next_rod)

    def _move_non_smallest_disk(
        self, rods: dict, rod_order: list[str]
    ) -> None:
        """
        Make the only legal move between the two rods not holding disk 1.

        A legal move means placing a smaller disk on top of a larger one,
        or onto an empty rod. Since disk 1 is excluded, we look at the
        tops of the other two rods and move the smaller onto the larger
        (or the only one if the other is empty).

        Parameters
        ----------
        rods : dict
            Current state mapping rod names to their disk stacks.
        rod_order : list[str]
            The ordered list of rods defining legal cyclic moves.
        """
        # Identify the rod holding disk 1
        smallest_rod = None
        for rod in rod_order:
            if rods[rod] and rods[rod][-1] == 1:
                smallest_rod = rod
                break

        # The two rods not holding disk 1
        other_rods = [r for r in rod_order if r != smallest_rod]
        rod_x, rod_y = other_rods[0], other_rods[1]

        top_x = rods[rod_x][-1] if rods[rod_x] else float("inf")
        top_y = rods[rod_y][-1] if rods[rod_y] else float("inf")

        # Move the smaller top disk onto the larger (or empty rod)
        if top_x < top_y:
            self.vis.move_disk(rod_x, rod_y)
        else:
            self.vis.move_disk(rod_y, rod_x)
    # ── END ITERATIVE SECTION ──────────────────────────────────────────────


# ─────────────────────────────────────────────
#  INPUT HELPER
# ─────────────────────────────────────────────

def get_disk_count() -> int:
    """
    Prompt the user to enter the number of disks with full error handling.

    Keeps asking until a valid positive integer (1–10) is provided.
    A non-integer entry or out-of-range value triggers a friendly re-prompt
    rather than a crash, satisfying robust UX and defensive coding standards.

    Returns
    -------
    int
        A validated integer in the range [1, 10].
    """
    while True:
        try:
            raw = input("  Enter number of disks (1–10): ").strip()
            n = int(raw)                    # Raises ValueError if not an int
            if not 1 <= n <= 10:
                print(f"  ✗  Please enter a number between 1 and 10.\n")
                continue
            return n
        except ValueError:
            # Handles non-integer input gracefully (e.g. "abc", "3.5", "")
            print(f"  ✗  '{raw}' is not a valid integer. Try again.\n")


def get_algorithm_choice() -> str:
    """
    Prompt the user to choose between the recursive and iterative solvers.

    Returns
    -------
    str
        Either 'R' (recursive) or 'I' (iterative).
    """
    while True:
        choice = input("  Choose algorithm — [R]ecursive / [I]terative: ").strip().upper()
        if choice in ("R", "I"):
            return choice
        print("  ✗  Please enter 'R' or 'I'.\n")


# ─────────────────────────────────────────────
#  MAIN BLOCK
# ─────────────────────────────────────────────

def main() -> None:
    """
    Entry point for the Tower of Hanoi simulation.

    Workflow
    --------
    1. Display a welcome banner.
    2. Collect and validate user inputs (disk count, algorithm choice).
    3. Instantiate the visualiser and chosen solver.
    4. Run the solver, which animates each move in real time.
    5. Print a completion summary.
    """
    # ── Banner ─────────────────────────────────────────────────────────────
    print()
    print("  ╔══════════════════════════════════════╗")
    print("  ║       TOWER  OF  HANOI               ║")
    print("  ║   Recursive & Iterative Approaches   ║")
    print("  ╚══════════════════════════════════════╝")
    print()

    # ── Input collection ───────────────────────────────────────────────────
    num_disks = get_disk_count()
    print()
    algorithm = get_algorithm_choice()
    print()

    # ── Setup ──────────────────────────────────────────────────────────────
    vis = HanoiVisualiser(num_disks)
    vis._render("Starting position …")
    time.sleep(DELAY)

    # ── Solve ──────────────────────────────────────────────────────────────
    if algorithm == "R":
        print(f"  Running RECURSIVE solver for {num_disks} disk(s) …\n")
        solver = RecursiveSolver(vis)
        solver.solve(num_disks, source="A", target="C", auxiliary="B")
    else:
        print(f"  Running ITERATIVE solver for {num_disks} disk(s) …\n")
        solver = IterativeSolver(vis)
        solver.solve(num_disks)

    # ── Summary ────────────────────────────────────────────────────────────
    optimal = 2 ** num_disks - 1
    print("  ✔  Puzzle solved!")
    print(f"     Disks        : {num_disks}")
    print(f"     Total moves  : {vis.move_count}")
    print(f"     Optimal moves: {optimal}")
    print(f"     Algorithm    : {'Recursive' if algorithm == 'R' else 'Iterative'}")
    print()


if __name__ == "__main__":
    main()