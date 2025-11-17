// Global state
let currentTreeData = null;
let currentFormat = 'svg';
let currentImageBlob = null;

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

        // Step 2: Render the tree as an image
        await renderTree(treeData, currentFormat);

        // Step 3: Show results
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

// Call the /render endpoint
async function renderTree(treeData, format = 'svg') {
    const response = await fetch(`/render?format=${format}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(treeData)
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Render failed! status: ${response.status}`);
    }

    const blob = await response.blob();
    currentImageBlob = blob;
    return blob;
}

// Display results in UI
function displayResults(treeData) {
    // Show JSON
    jsonOutput.textContent = JSON.stringify(treeData, null, 2);

    // Show visualization
    displayVisualization(currentImageBlob, currentFormat);

    // Show results section
    showResults();
}

// Display visualization based on format
function displayVisualization(blob, format) {
    const url = URL.createObjectURL(blob);

    if (format === 'svg') {
        // For SVG, embed directly
        fetch(url)
            .then(response => response.text())
            .then(svgText => {
                treeVisualization.innerHTML = svgText;
            });
    } else {
        // For PNG, use img tag
        treeVisualization.innerHTML = `<img src="${url}" alt="Attack Tree Visualization">`;
    }
}

// Switch between PNG and SVG formats
async function switchFormat(format) {
    if (!currentTreeData) return;

    currentFormat = format;

    // Update button states
    document.querySelectorAll('.format-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.format === format);
    });

    // Re-render with new format
    try {
        showLoading();
        const blob = await renderTree(currentTreeData, format);
        currentImageBlob = blob;
        displayVisualization(blob, format);
    } catch (error) {
        showError('Failed to render in ' + format.toUpperCase() + ' format: ' + error.message);
    } finally {
        hideLoading();
    }
}

// Download current image
function downloadImage() {
    if (!currentImageBlob) return;

    const url = URL.createObjectURL(currentImageBlob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `attack-tree.${currentFormat}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
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
    currentImageBlob = null;
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
