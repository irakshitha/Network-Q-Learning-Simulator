import plotly.graph_objects as go
import numpy as np

# Define complete components with better spacing
components_data = {
    "components": [
        # Frontend Components (top row) - using brand color #1FB8CD
        {"name": "React.js UI", "type": "Frontend", "x": 100, "y": 700, "color": "#1FB8CD"},
        {"name": "Cytoscape.js", "type": "Frontend", "x": 250, "y": 700, "color": "#1FB8CD"},
        {"name": "Dashboard", "type": "Frontend", "x": 400, "y": 700, "color": "#1FB8CD"},
        {"name": "Controls", "type": "Frontend", "x": 550, "y": 700, "color": "#1FB8CD"},
        
        # Backend Components (second row) - using brand color #2E8B57
        {"name": "FastAPI", "type": "Backend", "x": 100, "y": 550, "color": "#2E8B57"},
        {"name": "WebSocket", "type": "Backend", "x": 250, "y": 550, "color": "#2E8B57"},
        {"name": "RL Engine", "type": "Backend", "x": 400, "y": 550, "color": "#2E8B57"},
        {"name": "Sim Core", "type": "Backend", "x": 550, "y": 550, "color": "#2E8B57"},
        {"name": "Database", "type": "Backend", "x": 325, "y": 470, "color": "#2E8B57"},
        
        # AI/ML Components (third row) - using brand color #DB4545
        {"name": "DQN Agent", "type": "AI/ML", "x": 100, "y": 400, "color": "#DB4545"},
        {"name": "Q-learning", "type": "AI/ML", "x": 250, "y": 400, "color": "#DB4545"},
        {"name": "Exp Replay", "type": "AI/ML", "x": 400, "y": 400, "color": "#DB4545"},
        {"name": "Target Net", "type": "AI/ML", "x": 550, "y": 400, "color": "#DB4545"},
        {"name": "Reward Func", "type": "AI/ML", "x": 325, "y": 320, "color": "#DB4545"},
        
        # Network Components (bottom row) - using brand color #D2BA4C
        {"name": "Topology Gen", "type": "Network", "x": 100, "y": 250, "color": "#D2BA4C"},
        {"name": "Link Manager", "type": "Network", "x": 250, "y": 250, "color": "#D2BA4C"},
        {"name": "Packet Sim", "type": "Network", "x": 400, "y": 250, "color": "#D2BA4C"},
        {"name": "Failure Sim", "type": "Network", "x": 550, "y": 250, "color": "#D2BA4C"}
    ],
    "connections": [
        # Frontend to Backend (vertical connections)
        {"from": "React.js UI", "to": "FastAPI", "label": "HTTP/REST"},
        {"from": "Cytoscape.js", "to": "WebSocket", "label": "Real-time"},
        {"from": "Dashboard", "to": "Database", "label": "Metrics"},
        {"from": "Controls", "to": "Sim Core", "label": "Config"},
        
        # Backend to AI/ML (mostly vertical)
        {"from": "FastAPI", "to": "DQN Agent", "label": "Route Req"},
        {"from": "RL Engine", "to": "Q-learning", "label": "Training"},
        {"from": "Sim Core", "to": "Reward Func", "label": "State Info"},
        {"from": "Database", "to": "Exp Replay", "label": "History"},
        
        # AI/ML internal connections (horizontal)
        {"from": "DQN Agent", "to": "Q-learning", "label": "Learning"},
        {"from": "Q-learning", "to": "Exp Replay", "label": "Experience"},
        {"from": "Exp Replay", "to": "Target Net", "label": "Update"},
        {"from": "Reward Func", "to": "DQN Agent", "label": "Feedback"},
        
        # Network to AI/ML (vertical)
        {"from": "Topology Gen", "to": "DQN Agent", "label": "Network"},
        {"from": "Link Manager", "to": "Reward Func", "label": "Link State"},
        {"from": "Packet Sim", "to": "RL Engine", "label": "Sim Data"},
        {"from": "Failure Sim", "to": "Target Net", "label": "Failures"}
    ]
}

# Create figure
fig = go.Figure()

