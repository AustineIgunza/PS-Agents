"""
Practical Exercise 3 Part 2 - Uniform Cost Search
Problem : A self-driving trailer traverses Kenya's Highway Network
          from Nairobi to Kisumu at the lowest possible path cost.
Method  : The four steps of a problem-solving agent -
          1. Goal Formulation
          2. Problem Formulation
          3. Search      (Uniform Cost Search / Dijkstra)
          4. Execute
"""

import heapq
from itertools import count



# STATE SPACE  -  the directed graph from Part 1 of the exercise
# Each state is a town. Each action is a journey along a highway to an
# adjacent town. Each step cost is the road distance in kilometres.

TOWNS = {
    "Nairobi":    "Nairobi",
    "Thika":      "Central Highlands",
    "Nyeri":      "Central Highlands",
    "Nyahururu":  "Central Highlands",
    "Naivasha":   "Rift Valley",
    "Narok":      "Rift Valley",
    "Nakuru":     "Rift Valley",
    "Bomet":      "Rift Valley",
    "Kericho":    "Rift Valley",
    "Eldoret":    "Rift Valley",
    "Kisii":      "Lake Victoria Basin",
    "Kakamega":   "Lake Victoria Basin",
    "Kisumu":     "Lake Victoria Basin",
}

# GRAPH[state] = [(successor_state, step_cost_km, highway)]
GRAPH = {
    "Nairobi":   [("Thika",      45, "A2"),
                  ("Naivasha",   90, "A104"),
                  ("Narok",     142, "B3")],
    "Thika":     [("Nyeri",     106, "A2")],
    "Nyeri":     [("Nyahururu", 104, "B5")],
    "Nyahururu": [("Nakuru",     64, "B5")],
    "Naivasha":  [("Nakuru",     71, "A104"),
                  ("Narok",      90, "B3")],
    "Narok":     [("Bomet",      97, "B3")],
    "Nakuru":    [("Kericho",   110, "B1"),
                  ("Eldoret",   155, "A104")],
    "Bomet":     [("Kericho",    50, "C23"),
                  ("Kisii",      68, "B3")],
    "Kericho":   [("Kisumu",     90, "B1"),
                  ("Kisii",      85, "C23")],
    "Eldoret":   [("Kakamega",   80, "A104/B2")],
    "Kisii":     [("Kisumu",    118, "B1")],
    "Kakamega":  [("Kisumu",     52, "B2")],
    "Kisumu":    [],
}

INITIAL_STATE = "Nairobi"
GOAL_STATE = "Kisumu"

LINE = "=" * 78
THIN = "-" * 78


# NODE  -  a node in the search tree

class Node:
    """A node in the search tree: a state, its parent, the action that got
    here, and g(n), the cumulative path cost from the initial state."""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def expand(self):
        """Apply all legal actions to this state and return the child nodes."""
        children = []
        for successor, step_cost, highway in GRAPH[self.state]:
            action = f"travel {self.state} -> {successor} via {highway}"
            children.append(
                Node(successor, self, action, self.path_cost + step_cost)
            )
        return children

    def path(self):
        """Walk back up the parent links to recover the full path."""
        node, states = self, []
        while node:
            states.append(node.state)
            node = node.parent
        return list(reversed(states))

    def __repr__(self):
        return f"{self.state}({self.path_cost})"


# STEP 1  -  GOAL FORMULATION
def goal_formulation():
    print(LINE)
    print("STEP 1: GOAL FORMULATION")
    print(LINE)
    print(f"  Agent        : Self-driving trailer")
    print(f"  Environment  : Kenya's Highway Network")
    print(f"  Initial state: {INITIAL_STATE}")
    print(f"  Goal state   : {GOAL_STATE}")
    print()


# STEP 2  -  PROBLEM FORMULATION
def goal_test(state):
    """Factor 3: has the agent reached the goal state?"""
    return state == GOAL_STATE


def problem_formulation():
    print(LINE)
    print("STEP 2: PROBLEM FORMULATION")
    print(LINE)
    print(f"  1. Initial state      : {INITIAL_STATE}")
    print(f"  2. State space        : {len(TOWNS)} towns, "
          f"{sum(len(v) for v in GRAPH.values())} directed links (actions)")
    print(f"  3. Goal test          : is the trailer's current state "
          f"'{GOAL_STATE}'?")
    print(f"  4. Path cost function : g(n) = sum of step costs, where each")
    print(f"                          step cost is road distance in km")
    print()
    print("  Abstraction applied: low-level actions (steer, brake, accelerate)")
    print("  are collapsed into a single action 'travel(Town A -> Town B)'.")
    print()
    print(f"  {'FROM':<12}{'TO':<12}{'HIGHWAY':<10}{'STEP COST (km)':>15}")
    print(f"  {THIN[:49]}")
    for state in GRAPH:
        for successor, cost, highway in GRAPH[state]:
            print(f"  {state:<12}{successor:<12}{highway:<10}{cost:>15}")
    print()


