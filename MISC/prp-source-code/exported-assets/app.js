// Network topology data
const networkData = {
  nodes: [
    {id: "A", x: 100, y: 150, label: "Router A"},
    {id: "B", x: 250, y: 100, label: "Router B"},
    {id: "C", x: 400, y: 150, label: "Router C"},
    {id: "D", x: 550, y: 100, label: "Router D"},
    {id: "E", x: 100, y: 300, label: "Router E"},
    {id: "F", x: 250, y: 250, label: "Router F"},
    {id: "G", x: 400, y: 300, label: "Router G"},
    {id: "H", x: 550, y: 250, label: "Router H"}
  ],
  links: [
    {from: "A", to: "B", latency: 10, capacity: 100, congestion: 0, failed: false},
    {from: "A", to: "E", latency: 15, capacity: 80, congestion: 0, failed: false},
    {from: "B", to: "C", latency: 12, capacity: 90, congestion: 0, failed: false},
    {from: "B", to: "F", latency: 8, capacity: 120, congestion: 0, failed: false},
    {from: "C", to: "D", latency: 11, capacity: 95, congestion: 0, failed: false},
    {from: "C", to: "G", latency: 14, capacity: 85, congestion: 0, failed: false},
    {from: "D", to: "H", latency: 9, capacity: 110, congestion: 0, failed: false},
    {from: "E", to: "F", latency: 13, capacity: 75, congestion: 0, failed: false},
    {from: "F", to: "G", latency: 10, capacity: 100, congestion: 0, failed: false},
    {from: "G", to: "H", latency: 12, capacity: 90, congestion: 0, failed: false},
    {from: "A", to: "F", latency: 20, capacity: 60, congestion: 0, failed: false},
    {from: "C", to: "H", latency: 18, capacity: 70, congestion: 0, failed: false}
  ]
};

// Simulation state
let simulationState = {
  isRunning: false,
  source: null,
  destination: null,
  currentPath: [],
  algorithm: 'ai',
  aiEnabled: true,
  animationSpeed: 1,
  failureRate: 10,
  congestionLevel: 20,
  metrics: {
    latency: 0,
    hops: 0,
    packetLoss: 0,
    learningProgress: 0
  },
  qLearning: {
    qTable: new Map(),
    epsilon: 0.1,
    learningRate: 0.1,
    discount: 0.9,
    episodes: 0
  },
  performance: {
    traditional: 0,
    ai: 0
  }
};

// Canvas and rendering
let canvas, ctx;
const nodeRadius = 25;
const selectedNodeColor = '#1FB8CD';
const pathColor = '#1FB8CD';

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
  initializeCanvas();
  initializeControls();
  initializeTabs();
  updateNetworkConditions();
  drawNetwork();
  
  // Initialize Q-table with random values
  initializeQTable();
  
  // Start background network condition simulation
  setInterval(updateNetworkDynamics, 2000);
});

function initializeCanvas() {
  canvas = document.getElementById('networkCanvas');
  ctx = canvas.getContext('2d');
  
  canvas.addEventListener('click', handleCanvasClick);
  
  // Set canvas size
  canvas.width = 600;
  canvas.height = 400;
}

function initializeControls() {
  // Source and destination selects
  document.getElementById('sourceSelect').addEventListener('change', handleSourceChange);
  document.getElementById('destinationSelect').addEventListener('change', handleDestinationChange);
  
  // Simulation controls
  document.getElementById('startBtn').addEventListener('click', startSimulation);
  document.getElementById('pauseBtn').addEventListener('click', pauseSimulation);
  document.getElementById('resetBtn').addEventListener('click', resetSimulation);
  
  // AI controls
  document.getElementById('aiEnabled').addEventListener('change', handleAIToggle);
  document.getElementById('algorithmSelect').addEventListener('change', handleAlgorithmChange);
  
  // Network condition sliders
  document.getElementById('failureRate').addEventListener('input', handleFailureRateChange);
  document.getElementById('congestionLevel').addEventListener('input', handleCongestionChange);
  document.getElementById('animationSpeed').addEventListener('input', handleSpeedChange);
}

