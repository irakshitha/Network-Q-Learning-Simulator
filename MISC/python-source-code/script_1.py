# Create requirements.txt file
requirements = '''streamlit==1.28.0
networkx==3.1
matplotlib==3.7.2
pandas==2.0.3
numpy==1.24.3
'''

with open('requirements.txt', 'w', encoding='utf-8') as f:
    f.write(requirements)

# Create a simple README file
readme_content = '''# Simple AI Routing Simulator

## 🎯 Project Overview
A simple educational tool that demonstrates how AI (Q-Learning) can learn better network routes than traditional methods (Dijkstra).

## 🚀 How to Run
1. Install requirements: `pip install -r requirements.txt`
2. Run the app: `streamlit run ai_routing_simulator.py`
3. Open browser to: `http://localhost:8501`

## 🎮 How to Use
1. Select source and destination nodes
2. Try traditional routing first
3. Add congestion to some links
4. Train AI and compare results
5. See how AI adapts to congestion!

## 🧠 Key Concepts
- **Traditional Routing**: Always shortest path, never adapts
- **AI Routing**: Learns from experience, adapts to congestion

## 👥 Team Structure (3 people)
- **Person 1**: Dijkstra algorithm + network setup
- **Person 2**: Q-Learning implementation  
- **Person 3**: Streamlit interface + demo

Perfect for college presentations! 🎓
'''

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(readme_content)

print("✅ Requirements file created: requirements.txt")
print("✅ README file created: README.md")