# STEP 3  -  SEARCH (Uniform Cost Search)
def uniform_cost_search(verbose=True):
    """Uniform Cost Search.
    The frontier is a priority queue ordered by g(n), so the node with the
    lowest path cost is always expanded next. The goal test is applied when
    a node is EXPANDED (not when it is generated) - this is what guarantees
    the first goal node reached is the optimal one.
    """
    if verbose:
        print(LINE)
        print("STEP 3: SEARCH  -  UNIFORM COST SEARCH")
        print(LINE)
        print("  Strategy: always expand the frontier node with the lowest g(n)")
        print()

    tie = count()                      # keeps the heap stable for equal costs
    root = Node(INITIAL_STATE)
    frontier = [(root.path_cost, next(tie), root)]
    frontier_states = {INITIAL_STATE: 0}   # state -> best g(n) on the frontier
    explored = {}                          # state -> final g(n)
    step = 0
    discarded = []

    while frontier:
        cost, _, node = heapq.heappop(frontier)

        # Skip stale heap entries left behind by a cheaper replacement
        if node.state in explored:
            continue

        step += 1
        frontier_states.pop(node.state, None)
        explored[node.state] = node.path_cost

        # --- GOAL TEST on expansion ---
        if goal_test(node.state):
            if verbose:
                print(f"  Step {step:>2}: EXPAND {node.state:<11} "
                      f"g = {node.path_cost:<5}<-- GOAL TEST PASSED")
                print()
                print(f"  Search terminates after {step} expansions.")
                print()
            return node, explored, discarded

        # --- EXPANSION: apply all legal actions ---
        notes = []
        for child in node.expand():
            if child.state in explored:
                notes.append(f"{child.state} {child.path_cost} already explored"
                             f" at {explored[child.state]}")
                discarded.append((child.state, child.path_cost,
                                  explored[child.state]))
            elif child.state in frontier_states and \
                    frontier_states[child.state] <= child.path_cost:
                notes.append(f"{child.state} {child.path_cost} worse than "
                             f"{frontier_states[child.state]}")
                discarded.append((child.state, child.path_cost,
                                  frontier_states[child.state]))
            else:
                frontier_states[child.state] = child.path_cost
                heapq.heappush(frontier, (child.path_cost, next(tie), child))

        if verbose:
            queue = ", ".join(
                f"{s} {g}" for s, g in sorted(frontier_states.items(),
                                              key=lambda kv: kv[1])
            )
            print(f"  Step {step:>2}: EXPAND {node.state:<11} g = {node.path_cost}")
            print(f"           Frontier : {queue if queue else '(empty)'}")
            if notes:
                print(f"           Discarded: {'; '.join(notes)}")
            print()

    return None, explored, discarded


# STEP 4  -  EXECUTE
def execute(solution):
    print(LINE)
    print("STEP 4: EXECUTE  -  OPTIMAL SOLUTION")
    print(LINE)

    if solution is None:
        print("  No path found from "
              f"{INITIAL_STATE} to {GOAL_STATE}.")
        return

    path = solution.path()

    # Rebuild the sequence of actions with their individual step costs
    print(f"  {'#':<4}{'ACTION':<46}{'STEP COST':>12}{'g(n)':>10}")
    print(f"  {THIN[:72]}")
    running = 0
    for i in range(len(path) - 1):
        a, b = path[i], path[i + 1]
        step_cost, highway = next((c, h) for s, c, h in GRAPH[a] if s == b)
        running += step_cost
        print(f"  {i + 1:<4}{a + ' -> ' + b + '  (' + highway + ')':<46}"
              f"{step_cost:>12}{running:>10}")
    print(f"  {THIN[:72]}")

    print()
    print("  OPTIMAL PATH :  " + "  ->  ".join(path))
    print("  PATH COST    :  " +
          " + ".join(
              str(next(c for s, c, _ in GRAPH[path[i]] if s == path[i + 1]))
              for i in range(len(path) - 1)
          ) + f" = {solution.path_cost} km")
    print()
    print(f"  The trailer travels {solution.path_cost} km from {INITIAL_STATE} "
          f"to {GOAL_STATE}.")
    print("  This is the optimal solution because uniform cost search returns")
    print("  the path with the LEAST path cost.")
    print()


# VERIFICATION  -  enumerate every path and confirm the UCS result
def all_paths(state, goal, visited=None):
    """Depth-first enumeration of all simple paths, for verification."""
    visited = visited or [state]
    if state == goal:
        yield list(visited), 0
        return
    for successor, cost, _ in GRAPH[state]:
        if successor not in visited:
            for path, total in all_paths(successor, goal, visited + [successor]):
                yield path, total + cost


def verify(solution):
    print(LINE)
    print("VERIFICATION: ALL CANDIDATE ROUTES")
    print(LINE)
    routes = sorted(all_paths(INITIAL_STATE, GOAL_STATE), key=lambda r: r[1])
    print(f"  {'#':<4}{'ROUTE':<72}{'COST (km)':>11}")
    print(f"  {'-' * 87}")
    for i, (path, total) in enumerate(routes, 1):
        marker = "   <-- OPTIMAL" if i == 1 else ""
        print(f"  {i:<4}{' -> '.join(path):<72}{total:>11}{marker}")
    print()
    best_path, best_cost = routes[0]
    match = (best_cost == solution.path_cost and best_path == solution.path())
    print(f"  Total distinct routes                     : {len(routes)}")
    print(f"  Cheapest route found by exhaustive search : {best_cost} km")
    print(f"  Route returned by uniform cost search     : {solution.path_cost} km")
    print(f"  UCS returned the optimal path             : {match}")
    print()


# MAIN
def main():
    print()
    print ("ARTIFICIAL INTELLIGENCE  -  PRACTICAL EXERCISE 3")
    print("  PROBLEM-SOLVING AGENT: SELF-DRIVING TRAILER")
    print("  UNIFORM COST SEARCH ACROSS KENYA'S HIGHWAY NETWORK")
    print()

    goal_formulation()
    problem_formulation()
    solution, explored, discarded = uniform_cost_search(verbose=True)
    execute(solution)
    verify(solution)

    print(f"  States expanded: {len(explored)}   "
          f"Nodes discarded: {len(discarded)}")
    print()


if __name__ == "__main__":
    main()
