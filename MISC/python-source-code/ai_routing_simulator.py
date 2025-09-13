
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import random
import pandas as pd
import numpy as np
from collections import defaultdict, deque
import time

# Simple Network Class
class SimpleNetwork:
    def __init__(self):
        self.nodes = ['A', 'B', 'C', 'D', 'E', 'F']
        self.edges = [
            ('A', 'B', 10), ('A', 'C', 15), ('A', 'E', 12),
            ('B', 'D', 10), ('B', 'F', 20),
            ('C', 'D', 12), ('C', 'E', 8),
            ('D', 'F', 15), ('E', 'F', 18)
        ]
        self.congestion = {}  # Track congested links
        self.reset_network()
    
    def reset_network(self):
        self.congestion = {(u, v): False for u, v, w in self.edges}
        self.congestion.update({(v, u): False for u, v, w in self.edges})
    
    def add_congestion(self, node1, node2):
        self.congestion[(node1, node2)] = True
        self.congestion[(node2, node1)] = True
    
    def get_cost(self, node1, node2):
        base_cost = next((w for u, v, w in self.edges if (u, v) == (node1, node2) or (v, u) == (node1, node2)), float('inf'))
        if self.congestion.get((node1, node2), False):
            return base_cost * 3  # Congested links cost 3x more
        return base_cost

# Traditional Dijkstra Algorithm
class TraditionalRouter:
    def __init__(self, network):
        self.network = network
    
    def find_path(self, source, destination):
        distances = {node: float('inf') for node in self.network.nodes}
        distances[source] = 0
        previous = {}
        unvisited = set(self.network.nodes)
        
        while unvisited:
            current = min(unvisited, key=lambda x: distances[x])
            if distances[current] == float('inf'):
                break
            
            unvisited.remove(current)
            
            for u, v, w in self.network.edges:
                if u == current and v in unvisited:
                    neighbor = v
                elif v == current and u in unvisited:
                    neighbor = u
                else:
                    continue
                
                base_cost = w
                alt = distances[current] + base_cost
                
                if alt < distances[neighbor]:
                    distances[neighbor] = alt
                    previous[neighbor] = current
        
        path = []
        current = destination
        while current is not None:
            path.append(current)
            current = previous.get(current)
        
        return path[::-1] if path[0] == source else None

# Simple Q-Learning Router
class QLearningRouter:
    def __init__(self, network):
        self.network = network
        self.q_table = defaultdict(float)
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.epsilon = 0.1
        self.episodes = 0
    
    def get_neighbors(self, node):
        neighbors = []
        for u, v, w in self.network.edges:
            if u == node:
                neighbors.append(v)
            elif v == node:
                neighbors.append(u)
        return neighbors
    
    def choose_action(self, state, destination):
        neighbors = self.get_neighbors(state)
        valid_neighbors = [n for n in neighbors if n != state]
        
        if not valid_neighbors:
            return None
            
        if random.random() < self.epsilon:
            return random.choice(valid_neighbors)
        
        q_values = [(neighbor, self.q_table[(state, neighbor, destination)]) for neighbor in valid_neighbors]
        return max(q_values, key=lambda x: x[1])[0]
    
    def get_reward(self, current, next_node, destination):
        cost = self.network.get_cost(current, next_node)
        reward = -cost
        if next_node == destination:
            reward += 100
        return reward
    
    def update_q_value(self, state, action, reward, next_state, destination):
        current_q = self.q_table[(state, action, destination)]
        
        if next_state == destination:
            max_next_q = 0
        else:
            next_neighbors = self.get_neighbors(next_state)
            if next_neighbors:
                max_next_q = max([self.q_table[(next_state, neighbor, destination)] for neighbor in next_neighbors])
            else:
                max_next_q = 0
        
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_next_q - current_q)
        self.q_table[(state, action, destination)] = new_q
    
    def find_path(self, source, destination, train=True):
        if train:
            self.episodes += 1
        
        path = [source]
        current = source
        visited = set()
        max_steps = 10
        
        for _ in range(max_steps):
            if current == destination:
                break
                
            if current in visited:
                break
            visited.add(current)
            
            next_node = self.choose_action(current, destination)
            if next_node is None:
                break
            
            if train:
                reward = self.get_reward(current, next_node, destination)
                self.update_q_value(current, next_node, reward, next_node, destination)
            
            path.append(next_node)
            current = next_node
        
        return path if current == destination else None

