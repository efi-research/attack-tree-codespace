// Authentication state
let currentUser = null;

// Check authentication status on page load
async function checkAuthStatus() {
    try {
        const response = await fetch('/auth/user');
        const data = await response.json();

        if (data.authenticated) {
            currentUser = data.user;
            showMainApp();
        } else {
            showLoginScreen();
        }
    } catch (error) {
        console.error('Error checking auth status:', error);
        showLoginScreen();
    }
}

// Show login screen
function showLoginScreen() {
    document.getElementById('loginScreen').style.display = 'block';
    document.getElementById('mainApp').style.display = 'none';
}

// Show main app
function showMainApp() {
    document.getElementById('loginScreen').style.display = 'none';
    document.getElementById('mainApp').style.display = 'block';

    // Display user name
    if (currentUser) {
        const userName = document.getElementById('userName');
        userName.textContent = currentUser.name || currentUser.email || 'User';
    }
}

// Handle login button click
function handleLogin() {
    window.location.href = '/auth/login';
}

// Handle logout button click
function handleLogout() {
    window.location.href = '/auth/logout';
}

// Sample scenarios from SAMPLE_SCENARIOS.md
const SCENARIOS = [
    {
        title: 'E-Commerce Customer Data Theft',
        description: 'An attacker wants to steal customer credit card information and personal data from an e-commerce platform. The platform uses HTTPS, stores payment data in a PCI-DSS compliant database, has a web application firewall, implements rate limiting, and uses tokenization for credit card processing. The system has admin panels, customer-facing web applications, and integrates with third-party payment processors.'
    },
    {
        title: 'Smart Home Device Takeover',
        description: 'An attacker aims to gain control of smart home devices including security cameras, door locks, and thermostats. The devices communicate via WiFi and a central hub, use cloud services for remote access, have mobile apps for control, and implement firmware update mechanisms. Some devices use default credentials and have known vulnerabilities.'
    },
    {
        title: 'Business Email Compromise Attack',
        description: 'An attacker wants to compromise executive email accounts to perform wire fraud and steal sensitive business information. The organization uses Office 365 with multi-factor authentication, has email filtering and anti-phishing tools, conducts security awareness training, and has policies for financial transactions. Executives frequently travel and access email from various locations.'
    },
    {
        title: 'Electronic Health Records Theft',
        description: 'An attacker seeks to access and exfiltrate patient medical records from a hospital system. The hospital uses Electronic Health Records (EHR) systems with role-based access control, encrypts data at rest and in transit, has audit logging, complies with HIPAA regulations, and has multiple access points including doctor workstations, nurse stations, and administrative terminals.'
    },
    {
        title: 'Mobile Banking Application Compromise',
        description: 'An attacker wants to steal money from user accounts through a mobile banking application. The app uses certificate pinning, implements biometric authentication, has transaction limits, uses device fingerprinting, includes fraud detection systems, and communicates with backend services through encrypted APIs. Users can transfer money, pay bills, and view account information.'
    },
    {
        title: 'AWS Cloud Infrastructure Compromise',
        description: 'An attacker aims to gain control of an organization\'s AWS cloud infrastructure to steal data, mine cryptocurrency, or launch attacks. The infrastructure includes EC2 instances, S3 buckets, RDS databases, Lambda functions, and uses IAM for access control. Some services are publicly accessible, and the organization uses multiple AWS accounts with varying security configurations.'
    },
    {
        title: 'High-Profile Social Media Account Takeover',
        description: 'An attacker wants to take control of a celebrity or corporate social media account to spread misinformation, scam followers, or damage reputation. The account has two-factor authentication enabled, uses a strong password, is accessed from multiple devices and locations, has recovery email and phone number configured, and the platform has account protection features and anomaly detection.'
    },
    {
        title: 'Software Supply Chain Compromise',
        description: 'An attacker seeks to inject malicious code into a widely-used open-source software library to compromise downstream applications. The library is hosted on GitHub, uses automated CI/CD pipelines, has multiple maintainers with varying security practices, is distributed via npm/PyPI, and is used by thousands of applications. The attack could target the build process, dependencies, or maintainer accounts.'
    },
    {
        title: 'Data Center Physical Access Attack',
        description: 'An attacker wants to gain physical access to a data center to install hardware implants, steal hard drives, or cause service disruption. The facility has perimeter fencing, security guards, badge access systems, biometric scanners, video surveillance, mantrap entrances, and is located in a secure building. The data center houses critical servers and network equipment.'
    },
    {
        title: 'Enterprise Ransomware Attack',
        description: 'An attacker aims to deploy ransomware across a corporate network to encrypt all business data and demand payment. The network has endpoint protection, network segmentation, backup systems, email filtering, user access controls, patch management processes, and security monitoring. The organization has remote workers, on-premise servers, and cloud services.'
    },
    {
        title: 'RESTful API Exploitation',
        description: 'An attacker wants to exploit vulnerabilities in a company\'s REST API to access unauthorized data or perform privilege escalation. The API uses OAuth 2.0 authentication, has rate limiting, implements input validation, uses HTTPS, has API keys for different access levels, and serves both web and mobile applications. Some endpoints are public while others require authentication.'
    },
    {
        title: 'Cryptocurrency Exchange Wallet Theft',
        description: 'An attacker seeks to steal cryptocurrency from a digital currency exchange\'s hot and cold wallets. The exchange uses multi-signature wallets, implements withdrawal limits and delays, has KYC/AML procedures, uses hardware security modules, maintains cold storage for majority of funds, and has real-time transaction monitoring. The platform handles millions in daily trading volume.'
    },
    {
        title: 'SCADA System Sabotage',
        description: 'An attacker wants to disrupt operations of an industrial facility by compromising SCADA/ICS systems controlling manufacturing processes. The systems use proprietary protocols, have air-gapped networks, implement physical security controls, use legacy operating systems with limited patching, have HMI interfaces for operators, and control critical infrastructure like water treatment, power generation, or chemical processing.'
    },
    {
        title: 'Academic Research IP Theft',
        description: 'An attacker aims to steal valuable research data and intellectual property from a university research department. The university has network access controls, uses VPN for remote access, has shared computing resources, stores data on network drives and cloud services, has student and faculty accounts with varying privileges, and the research involves sensitive data that could be valuable to competitors or nation-states.'
    },
    {
        title: 'Self-Driving Car Remote Control',
        description: 'An attacker wants to remotely take control of autonomous vehicles to cause accidents, kidnapping, or mass disruption. The vehicles use multiple sensors (cameras, lidar, radar), communicate with cloud services for updates and navigation, have over-the-air update mechanisms, use AI for decision-making, connect to mobile apps, and implement various safety systems. The attack could target the vehicle directly or the supporting infrastructure.'
    },
    {
        title: 'Password Reset Attack',
        description: 'An attacker wants to gain access to a user account by exploiting the password reset functionality. The system sends reset links via email and asks security questions.'
    }
];

