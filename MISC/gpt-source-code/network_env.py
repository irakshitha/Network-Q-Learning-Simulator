# network_env.py
import random
import gymnasium as gym
from gymnasium import spaces

class NetworkRoutingEnv(gym.Env):
    def __init__(self, graph):
        super().__init__()
        self.graph = graph
        self.routers = list(graph.nodes)
        self.current_router = None
        self.destination_router = None
        self.action_space = spaces.Discrete(len(self.routers))
        self.observation_space = spaces.Discrete(len(self.routers))

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        self.current_router = random.choice(self.routers)
        self.destination_router = random.choice(self.routers)
        while self.destination_router == self.current_router:
            self.destination_router = random.choice(self.routers)
        return self.routers.index(self.current_router), {}

    def step(self, action):
        next_router = self.routers[action]
        done = next_router == self.destination_router

        if self.graph.has_edge(self.current_router, next_router):
            latency = self.graph[self.current_router][next_router]['weight']
            reward = -latency  # Negative latency as reward
            self.current_router = next_router
        else:
            reward = -10  # Penalty for invalid moves

        return self.routers.index(self.current_router), reward, done, False, {}

    def render(self):
        print(f"Current: {self.current_router} -> Destination: {self.destination_router}")
