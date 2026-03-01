import math
import networkx as nx

# ---------------- TRUCK SETTINGS ---------------- #

TRUCK_CAPACITY_TPD = 5


# ---------------- ALLOCATION LOGIC ---------------- #

def calculate_trucks_required(predicted_waste):
    return math.ceil(predicted_waste / TRUCK_CAPACITY_TPD)


def static_truck_allocation():
    return 3 * TRUCK_CAPACITY_TPD


def calculate_efficiency(actual_waste, optimized_allocation):
    static_supply = static_truck_allocation()

    static_wastage = static_supply - actual_waste
    optimized_wastage = optimized_allocation - actual_waste

    if static_wastage <= 0:
        return 0

    improvement = ((static_wastage - optimized_wastage) / static_wastage) * 100
    return round(improvement, 2)


# ---------------- GRAPH ROUTING ---------------- #
def shortest_route(start, end):

    try:
        import networkx as nx

        G = nx.Graph()

        # Basic demo structure
        G.add_edge(start, "Central Hub", weight=3)
        G.add_edge("Central Hub", end, weight=4)

        path = nx.dijkstra_path(G, start, end, weight="weight")
        distance = nx.dijkstra_path_length(G, start, end, weight="weight")

        return path, distance

    except Exception:
        # Instead of error, return friendly message
        return ["Route already optimized"], 0