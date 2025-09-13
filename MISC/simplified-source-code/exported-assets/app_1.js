// Simple network topology (6 nodes)
const networkData = {
  nodes: [
    {id: "A", x: 100, y: 100, label: "Node A"},
    {id: "B", x: 300, y: 100, label: "Node B"},
    {id: "C", x: 100, y: 200, label: "Node C"},
    {id: "D", x: 300, y: 200, label: "Node D"},
    {id: "E", x: 200, y: 150, label: "Node E"},
    {id: "F", x: 400, y: 150, label: "Node F"}
  ],
  links: [
    {from: "A", to: "B", cost: 10, congested: false},
    {from: "A", to: "C", cost: 15, congested: false},
    {from: "A", to: "E", cost: 12, congested: false},
    {from: "B", to: "D", cost: 10, congested: false},
    {from: "B", to: "F", cost: 20, congested: false},
    {from: "C", to: "D", cost: 12, congested: false},
    {from: "C", to: "E", cost: 8, congested: false},
    {from: "D", to: "F", cost: 15, congested: false},
    {from: "E", to: "F", cost: 18, congested: false}
  ]
};

// Simulation state
let state = {
  source: "A",
  destination: "F", // Default to F for demo
  mode: "traditional",
  isRunning: false,
  currentPath: [],
  packetCount: 0,
  successCount: 0,
  learningSteps: 0,
  qTable: new Map(),
  explanation: "Select a source and destination to start the simulation."
};

// Canvas variables
let canvas, ctx;
const nodeRadius = 25;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
  initializeCanvas();
  initializeControls();
  initializeQTable();
  
  // Set initial destination
  document.getElementById('destinationSelect').value = "F";
  
  // Calculate initial path
  calculateAndShowPath();
  drawNetwork();
  updateDisplay();
});

function initializeCanvas() {
  canvas = document.getElementById('networkCanvas');
  ctx = canvas.getContext('2d');
  
  // Handle canvas clicks for adding congestion
  canvas.addEventListener('click', handleCanvasClick);
}

function initializeControls() {
  document.getElementById('sourceSelect').addEventListener('change', handleSourceChange);
  document.getElementById('destinationSelect').addEventListener('change', handleDestinationChange);
  document.getElementById('modeSelect').addEventListener('change', handleModeChange);
  
  document.getElementById('startBtn').addEventListener('click', startSimulation);
  document.getElementById('addCongestionBtn').addEventListener('click', addRandomCongestion);
  document.getElementById('resetBtn').addEventListener('click', resetNetwork);
}

function initializeQTable() {
  // Initialize Q-table with small random values
  networkData.nodes.forEach(node => {
    const neighbors = getNeighbors(node.id);
    neighbors.forEach(neighbor => {
      const stateAction = `${node.id}-${neighbor}`;
      state.qTable.set(stateAction, Math.random() * 0.1);
    });
  });
}

function handleSourceChange(event) {
  state.source = event.target.value;
  if (state.destination && state.source !== state.destination) {
    calculateAndShowPath();
  }
  drawNetwork();
  updateDisplay();
}

function handleDestinationChange(event) {
  state.destination = event.target.value;
  if (state.source && state.destination && state.source !== state.destination) {
    calculateAndShowPath();
  }
  drawNetwork();
  updateDisplay();
}

function handleModeChange(event) {
  state.mode = event.target.value;
  if (state.source && state.destination) {
    calculateAndShowPath();
  }
  drawNetwork();
  updateDisplay();
}

function handleCanvasClick(event) {
  const rect = canvas.getBoundingClientRect();
  const x = event.clientX - rect.left;
  const y = event.clientY - rect.top;
  
  // Check if click is on a link
  const clickedLink = findClickedLink(x, y);
  if (clickedLink) {
    clickedLink.congested = !clickedLink.congested;
    
    // Recalculate path after congestion change
    if (state.source && state.destination) {
      calculateAndShowPath();
    }
    drawNetwork();
    updateDisplay();
  }
}

function findClickedLink(clickX, clickY) {
  for (const link of networkData.links) {
    const fromNode = networkData.nodes.find(n => n.id === link.from);
    const toNode = networkData.nodes.find(n => n.id === link.to);
    
    if (!fromNode || !toNode) continue;
    
    // Check if click is near the link line
    const distance = distanceToLine(clickX, clickY, fromNode.x, fromNode.y, toNode.x, toNode.y);
    if (distance < 15) { // Increased tolerance for easier clicking
      return link;
    }
  }
  return null;
}

