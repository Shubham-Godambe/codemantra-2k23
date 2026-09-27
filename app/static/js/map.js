/* Map Visualization JavaScript */

let map = null;
let currentGeoJSON = null;
let resultId = localStorage.getItem('lastResultId');

document.addEventListener('DOMContentLoaded', async function() {
    // Initialize map
    initializeMap();
    
    if (resultId) {
        await loadMapData(resultId);
    } else {
        document.getElementById('mapNote').textContent = 'No detection results available. Please run tree detection first.';
    }
});

function initializeMap() {
    // Create map centered on Delhi (demo location)
    map = L.map('map').setView([28.7041, 77.1025], 6);
    
    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19
    }).addTo(map);
}

async function loadMapData(id) {
    try {
        const response = await fetch(`/api/results/${id}`);
        if (!response.ok) throw new Error('Failed to fetch results');
        
        const results = await response.json();
        const trees = results.trees || [];

        // Update map stats
        document.getElementById('treeCount').textContent = `Trees Displayed: ${trees.length}`;
        
        if (trees.length > 0) {
            // Calculate center
            const centers = trees.map(t => {
                const lat = (t.pixel_y / results.image_dimensions[1] - 0.5) * 0.01 + 28.7041;
                const lon = (t.pixel_x / results.image_dimensions[0] - 0.5) * 0.01 + 77.1025;
                return [lat, lon];
            });
            
            const centerLat = centers.reduce((a, c) => a + c[0], 0) / centers.length;
            const centerLon = centers.reduce((a, c) => a + c[1], 0) / centers.length;
            
            document.getElementById('centerCoords').textContent = 
                `Center Coordinates: ${centerLat.toFixed(6)}, ${centerLon.toFixed(6)}`;
            
            // Center map on detected trees
            map.setView([centerLat, centerLon], 12);
            
            // Add tree markers
            const markerGroup = L.featureGroup();
            
            trees.forEach(tree => {
                const lat = (tree.pixel_y / results.image_dimensions[1] - 0.5) * 0.01 + 28.7041;
                const lon = (tree.pixel_x / results.image_dimensions[0] - 0.5) * 0.01 + 77.1025;
                
                const marker = L.circleMarker([lat, lon], {
                    radius: 8,
                    fillColor: '#27ae60',
                    color: '#1e8449',
                    weight: 2,
                    opacity: 0.8,
                    fillOpacity: 0.6
                });
                
                marker.bindPopup(`
                    <strong>Tree #${tree.tree_id}</strong><br>
                    Lat: ${lat.toFixed(6)}<br>
                    Lon: ${lon.toFixed(6)}<br>
                    Area: ${tree.contour_area_pixels.toFixed(0)} px²
                `);
                
                marker.addTo(markerGroup);
            });
            
            markerGroup.addTo(map);
            
            // Fit map to bounds
            if (markerGroup.getLayers().length > 0) {
                map.fitBounds(markerGroup.getBounds().pad(0.1));
            }
        }
        
    } catch (error) {
        console.error('Error loading map data:', error);
        document.getElementById('mapNote').textContent = `Error loading map: ${error.message}`;
    }
}
