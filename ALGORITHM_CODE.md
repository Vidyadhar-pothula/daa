# Algorithm Code Implementations

This document contains the actual Python code for all algorithms used in the project.

## 1. A* (A-Star) Search

```python
class AStarAI(GreedyAI):
    def __init__(self, start_node, goal_node, maze):
        super().__init__(start_node, goal_node, maze, 
                        heuristic_type='euclidean', 
                        algorithm_type='a_star')

    def heuristic(self, node):
        # Euclidean distance heuristic
        return math.sqrt((node.r - self.goal_node.r)**2 + 
                        (node.c - self.goal_node.c)**2)
    
    def compute_path(self):
        # Priority queue with f(n) = g(n) + h(n)
        frontier = PriorityQueue()
        frontier.put(self.current_node, 0)
        
        came_from = {self.current_node: None}
        cost_so_far = {self.current_node: 0}
        
        while not frontier.empty():
            current = frontier.get()
            
            if current == self.goal_node:
                break
            
            for neighbor in self.maze.get_neighbors(current):
                new_cost = cost_so_far[current] + self.get_edge_cost(current, neighbor)
                
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + self.heuristic(neighbor)
                    frontier.put(neighbor, priority)
                    came_from[neighbor] = current
        
        self.reconstruct_path(came_from, self.goal_node)
```

## 2. Breadth-First Search (BFS)

```python
class BFSAI(GreedyAI):
    def compute_path(self):
        queue = deque([self.current_node])
        visited = {self.current_node}
        came_from = {self.current_node: None}
        
        while queue:
            current = queue.popleft()
            self.metrics.record_visit(current)
            
            if current == self.goal_node:
                break
            
            for neighbor in self.maze.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = current
                    queue.append(neighbor)
        
        if current == self.goal_node:
            self.reconstruct_path(came_from, current)
```

## 3. Tarjan's Algorithm (Articulation Points)

```python
def run_tarjan(self):
    for r in range(height):
        for c in range(width):
            start_node = self.maze.grid[r][c]
            if start_node.type == '#' or start_node in self.visited:
                continue
                
            self.visited.add(start_node)
            self.discovery_time[start_node] = self.low_link[start_node] = self.time
            self.time += 1
            
            stack = [(start_node, None, iter(self.maze.get_neighbors(start_node)))]
            children = 0
            
            while stack:
                u, p, neighbors = stack[-1]
                
                try:
                    v = next(neighbors)
                    
                    if v == p:
                        continue
                    
                    if v in self.visited:
                        # Back-edge
                        self.low_link[u] = min(self.low_link[u], self.discovery_time[v])
                    else:
                        # Tree-edge
                        self.parent[v] = u
                        self.visited.add(v)
                        self.discovery_time[v] = self.low_link[v] = self.time
                        self.time += 1
                        
                        if u == start_node:
                            children += 1
                            
                        stack.append((v, u, iter(self.maze.get_neighbors(v))))
                
                except StopIteration:
                    stack.pop()
                    
                    if p is not None:
                        self.low_link[p] = min(self.low_link[p], self.low_link[u])
                        
                        # Articulation Point condition
                        if self.low_link[u] >= self.discovery_time[p]:
                            if p != start_node:
                                self.articulation_points.add(p)
            
            # Root with multiple children is AP
            if children > 1:
                self.articulation_points.add(start_node)
```

## 4. Flood Fill (Region Partitioning)

```python
def run_flood_fill(self):
    colors = [(0, 255, 0), (160, 32, 240), (0, 255, 255), 
              (255, 255, 0), (0, 0, 255), (255, 0, 255)]
    
    for r in range(height):
        for c in range(width):
            node = self.maze.grid[r][c]
            
            if node.type == '#' or node in self.visited or node in self.articulation_points:
                continue
                
            # Start new region
            self.region_id += 1
            self.region_graph[self.region_id] = set()
            self.regions_by_id[self.region_id] = []
            
            queue = [node]
            self.visited.add(node)
            self.regions[node] = self.region_id
            
            while queue:
                u = queue.pop(0)
                
                for v in self.maze.get_neighbors(u):
                    if v.type == '#':
                        continue
                    
                    # Stop at articulation points (bridges)
                    if v in self.articulation_points:
                        self.ap_connections[v].add(self.region_id)
                        continue
                    
                    if v not in self.visited:
                        self.visited.add(v)
                        self.regions[v] = self.region_id
                        self.regions_by_id[self.region_id].append(v)
                        queue.append(v)
```

## 5. Dynamic Programming (DP) - Circular Maze

```python
def compute_dp_costs(self):
    # Bottom-up DP from goal to all nodes
    self.goal_node.dp_cost = 0
    queue = deque([self.goal_node])
    visited = {self.goal_node}
    
    while queue:
        current = queue.popleft()
        current_cost = current.dp_cost
        
        for neighbor, edge_cost in self.get_weighted_neighbors(current):
            new_cost = current_cost + edge_cost
            
            if neighbor not in visited or new_cost < neighbor.dp_cost:
                neighbor.dp_cost = new_cost
                visited.add(neighbor)
                queue.append(neighbor)
```

## 6. DP Visualization Animation

