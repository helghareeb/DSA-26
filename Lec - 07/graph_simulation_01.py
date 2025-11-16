import tkinter as tk
from tkinter import ttk
from collections import deque

# =======================================
#           GRAPH DEFINITION
# =======================================

GRAPH = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "F"],
    "D": ["B"],
    "E": ["B", "F"],
    "F": ["C", "E"],
}

NODE_POSITIONS = {
    "A": (150, 80),
    "B": (80, 200),
    "C": (220, 200),
    "D": (40, 320),
    "E": (120, 320),
    "F": (260, 320),
}

NODE_RADIUS = 22


# =======================================
#       ALGORITHM TRACE BUILDERS
# =======================================

def build_dfs_states(graph, start):
    """
    Build a list of states for iterative DFS.

    Each state:
      {
        'current': node_being_processed,
        'frontier': [stack contents, top is RIGHT],
        'visited': [nodes_visited_so_far_in_order],
        'kind': 'DFS'
      }
    """
    if start not in graph:
        return []

    stack = [start]
    visited = []
    visited_set = set()
    states = []

    while stack:
        u = stack.pop()
        if u in visited_set:
            states.append({
                "current": u,
                "frontier": list(stack),
                "visited": list(visited),
                "kind": "DFS",
            })
            continue

        visited_set.add(u)
        visited.append(u)

        # Reverse neighbors to mimic recursive DFS order
        for v in reversed(graph[u]):
            if v not in visited_set:
                stack.append(v)

        states.append({
            "current": u,
            "frontier": list(stack),
            "visited": list(visited),
            "kind": "DFS",
        })

    return states


def build_bfs_states(graph, start):
    """
    Build a list of states for iterative BFS.

    Each state:
      {
        'current': node_being_processed,
        'frontier': [queue contents, front is LEFT],
        'visited': [nodes_visited_so_far_in_order],
        'kind': 'BFS'
      }
    """
    if start not in graph:
        return []

    q = deque([start])
    visited_set = {start}
    visited = []
    states = []

    while q:
        u = q.popleft()
        visited.append(u)

        for v in graph[u]:
            if v not in visited_set:
                visited_set.add(v)
                q.append(v)

        states.append({
            "current": u,
            "frontier": list(q),
            "visited": list(visited),
            "kind": "BFS",
        })

    return states


# =======================================
#             CANVAS CLASS
# =======================================