# Create component position lookup
comp_positions = {comp["name"]: (comp["x"], comp["y"]) for comp in components_data["components"]}

# Add connection arrows with better styling
for conn in components_data["connections"]:
    from_pos = comp_positions[conn["from"]]
    to_pos = comp_positions[conn["to"]]
    
    # Calculate arrow direction
    dx = to_pos[0] - from_pos[0]
    dy = to_pos[1] - from_pos[1]
    length = np.sqrt(dx**2 + dy**2)
    
    # Normalize and adjust for node size
    if length > 0:
        dx_norm = dx / length
        dy_norm = dy / length
        
        # Start and end points adjusted for node radius (30 pixels)
        start_x = from_pos[0] + dx_norm * 30
        start_y = from_pos[1] + dy_norm * 30
        end_x = to_pos[0] - dx_norm * 30
        end_y = to_pos[1] - dy_norm * 30
        
        # Add line with better visibility
        fig.add_trace(go.Scatter(
            x=[start_x, end_x],
            y=[start_y, end_y],
            mode='lines',
            line=dict(color='#333333', width=3),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        # Add arrow head
        arrow_size = 20
        angle = np.arctan2(dy, dx)
        arrow_x = end_x - arrow_size * np.cos(angle - np.pi/6)
        arrow_y = end_y - arrow_size * np.sin(angle - np.pi/6)
        arrow_x2 = end_x - arrow_size * np.cos(angle + np.pi/6)
        arrow_y2 = end_y - arrow_size * np.sin(angle + np.pi/6)
        
        fig.add_trace(go.Scatter(
            x=[arrow_x, end_x, arrow_x2],
            y=[arrow_y, end_y, arrow_y2],
            mode='lines',
            line=dict(color='#333333', width=3),
            fill='toself',
            fillcolor='#333333',
            showlegend=False,
            hoverinfo='skip'
        ))
        
        # Add connection label with better positioning
        mid_x = (start_x + end_x) / 2
        mid_y = (start_y + end_y) / 2
        
        # Offset label slightly to avoid line overlap
        if abs(dx) > abs(dy):  # Horizontal-ish line
            label_y = mid_y + 15
        else:  # Vertical-ish line
            label_y = mid_y
            
        fig.add_trace(go.Scatter(
            x=[mid_x],
            y=[label_y],
            mode='text',
            text=[conn["label"]],
            textfont=dict(size=10, color='#000000', family='Arial Bold'),
            showlegend=False,
            hoverinfo='skip'
        ))

# Group components by type for legend
component_types = {}
for comp in components_data["components"]:
    comp_type = comp["type"]
    if comp_type not in component_types:
        component_types[comp_type] = []
    component_types[comp_type].append(comp)

# Add components by type with better styling
for comp_type, comps in component_types.items():
    x_coords = [comp["x"] for comp in comps]
    y_coords = [comp["y"] for comp in comps]
    names = [comp["name"] for comp in comps]
    colors = [comp["color"] for comp in comps]
    
    fig.add_trace(go.Scatter(
        x=x_coords,
        y=y_coords,
        mode='markers+text',
        marker=dict(
            size=60,
            color=colors[0],
            line=dict(width=4, color='white')
        ),
        text=names,
        textposition='middle center',
        textfont=dict(size=10, color='white', family='Arial Black'),
        name=comp_type,
        hovertemplate='<b>%{text}</b><br>Type: ' + comp_type + '<extra></extra>',
        cliponaxis=False
    ))

# Update layout with better spacing
fig.update_layout(
    title="AI Adaptive Routing Simulator",
    showlegend=True,
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.05,
        xanchor='center',
        x=0.5
    ),
    xaxis=dict(
        showgrid=False,
        showticklabels=False,
        zeroline=False,
        showline=False,
        range=[50, 600]
    ),
    yaxis=dict(
        showgrid=False,
        showticklabels=False,
        zeroline=False,
        showline=False,
        range=[200, 750]
    ),
    plot_bgcolor='white',
    paper_bgcolor='white'
)

# Save the chart
fig.write_image("ai_routing_architecture.png")