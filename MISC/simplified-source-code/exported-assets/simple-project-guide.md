# Simple AI Routing Simulator - College Project Guide

## Project Overview

This is a **simplified AI-based network routing simulator** designed for easy implementation and demonstration by college teams. The project shows how AI can make smarter routing decisions compared to traditional methods.

### Key Concept
- **Traditional Routing**: Always uses the shortest path, never adapts
- **AI Routing**: Learns from experience and adapts to avoid congested routes

## Core Components (Simplified)

### 1. Network Topology
- **6 nodes only** (A, B, C, D, E, F) - easy to visualize and explain
- **9 links** connecting the nodes with different costs
- **Simple graph structure** that allows multiple paths between any two nodes

### 2. Two Routing Algorithms
```python
# Traditional Routing (Dijkstra)
def traditional_routing(source, destination):
    return shortest_path_by_distance(source, destination)

# AI Routing (Q-Learning)
def ai_routing(source, destination):
    return q_learning_best_path(source, destination)
```

### 3. Simple Web Interface
- **Canvas-based visualization** - draw network with HTML5 Canvas
- **Basic controls** - source/destination selection, mode toggle
- **Real-time updates** - show current path and metrics
- **Click to add congestion** - interactive demonstration

## Implementation Details

### Backend (Simplified Python - Optional)
```python
# Simple Q-Learning Implementation
class SimpleQRouter:
    def __init__(self):
        self.q_table = {}  # State-action values
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        
    def choose_next_hop(self, current_node, destination):
        # Epsilon-greedy action selection
        if random.random() < 0.1:  # Exploration
            return random.choice(neighbors[current_node])
        else:  # Exploitation
            return best_q_value_action(current_node, destination)
    
    def update_q_value(self, state, action, reward, next_state):
        # Basic Q-learning update rule
        current_q = self.q_table.get((state, action), 0)
        max_next_q = max([self.q_table.get((next_state, a), 0) 
                         for a in possible_actions(next_state)])
        
        new_q = current_q + self.learning_rate * (
            reward + self.discount_factor * max_next_q - current_q
        )
        self.q_table[(state, action)] = new_q
```

### Frontend (JavaScript Only)
```javascript
// Network data structure
const network = {
  nodes: [
    {id: "A", x: 100, y: 100},
    {id: "B", x: 300, y: 100},
    // ... more nodes
  ],
  links: [
    {from: "A", to: "B", cost: 10, congested: false},
    // ... more links
  ]
};

// Simple pathfinding
function findPath(source, destination, mode) {
  if (mode === "traditional") {
    return dijkstra(source, destination);
  } else {
    return qLearningPath(source, destination);
  }
}

// Canvas drawing
function drawNetwork() {
  // Draw links
  network.links.forEach(link => {
    ctx.strokeStyle = link.congested ? 'red' : 'gray';
    drawLine(link.from, link.to);
  });
  
  // Draw nodes
  network.nodes.forEach(node => {
    drawCircle(node.x, node.y, node.id);
  });
  
  // Highlight current path
  if (currentPath.length > 0) {
    ctx.strokeStyle = 'blue';
    ctx.lineWidth = 4;
    drawPath(currentPath);
  }
}
```

## Demo Script for Presentation

### Step 1: Introduction (1 minute)
*"Today we'll show how AI can make network routing smarter than traditional methods."*

1. Show the simple 6-node network
2. Explain: "Traditional routing always picks shortest path, AI learns better routes"

### Step 2: Traditional Routing Demo (2 minutes)
1. Set source to A, destination to F
2. Select "Traditional Mode"
3. Show the path: A → B → D → F
4. Explain: "This is shortest by distance, always the same"

### Step 3: Add Congestion (1 minute)
1. Click on B-D link to add congestion (turns red)
2. Traditional routing still uses same path
3. Explain: "Traditional doesn't care about congestion"

### Step 4: AI Routing Demo (2 minutes)
1. Switch to "AI Mode"
2. Show how it learns: first few tries might use bad path
3. After learning, it chooses: A → E → F (avoiding congestion)
4. Show metrics improving over time

### Step 5: Comparison (1 minute)
- **Traditional**: Path cost 35 (10+10+15), always same route
- **AI**: Path cost 30 (12+18), adapts to conditions
- **Key Point**: AI learns and adapts, traditional doesn't

## Team Responsibilities

### 3-Person Team Setup:
- **Person 1**: Implement pathfinding algorithms (Dijkstra + Q-learning)
- **Person 2**: Create web interface and visualization 
- **Person 3**: Handle integration and prepare demo

### Development Timeline (4 weeks):
- **Week 1**: Basic network topology and Dijkstra algorithm
- **Week 2**: Simple Q-learning implementation
- **Week 3**: Web interface with canvas visualization
- **Week 4**: Integration, testing, and demo preparation

## Key Files Structure
```
simple-ai-router/
├── index.html          # Main webpage
├── style.css           # Basic styling
├── app.js              # All JavaScript logic
└── README.md           # Project documentation
```

## Technical Requirements
- **Frontend Only**: HTML5, CSS3, JavaScript (no server needed)
- **Algorithms**: Dijkstra (traditional), Q-learning (AI)
- **Visualization**: HTML5 Canvas for drawing network
- **No external libraries** - keep it simple!

## Explanation for Reviewers

### What is Q-Learning?
*"Q-learning is like learning from experience. The AI remembers which routes worked well and which didn't. Over time, it gets better at picking good routes."*

### Why is this Better?
1. **Adapts to congestion** - avoids busy routes
2. **Learns from experience** - gets better over time  
3. **Real-world applicable** - similar to how GPS apps work

### Key Metrics to Show:
- **Path Cost**: Lower is better (AI learns to find cheaper routes)
- **Success Rate**: AI improves over time
- **Adaptation**: AI changes behavior when network changes

## Common Questions & Answers

**Q: How long does the AI take to learn?**
A: In our simple demo, about 10-20 routing attempts to see clear improvement.

**Q: What if there's no alternative path?**
A: AI will still use the congested path but remembers it performed poorly.

**Q: Is this realistic?**
A: Yes! Similar principles are used in real network protocols and traffic routing systems.

## Success Criteria

### For Demo:
1. ✅ Show traditional routing always uses same path
2. ✅ Add congestion and show AI adapts
3. ✅ Clear visual difference between modes
4. ✅ Simple metrics show AI improvement

### For Grading:
1. ✅ Working pathfinding algorithms
2. ✅ Interactive web interface
3. ✅ Clear demonstration of learning
4. ✅ Good code organization and comments

## Extensions (If Time Permits)
- Add more congestion scenarios
- Show Q-table values in real-time
- Add packet loss simulation
- Create multiple network topologies

## Conclusion

This simplified version focuses on the **core concept**: AI can learn and adapt while traditional methods cannot. The 6-node network is small enough to understand quickly but complex enough to demonstrate meaningful learning.

**Key Takeaway for Reviewers**: *"AI routing learns from experience and adapts to changing network conditions, while traditional routing always uses the same path regardless of current network state."*