function distanceToLine(px, py, x1, y1, x2, y2) {
  const dx = x2 - x1;
  const dy = y2 - y1;
  const length = Math.sqrt(dx * dx + dy * dy);
  
  if (length === 0) return Math.sqrt((px - x1) * (px - x1) + (py - y1) * (py - y1));
  
  const t = Math.max(0, Math.min(1, ((px - x1) * dx + (py - y1) * dy) / (length * length)));
  const projection_x = x1 + t * dx;
  const projection_y = y1 + t * dy;
  
  return Math.sqrt((px - projection_x) * (px - projection_x) + (py - projection_y) * (py - projection_y));
}

function startSimulation() {
  if (!state.destination || state.source === state.destination) {
    alert('Please select a valid source and destination');
    return;
  }
  
  state.isRunning = true;
  state.packetCount = 0;
  state.successCount = 0;
  
  document.getElementById('startBtn').disabled = true;
  document.getElementById('startBtn').textContent = 'Simulating...';
  
  runPacketSimulation();
}

function runPacketSimulation() {
  if (!state.isRunning) return;
  
  const path = calculatePath(state.source, state.destination, state.mode);
  state.currentPath = path;
  
  // Simulate packet transmission
  state.packetCount++;
  
  // Check if packet would succeed (no congested links in path)
  const hasCongestedLink = pathHasCongestedLinks(path);
  if (!hasCongestedLink) {
    state.successCount++;
  }
  
  // Update Q-table if in AI mode
  if (state.mode === 'ai') {
    updateQTable(path, !hasCongestedLink);
    state.learningSteps++;
  }
  
  updateDisplay();
  drawNetwork();
  
  // Continue simulation
  setTimeout(() => {
    if (state.isRunning && state.packetCount < 20) { // Reduced for quicker demo
      runPacketSimulation();
    } else {
      stopSimulation();
    }
  }, 200); // Faster animation
}

function stopSimulation() {
  state.isRunning = false;
  document.getElementById('startBtn').disabled = false;
  document.getElementById('startBtn').textContent = 'Start Simulation';
}

function addRandomCongestion() {
  // Add congestion to a random link
  const availableLinks = networkData.links.filter(link => !link.congested);
  if (availableLinks.length > 0) {
    const randomLink = availableLinks[Math.floor(Math.random() * availableLinks.length)];
    randomLink.congested = true;
    
    // Recalculate path after adding congestion
    if (state.source && state.destination) {
      calculateAndShowPath();
    }
    drawNetwork();
    updateDisplay();
  }
}

function resetNetwork() {
  // Reset all congestion
  networkData.links.forEach(link => {
    link.congested = false;
  });
  
  // Reset simulation state
  state.isRunning = false;
  state.currentPath = [];
  state.packetCount = 0;
  state.successCount = 0;
  state.learningSteps = 0;
  
  // Reinitialize Q-table
  initializeQTable();
  
  document.getElementById('startBtn').disabled = false;
  document.getElementById('startBtn').textContent = 'Start Simulation';
  
  // Recalculate clean path
  if (state.source && state.destination) {
    calculateAndShowPath();
  }
  
  drawNetwork();
  updateDisplay();
}

function calculatePath(source, destination, mode) {
  if (mode === 'traditional') {
    return dijkstraPath(source, destination, false); // Don't consider congestion
  } else {
    return aiPath(source, destination);
  }
}

function dijkstraPath(source, destination, considerCongestion = true) {
  const distances = {};
  const previous = {};
  const unvisited = new Set();
  
  // Initialize
  networkData.nodes.forEach(node => {
    distances[node.id] = Infinity;
    unvisited.add(node.id);
  });
  distances[source] = 0;
  
  while (unvisited.size > 0) {
    // Find minimum distance unvisited node
    let current = null;
    for (const node of unvisited) {
      if (current === null || distances[node] < distances[current]) {
        current = node;
      }
    }
    
    if (current === destination) break;
    unvisited.delete(current);
    
    // Update neighbors
    const neighbors = getNeighbors(current);
    neighbors.forEach(neighbor => {
      if (!unvisited.has(neighbor)) return;
      
      const link = getLink(current, neighbor);
      let cost = link.cost;
      
      // Traditional routing ignores congestion, AI considers it
      if (considerCongestion && link.congested) {
        cost += 50; // Heavy penalty for congested links
      }
      
      const alt = distances[current] + cost;
      
      if (alt < distances[neighbor]) {
        distances[neighbor] = alt;
        previous[neighbor] = current;
      }
    });
  }
  
  // Reconstruct path
  const path = [];
  let current = destination;
  while (current) {
    path.unshift(current);
    current = previous[current];
  }
  
  return path.length > 1 && path[0] === source ? path : [source];
}

