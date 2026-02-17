# Visualization Guide for "Divide & Conquer" AI

In **Simulation Mode** (press `S`), the **Divide & Conquer (Hierarchical)** AI is now the default agent.

## What Do The Colors Mean?

### 1. The "Divide" Phase (Planning)
The AI first breaks the maze down into isolated "islands" or **Regions**.
- **Colored Squares**: Each region (island) is painted a unique color (e.g., Purple, Cyan, Olive).
- This shows exactly how the AI perceives the maze structure.

### 2. The "Conquer" Strategy (High-Level Plan)
Once regions are identified, the AI plans a route across them.
- **Cyan Dots**: The **Center** of each Region in the plan.
- **Magenta Dots**: The **Bridges** (Articulation Points) connecting the regions.
- **Thick Blue Line**: The **High-Level Path** connecting these dots. This represents the AI's strategic plan: *"Go from Region 1 -> Bridge -> Region 2 -> Bridge -> Goal Region"*.

### 3. The Execution (Low-Level Path)
- **Orange Line**: The actual step-by-step path the AI walks.
- Notice how it closely follows the Blue Line plan but navigates around local obstacles within each region.

## How to Test
1. Approve the pending command to run `main.py`.
2. Press `S` to enter Simulation Mode.
3. Observe the overlay!
