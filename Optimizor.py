import networkx as nx


def minimum_cost(costs, capacities):
    """
    Minimize total assignment cost while respecting hospital capacities.

    Args:
        costs: Integer cost matrix; costs[i][j] assigns doctor i to hospital j.
        capacities: Nonnegative integer capacity of each hospital.

    Returns:
        assignments: Dictionary mapping doctor index to hospital index (0-based).
        total_cost: Minimum total assignment cost.

    Raises:
        ValueError: If dimensions are inconsistent or capacity is insufficient.
    """
    n = len(costs)
    m = len(capacities)

    if any(len(row) != m for row in costs):
        raise ValueError("Each cost row must have one entry per hospital.")

    if any(capacity < 0 for capacity in capacities):
        raise ValueError("Hospital capacities cannot be negative.")

    if sum(capacities) < n:
        raise ValueError("Insufficient hospital capacity to assign all doctors.")

    if n == 0:
        return {}, 0

    graph = nx.DiGraph()
    graph.add_node("S", demand=-n)
    graph.add_node("T", demand=n)

    for i in range(n):
        doctor = ("doctor", i)
        graph.add_node(doctor, demand=0)
        graph.add_edge("S", doctor, capacity=1, weight=0)

    for j in range(m):
        hospital = ("hospital", j)
        graph.add_node(hospital, demand=0)
        graph.add_edge(hospital, "T", capacity=capacities[j], weight=0)

    for i in range(n):
        for j in range(m):
            graph.add_edge(
                ("doctor", i),
                ("hospital", j),
                capacity=1,
                weight=costs[i][j],
            )

    flow = nx.min_cost_flow(graph)

    assignments = {
        i: j
        for i in range(n)
        for j in range(m)
        if flow[("doctor", i)][("hospital", j)] == 1
    }
    total_cost = nx.cost_of_flow(graph, flow)

    return assignments, total_cost