// Global state
let currentTreeData = null;
let currentFormat = 'svg';
let currentScenario = null;

// Initialize authentication check on page load
checkAuthStatus();

// DOM Elements - will be set after DOM loads
let form, generateBtn, clearBtn, loadingState, errorState, errorMessage, resultsSection, treeVisualization, jsonOutput;

// Wait for DOM to be fully loaded before attaching event listeners
document.addEventListener('DOMContentLoaded', () => {
    // Get DOM elements
    form = document.getElementById('scenarioForm');
    generateBtn = document.getElementById('generateBtn');
    clearBtn = document.getElementById('clearBtn');
    loadingState = document.getElementById('loadingState');
    errorState = document.getElementById('errorState');
    errorMessage = document.getElementById('errorMessage');
    resultsSection = document.getElementById('resultsSection');
    treeVisualization = document.getElementById('treeVisualization');
    jsonOutput = document.getElementById('jsonOutput');

    // Auth buttons
    const loginBtn = document.getElementById('loginBtn');
    const logoutBtn = document.getElementById('logoutBtn');

    // Event Listeners
    if (form) form.addEventListener('submit', handleGenerate);
    if (clearBtn) clearBtn.addEventListener('click', handleClear);
    if (loginBtn) loginBtn.addEventListener('click', handleLogin);
    if (logoutBtn) logoutBtn.addEventListener('click', handleLogout);

    // Load random scenario if authenticated
    if (currentUser) {
        loadRandomScenario();
    }
});