```python
def draw_dp_simulation(self):
    self.dp_sim_time += 1/60.0
    wave_speed = 50
    self.dp_sim_wave_radius = self.dp_sim_time * wave_speed
    
    # Center pulse
    pulse_scale = 1.0 + 0.3 * math.sin(self.dp_sim_time * 3)
    center_radius = 20 * pulse_scale
    for i in range(3):
        alpha = 180 - i * 50
        radius = center_radius + i * 8
        pygame.draw.circle(overlay, (0, 255, 200, alpha), (cx, cy), int(radius))
    
    # Wave spreading
    if self.dp_sim_wave_radius < max_radius:
        wave_thickness = 40
        for i in range(wave_thickness):
            alpha = int(150 * (1 - i / wave_thickness))
            radius = int(self.dp_sim_wave_radius - i)
            if radius > 0:
                pygame.draw.circle(overlay, (0, 180, 255, alpha), (cx, cy), radius, 2)
    
    # Light up nodes in cost order
    for r in range(num_rings):
        radius = (r + 0.5) * ring_step
        if radius <= self.dp_sim_wave_radius:
            for s in range(sectors):
                node = self.maze.grid[r][s]
                if node.dp_cost < float('inf'):
                    intensity = max(0, 20 - node.dp_cost) / 20.0
                    glow_color = (0, int(200 * intensity), int(220 * intensity), 180)
                    pygame.draw.circle(overlay, glow_color, (nx, ny), 8)
```

## 7. Greedy Best-First Search (GBFS)

```python
def compute_path_best_first(self):
    frontier = PriorityQueue()
    frontier.put(self.current_node, 0)
    
    came_from = {self.current_node: None}
    
    while not frontier.empty():
        current = frontier.get()
        
        if current == self.goal_node:
            break
        
        for neighbor in self.maze.get_neighbors(current):
            if neighbor not in came_from:
                # Greedy: priority = heuristic only
                priority = self.heuristic(neighbor)
                frontier.put(neighbor, priority)
                came_from[neighbor] = current
    
    self.reconstruct_path(came_from, self.goal_node)

# Euclidean variant
def heuristic_euclidean(self, node):
    return math.sqrt((node.r - self.goal_node.r)**2 + (node.c - self.goal_node.c)**2)

# Manhattan variant
def heuristic_manhattan(self, node):
    return abs(node.r - self.goal_node.r) + abs(node.c - self.goal_node.c)

# Chebyshev variant
def heuristic_chebyshev(self, node):
    return max(abs(node.r - self.goal_node.r), abs(node.c - self.goal_node.c))
```

## 8. Huffman Coding

```python
class HuffmanNode:
    def __init__(self, char, freq, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right
    
    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text):
    # Count frequencies
    freqs = {}
    for char in text:
        freqs[char] = freqs.get(char, 0) + 1
    
    # Build priority queue
    pq = []
    for char, freq in freqs.items():
        heapq.heappush(pq, HuffmanNode(char, freq))
    
    # Build tree
    while len(pq) > 1:
        left = heappop(pq)
        right = heappop(pq)
        parent = HuffmanNode(None, left.freq + right.freq, left, right)
        heappush(pq, parent)
    
    return heappop(pq)

def generate_codes(root, code="", codes={}):
    if root.char is not None:
        codes[root.char] = code
        return
    
    generate_codes(root.left, code + "0", codes)
    generate_codes(root.right, code + "1", codes)
```

## 9. DFS (Maze Generation)

```python
def generate_maze_dfs(self):
    stack = [(0, 0)]
    visited = set([(0, 0)])
    
    while stack:
        current_r, current_c = stack[-1]
        
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        random.shuffle(directions)
        
        found_next = False
        for dr, dc in directions:
            nr, nc = current_r + dr, current_c + dc
            if 0 <= nr < height and 0 <= nc < width and (nr, nc) not in visited:
                # Carve path
                wall_r, wall_c = current_r + dr // 2, current_c + dc // 2
                self.grid[wall_r][wall_c].type = '.'
                self.grid[nr][nc].type = '.'
                
                visited.add((nr, nc))
                stack.append((nr, nc))
                found_next = True
                break
        
        if not found_next:
            stack.pop()
```

## 10. Hierarchical Pathfinding (Divide & Conquer)

```python
def compute_hierarchical_path(self):
    # 1. Divide: Find articulation points
    articulation_points = RegionLogic.compute_articulation_points(self.maze)
    
    # 2. Partition: Create regions using flood fill
    regions, region_graph, regions_by_id = RegionLogic.compute_regions(
        self.maze, articulation_points
    )
    
    # 3. Plan: High-level path through regions
    start_region = regions.get(self.start_node)
    goal_region = regions.get(self.goal_node)
    
    # BFS on region graph
    queue = deque([(start_region, [start_region])])
    visited = {start_region}
    
    while queue:
        current_region, path = queue.popleft()
        
        if current_region == goal_region:
            self.high_level_plan = path
            break
        
        for next_region in region_graph[current_region]:
            if next_region not in visited:
                visited.add(next_region)
                queue.append((next_region, path + [next_region]))
    
    # 4. Conquer: Solve each regional sub-problem
    full_path = []
    for i in range(len(self.high_level_plan) - 1):
        region_path = self.solve_region(
            self.high_level_plan[i], 
            self.high_level_plan[i + 1]
        )
        full_path.extend(region_path)
    
    return full_path
```
