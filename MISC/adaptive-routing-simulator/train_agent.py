# train_agent.py
from stable_baselines3 import DQN
from network_env import NetworkRoutingEnv
from network_graph import create_network_graph

def train_and_save_model():
    G = create_network_graph()
    env = NetworkRoutingEnv(G)
    
    model = DQN("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=20000)

    model.save("models/adaptive_routing_model")
    print("Training complete. Model saved to models/adaptive_routing_model.zip")

if __name__ == "__main__":
    train_and_save_model()
