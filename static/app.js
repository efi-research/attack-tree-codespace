// Global state
let currentTreeData = null;
let currentFormat = 'svg';

// DOM Elements
const form = document.getElementById('scenarioForm');
const generateBtn = document.getElementById('generateBtn');
const clearBtn = document.getElementById('clearBtn');
const loadingState = document.getElementById('loadingState');
const errorState = document.getElementById('errorState');
const errorMessage = document.getElementById('errorMessage');
const resultsSection = document.getElementById('resultsSection');
const treeVisualization = document.getElementById('treeVisualization');
const jsonOutput = document.getElementById('jsonOutput');

// Event Listeners
form.addEventListener('submit', handleGenerate);
clearBtn.addEventListener('click', handleClear);

// Handle form submission
async function handleGenerate(e) {
    e.preventDefault();

    const title = document.getElementById('title').value.trim();
    const description = document.getElementById('description').value.trim();

    if (!title || !description) {
        showError('Please fill in both title and description');
        return;
    }

    // Show loading state
    showLoading();
    hideError();
    hideResults();

    try {
        // Step 1: Generate attack tree JSON
        const treeData = await generateAttackTree(title, description);
        currentTreeData = treeData;

        // Step 2: Show results with D3 rendering
        displayResults(treeData);

    } catch (error) {
        console.error('Error:', error);
        showError(error.message || 'An unexpected error occurred');
    } finally {
        hideLoading();
    }
}

// Call the /generate endpoint
async function generateAttackTree(title, description) {
    const response = await fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title, description })
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
}

// Render tree using D3.js in the frontend
function renderTreeD3(treeData) {
    // Convert attack tree JSON to D3 hierarchy format
    const hierarchyData = convertToHierarchy(treeData);

    // Clear previous visualization
    treeVisualization.innerHTML = '';

    // Set up SVG dimensions
    const width = 1200;
    const height = 800;
    const margin = { top: 40, right: 120, bottom: 40, left: 120 };

    // Create SVG element
    const svg = d3.select('#treeVisualization')
        .append('svg')
        .attr('width', width)
        .attr('height', height)
        .attr('viewBox', [0, 0, width, height])
        .attr('style', 'max-width: 100%; height: auto;');

    const g = svg.append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    // Create tree layout
    const treeLayout = d3.tree()
        .size([height - margin.top - margin.bottom, width - margin.left - margin.right]);

    // Create hierarchy
    const root = d3.hierarchy(hierarchyData);

    // Apply tree layout
    treeLayout(root);

    // Draw links (edges)
    g.selectAll('.link')
        .data(root.links())
        .enter()
        .append('path')
        .attr('class', 'link')
        .attr('fill', 'none')
        .attr('stroke', '#64748b')
        .attr('stroke-width', 2)
        .attr('d', d3.linkHorizontal()
            .x(d => d.y)
            .y(d => d.x));

    // Draw nodes
    const node = g.selectAll('.node')
        .data(root.descendants())
        .enter()
        .append('g')
        .attr('class', 'node')
        .attr('transform', d => `translate(${d.y},${d.x})`);

    // Add rectangles for nodes
    node.append('rect')
        .attr('width', d => d.depth === 0 ? 160 : 140)
        .attr('height', d => {
            // Calculate height based on label content
            const lines = d.data.label.split('\n').length;
            return Math.max(50, lines * 20 + 10);
        })
        .attr('x', d => d.depth === 0 ? -80 : -70)
        .attr('y', d => {
            const lines = d.data.label.split('\n').length;
            const height = Math.max(50, lines * 20 + 10);
            return -height / 2;
        })
        .attr('rx', 5)
        .attr('fill', d => d.depth === 0 ? '#e0f2fe' : '#f8fafc')
        .attr('stroke', d => d.depth === 0 ? '#0284c7' : '#64748b')
        .attr('stroke-width', 2);

    // Add text labels (multi-line support)
    node.each(function(d) {
        const nodeGroup = d3.select(this);
        const lines = d.data.label.split('\n');
        const lineHeight = 16;
        const startY = -(lines.length - 1) * lineHeight / 2;

        lines.forEach((line, i) => {
            nodeGroup.append('text')
                .attr('dy', startY + i * lineHeight)
                .attr('text-anchor', 'middle')
                .attr('font-size', '12px')
                .attr('font-weight', d.depth === 0 ? 'bold' : 'normal')
                .attr('fill', '#1e293b')
                .text(line);
        });
    });

    return svg.node();
}