function aiPath(source, destination) {
  // AI path uses Q-learning to make decisions, considering congestion
  const path = [source];
  let current = source;
  const visited = new Set([source]);
  const maxHops = 6;
  
  while (current !== destination && path.length < maxHops) {
    const neighbors = getNeighbors(current).filter(n => !visited.has(n));
    if (neighbors.length === 0) break;
    
    let nextNode;
    
    // Epsilon-greedy: sometimes explore, usually exploit best Q-value
    if (Math.random() < 0.2) { // 20% exploration
      nextNode = neighbors[Math.floor(Math.random() * neighbors.length)];
    } else {
      // Choose neighbor with highest Q-value, considering congestion
      nextNode = neighbors.reduce((best, neighbor) => {
        const link1 = getLink(current, neighbor);
        const link2 = getLink(current, best);
        
        let qValue1 = state.qTable.get(`${current}-${neighbor}`) || 0;
        let qValue2 = state.qTable.get(`${current}-${best}`) || 0;
        
        // Penalize congested links in AI decision
        if (link1 && link1.congested) qValue1 -= 2;
        if (link2 && link2.congested) qValue2 -= 2;
        
        return qValue1 > qValue2 ? neighbor : best;
      });
    }
    
    path.push(nextNode);
    visited.add(nextNode);
    current = nextNode;
  }
  
  // If we didn't reach destination, use dijkstra with congestion consideration
  if (current !== destination) {
    return dijkstraPath(source, destination, true);
  }
  
  return path;
}

function updateQTable(path, success) {
  if (path.length < 2) return;
  
  const reward = success ? 10 : -5; // Positive reward for success, negative for failure
  
  // Update Q-values for each step in the path
  for (let i = 0; i < path.length - 1; i++) {
    const stateAction = `${path[i]}-${path[i + 1]}`;
    const currentQ = state.qTable.get(stateAction) || 0;
    
    // Simple Q-learning update
    const learningRate = 0.1;
    const newQ = currentQ + learningRate * (reward - currentQ);
    state.qTable.set(stateAction, newQ);
  }
}

function getNeighbors(nodeId) {
  const neighbors = [];
  networkData.links.forEach(link => {
    if (link.from === nodeId) neighbors.push(link.to);
    if (link.to === nodeId) neighbors.push(link.from);
  });
  return neighbors;
}

function getLink(from, to) {
  return networkData.links.find(link => 
    (link.from === from && link.to === to) || 
    (link.from === to && link.to === from)
  );
}

function pathHasCongestedLinks(path) {
  for (let i = 0; i < path.length - 1; i++) {
    const link = getLink(path[i], path[i + 1]);
    if (link && link.congested) {
      return true;
    }
  }
  return false;
}

function calculatePathCost(path) {
  let totalCost = 0;
  for (let i = 0; i < path.length - 1; i++) {
    const link = getLink(path[i], path[i + 1]);
    if (link) {
      totalCost += link.cost + (link.congested ? 50 : 0); // High congestion penalty
    }
  }
  return totalCost;
}

function calculateAndShowPath() {
  if (!state.source || !state.destination || state.source === state.destination) {
    state.currentPath = [];
    document.getElementById('currentExplanation').textContent = "Select different source and destination nodes.";
    document.getElementById('pathComparison').classList.add('hidden');
    return;
  }
  
  // Calculate current mode path
  const currentPath = calculatePath(state.source, state.destination, state.mode);
  state.currentPath = currentPath;
  
  // Calculate both paths for comparison
  const traditionalPath = dijkstraPath(state.source, state.destination, false);
  const aiPathResult = aiPath(state.source, state.destination);
  
  // Update explanation
  updateExplanation(traditionalPath, aiPathResult, currentPath);
  
  // Show path comparison
  document.getElementById('traditionalPath').textContent = traditionalPath.join(' → ');
  document.getElementById('aiPath').textContent = aiPathResult.join(' → ');
  document.getElementById('pathComparison').classList.remove('hidden');
}