// Handle form submission
async function handleGenerate(e) {
    e.preventDefault();

    let title = document.getElementById('title').value.trim();
    let description = document.getElementById('description').value.trim();

    // If fields are empty, use the current scenario
    if (!title && !description && currentScenario) {
        title = currentScenario.title;
        description = currentScenario.description;
    } else if (!title || !description) {
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
        // Handle authentication errors
        if (response.status === 401) {
            showError('Session expired. Please log in again.');
            setTimeout(() => {
                window.location.href = '/auth/login';
            }, 2000);
            throw new Error('Authentication required');
        }

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
    const margin = { top: 60, right: 40, bottom: 40, left: 40 };

    // Create SVG element
    const svg = d3.select('#treeVisualization')
        .append('svg')
        .attr('width', width)
        .attr('height', height)
        .attr('viewBox', [0, 0, width, height])
        .attr('style', 'max-width: 100%; height: auto;');

    const g = svg.append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    // Create tree layout (vertical: root at top)
    const treeLayout = d3.tree()
        .size([width - margin.left - margin.right, height - margin.top - margin.bottom]);

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
        .attr('d', d3.linkVertical()
            .x(d => d.x)
            .y(d => d.y));

    // Draw nodes
    const node = g.selectAll('.node')
        .data(root.descendants())
        .enter()
        .append('g')
        .attr('class', 'node')
        .attr('transform', d => `translate(${d.x},${d.y})`);

    // Add rectangles for nodes
    node.append('rect')
        .attr('width', d => d.depth === 0 ? 170 : 150)
        .attr('height', d => {
            // Calculate height based on label content with padding
            const lines = d.data.label.split('\n').length;
            return Math.max(60, lines * 18 + 20);
        })
        .attr('x', d => d.depth === 0 ? -85 : -75)
        .attr('y', d => {
            const lines = d.data.label.split('\n').length;
            const height = Math.max(60, lines * 18 + 20);
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
        const lineHeight = 18;
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

// Wrap text to fit within a specified width
function wrapText(text, maxWidth) {
    const words = text.split(/\s+/);
    const lines = [];
    let currentLine = '';

    words.forEach(word => {
        const testLine = currentLine ? `${currentLine} ${word}` : word;
        // Rough estimate: ~7 pixels per character for 12px font
        const estimatedWidth = testLine.length * 7;

        if (estimatedWidth > maxWidth && currentLine) {
            lines.push(currentLine);
            currentLine = word;
        } else {
            currentLine = testLine;
        }
    });

    if (currentLine) {
        lines.push(currentLine);
    }

    return lines;
}

// Convert attack tree JSON to D3 hierarchy format
function convertToHierarchy(treeData) {
    // Create a map of all nodes by ID
    const nodeMap = new Map();

    // Add root node with wrapped text
    const rootLabel = wrapText(treeData.goal, 150).join('\n');
    const rootNode = {
        id: 'root',
        label: rootLabel,
        children: []
    };
    nodeMap.set('root', rootNode);

    // Add all other nodes
    treeData.nodes.forEach(node => {
        const label = buildNodeLabel(node, false);
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

// Build node label with metrics (returns object with lines and metadata)
function buildNodeLabel(node, isRoot = false) {
    // Determine max width based on node type
    const maxWidth = isRoot ? 150 : 130;

    // Wrap the main text
    const textLines = wrapText(node.text, maxWidth);

    // Add metrics on a separate line if present
    const extras = [];
    if (node.probability !== null && node.probability !== undefined) {
        extras.push(`P=${node.probability}`);
    }
    if (node.cost !== null && node.cost !== undefined) {
        extras.push(`C=${node.cost}`);
    }

    if (extras.length > 0) {
        textLines.push('(' + extras.join(', ') + ')');
    }

    return textLines.join('\n');
}

// Display results in UI
function displayResults(treeData) {
    // Show JSON
    jsonOutput.textContent = JSON.stringify(treeData, null, 2);

    // Render the tree using D3
    renderTreeD3(treeData);

    // Initialize format selector to SVG
    currentFormat = 'svg';
    document.querySelectorAll('.toggle-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.format === 'svg');
    });
    const downloadBtnText = document.getElementById('downloadBtnText');
    if (downloadBtnText) {
        downloadBtnText.textContent = 'Download SVG';
    }

    // Show results section
    showResults();
}

// Switch between PNG and SVG formats
function switchFormat(format) {
    if (!currentTreeData) return;

    currentFormat = format;

    // Update toggle button states
    document.querySelectorAll('.toggle-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.format === format);
    });

    // Update download button text
    const downloadBtnText = document.getElementById('downloadBtnText');
    if (downloadBtnText) {
        downloadBtnText.textContent = `Download ${format.toUpperCase()}`;
    }

    // Note: The visualization is always SVG in the DOM.
    // PNG conversion happens only during download.
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
    loadRandomScenario();
    document.getElementById('title').focus();
}

// Generate new tree (reset everything)
function generateNew() {
    hideResults();
    hideError();
    currentTreeData = null;
    currentFormat = 'svg';
    form.reset();
    loadRandomScenario();
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

// Select and display a random scenario
function loadRandomScenario() {
    const randomIndex = Math.floor(Math.random() * SCENARIOS.length);
    currentScenario = SCENARIOS[randomIndex];

    // Set as placeholder values
    document.getElementById('title').placeholder = currentScenario.title;
    document.getElementById('description').placeholder = currentScenario.description;
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
