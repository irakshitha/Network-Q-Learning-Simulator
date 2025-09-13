import streamlit as st
from network_graph import create_network_graph, add_congestion, generate_graph_visual, reset_graph
from routing_logic import dijkstra_path, a_star_path, rl_based_path
from stable_baselines3 import DQN
import os

st.set_page_config(layout="wide")
st.title("🚀 AI Routing Simulator")
st.write("Demonstrating Smart vs Traditional Network Routing")

model = DQN.load("models/adaptive_routing_model")

if 'G' not in st.session_state:
    st.session_state.G = create_network_graph()
    st.session_state.congested_links = []

routers = list(st.session_state.G.nodes)

col1, col2 = st.columns(2)
with col1:
    start = st.selectbox('From:', routers)
with col2:
    end = st.selectbox('To:', routers)

mode = st.radio('Mode:', ['Traditional Routing', 'AI Routing'])

if st.button('Add Congestion'):
    u = st.selectbox('Congest Link From:', routers)
    v = st.selectbox('Congest Link To:', routers)
    add_congestion(st.session_state.G, u, v)
    st.session_state.congested_links.append((u, v))

if st.button('Reset Network'):
    st.session_state.G = reset_graph()
    st.session_state.congested_links = []

if st.button('Start Simulation'):
    if mode == 'Traditional Routing':
        path1, cost1 = dijkstra_path(st.session_state.G, start, end)
        path2, cost2 = a_star_path(st.session_state.G, start, end)
        path3 = []

    else:
        path3 = rl_based_path(st.session_state.G, start, end, model)
        path1, cost1 = dijkstra_path(st.session_state.G, start, end)
        path2, cost2 = a_star_path(st.session_state.G, start, end)

    st.write("### Path Comparisons")
    st.write(f"✅ Dijkstra: Path = {path1}, Cost = {cost1}")
    st.write(f"✅ A*: Path = {path2}, Cost = {cost2}")
    st.write(f"✅ AI Routing Path: {path3}")

    graph_file = generate_graph_visual(st.session_state.G, path=path1, congested_links=st.session_state.congested_links)
    st.components.v1.html(open(graph_file, 'r', encoding='utf-8').read(), height=700)
