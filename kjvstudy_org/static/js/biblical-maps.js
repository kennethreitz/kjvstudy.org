/**
 * Simple Biblical Maps Implementation
 * Uses reliable tile providers with fallback options
 */

class SimpleBiblicalMaps {
    constructor() {
        this.map = null;
        this.markers = [];
        this.locations = this.getBiblicalLocations();
    }

    init(containerId) {
        try {
            // Initialize map centered on Jerusalem
            this.map = L.map(containerId, {
                center: [31.7683, 35.2137],
                zoom: 7,
                zoomControl: true
            });

            // Add base tiles with fallback
            this.addBaseTiles();
            
            // Add all biblical locations
            this.addLocations();
            
            console.log('Biblical maps initialized successfully');
            return this.map;
        } catch (error) {
            console.error('Failed to initialize biblical maps:', error);
            this.showError(containerId, error.message);
        }
    }

    addBaseTiles() {
        // Primary: CartoDB Voyager (clean, fast)
        const primaryTiles = L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>',
            subdomains: 'abcd',
            maxZoom: 20
        });

        // Fallback: OpenStreetMap
        const fallbackTiles = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            maxZoom: 19
        });

        // Try primary first, fallback on error
        primaryTiles.on('tileerror', () => {
            console.log('Primary tiles failed, using fallback');
            this.map.removeLayer(primaryTiles);
            fallbackTiles.addTo(this.map);
        });

        primaryTiles.addTo(this.map);

        // Additional layer options
        const satelliteTiles = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
            attribution: 'Tiles &copy; Esri'
        });

        const terrainTiles = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://opentopomap.org">OpenTopoMap</a>'
        });

        // Layer control
        L.control.layers({
            "Street Map": primaryTiles,
            "Satellite": satelliteTiles,
            "Terrain": terrainTiles
        }).addTo(this.map);
    }

    addLocations() {
        this.locations.forEach(location => {
            const marker = this.createMarker(location);
            marker.addTo(this.map);
            this.markers.push(marker);
        });
    }

    createMarker(location) {
        // Simple colored circle markers
        const colors = {
            city: '#8B4513',
            mountain: '#8B7355', 
            water: '#4682B4',
            temple: '#DAA520',
            event: '#DC143C',
            journey: '#9932CC'
        };

        const marker = L.circleMarker(location.coords, {
            radius: 8,
            fillColor: colors[location.type] || colors.city,
            color: '#fff',
            weight: 2,
            opacity: 1,
            fillOpacity: 0.8
        });

        // Create popup
        const popupContent = this.createPopupContent(location);
        marker.bindPopup(popupContent);

        return marker;
    }

    createPopupContent(location) {
        return `
            <div style="min-width: 200px; font-family: inherit;">
                <h4 style="margin: 0 0 8px 0; color: #4b2e83; font-size: 16px;">${location.name}</h4>
                <p style="margin: 0 0 8px 0; font-size: 14px; line-height: 1.4;">${location.description}</p>
                <div style="font-size: 12px; color: #666;">
                    <strong>Scripture References:</strong><br>
                    ${location.verses.join('<br>')}
                </div>
            </div>
        `;
    }

    showError(containerId, message) {
        const container = document.getElementById(containerId);
        if (container) {
            container.innerHTML = `
                <div style="padding: 40px; text-align: center; background: #f8f9fa; border-radius: 8px;">
                    <h3 style="color: #dc3545; margin-bottom: 16px;">Map Loading Error</h3>
                    <p style="color: #666; margin-bottom: 8px;">Unable to load the biblical maps.</p>
                    <p style="font-size: 12px; color: #999;">Error: ${message}</p>
                    <button onclick="location.reload()" style="margin-top: 16px; padding: 8px 16px; background: #4b2e83; color: white; border: none; border-radius: 4px; cursor: pointer;">
                        Try Again
                    </button>
                </div>
            `;
        }
    }

    getBiblicalLocations() {
        return [
            {
                name: "Jerusalem",
                coords: [31.7683, 35.2137],
                type: "city",
                description: "The holy city, site of Solomon's Temple and Jesus's crucifixion",
                verses: ["2 Samuel 5:6-7", "1 Kings 6:1", "Matthew 27:33"]
            },
            {
                name: "Bethlehem",
                coords: [31.7054, 35.2024],
                type: "city",
                description: "City of David's birth and Jesus's birth",
                verses: ["1 Samuel 16:1", "Micah 5:2", "Matthew 2:1"]
            },
            {
                name: "Nazareth",
                coords: [32.7009, 35.2976],
                type: "city",
                description: "Jesus's hometown",
                verses: ["Matthew 2:23", "Luke 1:26", "Luke 4:16"]
            },
            {
                name: "Capernaum",
                coords: [32.8819, 35.5747],
                type: "city",
                description: "Jesus's ministry headquarters",
                verses: ["Matthew 4:13", "Matthew 8:5", "Mark 2:1"]
            },
            {
                name: "Jericho",
                coords: [31.8667, 35.4444],
                type: "city",
                description: "First city conquered by Joshua",
                verses: ["Joshua 6:1-27", "Luke 19:1"]
            },
            {
                name: "Damascus",
                coords: [33.5138, 36.2765],
                type: "city",
                description: "Ancient city, site of Paul's conversion",
                verses: ["2 Kings 5:12", "Acts 9:3"]
            },
            {
                name: "Antioch",
                coords: [36.2012, 36.1611],
                type: "journey",
                description: "First Gentile church, Paul's mission base",
                verses: ["Acts 11:26", "Acts 13:1"]
            },
            {
                name: "Athens",
                coords: [37.9755, 23.7348],
                type: "journey",
                description: "Where Paul preached to philosophers",
                verses: ["Acts 17:16-34"]
            },
            {
                name: "Rome",
                coords: [41.9028, 12.4964],
                type: "journey",
                description: "Capital of the Roman Empire, Paul's final destination",
                verses: ["Acts 28:16", "Romans 1:7"]
            },
            {
                name: "Corinth",
                coords: [37.9063, 22.8781],
                type: "journey",
                description: "Major Greek city where Paul established a church",
                verses: ["Acts 18:1", "1 Corinthians 1:2"]
            },
            {
                name: "Ephesus",
                coords: [37.9495, 27.3630],
                type: "journey",
                description: "Important city in Paul's third missionary journey",
                verses: ["Acts 19:1", "Ephesians 1:1"]
            },
            {
                name: "Mount Sinai",
                coords: [28.5394, 33.9731],
                type: "mountain",
                description: "Where Moses received the Ten Commandments",
                verses: ["Exodus 19:20", "Exodus 24:16", "Deuteronomy 4:10"]
            },
            {
                name: "Mount Carmel",
                coords: [32.7319, 35.0478],
                type: "mountain",
                description: "Site of Elijah's contest with Baal's prophets",
                verses: ["1 Kings 18:19-40"]
            },
            {
                name: "Mount of Olives",
                coords: [31.7790, 35.2442],
                type: "mountain",
                description: "Where Jesus often prayed and ascended to heaven",
                verses: ["Matthew 24:3", "Acts 1:12"]
            },
            {
                name: "Sea of Galilee",
                coords: [32.8215, 35.5897],
                type: "water",
                description: "Where Jesus walked on water and called fishermen",
                verses: ["Matthew 4:18", "Matthew 14:25", "John 6:1"]
            },
            {
                name: "Jordan River",
                coords: [32.2808, 35.5408],
                type: "water",
                description: "Where Jesus was baptized by John",
                verses: ["Matthew 3:13", "Mark 1:9", "Luke 3:21"]
            },
            {
                name: "Dead Sea",
                coords: [31.5590, 35.4732],
                type: "water",
                description: "The salt sea, lowest point on Earth",
                verses: ["Genesis 14:3", "Joshua 3:16"]
            },
            {
                name: "Temple Mount",
                coords: [31.7781, 35.2360],
                type: "temple",
                description: "Site of Solomon's Temple and Herod's Temple",
                verses: ["1 Kings 6:1", "Matthew 21:12", "Acts 3:1"]
            },
            {
                name: "Garden of Gethsemane",
                coords: [31.7794, 35.2394],
                type: "event",
                description: "Where Jesus prayed before his crucifixion",
                verses: ["Matthew 26:36", "Mark 14:32"]
            },
            {
                name: "Calvary (Golgotha)",
                coords: [31.7784, 35.2297],
                type: "event",
                description: "Site of Jesus's crucifixion",
                verses: ["Matthew 27:33", "Mark 15:22", "John 19:17"]
            },
            {
                name: "Babylon",
                coords: [32.5355, 44.4275],
                type: "city",
                description: "Capital of Babylonian Empire, site of exile",
                verses: ["2 Kings 25:11", "Psalm 137:1", "Daniel 1:1"]
            }
        ];
    }
}

// Auto-initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    const mapContainer = document.getElementById('biblical-map');
    if (mapContainer && typeof L !== 'undefined') {
        // Remove loading message
        const loading = mapContainer.querySelector('.map-loading');
        if (loading) loading.style.display = 'none';

        // Initialize maps
        window.biblicalMaps = new SimpleBiblicalMaps();
        window.biblicalMaps.init('biblical-map');
    } else if (mapContainer) {
        // Leaflet not loaded
        setTimeout(() => {
            if (typeof L !== 'undefined') {
                window.biblicalMaps = new SimpleBiblicalMaps();
                window.biblicalMaps.init('biblical-map');
            } else {
                mapContainer.innerHTML = `
                    <div style="padding: 40px; text-align: center; background: #f8f9fa; border-radius: 8px;">
                        <h3 style="color: #dc3545;">Leaflet Library Not Loaded</h3>
                        <p>Please check your internet connection and refresh the page.</p>
                    </div>
                `;
            }
        }, 2000);
    }
});