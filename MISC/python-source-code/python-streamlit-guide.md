# Simple AI Routing Simulator - Python + Streamlit Implementation

## 🎯 Project Overview

This is a **super simplified** AI routing simulator using **only Python and Streamlit**. No HTML, CSS, or JavaScript needed! Perfect for college teams who want to focus on the core AI concepts without web development complexity.

## 📁 Project Structure
```
ai-routing-project/
├── ai_routing_simulator.py    # Main Streamlit app
├── simple_demo.py            # Command-line demo
├── requirements.txt          # Python dependencies
└── README.md                # Project documentation
```

## 🎮 Demo Flow (5 minutes)

### Step 1: Show Command Line Demo (1 minute)
```bash
python simple_demo.py
```
- Shows both algorithms working
- Clear output showing AI learning to avoid congestion
- No UI complexity, just pure algorithm demonstration

### Step 2: Launch Streamlit App (1 minute)
```bash
streamlit run ai_routing_simulator.py
```
- Beautiful web interface automatically created by Streamlit
- No web development needed!

### Step 3: Interactive Demo (3 minutes)
1. **Normal routing**: A → F using both methods
2. **Add congestion**: Click to add congestion to B-D link  
3. **Compare results**: Traditional still uses congested route, AI learns better path
4. **Show learning**: Display Q-table values and training progress

## 🧠 Core Algorithms (Easy to Explain)

### Traditional Routing (Dijkstra)
```python
def dijkstra_shortest_path(network, source, destination):
    """Always finds shortest path by base distance - ignores congestion"""
    distances = {node: float('inf') for node in network.nodes}
    distances[source] = 0
    # ... standard Dijkstra implementation
    return path
```

**Key Point**: Uses base costs only, never adapts to congestion.

### AI Routing (Q-Learning)
```python
class SimpleQLearning:
    def __init__(self, network):
        self.q_table = {}  # Learns which actions work best
        self.learning_rate = 0.1
        self.epsilon = 0.1  # Exploration vs exploitation
    
    def choose_action(self, state, destination):
        if random.random() < self.epsilon:
            return random.choice(neighbors)  # Explore
        else:
            return best_q_value_action()     # Use learned knowledge
    
    def train_episode(self, source, destination):
        # Learn from experience, update Q-values
        reward = -cost  # Negative cost = good reward
        self.q_table[state, action] += learning_rate * (reward + future_value - current_value)
```

**Key Point**: Learns from experience, adapts to find better routes over time.

## 👥 Team Division (3 People)

### Person 1: Core Algorithms
- Implement Dijkstra's algorithm
- Create network topology class
- Handle path calculation and cost computation

### Person 2: Q-Learning Implementation  
- Implement Q-learning algorithm
- Design reward function
- Handle training and learning logic

### Person 3: Streamlit Interface
- Create web interface using Streamlit
- Add interactive controls and visualization
- Prepare demo and presentation

## ⏱️ 4-Week Timeline

### Week 1: Foundation
- Set up Python environment
- Implement basic network class
- Create simple Dijkstra algorithm
- Test with command-line demo

### Week 2: AI Implementation
- Implement Q-learning algorithm
- Design reward system
- Test learning on simple scenarios
- Verify AI can find alternate routes

### Week 3: Streamlit Interface
- Learn Streamlit basics
- Create interactive web app
- Add network visualization
- Connect algorithms to UI

### Week 4: Polish & Demo
- Test all features
- Prepare presentation
- Add explanations and documentation
- Practice demo flow

## 🎯 Key Advantages

### For Students:
1. **Pure Python** - no web development skills needed
2. **Streamlit magic** - beautiful UI with minimal code
3. **Focus on AI** - spend time on algorithms, not UI
4. **Easy to debug** - simple Python debugging
5. **Clear visualization** - Streamlit handles all UI complexity

### For Presentation:
1. **Quick setup** - `pip install` and run
2. **Visual demo** - network graphs and interactive controls
3. **Side-by-side comparison** - clear difference between methods
4. **Real-time metrics** - show learning progress
5. **Easy to explain** - focus on core concepts

## 🔑 Core Code Snippets to Explain

