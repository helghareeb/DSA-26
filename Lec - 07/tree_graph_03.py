import tkinter as tk
from tkinter import ttk
from collections import deque

# =======================================
#              CONSTANTS
# =======================================

MODE_TREE = "Tree Traversal"
MODE_GRAPH = "Graph Traversal"

# ----- Graph structure (small undirected graph) -----
GRAPH_STRUCT = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "F"],
    "D": ["B"],
    "E": ["B", "F"],
    "F": ["C", "E"],
}

GRAPH_POSITIONS = {
    "A": (150, 80),
    "B": (80, 200),
    "C": (220, 200),
    "D": (40, 320),
    "E": (120, 320),
    "F": (260, 320),
}

# ----- Tree structure (perfect binary tree of height 2) -----
TREE_STRUCT = {
    "1": ["2", "3"],
    "2": ["4", "5"],
    "3": ["6", "7"],
    "4": [],
    "5": [],
    "6": [],
    "7": [],
}

TREE_ROOT = "1"

TREE_POSITIONS = {
    "1": (250, 60),
    "2": (150, 150),
    "3": (350, 150),
    "4": (100, 260),
    "5": (200, 260),
    "6": (300, 260),
    "7": (400, 260),
}

NODE_RADIUS = 22


# =======================================
#       GRAPH TRAVERSAL STATE BUILDERS
# =======================================

def build_dfs_states(graph, start):
    """
    Graph DFS (iterative) – builds a list of states.
    kind = 'GRAPH_DFS'
    frontier = stack (LIFO)
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
                "kind": "GRAPH_DFS",
            })
            continue

        visited_set.add(u)
        visited.append(u)

        # Push neighbors in reverse order so left-most neighbor is processed first
        for v in reversed(graph[u]):
            if v not in visited_set:
                stack.append(v)

        states.append({
            "current": u,
            "frontier": list(stack),
            "visited": list(visited),
            "kind": "GRAPH_DFS",
        })

    return states


def build_bfs_states(graph, start):
    """
    Graph BFS – builds a list of states.
    kind = 'GRAPH_BFS'
    frontier = queue (FIFO)
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
            "kind": "GRAPH_BFS",
        })

    return states


# =======================================
#        TREE TRAVERSAL (ITERATIVE)
#        Pre / In / Post / DFS / BFS
# =======================================

def get_children(tree, node):
    children = tree.get(node, [])
    left = children[0] if len(children) > 0 else None
    right = children[1] if len(children) > 1 else None
    return left, right


def build_tree_preorder_states(tree, root):
    """
    Iterative Preorder (Root, Left, Right) using explicit stack.
    kind = 'TREE_PRE_DFS'
    """
    if root not in tree:
        return []

    stack = [root]
    visited = []
    states = []

    while stack:
        node = stack.pop()
        if node is None:
            continue
        visited.append(node)

        left, right = get_children(tree, node)
        # Stack: push right then left so left is processed first
        if right is not None:
            stack.append(right)
        if left is not None:
            stack.append(left)

        states.append({
            "current": node,
            "frontier": list(stack),
            "visited": list(visited),
            "kind": "TREE_PRE_DFS",
        })

    return states


def build_tree_inorder_states(tree, root):
    """
    Iterative Inorder (Left, Root, Right) using explicit stack.
    kind = 'TREE_IN_DFS'
    """
    if root not in tree:
        return []

    stack = []
    current = root
    visited = []
    states = []

    while stack or current is not None:
        while current is not None:
            stack.append(current)
            left, _ = get_children(tree, current)
            current = left

        current = stack.pop()
        visited.append(current)

        states.append({
            "current": current,
            "frontier": list(stack),
            "visited": list(visited),
            "kind": "TREE_IN_DFS",
        })

        _, right = get_children(tree, current)
        current = right

    return states


