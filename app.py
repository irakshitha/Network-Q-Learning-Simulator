
"""
🤖 AI vs Traditional Network Routing Simulator
Single file implementation using Python + Streamlit

Run with: streamlit run app.py

Author: College AI Project Team
"""

import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import random
import pandas as pd
import numpy as np
from collections import defaultdict
import time

# =============================================================================
# 1. NETWORK TOPOLOGY CLASS
# =============================================================================

class NetworkTopology:
    """Simple 6-node network for demonstration"""

    def __init__(self):
        # 6 nodes for simplicity
        self.nodes = ['A', 'B', 'C', 'D', 'E', 'F']

        # Network connections with costs
        self.edges = [
            ('A', 'B', 10), ('A', 'C', 15), ('A', 'E', 12),
            ('B', 'D', 10), ('B', 'F', 20),
            ('C', 'D', 12), ('C', 'E', 8),
            ('D', 'F', 15), ('E', 'F', 18)
        ]

        # Track congestion status
        self.congestion = set()

    def reset_congestion(self):
        """Clear all congestion"""
        self.congestion.clear()

    def add_congestion(self, node1, node2):
        """Add congestion to a link (both directions)"""
        self.congestion.add((node1, node2))
        self.congestion.add((node2, node1))

    def remove_congestion(self, node1, node2):
        """Remove congestion from a link"""
        self.congestion.discard((node1, node2))
        self.congestion.discard((node2, node1))

    def get_base_cost(self, node1, node2):
        """Get base cost between two nodes"""
        for u, v, cost in self.edges:
            if (u == node1 and v == node2) or (v == node1 and u == node2):
                return cost
        return float('inf')

    def get_actual_cost(self, node1, node2):
        """Get actual cost considering congestion"""
        base_cost = self.get_base_cost(node1, node2)
        if base_cost == float('inf'):
            return float('inf')

        # Congested links cost 3x more
        if (node1, node2) in self.congestion:
            return base_cost * 3
        return base_cost

    def get_neighbors(self, node):
        """Get all neighboring nodes"""
        neighbors = []
        for u, v, _ in self.edges:
            if u == node:
                neighbors.append(v)
            elif v == node:
                neighbors.append(u)
        return neighbors

# =============================================================================
# 2. TRADITIONAL DIJKSTRA ROUTING
# =============================================================================

class TraditionalRouter:
    """Traditional Dijkstra routing - always shortest path by base distance"""

    def __init__(self, network):
        self.network = network

    def find_shortest_path(self, source, destination):
        """Find shortest path using Dijkstra algorithm (ignores congestion)"""
        distances = {node: float('inf') for node in self.network.nodes}
        distances[source] = 0
        previous = {}
        unvisited = set(self.network.nodes)

        while unvisited:
            # Get node with minimum distance
            current = min(unvisited, key=lambda x: distances[x])

            if distances[current] == float('inf'):
                break  # No more reachable nodes

            unvisited.remove(current)

            # Check all neighbors
            for neighbor in self.network.get_neighbors(current):
                if neighbor in unvisited:
                    # Use BASE cost only (ignore congestion)
                    base_cost = self.network.get_base_cost(current, neighbor)
                    alternative = distances[current] + base_cost

                    if alternative < distances[neighbor]:
                        distances[neighbor] = alternative
                        previous[neighbor] = current

        # Debugging output
        print(f"Distances: {distances}")
        print(f"Previous mapping: {previous}")

        # Reconstruct path
        path = []
        current = destination
        while current is not None:
            path.append(current)
            current = previous.get(current)

        path = path[::-1]

        # Validate path
        if path and path[0] == source and path[-1] == destination:
            return path
        else:
            return None


# =============================================================================
# 3. AI Q-LEARNING ROUTING
# =============================================================================