### Network Representation
```python
class SimpleNetwork:
    def __init__(self):
        self.nodes = ['A', 'B', 'C', 'D', 'E', 'F']  # Simple 6-node network
        self.edges = [('A', 'B', 10), ...]           # (from, to, cost)
        self.congestion = {}                         # Track congested links
    
    def get_cost(self, node1, node2):
        base_cost = self.find_edge_cost(node1, node2)
        if self.is_congested(node1, node2):
            return base_cost * 3  # Congested links cost 3x more
        return base_cost
```

### Q-Learning Update Rule (The Heart of AI)
```python
def update_q_value(self, state, action, reward, next_state):
    current_q = self.q_table[(state, action)]
    max_next_q = max(self.q_table[(next_state, a)] for a in possible_actions)
    
    # Q-learning formula
    new_q = current_q + learning_rate * (reward + discount * max_next_q - current_q)
    self.q_table[(state, action)] = new_q
```

### Streamlit Interface (Magical Simplicity)
```python
# This creates a beautiful web app!
source = st.selectbox("Source Node", network.nodes)
destination = st.selectbox("Destination Node", network.nodes)

if st.button("Find AI Path"):
    # Train AI
    for episode in range(50):
        ai_router.train_episode(source, destination)
    
    # Get best path and show results
    path = ai_router.get_best_path(source, destination)
    st.success(f"Best path: {' → '.join(path)}")
    
    # Visualize network - Streamlit handles all the complexity!
    fig = visualize_network(network, path)
    st.pyplot(fig)
```

## 📊 What Reviewers Will See

### 1. Command Line Demo
```
🤖 AI vs Traditional Routing Demo
========================================

📍 Finding route from A to F
🔄 Traditional Route: A → B → D → F
💰 Cost: 35

🚨 Adding congestion to B-D link...
🔄 Traditional Route (with congestion): A → B → D → F  
💰 Cost: 65 (higher due to congestion!)

🧠 Training AI router...
🧠 AI Route: A → E → F
💰 Cost: 30

🏆 AI WINS! Saves 35 cost units!
   AI learned to avoid congested route!
```

### 2. Streamlit Web App
- Interactive network visualization
- Real-time path highlighting
- Training progress bars
- Side-by-side algorithm comparison
- Click-to-add congestion
- Performance metrics

## 🎤 Presentation Script (7 minutes)

### Slide 1: Problem Introduction (1 min)
*"Traditional network routing always uses the same path. But what if that path gets congested? We built an AI that learns better routes."*

### Slide 2: Command Demo (2 min)
- Run `python simple_demo.py`
- Show traditional routing ignoring congestion
- Show AI learning to find better path

### Slide 3: Interactive Demo (3 min)
- Launch Streamlit app
- Demo traditional vs AI routing
- Add congestion interactively
- Show AI adaptation in real-time

### Slide 4: Technical Explanation (1 min)
- "Traditional: Always shortest path"
- "AI: Learns from experience using Q-learning"
- "Result: AI adapts, traditional doesn't"

## 🔧 Installation & Running

### Setup (One-time)
```bash
git clone <your-repo>
cd ai-routing-project
pip install -r requirements.txt
```

### Run Command Demo
```bash
python simple_demo.py
```

### Run Web App
```bash
streamlit run ai_routing_simulator.py
```

## ✅ Success Checklist

### Technical Implementation:
- [ ] Dijkstra algorithm working
- [ ] Q-learning algorithm working  
- [ ] Network visualization working
- [ ] Interactive controls working
- [ ] Congestion simulation working

### Demo Preparation:
- [ ] Command demo runs smoothly
- [ ] Streamlit app launches without errors
- [ ] Can show clear difference between methods
- [ ] Team members know their parts
- [ ] Timing fits within presentation limit

### Explanation Ready:
- [ ] Can explain Q-learning in simple terms
- [ ] Can show why AI is better than traditional
- [ ] Can handle questions about algorithms
- [ ] Code is clean and commented

## 🎓 Learning Outcomes

Students will learn:
1. **Routing Algorithms**: Dijkstra vs reinforcement learning
2. **AI Concepts**: Q-learning, exploration vs exploitation
3. **Python Programming**: Classes, algorithms, data structures
4. **UI Development**: Streamlit for rapid prototyping
5. **Problem Solving**: Adaptive vs static solutions

## 💡 Key Takeaway

*"AI routing learns from experience and adapts to changing conditions, while traditional routing always uses the same path regardless of network state. This makes AI routing more suitable for real-world networks with dynamic conditions."*

Perfect for college presentations - **simple to implement, impressive to demonstrate, easy to explain!**