class GraphCanvas:
    def __init__(self, root, graph, positions):
        self.graph = graph
        self.positions = positions
        self.node_items = {}  # node -> (circle_id, text_id)
        self.canvas = tk.Canvas(root, width=500, height=400, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.draw_graph()

    def draw_graph(self):
        drawn_edges = set()
        for u, neighbors in self.graph.items():
            x1, y1 = self.positions[u]
            for v in neighbors:
                if (v, u) in drawn_edges:
                    continue
                x2, y2 = self.positions[v]
                self.canvas.create_line(x1, y1, x2, y2, width=2)
                drawn_edges.add((u, v))

        for node, (x, y) in self.positions.items():
            circle = self.canvas.create_oval(
                x - NODE_RADIUS,
                y - NODE_RADIUS,
                x + NODE_RADIUS,
                y + NODE_RADIUS,
                fill="#DDDDDD",
                outline="black",
                width=2,
            )
            text = self.canvas.create_text(x, y, text=node, font=("Arial", 14, "bold"))
            self.node_items[node] = (circle, text)

    def reset_colors(self):
        for node, (circle, _) in self.node_items.items():
            self.canvas.itemconfig(circle, fill="#DDDDDD")

    def highlight_node(self, node, color):
        if node in self.node_items:
            circle, _ = self.node_items[node]
            self.canvas.itemconfig(circle, fill=color)

    def emphasize_node(self, node):
        self.highlight_node(node, "#FFA500")  # orange

    def mark_visited(self, node):
        self.highlight_node(node, "#90EE90")  # light green


# =======================================
#         ANIMATOR WITH STACK/QUEUE
# =======================================

class AlgorithmAnimator:
    def __init__(self, root, graph_canvas, graph, controls_frame):
        self.root = root
        self.graph_canvas = graph_canvas
        self.graph = graph

        self.states = []
        self.index = 0
        self.running = False
        self.current_kind = None  # last prepared algorithm kind ("DFS"/"BFS")

        # ---------- UI on the right ----------

        # Start node
        tk.Label(controls_frame, text="Start node:", font=("Arial", 11, "bold")).pack(
            anchor="w", pady=(5, 0)
        )
        self.start_var = tk.StringVar(value="A")
        start_nodes = sorted(self.graph.keys())
        self.start_menu = ttk.Combobox(
            controls_frame,
            textvariable=self.start_var,
            values=start_nodes,
            state="readonly",
            width=5,
        )
        self.start_menu.pack(anchor="w", pady=(0, 5))

        # Algorithm selector (DFS / BFS)
        tk.Label(controls_frame, text="Algorithm:", font=("Arial", 11, "bold")).pack(
            anchor="w", pady=(5, 0)
        )
        self.algorithm_var = tk.StringVar(value="DFS")
        self.algorithm_menu = ttk.Combobox(
            controls_frame,
            textvariable=self.algorithm_var,
            values=["DFS", "BFS"],
            state="readonly",
            width=7,
        )
        self.algorithm_menu.pack(anchor="w", pady=(0, 10))

        btn_frame = tk.Frame(controls_frame)
        btn_frame.pack(fill="x", pady=5)

        # Auto-run buttons (still available)
        self.btn_dfs = tk.Button(
            btn_frame, text="Run DFS", command=self.run_dfs, width=10
        )
        self.btn_dfs.grid(row=0, column=0, padx=2, pady=2)

        self.btn_bfs = tk.Button(
            btn_frame, text="Run BFS", command=self.run_bfs, width=10
        )
        self.btn_bfs.grid(row=0, column=1, padx=2, pady=2)

        # Step + Reset
        self.btn_step = tk.Button(
            btn_frame, text="Step ▶", command=self.step_once, width=10
        )
        self.btn_step.grid(row=1, column=0, padx=2, pady=2)

        self.btn_reset = tk.Button(
            btn_frame, text="Reset", command=self.reset, width=10
        )
        self.btn_reset.grid(row=1, column=1, padx=2, pady=2)

        # Info labels
        tk.Label(
            controls_frame, text="Current algorithm:", font=("Arial", 11, "bold")
        ).pack(anchor="w", pady=(10, 0))
        self.algorithm_label = tk.Label(controls_frame, text="-", font=("Arial", 11))
        self.algorithm_label.pack(anchor="w")

        tk.Label(
            controls_frame, text="Currently visiting:", font=("Arial", 11, "bold")
        ).pack(anchor="w", pady=(10, 0))
        self.current_label = tk.Label(controls_frame, text="-", font=("Arial", 11))
        self.current_label.pack(anchor="w")

        tk.Label(
            controls_frame, text="Visited order:", font=("Arial", 11, "bold")
        ).pack(anchor="w", pady=(10, 0))
        self.visited_label = tk.Label(
            controls_frame, text="[]", font=("Consolas", 10),
            wraplength=230, justify="left"
        )
        self.visited_label.pack(anchor="w")

        tk.Label(
            controls_frame, text="Frontier (stack/queue):", font=("Arial", 11, "bold")
        ).pack(anchor="w", pady=(10, 0))
        self.frontier_label = tk.Label(
            controls_frame, text="[]", font=("Consolas", 10),
            wraplength=230, justify="left"
        )
        self.frontier_label.pack(anchor="w")

        tk.Label(
            controls_frame,
            text="DFS: frontier is a STACK (top = right).\n"
                 "BFS: frontier is a QUEUE (front = left).",
            font=("Arial", 9),
            justify="left",
            fg="gray25",
        ).pack(anchor="w", pady=(5, 0))

        # Speed control
        tk.Label(
            controls_frame, text="Animation delay (ms):", font=("Arial", 11, "bold")
        ).pack(anchor="w", pady=(10, 0))
        self.speed_var = tk.IntVar(value=800)
        self.speed_scale = tk.Scale(
            controls_frame,
            from_=100,
            to=2000,
            orient=tk.HORIZONTAL,
            variable=self.speed_var,
        )
        self.speed_scale.pack(fill="x")

    # ---------- Helpers ----------

    def prepare_algorithm(self, kind):
        start = self.start_var.get()
        if start not in self.graph:
            return

        self.reset_visual_only()

        if kind == "DFS":
            self.states = build_dfs_states(self.graph, start)
        else:
            self.states = build_bfs_states(self.graph, start)

        self.current_kind = kind
        self.algorithm_label.config(text=kind)
        self.index = 0
        self.running = False
        self.update_ui_for_state(None)

    def run_dfs(self):
        self.algorithm_var.set("DFS")
        self.prepare_algorithm("DFS")
        self.running = True
        self._auto_step()

    def run_bfs(self):
        self.algorithm_var.set("BFS")
        self.prepare_algorithm("BFS")
        self.running = True
        self._auto_step()

    def step_once(self):
        # Determine which algorithm is currently selected in the dropdown
        selected_kind = self.algorithm_var.get()

        # If states are empty OR algorithm has changed since last prepare,
        # re-prepare according to the selected algorithm.
        if not self.states or self.current_kind != selected_kind:
            self.prepare_algorithm(selected_kind)
            if not self.states:
                return

        self._do_step()

    def _do_step(self):
        if self.index >= len(self.states):
            self.running = False
            self.current_label.config(text="Finished")
            return

        state = self.states[self.index]
        current = state["current"]

        self.graph_canvas.emphasize_node(current)
        self.current_label.config(text=current)

        # Color visited nodes
        for node in state["visited"]:
            self.graph_canvas.mark_visited(node)

        self.update_ui_for_state(state)
        self.index += 1

    def _auto_step(self):
        if not self.running:
            return
        self._do_step()
        if self.index < len(self.states):
            delay = self.speed_var.get()
            self.root.after(delay, self._auto_step)

    def update_ui_for_state(self, state):
        if state is None:
            self.visited_label.config(text="[]")
            self.frontier_label.config(text="[]")
            return

        visited = state["visited"]
        frontier = state["frontier"]
        self.visited_label.config(text=str(visited))

        if state["kind"] == "DFS":
            self.frontier_label.config(
                text=f"{frontier}   (stack, top ➜ right)"
            )
        else:
            self.frontier_label.config(
                text=f"{frontier}   (queue, front ➜ left)"
            )

    def reset_visual_only(self):
        """Reset colors and labels, but keep algorithm dropdown etc."""
        self.graph_canvas.reset_colors()
        self.current_label.config(text="-")
        self.visited_label.config(text="[]")
        self.frontier_label.config(text="[]")

    def reset(self):
        self.reset_visual_only()
        self.states = []
        self.index = 0
        self.running = False
        self.current_kind = None
        self.algorithm_label.config(text="-")


# =======================================
#                MAIN APP
# =======================================

def main():
    root = tk.Tk()
    root.title("Graph Traversal Simulator (DFS/BFS + Stack/Queue)")

    graph_canvas = GraphCanvas(root, GRAPH, NODE_POSITIONS)

    controls_frame = tk.Frame(root, padx=10, pady=10)
    controls_frame.pack(side=tk.RIGHT, fill=tk.Y)

    AlgorithmAnimator(root, graph_canvas, GRAPH, controls_frame)

    root.mainloop()


if __name__ == "__main__":
    main()