class QLearningRouter:
    """AI router using Q-Learning algorithm"""

    def __init__(self, network):
        self.network = network
        self.q_table = defaultdict(float)  # (state, action, destination) -> Q-value
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.epsilon = 0.1  # Exploration rate
        self.training_episodes = 0

    def get_reward(self, current, next_node, destination):
        """Calculate reward for taking an action"""
        # Use actual cost (including congestion)
        cost = self.network.get_actual_cost(current, next_node)

        # Negative cost as reward (lower cost = higher reward)
        reward = -cost

        # Bonus for reaching destination
        if next_node == destination:
            reward += 100

        return reward

    def choose_action(self, state, destination, training=True):
        """Choose next node using epsilon-greedy policy"""
        neighbors = self.network.get_neighbors(state)

        if not neighbors:
            return None

        # During training, use epsilon-greedy
        if training and random.random() < self.epsilon:
            return random.choice(neighbors)  # Explore

        # Exploit: choose action with highest Q-value
        best_action = None
        best_q_value = float('-inf')

        for neighbor in neighbors:
            q_value = self.q_table[(state, neighbor, destination)]
            if q_value > best_q_value:
                best_q_value = q_value
                best_action = neighbor

        return best_action if best_action else random.choice(neighbors)

    def update_q_value(self, state, action, reward, next_state, destination):
        """Update Q-value using Q-learning formula"""
        current_q = self.q_table[(state, action, destination)]

        # Get maximum Q-value for next state
        if next_state == destination:
            max_next_q = 0  # Terminal state
        else:
            next_neighbors = self.network.get_neighbors(next_state)
            if next_neighbors:
                max_next_q = max([self.q_table[(next_state, neighbor, destination)] 
                                for neighbor in next_neighbors])
            else:
                max_next_q = 0

        # Q-learning update formula
        new_q = current_q + self.learning_rate * (
            reward + self.discount_factor * max_next_q - current_q
        )

        self.q_table[(state, action, destination)] = new_q

    def train_episode(self, source, destination):
        """Train one episode"""
        current = source
        path = [current]
        visited = set()
        max_steps = 10

        for step in range(max_steps):
            if current == destination:
                break

            if current in visited:
                break  # Avoid cycles

            visited.add(current)

            # Choose action
            next_node = self.choose_action(current, destination, training=True)
            if next_node is None:
                break

            # Get reward
            reward = self.get_reward(current, next_node, destination)

            # Update Q-value
            self.update_q_value(current, next_node, reward, next_node, destination)

            # Move to next state
            path.append(next_node)
            current = next_node

        self.training_episodes += 1
        return path

    def find_best_path(self, source, destination):
        """Find best path using learned Q-values (no exploration)"""
        current = source
        path = [current]
        visited = set()
        max_steps = 10

        for step in range(max_steps):
            if current == destination:
                break

            if current in visited:
                break

            visited.add(current)

            # Choose best action (no exploration)
            next_node = self.choose_action(current, destination, training=False)
            if next_node is None:
                break

            path.append(next_node)
            current = next_node

        return path if current == destination else None

# =============================================================================
# 4. NETWORK VISUALIZATION
# =============================================================================