// Convert attack tree JSON to D3 hierarchy format
function convertToHierarchy(treeData) {
    // Create a map of all nodes by ID
    const nodeMap = new Map();

    // Add root node
    const rootNode = {
        id: 'root',
        label: treeData.goal,
        children: []
    };
    nodeMap.set('root', rootNode);

    // Add all other nodes
    treeData.nodes.forEach(node => {
        const label = buildNodeLabel(node);
        nodeMap.set(node.id, {
            id: node.id,
            label: label,
            children: []
        });
    });

    // Build hierarchy by connecting children
    const childIds = new Set();
    treeData.nodes.forEach(node => {
        node.children.forEach(childId => {
            childIds.add(childId);
        });
    });

    // Find top-level nodes (not children of any node)
    const topLevelNodes = treeData.nodes.filter(node => !childIds.has(node.id));

    // Connect top-level nodes to root
    topLevelNodes.forEach(node => {
        const hierarchyNode = nodeMap.get(node.id);
        if (hierarchyNode) {
            rootNode.children.push(hierarchyNode);
        }
    });

    // Connect all other parent-child relationships
    treeData.nodes.forEach(node => {
        const parentNode = nodeMap.get(node.id);
        if (parentNode) {
            node.children.forEach(childId => {
                const childNode = nodeMap.get(childId);
                if (childNode) {
                    parentNode.children.push(childNode);
                }
            });
        }
    });

    return rootNode;
}

// Build node label with metrics
function buildNodeLabel(node) {
    let label = node.text;
    const extras = [];

    if (node.probability !== null && node.probability !== undefined) {
        extras.push(`P=${node.probability}`);
    }
    if (node.cost !== null && node.cost !== undefined) {
        extras.push(`C=${node.cost}`);
    }

    if (extras.length > 0) {
        label += '\n(' + extras.join(', ') + ')';
    }

    return label;
}

// Display results in UI
function displayResults(treeData) {
    // Show JSON
    jsonOutput.textContent = JSON.stringify(treeData, null, 2);

    // Render the tree using D3
    renderTreeD3(treeData);

    // Show results section
    showResults();
}

// Switch between PNG and SVG formats
function switchFormat(format) {
    if (!currentTreeData) return;

    currentFormat = format;

    // Update button states
    document.querySelectorAll('.format-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.format === format);
    });

    // Note: The visualization is always SVG in the DOM.
    // PNG conversion happens only during download.
    // We could add visual feedback here if needed, but the SVG display works for both formats.
}

// Convert SVG to PNG using Canvas
async function svgToPng(svgElement) {
    return new Promise((resolve, reject) => {
        // Get SVG data
        const svgData = new XMLSerializer().serializeToString(svgElement);
        const svgBlob = new Blob([svgData], { type: 'image/svg+xml;charset=utf-8' });
        const url = URL.createObjectURL(svgBlob);

        // Create an image element
        const img = new Image();
        img.onload = () => {
            // Create canvas
            const canvas = document.createElement('canvas');
            canvas.width = svgElement.width.baseVal.value;
            canvas.height = svgElement.height.baseVal.value;

            // Draw image on canvas
            const ctx = canvas.getContext('2d');
            ctx.fillStyle = 'white';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(img, 0, 0);

            // Convert to blob
            canvas.toBlob(blob => {
                URL.revokeObjectURL(url);
                resolve(blob);
            }, 'image/png');
        };

        img.onerror = () => {
            URL.revokeObjectURL(url);
            reject(new Error('Failed to load SVG'));
        };

        img.src = url;
    });
}

// Download current image
async function downloadImage() {
    if (!currentTreeData) return;

    try {
        const svgElement = document.querySelector('#treeVisualization svg');
        if (!svgElement) {
            showError('No visualization found to download');
            return;
        }

        let blob;
        let filename;

        if (currentFormat === 'png') {
            // Convert SVG to PNG
            blob = await svgToPng(svgElement);
            filename = 'attack-tree.png';
        } else {
            // Download SVG directly
            const svgData = new XMLSerializer().serializeToString(svgElement);
            blob = new Blob([svgData], { type: 'image/svg+xml;charset=utf-8' });
            filename = 'attack-tree.svg';
        }

        // Trigger download
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    } catch (error) {
        console.error('Download error:', error);
        showError('Failed to download image: ' + error.message);
    }
}

// Download JSON data
function downloadJSON() {
    if (!currentTreeData) return;

    const dataStr = JSON.stringify(currentTreeData, null, 2);
    const blob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'attack-tree.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Clear form
function handleClear() {
    form.reset();
    document.getElementById('title').focus();
}

// Generate new tree (reset everything)
function generateNew() {
    hideResults();
    hideError();
    currentTreeData = null;
    currentFormat = 'svg';
    form.reset();
    document.getElementById('title').focus();
}

// UI State Management
function showLoading() {
    loadingState.style.display = 'block';
    generateBtn.disabled = true;
}

function hideLoading() {
    loadingState.style.display = 'none';
    generateBtn.disabled = false;
}

function showError(message) {
    errorMessage.textContent = message;
    errorState.style.display = 'block';
}

function hideError() {
    errorState.style.display = 'none';
}

function showResults() {
    resultsSection.style.display = 'block';
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function hideResults() {
    resultsSection.style.display = 'none';
}

// Sample data for testing (can be removed in production)
function fillSampleData() {
    document.getElementById('title').value = 'Web Application Breach';
    document.getElementById('description').value = 'An attacker wants to gain unauthorized access to a company web application to steal customer data. The application uses authentication, has a database backend, and is hosted on cloud infrastructure.';
}

// Add keyboard shortcut for sample data (Ctrl+Shift+S)
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.shiftKey && e.key === 'S') {
        e.preventDefault();
        fillSampleData();
    }
});

console.log('Attack Tree Generator loaded. Press Ctrl+Shift+S to fill sample data.');
