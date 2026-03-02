class DFSSimulator:
    """Step-by-step specific DFS algorithm visualizing backtracks for 'S' Simulation Mode"""
    def __init__(self, start_node, goal_node, maze):
        self.maze = maze
        self.start_node = start_node
        self.goal_node = goal_node
        # Stack structure: list of (node, parent_node) to trace edges
        self.stack = [(start_node, None)]
        self.visited = set()
        self.current_node = start_node
        
        # UI Tracking States
        self.state = "IDLE" # IDLE, FORWARD, DEAD_END, BACKTRACK, FINISHED
        self.decision_log = "Simulation Initialized. Press S to start."
        self.backtrack_count = 0
        self.dead_ends_encountered = 0
        self.backtrack_edges = [] # List of tuples (node1, node2) for dashed red lines
        self.forward_edges = [] # List of tuples (node1, node2) for green lines
        self.rejected_edges = set() # Set of permanently failed edge tuples
        self.rejected_nodes = set() # Set of permanently failed nodes
        self.frontier_nodes = set()
        self.path = [] # Current path line
        
        # Live Graph Metrics
        import time
        self.start_time = time.time()
        self.step_count = 0
        self.history_metrics = [] # [{"step": int, "runtime": float, "nodes": int, "backtracks": int, "stack_depth": int, "state": str}]
        
        self.full_exploration_mode = False
        
    def step(self):
        if self.state == "FINISHED":
            return
            
        # 1. Handle Dead End / Backtrack visualization state transitions
        if self.state == "DEAD_END":
            self.state = "BACKTRACK"
            self.backtrack_count += 1
            if not self.stack:
                self.decision_log = "Search Exhausted. No path found."
                self.state = "FINISHED"
                return
            else:
                next_node, _ = self.stack[-1]
                self.decision_log = "Dead End Reached. Backtracking..."
            return
            
        if self.state == "BACKTRACK":
            if not self.stack:
                self.state = "FINISHED"
                if self.full_exploration_mode:
                    self.decision_log = "Full Graph Exploration Complete."
                else:
                    self.decision_log = "Stack Empty: No Path Found."
                return
                
            next_target, target_parent = self.stack[-1]
            if not self.path or self.path[-1] == target_parent:
                self.state = "FORWARD"
                self.decision_log = f"Exploring new branch from ({target_parent.r if target_parent else self.start_node.r}, {target_parent.c if target_parent else self.start_node.c})"
                # Fall through to pop the new target and move forward
            else:
                prev_node = self.path.pop()
                self.rejected_nodes.add(prev_node)
                if self.path:
                    new_curr = self.path[-1]
                    self.backtrack_edges.append((prev_node, new_curr))
                    # Mark edge as permanently rejected, sorting to handle undirected graph matching easily
                    edge = tuple(sorted(((prev_node.r, prev_node.c), (new_curr.r, new_curr.c))))
                    self.rejected_edges.add(edge)
                    self.current_node = new_curr
                    self.decision_log = f"Popping ({prev_node.r}, {prev_node.c}) - Returning to parent ({new_curr.r}, {new_curr.c})"
                return # Only ONE action per frame: We stepped backward visually. Run next frame.
            
        # 2. Main Logic Step
        if self.state == "FORWARD" or self.state == "IDLE":
            if not self.stack:
                if self.full_exploration_mode:
                    self.decision_log = "Full Graph Exploration Complete."
                else:
                    self.decision_log = "Stack Empty: No Path Found."
                self.state = "FINISHED"
                return
                
            self.current_node, parent = self.stack.pop()
            
            if self.current_node in self.visited:
                # Already visited, just skip it but log
                self.decision_log = f"Skipping visited node ({self.current_node.r}, {self.current_node.c})"
                self.state = "FORWARD"
                return
    
            self.visited.add(self.current_node)
            self.path.append(self.current_node)
            if parent:
                self.forward_edges.append((parent, self.current_node))
                
            if self.current_node == self.goal_node and not self.full_exploration_mode:
                self.decision_log = "Goal Reached!"
                self.state = "FINISHED"
                return
                
            # 3. Explore Neighbors
            neighbors = self.maze.get_neighbors(self.current_node)
            # Avoid walls and visited nodes
            valid_neighbors = [n for n in neighbors if n not in self.visited and n.type != '#']
            
            # Clear old frontier visuals
            self.frontier_nodes = set()
            
            if not valid_neighbors:
                self.state = "DEAD_END"
                self.dead_ends_encountered += 1
                self.decision_log = "Dead End Reached. Backtracking..."
            else:
                self.state = "FORWARD"
                self.decision_log = f"Moving to ({self.current_node.r}, {self.current_node.c})"
                # Heuristic sort to guide DFS towards goal
                # For Backtracking Mode: Sort backwards to intentionally prioritize exploring the WRONG outward-facing dead-end branches first.
                should_reverse = True
                if getattr(self.maze, 'maze_type', None) == "BACKTRACKING":
                    should_reverse = False
                    
                valid_neighbors.sort(key=lambda n: self.maze.heuristic(n, 'manhattan'), reverse=should_reverse)
                
                for neighbor in valid_neighbors:
                    self.frontier_nodes.add(neighbor)
                    self.stack.append((neighbor, self.current_node))
                    
        # 4. Finalize Step Metrics Snapshot
        self.step_count += 1
        import time
        runtime_ms = (time.time() - self.start_time) * 1000
        snapshot = {
            "step": self.step_count,
            "runtime": runtime_ms,
            "nodes": len(self.visited),
            "backtracks": self.backtrack_count,
            "stack_depth": len(self.stack),
            "state": self.state
        }
        self.history_metrics.append(snapshot)

    def get_metrics(self):
        explored = len(self.visited)
        efficiency = 0
        if explored > 0:
            # Efficiency based on optimal path length vs explored nodes
            opt = getattr(self.maze, 'optimal_path_length', 1)
            efficiency = min(100, (opt / explored) * 100)
        return {
            "backtracks": self.backtrack_count,
            "dead_ends": self.dead_ends_encountered,
            "explored": explored,
            "efficiency": f"{efficiency:.1f}%"
        }
