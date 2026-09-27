/* Results Page JavaScript */

let currentAnalysisData = null;
let treeChartInstance = null;

// Get result_id from URL query parameter
const searchParams = new URLSearchParams(window.location.search);
const resultId = searchParams.get('result_id') || localStorage.getItem('lastResultId');

document.addEventListener('DOMContentLoaded', async function() {
    if (resultId) {
        await loadResults(resultId);
        localStorage.setItem('lastResultId', resultId);
    } else {
        document.getElementById('tableMessage').textContent = 'No results available. Please run detection first.';
    }

    setupExportButtons();
});

async function loadResults(id) {
    try {
        // Fetch results
        const resultsResponse = await fetch(`/api/results/${id}`);
        if (!resultsResponse.ok) throw new Error('Failed to fetch results');
        const results = await resultsResponse.json();

        // Fetch analysis
        const analysisResponse = await fetch(`/api/analysis/${id}`);
        if (!analysisResponse.ok) throw new Error('Failed to fetch analysis');
        const analysis = await analysisResponse.json();

        currentAnalysisData = analysis;

        // Fetch processed image
        const imageUrl = `/api/results/${id}/image`;
        document.getElementById('processedImage').src = imageUrl;
        document.getElementById('originalImage').src = imageUrl;

        // Display metrics
        displayMetrics(analysis);

        // Display trees table
        displayTreesTable(results.trees || []);

        // Create chart
        createTreeChart(results.trees || []);

    } catch (error) {
        console.error('Error loading results:', error);
        document.getElementById('tableMessage').textContent = `Error loading results: ${error.message}`;
    }
}

function displayMetrics(analysis) {
    document.getElementById('metricTotalTrees').textContent = analysis.total_trees;
    document.getElementById('metricArea').textContent = `${analysis.estimated_area_m2.toFixed(0)} m²`;
    document.getElementById('metricDensity').textContent = `${analysis.estimated_tree_density.trees_per_hectare.toFixed(2)} trees/hectare`;
    document.getElementById('metricAvgArea').textContent = `${analysis.crown_area_statistics.average_pixels.toFixed(0)} px`;
    document.getElementById('metricMaxArea').textContent = `${analysis.crown_area_statistics.max_pixels.toFixed(0)} px`;
    document.getElementById('metricMinArea').textContent = `${analysis.crown_area_statistics.min_pixels.toFixed(0)} px`;
}

function displayTreesTable(trees) {
    const tbody = document.getElementById('treesList');
    tbody.innerHTML = '';

    if (trees.length === 0) {
        document.getElementById('tableMessage').textContent = 'No trees detected';
        return;
    }

    document.getElementById('tableMessage').style.display = 'none';

    trees.forEach(tree => {
        // Convert pixel to approximate geographic coordinates
        const lat = (tree.pixel_y / currentAnalysisData.image_dimensions.height_pixels - 0.5) * 0.01 + 28.7041;
        const lon = (tree.pixel_x / currentAnalysisData.image_dimensions.width_pixels - 0.5) * 0.01 + 77.1025;

        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${tree.tree_id}</td>
            <td>${tree.pixel_x.toFixed(0)}</td>
            <td>${tree.pixel_y.toFixed(0)}</td>
            <td>${tree.contour_area_pixels.toFixed(0)}</td>
            <td>${tree.radius_pixels.toFixed(0)}</td>
            <td>${lat.toFixed(6)}</td>
            <td>${lon.toFixed(6)}</td>
        `;
        tbody.appendChild(row);
    });
}

function createTreeChart(trees) {
    if (trees.length === 0) return;

    const ctx = document.getElementById('areaChart').getContext('2d');
    
    const labels = trees.map(t => `T${t.tree_id}`);
    const data = trees.map(t => t.contour_area_pixels);

    if (treeChartInstance) {
        treeChartInstance.destroy();
    }

    treeChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Crown Area (pixels)',
                data: data,
                backgroundColor: 'rgba(52, 152, 219, 0.6)',
                borderColor: 'rgba(52, 152, 219, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                title: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Area (pixels²)'
                    }
                }
            }
        }
    });
}

function setupExportButtons() {
    document.getElementById('exportCSV').addEventListener('click', () => {
        if (resultId) {
            window.location.href = `/api/results/${resultId}/csv`;
        }
    });

    document.getElementById('exportGeoJSON').addEventListener('click', () => {
        if (resultId) {
            window.location.href = `/api/results/${resultId}/geojson`;
        }
    });
}
