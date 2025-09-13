# network_graph.py
import networkx as nx
import random

def create_network_graph():
    G = nx.Graph()

    # Sample graph (you can customize the topology)
    G.add_edge('A', 'B', weight=5)
    G.add_edge('B', 'C', weight=3)
    G.add_edge('C', 'D', weight=2)
    G.add_edge('A', 'D', weight=10)
    G.add_edge('B', 'D', weight=6)
    G.add_edge('A', 'C', weight=8)

    return G

def simulate_traffic_congestion(G, congestion_value):
    for u, v in G.edges():
        G[u][v]['weight'] += congestion_value

def simulate_link_failure(G):
    if len(G.edges()) == 0:
        return
    edge = random.choice(list(G.edges()))
    G.remove_edge(*edge)
    return edge
