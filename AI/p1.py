import heapq
import sys
"""
Euristica aleasă este distanța Manhattan, calculată ca abs(x1 - x2) + abs(y1 - y2), unde (x1, y1) și (x2, y2) sunt coordonatele a două noduri. 
Această euristică este admisibilă deoarece, în acest graf specific, costul fiecărei muchii este exact egal cu distanța Manhattan dintre coordonatele nodurilor conectate de acea muchie. 
Prin urmare, costul oricărui drum din graf este egal cu suma distanțelor Manhattan ale muchiilor de pe acel drum. 
Deoarece distanța Manhattan directă dintre nodul de start și nodul scop reprezintă cea mai mică sumă posibilă a distanțelor Manhattan (și deci a costurilor) necesară pentru a ajunge la scop, 
valoarea euristicii nu va supraestima niciodată costul real al celui mai scurt drum, asigurând astfel admisibilitatea.
"""



class Graph:
    def __init__(self):
        self.coords = {
            1: (0, 0), 2: (0, 3), 3: (0, 6),
            4: (1, 1), 5: (1, 3), 6: (1, 5),
            7: (2, 2), 8: (2, 3), 9: (2, 4),
            10: (3, 0), 11: (3, 1), 12: (3, 2),
            13: (3, 4), 14: (3, 5), 15: (3, 6),
            16: (4, 2), 17: (4, 3), 18: (4, 4),
            19: (5, 1), 20: (5, 3), 21: (5, 5),
            22: (6, 0), 23: (6, 3), 24: (6, 6)
        }
        self.graph = {node: {} for node in self.coords}
        self._setup_edges()

    def _setup_edges(self):
        cost3_edges = [(1, 2), (1, 10), (2, 3), (3, 15), (10, 22), (15, 24), (22, 23), (23, 24)]
        cost2_edges = [(4, 5), (4, 11), (5, 6), (6, 14), (11, 19), (14, 21), (19, 20), (20, 21)]
        cost1_edges = [(2, 5), (5, 8), (7, 8), (7, 12), (8, 9), (9, 13), (10, 11), (11, 12), (12, 16), (13, 14),
                       (13, 18), (14, 15), (16, 17), (17, 18), (17, 20), (20, 23)]

        for u, v in cost3_edges: self._add_edge(u, v, 3)
        for u, v in cost2_edges: self._add_edge(u, v, 2)
        for u, v in cost1_edges: self._add_edge(u, v, 1)

    def _add_edge(self, u, v, cost):
        self.graph[u][v] = cost
        self.graph[v][u] = cost

    def get_neighbors(self, node):
        return self.graph.get(node, {})

    def heuristic(self, node, goals):
        if not goals:
            return 0  
        x1, y1 = self.coords[node]
        min_h = float('inf')
        for goal in goals:
            x2, y2 = self.coords[goal]
            # Manhattan distance
            distance = abs(x1 - x2) + abs(y1 - y2)
            min_h = min(min_h, distance)
        return min_h

def astar_search(graph, start_node, goal_nodes, steps_limit):
    initial_h = graph.heuristic(start_node, goal_nodes)
    open_set = [(initial_h, 0, start_node, [start_node])] # f=h, g=0
    closed_set = set()
    nodes_expanded = 0

    while open_set and nodes_expanded < steps_limit:
        f_score, g_score, current_node, path = heapq.heappop(open_set)

        if current_node in closed_set:
            continue

        closed_set.add(current_node)
        nodes_expanded += 1

        if current_node in goal_nodes:
            return current_node 
        for neighbor, cost in graph.get_neighbors(current_node).items():
            if neighbor not in closed_set:
                new_g_score = g_score + cost
                h_score = graph.heuristic(neighbor, goal_nodes)
                new_f_score = new_g_score + h_score
                new_path = path + [neighbor]
                heapq.heappush(open_set, (new_f_score, new_g_score, neighbor, new_path))

    if nodes_expanded >= steps_limit:
        open_list_formatted = [f"{node} ({f})" for f, g, node, p in open_set]
        return open_list_formatted 
    return None 