def visualize_network(network, path=None, title="Network Topology"):
    G = nx.Graph()
    
    for node in network.nodes:
        G.add_node(node)
    
    for u, v, w in network.edges:
        G.add_edge(u, v, weight=w)
    
    plt.figure(figsize=(10, 6))
    pos = {'A': (0, 1), 'B': (2, 1), 'C': (0, 0), 'D': (2, 0), 'E': (1, 0.5), 'F': (3, 0.5)}
    nx.draw_networkx_edges(G, pos, alpha=0.3, width=1)
    
    congested_edges = [(u, v) for (u, v), congested in network.congestion.items() if congested and u < v]
    if congested_edges:
        nx.draw_networkx_edges(G, pos, edgelist=congested_edges, edge_color='red', width=3)
    
    if path and len(path) > 1:
        path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='blue', width=4)
    
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=800)
    nx.draw_networkx_labels(G, pos, font_size=16, font_weight='bold')
    edge_labels = {(u, v): w for u, v, w in network.edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels)
    
    plt.title(title, size=16)
    plt.axis('off')
    return plt

def main():
    st.set_page_config(page_title="AI Routing Simulator", layout="wide")
    st.title("🤖 AI vs Traditional Routing Simulator")
    st.markdown("### Compare AI (Q-Learning) with Dijkstra Routing")

    if 'network' not in st.session_state:
        st.session_state.network = SimpleNetwork()
        st.session_state.traditional_router = TraditionalRouter(st.session_state.network)
        st.session_state.ai_router = QLearningRouter(st.session_state.network)
        st.session_state.results = []

    network = st.session_state.network
    traditional_router = st.session_state.traditional_router
    ai_router = st.session_state.ai_router

    source = st.sidebar.selectbox("Source Node", network.nodes, index=0)
    destination = st.sidebar.selectbox("Destination Node", network.nodes, index=5)

    if st.sidebar.button("🔄 Reset Network"):
        network.reset_network()
        st.session_state.ai_router = QLearningRouter(network)
        st.session_state.results = []
        st.experimental_rerun()

    col1, col2 = st.sidebar.columns(2)
    node1 = col1.selectbox("From", network.nodes, key="cong1")
    node2 = col2.selectbox("To", network.nodes, key="cong2", index=1)

    if st.sidebar.button("Add Congestion"):
        if node1 != node2:
            network.add_congestion(node1, node2)
            st.sidebar.success(f"Congestion added to {node1}-{node2}")
            st.experimental_rerun()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔄 Traditional Routing (Dijkstra)")
        if st.button("Find Traditional Path"):
            trad_path = traditional_router.find_path(source, destination)
            if trad_path:
                cost = sum(network.get_cost(trad_path[i], trad_path[i+1]) for i in range(len(trad_path)-1))
                st.success(f"Path: {' → '.join(trad_path)} (Cost: {cost})")
                fig = visualize_network(network, trad_path, "Traditional Path")
                st.pyplot(fig)
                plt.close()
            else:
                st.error("No path found")

    with col2:
        st.subheader("🧠 AI Routing (Q-Learning)")
        train_episodes = st.slider("Training Episodes", 1, 100, 20)

        if st.button("Train & Find AI Path"):
            progress_bar = st.progress(0)
            for episode in range(train_episodes):
                ai_router.find_path(source, destination, train=True)
                progress_bar.progress((episode + 1) / train_episodes)

            ai_router.epsilon = 0
            ai_path = ai_router.find_path(source, destination, train=False)
            ai_router.epsilon = 0.1

            if ai_path:
                cost = sum(network.get_cost(ai_path[i], ai_path[i+1]) for i in range(len(ai_path)-1))
                st.success(f"Path: {' → '.join(ai_path)} (Cost: {cost})")
                st.info(f"Episodes Trained: {ai_router.episodes}")
                fig = visualize_network(network, ai_path, "AI Path")
                st.pyplot(fig)
                plt.close()
            else:
                st.error("No path found")

    st.header("📊 Comparison")

    if st.button("🆚 Compare Methods"):
        trad_path = traditional_router.find_path(source, destination)
        trad_cost = sum(network.get_cost(trad_path[i], trad_path[i+1]) for i in range(len(trad_path)-1)) if trad_path else float('inf')

        for _ in range(50):
            ai_router.find_path(source, destination, train=True)

        ai_router.epsilon = 0
        ai_path = ai_router.find_path(source, destination, train=False)
        ai_router.epsilon = 0.1
        ai_cost = sum(network.get_cost(ai_path[i], ai_path[i+1]) for i in range(len(ai_path)-1)) if ai_path else float('inf')

        data = {
            'Method': ['Traditional (Dijkstra)', 'AI (Q-Learning)'],
            'Path': [' → '.join(trad_path) if trad_path else 'No path',
                     ' → '.join(ai_path) if ai_path else 'No path'],
            'Total Cost': [trad_cost, ai_cost],
            'Adapts to Congestion': ['❌', '✅']
        }

        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()