def create_network_visualization(network, path=None, title="Network Topology"):
    """Create network visualization using NetworkX and Matplotlib"""

    # Create NetworkX graph
    G = nx.Graph()

    # Add nodes
    for node in network.nodes:
        G.add_node(node)

    # Add edges
    for u, v, weight in network.edges:
        G.add_edge(u, v, weight=weight)

    # Set up the plot
    plt.figure(figsize=(10, 6))

    # Node positions (fixed layout for consistency)
    pos = {
        'A': (0, 1), 'B': (2, 1), 'C': (0, 0), 
        'D': (2, 0), 'E': (1, 0.5), 'F': (3, 0.5)
    }

    # Draw all edges (normal)
    nx.draw_networkx_edges(G, pos, alpha=0.3, width=2, edge_color='gray')

    # Draw congested edges in red
    congested_edges = []
    for u, v, _ in network.edges:
        if (u, v) in network.congestion or (v, u) in network.congestion:
            congested_edges.append((u, v))

    if congested_edges:
        nx.draw_networkx_edges(G, pos, edgelist=congested_edges, 
                             edge_color='red', width=4, alpha=0.8)

    # Draw current path in blue
    if path and len(path) > 1:
        path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, 
                             edge_color='blue', width=5, alpha=0.9)

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', 
                          node_size=1000, alpha=0.9)

    # Draw node labels
    nx.draw_networkx_labels(G, pos, font_size=14, font_weight='bold')

    # Draw edge labels (costs)
    edge_labels = {}
    for u, v, weight in network.edges:
        if (u, v) in network.congestion or (v, u) in network.congestion:
            edge_labels[(u, v)] = f"{weight}×3"  # Show congestion multiplier
        else:
            edge_labels[(u, v)] = str(weight)

    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=10)

    plt.title(title, fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()

    return plt

# =============================================================================
# 5. UTILITY FUNCTIONS
# =============================================================================

def calculate_path_cost(network, path):
    """Calculate total cost of a path"""
    if not path or len(path) < 2:
        return float('inf')

    total_cost = 0
    for i in range(len(path) - 1):
        total_cost += network.get_actual_cost(path[i], path[i+1])

    return total_cost

def format_path(path):
    """Format path for display"""
    return ' → '.join(path) if path else 'No path found'

# =============================================================================
# 6. STREAMLIT WEB APPLICATION
# =============================================================================

def main():
    """Main Streamlit application"""

    # Page configuration
    st.set_page_config(
        page_title="AI vs Traditional Routing",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Title and description
    st.title("🤖 AI vs Traditional Network Routing")
    st.markdown("### Compare how AI learns better routes than traditional methods!")

    # Initialize session state
    if 'network' not in st.session_state:
        st.session_state.network = NetworkTopology()
        st.session_state.traditional_router = TraditionalRouter(st.session_state.network)
        st.session_state.ai_router = QLearningRouter(st.session_state.network)

    network = st.session_state.network
    traditional_router = st.session_state.traditional_router
    ai_router = st.session_state.ai_router

    # Sidebar controls
    st.sidebar.header("🎮 Controls")

    # Route selection
    source = st.sidebar.selectbox("Source Node", network.nodes, index=0)
    destination = st.sidebar.selectbox("Destination Node", network.nodes, index=5)

    # Reset button
    if st.sidebar.button("🔄 Reset Everything", type="secondary"):
        st.session_state.network = NetworkTopology()
        st.session_state.traditional_router = TraditionalRouter(st.session_state.network)
        st.session_state.ai_router = QLearningRouter(st.session_state.network)
        st.rerun()

    # Congestion controls
    st.sidebar.subheader("🚨 Network Congestion")

    # Predefined congestion scenarios
    scenario = st.sidebar.selectbox(
        "Quick Scenarios",
        ["No Congestion", "Congest B-D", "Congest A-B", "Congest Multiple"]
    )

    if st.sidebar.button("Apply Scenario"):
        network.reset_congestion()
        if scenario == "Congest B-D":
            network.add_congestion('B', 'D')
        elif scenario == "Congest A-B":
            network.add_congestion('A', 'B')
        elif scenario == "Congest Multiple":
            network.add_congestion('B', 'D')
            network.add_congestion('A', 'B')
        st.sidebar.success(f"Applied: {scenario}")
        st.rerun()

    # Manual congestion control
    st.sidebar.write("Manual Congestion:")
    col1, col2 = st.sidebar.columns(2)
    node1 = col1.selectbox("From", network.nodes, key="manual1")
    node2 = col2.selectbox("To", network.nodes, key="manual2", index=1)

    col3, col4 = st.sidebar.columns(2)
    if col3.button("Add"):
        if node1 != node2:
            network.add_congestion(node1, node2)
            st.sidebar.success(f"Added congestion: {node1}-{node2}")
            st.rerun()

    if col4.button("Remove"):
        if node1 != node2:
            network.remove_congestion(node1, node2)
            st.sidebar.success(f"Removed congestion: {node1}-{node2}")
            st.rerun()

    # Main content
    col1, col2 = st.columns(2)

    # Traditional Routing
    with col1:
        st.subheader("🔄 Traditional Routing")
        st.write("*Always uses shortest path by base distance*")

        if st.button("Find Traditional Path", type="primary", key="trad"):
            trad_path = traditional_router.find_shortest_path(source, destination)
            trad_cost = calculate_path_cost(network, trad_path)

            if trad_path:
                st.success(f"**Path:** {format_path(trad_path)}")
                st.info(f"**Total Cost:** {trad_cost}")

                # Show visualization
                fig = create_network_visualization(network, trad_path, 
                                                "Traditional Routing Path")
                st.pyplot(fig)
                plt.close()
            else:
                st.error("❌ No path found!")

    # AI Routing
    with col2:
        st.subheader("🧠 AI Routing")
        st.write("*Learns from experience and adapts*")

        # Training controls
        episodes = st.slider("Training Episodes", 10, 200, 50, key="episodes")

        if st.button("Train AI & Find Path", type="primary", key="ai"):
            # Training progress
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Train the AI
            for episode in range(episodes):
                ai_router.train_episode(source, destination)
                progress_bar.progress((episode + 1) / episodes)
                status_text.text(f"Training episode {episode + 1}/{episodes}")

            status_text.text("Training complete! Finding best path...")

            # Get best path
            ai_path = ai_router.find_best_path(source, destination)
            ai_cost = calculate_path_cost(network, ai_path)

            status_text.empty()
            progress_bar.empty()

            if ai_path:
                st.success(f"**Path:** {format_path(ai_path)}")
                st.info(f"**Total Cost:** {ai_cost}")
                st.info(f"**Training Episodes:** {ai_router.training_episodes}")

                # Show visualization
                fig = create_network_visualization(network, ai_path, 
                                                "AI Routing Path")
                st.pyplot(fig)
                plt.close()
            else:
                st.error("❌ No path found!")

    # Comparison section
    st.header("📊 Head-to-Head Comparison")

    if st.button("🆚 Compare Both Methods", type="secondary"):
        with st.spinner("Comparing routing methods..."):
            # Get traditional path
            trad_path = traditional_router.find_shortest_path(source, destination)
            trad_cost = calculate_path_cost(network, trad_path)

            # Train AI and get best path
            for _ in range(50):
                ai_router.train_episode(source, destination)

            ai_path = ai_router.find_best_path(source, destination)
            ai_cost = calculate_path_cost(network, ai_path)

            # Create comparison table
            comparison_data = {
                'Method': ['Traditional (Dijkstra)', 'AI (Q-Learning)'],
                'Path': [format_path(trad_path), format_path(ai_path)],
                'Total Cost': [trad_cost, ai_cost],
                'Adapts to Congestion': ['❌ No', '✅ Yes'],
                'Learning Required': ['❌ No', '✅ Yes']
            }

            df = pd.DataFrame(comparison_data)
            st.dataframe(df, use_container_width=True)

            # Declare winner
            if ai_cost < trad_cost:
                st.success("🏆 **AI Routing WINS!** Lower total cost by adapting to congestion.")
            elif trad_cost < ai_cost:
                st.info("🔄 **Traditional Routing** has lower cost in this scenario.")
            else:
                st.info("🤝 **TIE** - Both methods found equally good paths.")

    # Current network state
    st.header("🗺️ Current Network State")
    fig = create_network_visualization(network, 
                                     title="Network Topology (Red = Congested, Blue = Current Path)")
    st.pyplot(fig)
    plt.close()

    # Educational content
    st.header("📚 How It Works")

    tab1, tab2, tab3 = st.tabs(["🔄 Traditional", "🧠 AI Learning", "🎯 Demo Guide"])

    with tab1:
        st.markdown("""
        ### Traditional Routing (Dijkstra Algorithm)

        **How it works:**
        - Finds shortest path based on base link costs only
        - Completely ignores current network conditions
        - Always produces the same result for same source/destination
        - Fast and predictable

        **Algorithm:**
        ```python
        def dijkstra(source, destination):
            distances = {node: infinity for all nodes}
            distances[source] = 0

            while unvisited_nodes:
                current = node_with_minimum_distance
                for neighbor in current.neighbors:
                    alternative = distances[current] + base_cost(current, neighbor)
                    if alternative < distances[neighbor]:
                        distances[neighbor] = alternative
        ```

        **Pros:** ✅ Simple, fast, predictable  
        **Cons:** ❌ Cannot adapt to congestion or failures
        """)

    with tab2:
        st.markdown("""
        ### AI Routing (Q-Learning Algorithm)

        **How it works:**
        - Learns from experience through trial and error
        - Builds a "Q-table" of quality values for each action
        - Balances exploration (trying new routes) vs exploitation (using known good routes)
        - Adapts to network conditions over time

        **Q-Learning Formula:**
        ```
        Q(state, action) = Q(state, action) + α × [reward + γ × max(Q(next_state)) - Q(state, action)]
        ```

        Where:
        - **α** = Learning rate (how fast to learn)
        - **γ** = Discount factor (how much to value future rewards)
        - **reward** = Negative cost (lower cost = higher reward)

        **Pros:** ✅ Adaptive, learns optimal routes, handles dynamic conditions  
        **Cons:** ❌ Needs training time, more complex
        """)

    with tab3:
        st.markdown("""
        ### 🎯 Demo Instructions for Presentation

        **Step 1: Normal Network**
        1. Set route A → F
        2. Find traditional path (usually A→B→D→F)
        3. Note the cost and path

        **Step 2: Add Congestion**
        1. Use "Congest B-D" scenario
        2. Find traditional path again
        3. **Key Point:** Same path, but higher cost!

        **Step 3: Train AI**
        1. Train AI with 50+ episodes
        2. AI finds alternative path (like A→E→F)
        3. **Key Point:** AI adapts and finds better route!

        **Step 4: Compare**
        1. Use "Compare Both Methods" button
        2. Show side-by-side results
        3. **Conclusion:** AI learns and adapts, Traditional doesn't!

        ### 🎤 Talking Points:
        - "Traditional routing is like always taking the same highway, even in traffic"
        - "AI routing is like using GPS that learns from traffic patterns"
        - "This is how modern networks can become smarter and more efficient"
        """)

if __name__ == "__main__":
    main()
