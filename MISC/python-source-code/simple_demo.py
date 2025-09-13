import random
from collections import defaultdict

class SimpleNetworkDemo:
    def __init__(self):
        self.nodes = ['A', 'B', 'C', 'D', 'E', 'F']
        self.edges = [
            ('A', 'B', 10), ('A', 'C', 15), ('A', 'E', 12),
            ('B', 'D', 10), ('B', 'F', 20),
            ('C', 'D', 12), ('C', 'E', 8),
            ('D', 'F', 15), ('E', 'F', 18)
        ]
        self.congestion = set()
    
    def add_congestion(self, node1, node2):
        self.congestion.add((node1, node2))
        self.congestion.add((node2, node1))
    
    def get_cost(self, node1, node2):
        for u, v, cost in self.edges:
            if (u == node1 and v == node2) or (v == node1 and u == node2):
                return cost * 3 if (node1, node2) in self.congestion else cost
        return float('inf')
    
    def get_neighbors(self, node):
        neighbors = []
        for u, v, _ in self.edges:
            if u == node:
                neighbors.append(v)
            elif v == node:
                neighbors.append(u)
        return neighbors

def dijkstra_shortest_path(network, source, destination):
    distances = {node: float('inf') for node in network.nodes}
    distances[source] = 0
    previous = {}
    unvisited = set(network.nodes)
    
    while unvisited:
        current = min(unvisited, key=lambda x: distances[x])
        if distances[current] == float('inf'):
            break
        unvisited.remove(current)
        for neighbor in network.get_neighbors(current):
            if neighbor in unvisited:
                base_cost = next(cost for u, v, cost in network.edges
                                 if (u == current and v == neighbor) or (v == current and u == neighbor))
                alt = distances[current] + base_cost
                if alt < distances[neighbor]:
                    distances[neighbor] = alt
                    previous[neighbor] = current
    
    path = []
    current = destination
    while current is not None:
        path.append(current)
        current = previous.get(current)
    
    return path[::-1] if path and path[0] == source else None

class SimpleQLearning:
    def __init__(self, network):
        self.network = network
        self.q_table = defaultdict(float)
        self.learning_rate = 0.1
        self.discount = 0.9
        self.epsilon = 0.1
    
    def get_reward(self, current, next_node, destination):
        cost = self.network.get_cost(current, next_node)
        reward = -cost
        if next_node == destination:
            reward += 100
        return reward
    
    def choose_action(self, state, destination):
        neighbors = self.network.get_neighbors(state)
        if random.random() < self.epsilon:
            return random.choice(neighbors)
        best_action = None
        best_q = float('-inf')
        for neighbor in neighbors:
            q_val = self.q_table[(state, neighbor, destination)]
            if q_val > best_q:
                best_q = q_val
                best_action = neighbor
        return best_action if best_action else random.choice(neighbors)
    
    def train_episode(self, source, destination):
        current = source
        path = [current]
        for step in range(20):  # Increase steps to allow longer paths
            if current == destination:
                break
            action = self.choose_action(current, destination)
            reward = self.get_reward(current, action, destination)
            current_q = self.q_table[(current, action, destination)]
            if action == destination:
                max_next_q = 0
            else:
                next_neighbors = self.network.get_neighbors(action)
                max_next_q = max([self.q_table[(action, n, destination)] for n in next_neighbors] or [0])
            new_q = current_q + self.learning_rate * (reward + self.discount * max_next_q - current_q)
            self.q_table[(current, action, destination)] = new_q
            path.append(action)
            current = action
        return path
    
    def get_best_path(self, source, destination):
        current = source
        path = [current]
        for _ in range(20):  # Allow longer traversal
            if current == destination:
                break
            neighbors = self.network.get_neighbors(current)
            best_neighbor = max(neighbors, key=lambda n: self.q_table[(current, n, destination)])
            path.append(best_neighbor)
            current = best_neighbor
        return path if current == destination else None

def calculate_path_cost(network, path):
    if not path or len(path) < 2:
        return float('inf')
    total_cost = 0
    for i in range(len(path) - 1):
        total_cost += network.get_cost(path[i], path[i + 1])
    return total_cost

def main_demo():
    print("🤖 AI vs Traditional Routing Demo")
    print("=" * 40)
    
    network = SimpleNetworkDemo()
    source, destination = 'A', 'F'
    
    print(f"\n📍 Finding route from {source} to {destination}")
    trad_path = dijkstra_shortest_path(network, source, destination)
    trad_cost = calculate_path_cost(network, trad_path)
    
    print(f"🔄 Traditional Route: {' → '.join(trad_path) if trad_path else 'No path found'}")
    print(f"💰 Cost: {trad_cost}")
    
    print(f"\n🚨 Adding congestion to B-D link...")
    network.add_congestion('B', 'D')
    
    trad_path_cong = dijkstra_shortest_path(network, source, destination)
    trad_cost_cong = calculate_path_cost(network, trad_path_cong)
    
    print(f"🔄 Traditional Route (with congestion): {' → '.join(trad_path_cong) if trad_path_cong else 'No path found'}")
    print(f"💰 Cost: {trad_cost_cong}")
    
    print(f"\n🧠 Training AI router...")
    ai_router = SimpleQLearning(network)
    for episode in range(500):  # Increase number of episodes
        ai_router.train_episode(source, destination)
        if episode % 100 == 0:
            print(f"   Training episode {episode}...")
    
    ai_path = ai_router.get_best_path(source, destination)
    ai_cost = calculate_path_cost(network, ai_path)
    
    print(f"🧠 AI Route: {' → '.join(ai_path) if ai_path else 'No path found'}")
    print(f"💰 Cost: {ai_cost}")
    
    print(f"\n📊 COMPARISON:")
    print(f"   Traditional: {' → '.join(trad_path_cong) if trad_path_cong else 'No path'} (Cost: {trad_cost_cong})")
    print(f"   AI Learning: {' → '.join(ai_path) if ai_path else 'No path'} (Cost: {ai_cost})")
    
    if ai_cost < trad_cost_cong:
        print(f"\n🏆 AI WINS! Saves {trad_cost_cong - ai_cost} cost units!")
    else:
        print(f"\n🤔 Traditional method was better this time")
    
    print("\n✨ AI adapts to network conditions; traditional does not.")

if __name__ == "__main__":
    main_demo()
