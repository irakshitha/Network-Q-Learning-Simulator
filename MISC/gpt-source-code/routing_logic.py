import heapq
from stable_baselines3 import DQN
from network_env import NetworkRoutingEnv

routers = ['A', 'B', 'C', 'D', 'E', 'F']

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

def a_star_path(graph, start, end):
    def heuristic(a, b):
        return 1  # Dummy heuristic

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

def rl_based_path(graph, start, end, model):
    env = NetworkRoutingEnv(graph)
    env.current_router = start
    env.destination_router = end
    obs = routers.index(start)
    done = False
    steps = 0
    rl_route = [start]

    while not done and steps < 20:
        action, _ = model.predict(obs)
        obs, reward, done, _, _ = env.step(action)
        rl_route.append(env.routers[obs])
        steps +=1

    return rl_route