def build_tree_postorder_states(tree, root):
    """
    Iterative Postorder (Left, Right, Root) using explicit stack.
    We use (node, expanded) flag.
    kind = 'TREE_POST_DFS'
    """
    if root not in tree:
        return []

    stack = [(root, False)]
    visited = []
    states = []

    while stack:
        node, expanded = stack.pop()
        if node is None:
            continue

        if expanded:
            visited.append(node)
            states.append({
                "current": node,
                "frontier": [n for (n, _) in stack],
                "visited": list(visited),
                "kind": "TREE_POST_DFS",
            })
        else:
            # Postorder: Left, Right, Node
            # Stack is LIFO, so push Node (expanded), then Right, then Left
            stack.append((node, True))
            left, right = get_children(tree, node)
            if right is not None:
                stack.append((right, False))
            if left is not None:
                stack.append((left, False))

    return states


def build_tree_dfs_generic_states(tree, root):
    """
    Generic DFS on tree using stack (similar to Preorder).
    kind = 'TREE_DFS'
    """
    if root not in tree:
        return []

    stack = [root]
    visited = []
    states = []

    while stack:
        node = stack.pop()
        if node is None:
            continue
        visited.append(node)

        left, right = get_children(tree, node)
        if right is not None:
            stack.append(right)
        if left is not None:
            stack.append(left)

        states.append({
            "current": node,
            "frontier": list(stack),
            "visited": list(visited),
            "kind": "TREE_DFS",
        })

    return states


def build_tree_bfs_states(tree, root):
    """
    BFS / Level-order on tree using queue.
    kind = 'TREE_BFS'
    """
    if root not in tree:
        return []

    q = deque([root])
    visited = []
    states = []

    while q:
        u = q.popleft()
        visited.append(u)
        for v in tree[u]:
            q.append(v)

        states.append({
            "current": u,
            "frontier": list(q),
            "visited": list(visited),
            "kind": "TREE_BFS",
        })

    return states


# =======================================
#            DRAWING CANVAS
# =======================================

