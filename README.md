# Duel of Labyrinth

[![Play Online](https://img.shields.io/badge/Play-Online-green?style=for-the-badge&logo=google-chrome)](https://vidyadhar-pothula.github.io/DAA-Maze-Runner/)

## 🎯 Overview
**Duel of Labyrinth** is a comprehensive maze exploration and algorithm visualization game where you (the player) compete against various pathfinding AIs. 

It is designed as an educational tool for the **Design and Analysis of Algorithms (DAA)**. Watch in real-time as algorithms construct paths, evaluate graph heuristics, divide-and-conquer regions, and dynamically react to graph changes!

## 🌟 Game Features
- **Race Against AI**: Play simultaneously against an AI opponent navigating the exact same maze.
- **Backtracking System**: Undo your moves seamlessly using the built-in backtracking system, complete with HUD flashes and history state tracking.
- **Advanced Graph Visualizations**: Toggle overlays to view underlying graph edges, heuristics, DP grids, regions, and articulation points.
- **Rich Metric Analysis**: Monitor nodes explored, total cost, efficiency, and backtrack counts in real-time.

## 🎮 Game Levels & Modes
1. **EASY / MEDIUM / HARD**: Traditional grid-based mazes of increasing complexity and size.
2. **DYNAMIC**: The maze architecture is unstable and changes in real-time! Walls generate and collapse dynamically, forcing the AI (and you) to adapt your paths on the fly.
3. **CIRCULAR**: Navigates through a distinctly non-standard circular (polar) coordinate maze.
   
## 🤖 Algorithms & Techniques Implemented
Dive deep into graph theory with our rich suite of embedded algorithms:

1. **Depth-First Search (DFS)**: Primarily utilized for generating the complex maze grids.
2. **Greedy Best-First Search (GBFS)**: Follows the Euclidean/Manhattan heuristic blindly to rush the goal. Quick, but not always optimal.
3. **A* (A-Star) Search**: Combines distance traveled and heuristic distance to find the optimal path. Takes trap (+3 cost) and powerup (-2 cost) edge weights into consideration.
4. **Dijkstra's Algorithm**: Exhaustive, heuristic-free shortest path search.
5. **Hill Climbing**: Pure greedy local-search logic that does not utilize a backtracking frontier. Watch it get stuck in local minima (dead ends)!
6. **Hierarchical AI (Divide & Conquer)**: An advanced planner that computes *Articulation Points* to break the graph into separate *Regions*. It plans a high-level sequence of regions before stitching low-level paths together!
7. **Tarjan's Bridge-Finding**: Analyzes the connectivity of the graph to visualize critical edge bridges and articulation vertices.
8. **Dynamic Programming (DP)**: Utilizes a wavefront propagation approach yielding optimal substructures, complete with a visual simulation mode!

## 🕹️ Controls

### Gameplay & Movement
- **WASD / Arrow Keys** `↑ ↓ ← →` : Move your player (Blue Circle).
- **Q, E, Z, C** : Move diagonally.
- **U / Backspace** : Backtrack (undo your last move and revert AI history).
- **R** : Restart the current level.
- **ESC** : Return to Main Menu.
- **S** : Open Simulation Mode from the Playing state.

### Visualizations & Toggles
- **G** : Toggle the Live Graph Overlay (Visualize the mathematical graph nodes and edges).
- **L** : Visualize Logic mode (Steps through Tarjan's analysis).
- **H** : Toggle Heuristic values directly on nodes.
- **J** : Run DP (Dynamic Programming) Simulation Wavefront.
- **K** : Toggle DP Visualization values layer.
- **A** : Toggle AI Candidate Annotations (Highlights frontier nodes).
- **B** : Toggle BFS overlay.
- **V** : Toggle Regions Visualization (Visualizes Hierarchical islands).

## 🚀 Installation & Setup

Ensure you have **Python 3.8+** installed along with **pygame**.

```bash
# Clone the repository and navigate inside
git clone https://github.com/Vidyadhar-Pothula/DAA-Maze-Runner.git
cd DAA-Maze-Runner

# Install dependencies
pip install -r requirements.txt
# OR directly: pip install pygame

# Run the game!
python3 main.py

# Run the comprehensive test suite
python3 -m unittest test_greedy.py test_logic.py test_simulation.py -v
```

## 📈 Real-Time Metrics Glossary
- **Cost**: The graph edge weight cost. Traps cost `3`, standard moves cost `1`, diagonals `1.414`, and powerups `-2`.
- **Steps**: Raw movement steps taken.
- **Explored**: Total frontier nodes evaluated by the chosen algorithm.
- **Efficiency**: `(Optimal_Path_Length / AI_Path_Length) × 100`. Demonstrates how close the AI's path was to perfection.
- **Backtracks**: How many times the AI hit a dead end and reversed course.

## 🤝 Contributing
Built for educational demonstration of graph algorithms. Free to use, fork, and modify to implement your own traversal strategies or heuristics!