function initializeTabs() {
  const tabButtons = document.querySelectorAll('.tab-btn');
  const tabPanes = document.querySelectorAll('.tab-pane');
  
  tabButtons.forEach(button => {
    button.addEventListener('click', () => {
      const targetTab = button.getAttribute('data-tab');
      
      // Remove active class from all buttons and panes
      tabButtons.forEach(btn => btn.classList.remove('active'));
      tabPanes.forEach(pane => pane.classList.remove('active'));
      
      // Add active class to clicked button and corresponding pane
      button.classList.add('active');
      document.getElementById(targetTab).classList.add('active');
    });
  });
}

function initializeQTable() {
  // Initialize Q-table with small random values for each state-action pair
  networkData.nodes.forEach(node => {
    const neighbors = getNeighbors(node.id);
    neighbors.forEach(neighbor => {
      const state = `${node.id}->${neighbor}`;
      simulationState.qLearning.qTable.set(state, Math.random() * 0.1);
    });
  });
}

function handleCanvasClick(event) {
  const rect = canvas.getBoundingClientRect();
  const x = event.clientX - rect.left;
  const y = event.clientY - rect.top;
  
  // Find clicked node
  const clickedNode = networkData.nodes.find(node => {
    const distance = Math.sqrt((x - node.x) ** 2 + (y - node.y) ** 2);
    return distance <= nodeRadius;
  });
  
  if (clickedNode) {
    if (!simulationState.source) {
      setSource(clickedNode.id);
    } else if (!simulationState.destination && clickedNode.id !== simulationState.source) {
      setDestination(clickedNode.id);
    } else {
      // Reset selection
      resetSelection();
      setSource(clickedNode.id);
    }
  }
}

function setSource(nodeId) {
  simulationState.source = nodeId;
  document.getElementById('sourceSelect').value = nodeId;
  updatePathDisplay();
  drawNetwork();
}

function setDestination(nodeId) {
  simulationState.destination = nodeId;
  document.getElementById('destinationSelect').value = nodeId;
  updatePathDisplay();
  drawNetwork();
}

function resetSelection() {
  simulationState.source = null;
  simulationState.destination = null;
  simulationState.currentPath = [];
  document.getElementById('sourceSelect').value = '';
  document.getElementById('destinationSelect').value = '';
}

function handleSourceChange(event) {
  const value = event.target.value;
  simulationState.source = value || null;
  updatePathDisplay();
  drawNetwork();
}

function handleDestinationChange(event) {
  const value = event.target.value;
  simulationState.destination = value || null;
  updatePathDisplay();
  drawNetwork();
}

function startSimulation() {
  if (!simulationState.source || !simulationState.destination) {
    alert('Please select both source and destination nodes');
    return;
  }
  
  simulationState.isRunning = true;
  document.getElementById('startBtn').textContent = 'Running...';
  document.getElementById('startBtn').disabled = true;
  
  runSimulation();
}

function pauseSimulation() {
  simulationState.isRunning = false;
  document.getElementById('startBtn').textContent = 'Start Simulation';
  document.getElementById('startBtn').disabled = false;
}

function resetSimulation() {
  simulationState.isRunning = false;
  simulationState.currentPath = [];
  simulationState.metrics = {
    latency: 0,
    hops: 0,
    packetLoss: 0,
    learningProgress: 0
  };
  
  // Reset network conditions
  networkData.links.forEach(link => {
    link.congestion = 0;
    link.failed = false;
  });
  
  document.getElementById('startBtn').textContent = 'Start Simulation';
  document.getElementById('startBtn').disabled = false;
  
  updateMetricsDisplay();
  drawNetwork();
}

function handleAIToggle(event) {
  simulationState.aiEnabled = event.target.checked;
  simulationState.algorithm = event.target.checked ? 'ai' : 'traditional';
  document.getElementById('algorithmSelect').value = simulationState.algorithm;
  updatePathDisplay();
}

function handleAlgorithmChange(event) {
  simulationState.algorithm = event.target.value;
  simulationState.aiEnabled = event.target.value === 'ai';
  document.getElementById('aiEnabled').checked = simulationState.aiEnabled;
  updatePathDisplay();
}

function handleFailureRateChange(event) {
  simulationState.failureRate = parseInt(event.target.value);
  document.getElementById('failureRateValue').textContent = `${simulationState.failureRate}%`;
  updateNetworkConditions();
}

