import networkx as nx
from pyvis.network import Network
import random
import os

GRAPH_FILE = "network_graph.html"

def create_network_graph():
    G = nx.Graph()
    G.add_edge('A', 'B', weight=10)
    G.add_edge('A', 'C', weight=15)
    G.add_edge('B', 'D', weight=20)
    G.add_edge('C', 'E', weight=12)
    G.add_edge('E', 'F', weight=8)
    G.add_edge('B', 'E', weight=18)
    G.add_edge('D', 'F', weight=15)
    return G

def add_congestion(G, u, v):
    if G.has_edge(u, v):
        G[u][v]['weight'] += random.randint(5, 15)

def reset_graph():
    return create_network_graph()

def generate_graph_visual(G, path=[], congested_links=[]):
    net = Network(height="600px", width="100%", directed=False)
    for node in G.nodes:
        color = 'red' if node == path[-1] else 'blue'
        net.add_node(node, label=node, color=color)

    for u, v, data in G.edges(data=True):
        edge_color = 'red' if (u, v) in congested_links or (v, u) in congested_links else 'gray'
        net.add_edge(u, v, value=data['weight'], title=f"Weight: {data['weight']}", color=edge_color)

    net.set_options("""
    var options = {
      "nodes": {
        "font": {
          "size": 20
        }
      },
      "edges": {
        "color": {
          "inherit": true
        },
        "smooth": false
      },
      "interaction": {
        "hover": true,
        "multiselect": false,
        "navigationButtons": true
      },
      "physics": {
        "enabled": true
      }
    }
    """)
    net.save_graph(GRAPH_FILE)
    return GRAPH_FILE