function updateExplanation(traditionalPath, aiPathResult, currentPath) {
  let explanation = "";
  
  const hasCongestedInTraditional = pathHasCongestedLinks(traditionalPath);
  const hasCongestedInAI = pathHasCongestedLinks(aiPathResult);
  
  if (state.mode === 'traditional') {
    explanation = `Traditional routing uses shortest path: ${currentPath.join(' → ')}. `;
    if (hasCongestedInTraditional) {
      explanation += "⚠️ This path has congestion but traditional routing doesn't adapt!";
    } else {
      explanation += "This path is clear of congestion.";
    }
  } else {
    explanation = `AI routing chose: ${currentPath.join(' → ')}. `;
    
    if (JSON.stringify(traditionalPath) !== JSON.stringify(aiPathResult)) {
      explanation += "🤖 AI learned to avoid congested routes - notice the different path!";
    } else {
      if (hasCongestedInAI) {
        explanation += "AI is still learning better routes...";
      } else {
        explanation += "AI agrees with traditional routing for this scenario.";
      }
    }
  }
  
  document.getElementById('currentExplanation').textContent = explanation;
}

function updateDisplay() {
  // Update metrics
  const pathCost = state.currentPath.length > 0 ? calculatePathCost(state.currentPath) : 0;
  const successRate = state.packetCount > 0 ? Math.round((state.successCount / state.packetCount) * 100) : 0;
  
  document.getElementById('pathCost').textContent = pathCost > 0 ? pathCost : '--';
  document.getElementById('packetCount').textContent = state.packetCount;
  document.getElementById('successRate').textContent = state.packetCount > 0 ? `${successRate}%` : '--%';
  document.getElementById('learningSteps').textContent = state.learningSteps;
  
  // Color code success rate
  const successElement = document.getElementById('successRate');
  successElement.className = 'metric-value';
  if (successRate >= 80) successElement.classList.add('success');
  else if (successRate >= 60) successElement.classList.add('warning');
  else if (successRate > 0) successElement.classList.add('error');
}

function drawNetwork() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  
  // Draw links first (so they appear under nodes)
  networkData.links.forEach(link => {
    const fromNode = networkData.nodes.find(n => n.id === link.from);
    const toNode = networkData.nodes.find(n => n.id === link.to);
    
    if (!fromNode || !toNode) return;
    
    // Determine link appearance
    let strokeStyle = '#626C71'; // Normal (gray)
    let lineWidth = 3;
    
    if (link.congested) {
      strokeStyle = '#C0152F'; // Congested (red)
      lineWidth = 4;
    }
    
    // Highlight if part of current path
    const isInCurrentPath = isLinkInPath(link, state.currentPath);
    if (isInCurrentPath) {
      strokeStyle = '#1FB8CD'; // Selected path (bright teal)
      lineWidth = 6;
    }
    
    // Draw link
    ctx.beginPath();
    ctx.moveTo(fromNode.x, fromNode.y);
    ctx.lineTo(toNode.x, toNode.y);
    ctx.strokeStyle = strokeStyle;
    ctx.lineWidth = lineWidth;
    ctx.stroke();
    
    // Draw cost label
    const midX = (fromNode.x + toNode.x) / 2;
    const midY = (fromNode.y + toNode.y) / 2;
    
    // Background for cost label
    ctx.fillStyle = 'rgba(252, 252, 249, 0.8)';
    ctx.fillRect(midX - 12, midY - 18, 24, 16);
    
    ctx.fillStyle = '#134A3B';
    ctx.font = 'bold 11px "FKGroteskNeue", sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(link.cost.toString(), midX, midY - 10);
  });
  
  // Draw nodes
  networkData.nodes.forEach(node => {
    let fillStyle = '#21808D'; // Default node color
    let strokeStyle = '#1D7480';
    
    // Highlight source and destination
    if (node.id === state.source) {
      fillStyle = '#32B8C6'; // Highlighted source
      strokeStyle = '#1FB8CD';
    } else if (node.id === state.destination) {
      fillStyle = '#A84B2F'; // Different color for destination
      strokeStyle = '#C0152F';
    }
    
    // Draw node circle
    ctx.beginPath();
    ctx.arc(node.x, node.y, nodeRadius, 0, 2 * Math.PI);
    ctx.fillStyle = fillStyle;
    ctx.fill();
    ctx.strokeStyle = strokeStyle;
    ctx.lineWidth = 3;
    ctx.stroke();
    
    // Draw node label
    ctx.fillStyle = '#FCFCF9';
    ctx.font = 'bold 18px "FKGroteskNeue", sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(node.id, node.x, node.y);
  });
}

function isLinkInPath(link, path) {
  if (path.length < 2) return false;
  
  for (let i = 0; i < path.length - 1; i++) {
    const from = path[i];
    const to = path[i + 1];
    if ((link.from === from && link.to === to) || 
        (link.from === to && link.to === from)) {
      return true;
    }
  }
  return false;
}