function handleCongestionChange(event) {
  simulationState.congestionLevel = parseInt(event.target.value);
  document.getElementById('congestionValue').textContent = `${simulationState.congestionLevel}%`;
  updateNetworkConditions();
}

function handleSpeedChange(event) {
  simulationState.animationSpeed = parseFloat(event.target.value);
  document.getElementById('speedValue').textContent = `${simulationState.animationSpeed}x`;
}

function updateNetworkConditions() {
  networkData.links.forEach(link => {
    // Apply random failures based on failure rate
    if (Math.random() * 100 < simulationState.failureRate) {
      link.failed = Math.random() < 0.3; // 30% chance of actual failure
    }
    
    // Apply congestion based on congestion level
    link.congestion = Math.random() * simulationState.congestionLevel / 100;
  });
  
  drawNetwork();
}

function updateNetworkDynamics() {
  if (!simulationState.isRunning) return;
  
  // Simulate dynamic network conditions
  networkData.links.forEach(link => {
    // Randomly change congestion levels
    link.congestion += (Math.random() - 0.5) * 0.1;
    link.congestion = Math.max(0, Math.min(1, link.congestion));
    
    // Randomly fix/break links
    if (Math.random() < 0.05) { // 5% chance of state change
      link.failed = !link.failed && Math.random() < simulationState.failureRate / 100;
    }
  });
  
  // Recalculate path if needed
  if (simulationState.source && simulationState.destination) {
    updatePathDisplay();
  }
  
  drawNetwork();
}

function runSimulation() {
  if (!simulationState.isRunning) return;
  
  const path = calculatePath(simulationState.source, simulationState.destination);
  simulationState.currentPath = path;
  
  // Update metrics
  updateMetrics(path);
  updateMetricsDisplay();
  updateQValues();
  updatePerformanceComparison();
  
  // Continue simulation
  setTimeout(() => {
    if (simulationState.isRunning) {
      runSimulation();
    }
  }, 1000 / simulationState.animationSpeed);
  
  drawNetwork();
}

function calculatePath(source, destination) {
  if (simulationState.algorithm === 'traditional') {
    return dijkstraPath(source, destination);
  } else {
    return qLearningPath(source, destination);
  }
}

function dijkstraPath(source, destination) {
  const distances = {};
  const previous = {};
  const unvisited = new Set();
  
  // Initialize distances
  networkData.nodes.forEach(node => {
    distances[node.id] = Infinity;
    unvisited.add(node.id);
  });
  distances[source] = 0;
  
  while (unvisited.size > 0) {
    // Find unvisited node with minimum distance
    let current = null;
    for (const node of unvisited) {
      if (current === null || distances[node] < distances[current]) {
        current = node;
      }
    }
    
    if (current === destination) break;
    
    unvisited.delete(current);
    
    // Check neighbors
    const neighbors = getNeighbors(current);
    neighbors.forEach(neighbor => {
      if (!unvisited.has(neighbor)) return;
      
      const link = getLink(current, neighbor);
      if (link.failed) return;
      
      const distance = distances[current] + link.latency + (link.congestion * 10);
      if (distance < distances[neighbor]) {
        distances[neighbor] = distance;
        previous[neighbor] = current;
      }
    });
  }
  
  // Reconstruct path
  const path = [];
  let current = destination;
  while (current !== undefined) {
    path.unshift(current);
    current = previous[current];
  }
  
  return path.length > 1 ? path : [];
}

function qLearningPath(source, destination) {
  const path = [source];
  let current = source;
  const maxSteps = 10;
  let steps = 0;
  
  while (current !== destination && steps < maxSteps) {
    const neighbors = getNeighbors(current);
    const availableNeighbors = neighbors.filter(neighbor => {
      const link = getLink(current, neighbor);
      return !link.failed && !path.includes(neighbor);
    });
    
    if (availableNeighbors.length === 0) break;
    
    let nextNode;
    if (Math.random() < simulationState.qLearning.epsilon) {
      // Exploration: random action
      nextNode = availableNeighbors[Math.floor(Math.random() * availableNeighbors.length)];
    } else {
      // Exploitation: best Q-value
      nextNode = availableNeighbors.reduce((best, neighbor) => {
        const stateAction = `${current}->${neighbor}`;
        const qValue = simulationState.qLearning.qTable.get(stateAction) || 0;
        const bestStateAction = `${current}->${best}`;
        const bestQValue = simulationState.qLearning.qTable.get(bestStateAction) || 0;
        return qValue > bestQValue ? neighbor : best;
      });
    }
    
    path.push(nextNode);
    current = nextNode;
    steps++;
  }
  
  // Update Q-values based on path performance
  updateQTable(path);
  
  return path;
}