class IdaStarSearcher:
    def __init__(self, graph, start_node, goal_nodes, steps_limit):
        self.graph = graph
        self.start_node = start_node
        self.goal_nodes = set(goal_nodes) 
        self.steps_limit = steps_limit
        self.nodes_expanded = 0
        self.found_goal = None
        self.limit_reached = False

    def _search_recursive(self, node, g_score, path, threshold):
        if self.nodes_expanded >= self.steps_limit:
            self.limit_reached = True
            return threshold, True 
        self.nodes_expanded += 1

        h_score = self.graph.heuristic(node, self.goal_nodes)
        f_score = g_score + h_score

        if f_score > threshold:
            return f_score, False 
        if node in self.goal_nodes:
            self.found_goal = node
            print(f"Debug: IDA* Goal {node} found. Path: {path}") 
            return threshold, True 
        min_next_threshold = float('inf')
        limit_hit_in_subtree = False

        neighbors = sorted(
            self.graph.get_neighbors(node).items(),
            key=lambda item: self.graph.heuristic(item[0], self.goal_nodes)
        )

        for neighbor, cost in neighbors:
            if neighbor not in path: 
                new_path = path + (neighbor,) 
                next_threshold, status = self._search_recursive(
                    neighbor, g_score + cost, new_path, threshold
                )
                if self.found_goal is not None or self.limit_reached:
                    return threshold, True 

                min_next_threshold = min(min_next_threshold, next_threshold)

        return min_next_threshold, False 

    def search(self):
        threshold = self.graph.heuristic(self.start_node, self.goal_nodes)
        path = (self.start_node,) 
        while True:
            print(f"Debug: IDA* Iteration with threshold: {threshold}") 
            self.nodes_expanded = 0 # Reset counter for each iteration (or keep cumulative?)
                                    # Let's keep it cumulative to match A* step limit interpretation
            # If using cumulative, check limit *before* starting search iteration
            if self.nodes_expanded >= self.steps_limit:
                 self.limit_reached = True
                 break

            next_threshold, status = self._search_recursive(self.start_node, 0, path, threshold)

            if self.found_goal is not None:
                return self.found_goal 
            if self.limit_reached:
                return f"IDA* stopped after {self.steps_limit} node expansions."
            if next_threshold == float('inf'):
                return None 
            if next_threshold <= threshold:
                 # safety break
                 print("Warning: IDA* threshold did not increase.")
                 return None
            threshold = next_threshold 

if __name__ == "__main__":
    g = Graph()

    try:
        start_node = int(input("Enter start node: "))
        if start_node not in g.coords: raise ValueError("Invalid start node")

        goal_nodes_str = input("Enter goal nodes (space-separated): ").split()
        goal_nodes = [int(g_node) for g_node in goal_nodes_str]
        if not goal_nodes: raise ValueError("At least one goal node required")
        for g_node in goal_nodes:
            if g_node not in g.coords: raise ValueError(f"Invalid goal node: {g_node}")

        steps = int(input("Enter number of steps (n): "))
        if steps <= 0: raise ValueError("Number of steps must be positive")

        algorithm = input("Enter search algorithm (A* or IDA*): ").strip().upper()

        result = None
        if algorithm == "A*":
            print(f"\nRunning A* from {start_node} to {goal_nodes} with step limit {steps}...")
            result = astar_search(g, start_node, goal_nodes, steps)
        elif algorithm == "IDA*":
            print(f"\nRunning IDA* from {start_node} to {goal_nodes} with step limit {steps}...")
            ida_searcher = IdaStarSearcher(g, start_node, goal_nodes, steps)
            result = ida_searcher.search()
        else:
            print("Invalid algorithm choice. Please enter A* or IDA*.")

        if result is not None:
            if isinstance(result, int): 
                print(f"\nOutput: {result}")
            elif isinstance(result, list): 
                print(f"\nOutput for n {steps}: {result}")
            elif isinstance(result, str):
                 print(f"\nOutput: {result}")
            else:
                 print(f"\nUnexpected result type: {result}")

        else:
            print("\nNo solution found within the given constraints.")

    except ValueError as e:
        print(f"Input Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")