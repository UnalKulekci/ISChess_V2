# Ultimate Chess Bot: Algorithms & Data Structures Plan

This plan is structured to demonstrate mastery of various computer science concepts, from basic arrays to complex optimization algorithms.

## Phase 1: Foundations & Matrix Operations (Profiling & Traversal)
**Goal:** Treat the board as a Matrix and set up measurement tools.
*   **Step 1.1: Profiling Infrastructure**
    *   Create a `PerformanceProfiler` class to measure execution time (`ms`) and count operations (`nodes visited`).
    *   *Concept:* Algorithmic Complexity Analysis ($O(n)$).
*   **Step 1.2: Matrix Traversal & Knight Logic**
    *   Implement `Knight` movement using coordinate arithmetic (L-shapes) on the 2D board array.
    *   *Concept:* Coordinate Geometry & Matrix Iteration.

## Phase 2: Graph Theory & State Space (Move Generation)
**Goal:** Define the "Game Tree" by generating valid edges (moves).
*   **Step 2.1: Universal Move Generator**
    *   Implement `get_valid_moves(board, color)` for all pieces using `match-case` logic.
    *   This defines the "Branching Factor" of our graph.
    *   *Concept:* Directed Graphs & State Space Generation.

## Phase 3: Heuristics & Data Structures (Evaluation Function)
**Goal:** Use Arrays and Logic to evaluate "Good" vs "Bad" states.
*   **Step 3.1: Material Evaluation (Basic Heuristic)**
    *   Assign static integer values: Pawn=10, Knight=30, etc.
*   **Step 3.2: Piece-Square Tables (Advanced Heuristic)**
    *   Use **2D Arrays (Matrices)** to give bonuses based on position (e.g., Knights are better in the center).
    *   Example: `PAWN_TABLE[8][8]` array where center squares have higher values.
    *   *Concept:* Array Lookups ($O(1)$) & Domain Knowledge Modeling.

## Phase 4: Search Algorithms (DFS, Minimax & Pruning)
**Goal:** Explore the Game Tree recursively to find the optimal path.
*   **Step 4.1: Greedy Search (Local Optima)**
    *   A bot that just picks the best Heuristic score *immediately*.
*   **Step 4.2: Minimax Algorithm (DFS)**
    *   Implement Recursive Depth-First Search to look ahead.
*   **Step 4.3: Alpha-Beta Pruning**
    *   Optimize the search by pruning irrelevant branches.
    *   *Concept:* Tree Traversal & Branch-and-Bound Optimization.

## Phase 5: Optimization & Probability (Stochastics & SA)
**Goal:** Advanced techniques for global optimization.
*   **Step 5.1: Opening Book (Hash Maps)**
    *   Use a Python `dictionary` for $O(1)$ access to standard opening moves.
*   **Step 5.2: Stochastic Move Selection**
    *   Use Weighted Randomness to avoid deterministic loops.
*   **Step 5.3: Simulated Annealing (Parameter Tuning)**
    *   Logic to optimize the values in Phase 3 (e.g., "Is a Bishop worth 30 or 33?") using randomized cooling schedules.
    *   *Concept:* Global Optimization & Probabilistic Algorithms.

## Phase 6: Graph Algorithms (BFS Pathfinding)
**Goal:** Solve specific traversal problems.
*   **Step 6.1: BFS Pathfinding**
    *   Implement Breadth-First Search to find the shortest path for a piece to reach a target square.
    *   *Concept:* Shortest Path Algorithms (Unweighted Graph).