function updateQTable(path) {
  if (path.length < 2) return;
  
  const totalLatency = calculatePathLatency(path);
  const reward = -totalLatency; // Negative latency as reward (lower is better)
  
  // Update Q-values for each step in the path
  for (let i = 0; i < path.length - 1; i++) {
    const state = path[i];
    const action = path[i + 1];
    const stateAction = `${state}->${action}`;
    
    const currentQ = simulationState.qLearning.qTable.get(stateAction) || 0;
    const futureQ = i < path.length - 2 ? 
      simulationState.qLearning.qTable.get(`${action}->${path[i + 2]}`) || 0 : 0;
    
    const newQ = currentQ + simulationState.qLearning.learningRate * 
      (reward + simulationState.qLearning.discount * futureQ - currentQ);
    
    simulationState.qLearning.qTable.set(stateAction, newQ);
  }
  
  simulationState.qLearning.episodes++;
  
  // Decrease exploration over time
  simulationState.qLearning.epsilon = Math.max(0.01, 
    simulationState.qLearning.epsilon * 0.995);
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

function calculatePathLatency(path) {
  if (path.length < 2) return 0;
  
  let totalLatency = 0;
  for (let i = 0; i < path.length - 1; i++) {
    const link = getLink(path[i], path[i + 1]);
    if (link) {
      totalLatency += link.latency + (link.congestion * 20);
    }
  }
  return totalLatency;
}

function updateMetrics(path) {
  simulationState.metrics.latency = calculatePathLatency(path);
  simulationState.metrics.hops = Math.max(0, path.length - 1);
  
  // Calculate packet loss based on congestion
  let totalCongestion = 0;
  for (let i = 0; i < path.length - 1; i++) {
    const link = getLink(path[i], path[i + 1]);
    if (link) totalCongestion += link.congestion;
  }
  simulationState.metrics.packetLoss = Math.min(100, totalCongestion * 50);
  
  // Update learning progress
  simulationState.metrics.learningProgress = Math.min(100, 
    simulationState.qLearning.episodes * 2);
}

function updateMetricsDisplay() {
  document.getElementById('currentLatency').textContent = 
    `${Math.round(simulationState.metrics.latency)} ms`;
  document.getElementById('hopCount').textContent = 
    simulationState.metrics.hops;
  document.getElementById('packetLoss').textContent = 
    `${Math.round(simulationState.metrics.packetLoss)}%`;
  document.getElementById('learningProgress').textContent = 
    `${Math.round(simulationState.metrics.learningProgress)}%`;
}

function updateQValues() {
  if (!simulationState.source || !simulationState.destination) return;
  
  const neighbors = getNeighbors(simulationState.source);
  if (neighbors.length > 0) {
    const bestNeighbor = neighbors.reduce((best, neighbor) => {
      const stateAction1 = `${simulationState.source}->${neighbor}`;
      const stateAction2 = `${simulationState.source}->${best}`;
      const qValue1 = simulationState.qLearning.qTable.get(stateAction1) || 0;
      const qValue2 = simulationState.qLearning.qTable.get(stateAction2) || 0;
      return qValue1 > qValue2 ? neighbor : best;
    });
    
    const bestStateAction = `${simulationState.source}->${bestNeighbor}`;
    const bestQValue = simulationState.qLearning.qTable.get(bestStateAction) || 0;
    
    document.getElementById('currentState').textContent = simulationState.source;
    document.getElementById('bestAction').textContent = bestNeighbor;
    document.getElementById('qValue').textContent = bestQValue.toFixed(3);
  }
}

function updatePerformanceComparison() {
  // Calculate performance scores (inverse of latency + packet loss)
  const traditionaScore = Math.max(0, 100 - (simulationState.metrics.latency / 10 + simulationState.metrics.packetLoss));
  const aiScore = Math.max(0, traditionaScore + simulationState.metrics.learningProgress / 5);
  
  simulationState.performance.traditional = traditionaScore;
  simulationState.performance.ai = aiScore;
  
  document.getElementById('traditionalPerf').style.width = `${traditionaScore}%`;
  document.getElementById('aiPerf').style.width = `${aiScore}%`;
  document.getElementById('traditionalScore').textContent = Math.round(traditionaScore);
  document.getElementById('aiScore').textContent = Math.round(aiScore);
}

function updatePathDisplay() {
  if (!simulationState.source || !simulationState.destination) {
    simulationState.currentPath = [];
    document.getElementById('decisionExplanation').textContent = 
      'Select source and destination nodes to see routing decisions.';
    document.getElementById('pathDetails').innerHTML = '';
    return;
  }
  
  const path = calculatePath(simulationState.source, simulationState.destination);
  simulationState.currentPath = path;
  
  // Update decision explanation
  const algorithmName = simulationState.algorithm === 'ai' ? 'Deep Q-Learning' : 'Dijkstra\'s Algorithm';
  document.getElementById('decisionExplanation').textContent = 
    `Using ${algorithmName} to route from ${simulationState.source} to ${simulationState.destination}`;
  
  // Update path details
  if (path.length > 0) {
    const pathStr = path.join(' → ');
    const latency = calculatePathLatency(path);
    document.getElementById('pathDetails').innerHTML = 
      `<strong>Selected Path:</strong> ${pathStr}<br>
       <strong>Total Latency:</strong> ${Math.round(latency)} ms<br>
       <strong>Hops:</strong> ${path.length - 1}`;
  }
  
  drawNetwork();
}

function drawNetwork() {
  // Clear canvas
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  
  // Draw links
  networkData.links.forEach(link => {
    const fromNode = networkData.nodes.find(n => n.id === link.from);
    const toNode = networkData.nodes.find(n => n.id === link.to);
    
    if (!fromNode || !toNode) return;
    
    // Determine link color based on state
    let linkColor = '#33808D'; // Default active color
    let lineWidth = 2;
    
    if (link.failed) {
      linkColor = '#C0152F'; // Failed
    } else if (link.congestion > 0.5) {
      linkColor = '#A84B2F'; // Congested
    }
    
    // Highlight if part of current path
    const isInPath = isLinkInPath(link, simulationState.currentPath);
    if (isInPath) {
      linkColor = '#1FB8CD'; // Selected path
      lineWidth = 4;
    }
    
    // Draw link
    ctx.beginPath();
    ctx.moveTo(fromNode.x, fromNode.y);
    ctx.lineTo(toNode.x, toNode.y);
    ctx.strokeStyle = linkColor;
    ctx.lineWidth = lineWidth;
    ctx.stroke();
    
    // Draw latency label
    const midX = (fromNode.x + toNode.x) / 2;
    const midY = (fromNode.y + toNode.y) / 2;
    ctx.fillStyle = '#626C71';
    ctx.font = '10px "FKGroteskNeue", sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(`${link.latency}ms`, midX, midY - 5);
  });
  
  // Draw nodes
  networkData.nodes.forEach(node => {
    let nodeColor = '#21808D'; // Default
    let borderColor = '#1D7480';
    let textColor = '#FCFCF9';
    
    // Highlight source and destination
    if (node.id === simulationState.source) {
      nodeColor = '#32B8C6';
      borderColor = '#1FB8CD';
    } else if (node.id === simulationState.destination) {
      nodeColor = '#32B8C6';
      borderColor = '#1FB8CD';
    }
    
    // Draw node circle
    ctx.beginPath();
    ctx.arc(node.x, node.y, nodeRadius, 0, 2 * Math.PI);
    ctx.fillStyle = nodeColor;
    ctx.fill();
    ctx.strokeStyle = borderColor;
    ctx.lineWidth = 2;
    ctx.stroke();
    
    // Draw node label
    ctx.fillStyle = textColor;
    ctx.font = 'bold 14px "FKGroteskNeue", sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(node.id, node.x, node.y + 5);
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