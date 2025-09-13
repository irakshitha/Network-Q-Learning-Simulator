# app.py
import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
import time
from network_graph import create_network_graph, simulate_traffic_congestion, simulate_link_failure
from network_env import NetworkRoutingEnv
from stable_baselines3 import DQN
import heapq

st.set_page_config(layout="wide")
st.title("🚀 AI-Based Adaptive Routing Protocol Simulator")

# Load graph and model
G = create_network_graph()
model = DQN.load("models/adaptive_routing_model")

routers = list(G.nodes)

pos = nx.spring_layout(G)

def plot_network(current=None, destination=None, path=None):
    plt.figure(figsize=(8,6))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500)
    nx.draw_networkx_edges(G, pos, width=1)

    if current:
        nx.draw_networkx_nodes(G, pos, nodelist=[current], node_color='orange', node_size=700)
    if destination:
        nx.draw_networkx_nodes(G, pos, nodelist=[destination], node_color='green', node_size=700)
    if path:
        path_edges = list(zip(path[:-1], path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3)
    st.pyplot(plt)

def dijkstra_path(graph, start, end):
    visited = {start: 0}
    path = {}
    nodes = set(graph.nodes)

    while nodes:
        min_node = None
        for node in nodes:
            if node in visited:
                if min_node is None or visited[node] < visited[min_node]:
                    min_node = node

        if min_node is None:
            break

        nodes.remove(min_node)
        current_weight = visited[min_node]

        for neighbor in graph.neighbors(min_node):
            weight = graph[min_node][neighbor]['weight']
            if neighbor not in visited or current_weight + weight < visited[neighbor]:
                visited[neighbor] = current_weight + weight
                path[neighbor] = min_node

    # Reconstruct path
    route = []
    node = end
    while node != start:
        route.append(node)
        node = path.get(node)
        if node is None:
            return [], float('inf')
    route.append(start)
    route.reverse()

    total_cost = visited[end]
    return route, total_cost

def heuristic(a, b):
    # Dummy heuristic (as routers are symbolic)
    return 1

def a_star_path(graph, start, end):
    queue = []
    heapq.heappush(queue, (0, start))
    path = {}
    cost_so_far = {start: 0}

    while queue:
        _, current = heapq.heappop(queue)

        if current == end:
            break

        for neighbor in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph[current][neighbor]['weight']
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, end)
                heapq.heappush(queue, (priority, neighbor))
                path[neighbor] = current

    route = []
    node = end
    while node != start:
        route.append(node)
        node = path.get(node)
        if node is None:
            return [], float('inf')
    route.append(start)
    route.reverse()

    total_cost = cost_so_far[end]
    return route, total_cost

# Controls
traffic_increase = st.slider("Simulate Traffic Congestion", 0, 10, 0)
if traffic_increase > 0:
    simulate_traffic_congestion(G, traffic_increase)

if st.button('Simulate Link Failure'):
    edge = simulate_link_failure(G)
    if edge:
        st.warning(f"Link {edge} failed!")

# User input
start_router = st.selectbox('Select Start Router', routers)
end_router = st.selectbox('Select Destination Router', routers)

if st.button('Run Simulation'):
    # Dijkstra
    dijkstra_route, dijkstra_cost = dijkstra_path(G, start_router, end_router)
    
    # A*
    a_star_route, a_star_cost = a_star_path(G, start_router, end_router)

    # RL-based
    env = NetworkRoutingEnv(G)
    env.current_router = start_router
    env.destination_router = end_router
    obs = routers.index(start_router)
    done = False
    total_reward = 0
    rl_route = [start_router]
    steps = 0

    while not done and steps < 20:
        action, _ = model.predict(obs)
        obs, reward, done, _ = env.step(action)
        total_reward += reward
        rl_route.append(env.routers[obs])
        steps +=1

    # Display comparison
    st.subheader("Comparison of Routing Algorithms")
    st.write(f"✅ Dijkstra's Path: {dijkstra_route} | Cost: {dijkstra_cost}")
    st.write(f"✅ A* Path: {a_star_route} | Cost: {a_star_cost}")
    st.write(f"✅ RL-based Path: {rl_route} | Total Reward: {total_reward}")

    # Visualize RL result
    plot_network(current=rl_route[-1], destination=end_router, path=rl_route)