class GraphCanvas:
    def __init__(self, root):
        self.canvas = tk.Canvas(root, width=500, height=380, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.graph = {}
        self.positions = {}
        self.node_items = {}

    def set_structure(self, graph, positions):
        """Clear and redraw structure (tree or graph)."""
        self.graph = graph
        self.positions = positions
        self.canvas.delete("all")
        self.node_items = {}
        self._draw_graph()

    def _draw_graph(self):
        drawn_edges = set()
        # Draw edges
        for u, neighbors in self.graph.items():
            if u not in self.positions:
                continue
            x1, y1 = self.positions[u]
            for v in neighbors:
                if v not in self.positions:
                    continue
                edge_key = tuple(sorted((u, v)))
                if edge_key in drawn_edges:
                    continue
                x2, y2 = self.positions[v]
                self.canvas.create_line(x1, y1, x2, y2, width=2)
                drawn_edges.add(edge_key)

        # Draw nodes
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
        self.highlight_node(node, "#FFA500")  # current node

    def mark_visited(self, node):
        self.highlight_node(node, "#90EE90")  # visited node


# =======================================
#          MAIN APP / CONTROLLER
# =======================================

class TraversalApp:
    def __init__(self, root):
        self.root = root
        self.graph_canvas = GraphCanvas(root)

        self.controls = tk.Frame(root, padx=10, pady=10)
        self.controls.pack(side=tk.RIGHT, fill=tk.Y)

        # ------- Mode selection: Tree / Graph -------
        tk.Label(self.controls, text="Mode:", font=("Arial", 11, "bold")).pack(anchor="w")
        self.mode_var = tk.StringVar(value=MODE_TREE)
        self.mode_menu = ttk.Combobox(
            self.controls,
            textvariable=self.mode_var,
            values=[MODE_TREE, MODE_GRAPH],
            state="readonly",
            width=18,
        )
        self.mode_menu.pack(anchor="w", pady=(0, 8))
        self.mode_menu.bind("<<ComboboxSelected>>", self.on_mode_change)

        # ------- Description -------
        tk.Label(self.controls, text="Description:", font=("Arial", 11, "bold")).pack(anchor="w")
        self.description_label = tk.Label(
            self.controls,
            text="",
            font=("Arial", 9),
            justify="left",
            wraplength=260,
        )
        self.description_label.pack(anchor="w", pady=(0, 8))

        # ------- Start / Root node -------
        tk.Label(self.controls, text="Start / Root node:", font=("Arial", 11, "bold")).pack(anchor="w")
        self.start_var = tk.StringVar(value="")
        self.start_menu = ttk.Combobox(
            self.controls,
            textvariable=self.start_var,
            values=[],
            state="readonly",
            width=5,
        )
        self.start_menu.pack(anchor="w", pady=(0, 8))

        # ------- Algorithm selection -------
        tk.Label(self.controls, text="Traversal algorithm:", font=("Arial", 11, "bold")).pack(anchor="w")
        self.algorithm_var = tk.StringVar(value="")
        self.algorithm_menu = ttk.Combobox(
            self.controls,
            textvariable=self.algorithm_var,
            values=[],
            state="readonly",
            width=18,
        )
        self.algorithm_menu.pack(anchor="w", pady=(0, 10))

        # ------- Buttons -------
        btn_frame = tk.Frame(self.controls)
        btn_frame.pack(fill="x", pady=5)

        self.btn_run = tk.Button(btn_frame, text="Run Auto", command=self.run_auto, width=10)
        self.btn_run.grid(row=0, column=0, padx=2, pady=2)

        self.btn_step = tk.Button(btn_frame, text="Step ▶", command=self.step_once, width=10)
        self.btn_step.grid(row=0, column=1, padx=2, pady=2)

        self.btn_reset = tk.Button(btn_frame, text="Reset", command=self.reset, width=10)
        self.btn_reset.grid(row=1, column=0, padx=2, pady=2)

        # ------- Info labels -------
        tk.Label(self.controls, text="Current:", font=("Arial", 11, "bold")).pack(anchor="w", pady=(10, 0))
        self.current_label = tk.Label(self.controls, text="-", font=("Arial", 11))
        self.current_label.pack(anchor="w")

        tk.Label(self.controls, text="Visited order:", font=("Arial", 11, "bold")).pack(anchor="w", pady=(10, 0))
        self.visited_label = tk.Label(
            self.controls, text="[]", font=("Consolas", 9),
            justify="left", wraplength=260
        )
        self.visited_label.pack(anchor="w")

        tk.Label(self.controls, text="Frontier (stack/queue):", font=("Arial", 11, "bold")).pack(anchor="w", pady=(10, 0))
        self.frontier_label = tk.Label(
            self.controls, text="[]", font=("Consolas", 9),
            justify="left", wraplength=260
        )
        self.frontier_label.pack(anchor="w")

        tk.Label(
            self.controls,
            text="DFS & tree traversals: use a stack.\n"
                 "BFS & level-order: use a queue.",
            font=("Arial", 8),
            fg="gray25",
            justify="left",
            wraplength=260,
        ).pack(anchor="w", pady=(5, 0))

        # ------- Speed control -------
        tk.Label(self.controls, text="Animation delay (ms):", font=("Arial", 11, "bold")).pack(anchor="w", pady=(10, 0))
        self.speed_var = tk.IntVar(value=700)
        self.speed_scale = tk.Scale(
            self.controls,
            from_=100,
            to=2000,
            orient=tk.HORIZONTAL,
            variable=self.speed_var,
        )
        self.speed_scale.pack(fill="x")

        # Simulation state
        self.states = []
        self.index = 0
        self.running = False

        # Initial mode = Tree
        self.configure_for_mode(MODE_TREE)

    # -------- Mode configuration --------

    def configure_for_mode(self, mode):
        if mode == MODE_TREE:
            self.graph_canvas.set_structure(TREE_STRUCT, TREE_POSITIONS)
            nodes = sorted(TREE_STRUCT.keys(), key=lambda x: int(x))
            self.start_menu["values"] = nodes
            self.start_var.set(TREE_ROOT)
            self.algorithm_menu["values"] = [
                "Preorder (DFS)",
                "Inorder (DFS)",
                "Postorder (DFS)",
                "DFS (Tree)",
                "BFS (Tree / Level-order)",
            ]
            self.algorithm_var.set("Preorder (DFS)")

            desc = (
                "Tree Traversal mode:\n"
                f"- Nodes: {len(TREE_STRUCT)}\n"
                f"- Root: {TREE_ROOT}\n"
                "- Parent-child relations:\n"
                "  1 → [2, 3]\n"
                "  2 → [4, 5]\n"
                "  3 → [6, 7]\n\n"
                "Traversals (all DFS except BFS):\n"
                "- Preorder (Root, Left, Right)\n"
                "- Inorder (Left, Root, Right)\n"
                "- Postorder (Left, Right, Root)\n"
                "- DFS (Tree) ~ preorder DFS\n"
                "- BFS (Tree / Level-order) ~ queue-based BFS"
            )
            self.description_label.config(text=desc)
        else:
            self.graph_canvas.set_structure(GRAPH_STRUCT, GRAPH_POSITIONS)
            nodes = sorted(GRAPH_STRUCT.keys())
            self.start_menu["values"] = nodes
            self.start_var.set("A")
            self.algorithm_menu["values"] = ["DFS", "BFS"]
            self.algorithm_var.set("DFS")

            edge_set = set()
            for u, nbrs in GRAPH_STRUCT.items():
                for v in nbrs:
                    edge_set.add(tuple(sorted((u, v))))
            desc = (
                "Graph Traversal mode:\n"
                f"- Nodes: {len(GRAPH_STRUCT)}\n"
                f"- Undirected edges: {len(edge_set)}\n\n"
                "Adjacency example:\n"
                "  A → [B, C]\n"
                "  B → [A, D, E]\n"
                "  C → [A, F]\n\n"
                "Traversals:\n"
                "- Depth-First Search (DFS) using stack\n"
                "- Breadth-First Search (BFS) using queue"
            )
            self.description_label.config(text=desc)

        self.reset()

    def on_mode_change(self, event):
        mode = self.mode_var.get()
        self.configure_for_mode(mode)

    # -------- State preparation --------

    def prepare_states(self):
        mode = self.mode_var.get()
        algo = self.algorithm_var.get()
        start = self.start_var.get()

        if mode == MODE_GRAPH:
            if algo == "DFS":
                self.states = build_dfs_states(GRAPH_STRUCT, start)
            else:
                self.states = build_bfs_states(GRAPH_STRUCT, start)
        else:
            # Tree mode
            root = start if start in TREE_STRUCT else TREE_ROOT

            if algo.startswith("Preorder"):
                self.states = build_tree_preorder_states(TREE_STRUCT, root)
            elif algo.startswith("Inorder"):
                self.states = build_tree_inorder_states(TREE_STRUCT, root)
            elif algo.startswith("Postorder"):
                self.states = build_tree_postorder_states(TREE_STRUCT, root)
            elif algo.startswith("DFS"):
                self.states = build_tree_dfs_generic_states(TREE_STRUCT, root)
            else:  # BFS (Tree / Level-order)
                self.states = build_tree_bfs_states(TREE_STRUCT, root)

        self.index = 0

    # -------- Controls: Run / Step / Reset --------

    def run_auto(self):
        self.prepare_states()
        if not self.states:
            return
        self.running = True
        self._auto_step()

    def step_once(self):
        if not self.states:
            self.prepare_states()
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
        visited = state["visited"]
        frontier = state["frontier"]
        kind = state["kind"]

        # Update colors
        self.graph_canvas.reset_colors()
        for node in visited:
            self.graph_canvas.mark_visited(node)
        self.graph_canvas.emphasize_node(current)

        # Update labels
        self.current_label.config(text=current)
        self.visited_label.config(text=str(visited))

        # Decide how to display frontier
        if "DFS" in kind:
            self.frontier_label.config(text=f"{frontier}   (stack, top → right)")
        elif "BFS" in kind:
            self.frontier_label.config(text=f"{frontier}   (queue, front → left)")
        else:
            self.frontier_label.config(text=str(frontier))

        self.index += 1

    def _auto_step(self):
        if not self.running:
            return
        self._do_step()
        if self.index < len(self.states):
            delay = self.speed_var.get()
            self.root.after(delay, self._auto_step)

    def reset(self):
        self.graph_canvas.reset_colors()
        self.states = []
        self.index = 0
        self.running = False
        self.current_label.config(text="-")
        self.visited_label.config(text="[]")
        self.frontier_label.config(text="[]")


# =======================================
#                 MAIN
# =======================================

def main():
    root = tk.Tk()
    root.title("Tree & Graph Traversal Simulator")
    app = TraversalApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
