import plotly.graph_objects as go
import plotly.io as pio
import json
import numpy as np

# Parse the data
data = {
  "components": [
    {"name": "HTML5 Canvas", "type": "UI", "x": 50, "y": 50, "color": "#3498db"},
    {"name": "Control Panel", "type": "UI", "x": 200, "y": 50, "color": "#3498db"},
    {"name": "Metrics Display", "type": "UI", "x": 350, "y": 50, "color": "#3498db"},
    {"name": "Traditional Routing", "type": "Logic", "x": 50, "y": 200, "color": "#2ecc71"},
    {"name": "AI Routing (Q-Learning)", "type": "Logic", "x": 200, "y": 200, "color": "#2ecc71"},
    {"name": "Network State Manager", "type": "Logic", "x": 350, "y": 200, "color": "#2ecc71"},
    {"name": "Network Topology", "type": "Data", "x": 50, "y": 350, "color": "#f39c12"},
    {"name": "Q-Table", "type": "Data", "x": 200, "y": 350, "color": "#f39c12"},
    {"name": "Path State", "type": "Data", "x": 350, "y": 350, "color": "#f39c12"}
  ],
  "connections": [
    {"from": "Control Panel", "to": "Traditional Routing", "label": "Mode Select"},
    {"from": "Control Panel", "to": "AI Routing (Q-Learning)", "label": "Src/Dest"},
    {"from": "Traditional Routing", "to": "HTML5 Canvas", "label": "Show Path"},
    {"from": "AI Routing (Q-Learning)", "to": "HTML5 Canvas", "label": "Show Path"},
    {"from": "Traditional Routing", "to": "Network Topology", "label": "Read Graph"},
    {"from": "AI Routing (Q-Learning)", "to": "Q-Table", "label": "Learn/Recall"},
    {"from": "Network State Manager", "to": "Path State", "label": "Update State"},
    {"from": "AI Routing (Q-Learning)", "to": "Metrics Display", "label": "Performance"}
  ]
}

# Create figure
fig = go.Figure()

# Create component name mapping for connections
name_to_pos = {comp["name"]: (comp["x"], comp["y"]) for comp in data["components"]}

# Add connection lines with arrows and labels
for i, conn in enumerate(data["connections"]):
    from_pos = name_to_pos[conn["from"]]
    to_pos = name_to_pos[conn["to"]]
    
    # Calculate arrow position (closer to destination)
    dx = to_pos[0] - from_pos[0]
    dy = to_pos[1] - from_pos[1]
    length = np.sqrt(dx**2 + dy**2)
    
    # Adjust start and end points to not overlap with boxes
    start_x = from_pos[0] + (dx/length) * 25
    start_y = from_pos[1] + (dy/length) * 25
    end_x = to_pos[0] - (dx/length) * 25
    end_y = to_pos[1] - (dy/length) * 25
    
    # Add connection line
    fig.add_trace(go.Scatter(
        x=[start_x, end_x],
        y=[start_y, end_y],
        mode='lines',
        line=dict(color='#666666', width=3),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Add arrow head
    arrow_x = end_x - (dx/length) * 8
    arrow_y = end_y - (dy/length) * 8
    
    # Calculate perpendicular for arrow wings
    perp_x = -dy/length * 4
    perp_y = dx/length * 4
    
    fig.add_trace(go.Scatter(
        x=[arrow_x + perp_x, end_x, arrow_x - perp_x],
        y=[arrow_y + perp_y, end_y, arrow_y - perp_y],
        mode='lines',
        line=dict(color='#666666', width=3),
        fill='toself',
        fillcolor='#666666',
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Add connection label at midpoint
    mid_x = (start_x + end_x) / 2
    mid_y = (start_y + end_y) / 2
    
    fig.add_trace(go.Scatter(
        x=[mid_x],
        y=[mid_y],
        mode='text',
        text=[conn["label"]],
        textfont=dict(size=9, color='#333333'),
        showlegend=False,
        hoverinfo='skip'
    ))

# Add components by layer
layers = {"UI": [], "Logic": [], "Data": []}
for comp in data["components"]:
    layers[comp["type"]].append(comp)

# Create traces for each layer with better text handling
for layer_name, components in layers.items():
    x_vals = [comp["x"] for comp in components]
    y_vals = [comp["y"] for comp in components]
    colors = [comp["color"] for comp in components]
    
    # Abbreviate component names smartly to fit in 15 chars while keeping meaning
    names = []
    for comp in components:
        name = comp["name"]
        if name == "HTML5 Canvas":
            name = "HTML5<br>Canvas"
        elif name == "Control Panel":
            name = "Control<br>Panel"
        elif name == "Metrics Display":
            name = "Metrics<br>Display"
        elif name == "Traditional Routing":
            name = "Traditional<br>Routing"
        elif name == "AI Routing (Q-Learning)":
            name = "AI Routing<br>(Q-Learning)"
        elif name == "Network State Manager":
            name = "Network State<br>Manager"
        elif name == "Network Topology":
            name = "Network<br>Topology"
        elif name == "Path State":
            name = "Path<br>State"
        names.append(name)
    
    fig.add_trace(go.Scatter(
        x=x_vals,
        y=y_vals,
        mode='markers+text',
        marker=dict(
            color=colors[0], 
            size=50,
            symbol='square',
            line=dict(width=2, color='white')
        ),
        text=names,
        textposition='middle center',
        textfont=dict(size=12, color='white', family="Arial Black"),
        name=f"{layer_name} Layer",
        showlegend=True
    ))

# Update layout
fig.update_layout(
    title="AI Routing Simulator Architecture",
    xaxis=dict(
        showgrid=False,
        showticklabels=False,
        zeroline=False,
        range=[-25, 425]
    ),
    yaxis=dict(
        showgrid=False,
        showticklabels=False,
        zeroline=False,
        range=[-25, 425],
        autorange='reversed'
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.05,
        xanchor='center',
        x=0.5,
        font=dict(size=14)
    )
)

# Save the chart
fig.write_image("architecture_diagram.png")