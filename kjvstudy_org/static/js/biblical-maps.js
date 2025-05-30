/**
 * Biblical Maps - Interactive maps for KJV Study
 * Uses OpenStreetMap with Leaflet.js (free, no API key required)
 */

class BiblicalMaps {
    constructor() {
        this.map = null;
        this.currentMarkers = [];
        this.currentLayer = null;
        this.biblicalLocations = this.getBiblicalLocations();
        this.mapLayers = this.getMapLayers();
    }

    /**
     * Initialize the map
     */
    init(containerId, options = {}) {
        const defaultCenter = [31.7683, 35.2137]; // Jerusalem
        const defaultZoom = 7;

        this.map = L.map(containerId, {
            center: options.center || defaultCenter,
            zoom: options.zoom || defaultZoom,
            zoomControl: true,
            scrollWheelZoom: true,
            doubleClickZoom: true,
            boxZoom: true,
            keyboard: true,
            dragging: true,
            touchZoom: true
        });

        // Add default OpenStreetMap layer
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            maxZoom: 18,
            minZoom: 3
        }).addTo(this.map);

        // Add layer control
        this.addLayerControl();

        // Add biblical locations
        this.addBiblicalLocations();

        return this.map;
    }

    /**
     * Add layer control for different map types
     */
    addLayerControl() {
        const baseLayers = {
            "OpenStreetMap": L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }),
            "Dark Theme": L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
                subdomains: 'abcd',
                maxZoom: 20
            }),
            "Terrain": L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://opentopomap.org">OpenTopoMap</a> contributors'
            }),
            "Satellite": L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
                attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
            })
        };

        L.control.layers(baseLayers, this.mapLayers).addTo(this.map);
    }

    /**
     * Get map overlay layers for different biblical periods
     */
    getMapLayers() {
        const layers = {};

        // Create marker groups for different periods
        layers["Old Testament Cities"] = L.layerGroup();
        layers["New Testament Cities"] = L.layerGroup();
        layers["Paul's Journeys"] = L.layerGroup();
        layers["Tribal Territories"] = L.layerGroup();
        layers["Major Events"] = L.layerGroup();

        return layers;
    }

    /**
     * Biblical locations with coordinates and information
     */
    getBiblicalLocations() {
        return {
            // Major Old Testament Cities
            jerusalem: {
                name: "Jerusalem",
                coords: [31.7683, 35.2137],
                type: "city",
                period: ["ot", "nt"],
                description: "The holy city, site of Solomon's Temple and Jesus's crucifixion",
                verses: ["2 Samuel 5:6-7", "1 Kings 6:1", "Matthew 27:33"],
                layer: ["Old Testament Cities", "New Testament Cities"]
            },
            bethlehem: {
                name: "Bethlehem",
                coords: [31.7054, 35.2024],
                type: "city",
                period: ["ot", "nt"],
                description: "City of David's birth and Jesus's birth",
                verses: ["1 Samuel 16:1", "Micah 5:2", "Matthew 2:1"],
                layer: ["Old Testament Cities", "New Testament Cities"]
            },
            nazareth: {
                name: "Nazareth",
                coords: [32.7009, 35.2976],
                type: "city",
                period: ["nt"],
                description: "Jesus's hometown",
                verses: ["Matthew 2:23", "Luke 1:26", "Luke 4:16"],
                layer: ["New Testament Cities"]
            },
            capernaum: {
                name: "Capernaum",
                coords: [32.8819, 35.5747],
                type: "city",
                period: ["nt"],
                description: "Jesus's ministry headquarters",
                verses: ["Matthew 4:13", "Matthew 8:5", "Mark 2:1"],
                layer: ["New Testament Cities"]
            },
            jericho: {
                name: "Jericho",
                coords: [31.8667, 35.4444],
                type: "city",
                period: ["ot", "nt"],
                description: "First city conquered by Joshua",
                verses: ["Joshua 6:1-27", "Luke 19:1"],
                layer: ["Old Testament Cities", "New Testament Cities"]
            },
            damascus: {
                name: "Damascus",
                coords: [33.5138, 36.2765],
                type: "city",
                period: ["ot", "nt"],
                description: "Ancient city, site of Paul's conversion",
                verses: ["2 Kings 5:12", "Acts 9:3"],
                layer: ["Old Testament Cities", "Paul's Journeys"]
            },
            babylon: {
                name: "Babylon",
                coords: [32.5355, 44.4275],
                type: "city",
                period: ["ot"],
                description: "Capital of Babylonian Empire, site of exile",
                verses: ["2 Kings 25:11", "Psalm 137:1", "Daniel 1:1"],
                layer: ["Old Testament Cities"]
            },
            egypt_memphis: {
                name: "Memphis (Egypt)",
                coords: [29.8467, 31.2500],
                type: "city",
                period: ["ot"],
                description: "Ancient capital of Egypt",
                verses: ["Isaiah 19:13", "Jeremiah 2:16", "Hosea 9:6"],
                layer: ["Old Testament Cities"]
            },
            mount_sinai: {
                name: "Mount Sinai",
                coords: [28.5394, 33.9731],
                type: "mountain",
                period: ["ot"],
                description: "Where Moses received the Ten Commandments",
                verses: ["Exodus 19:20", "Exodus 24:16", "Deuteronomy 4:10"],
                layer: ["Major Events"]
            },
            mount_carmel: {
                name: "Mount Carmel",
                coords: [32.7319, 35.0478],
                type: "mountain",
                period: ["ot"],
                description: "Site of Elijah's contest with Baal's prophets",
                verses: ["1 Kings 18:19-40"],
                layer: ["Major Events"]
            },
            // Paul's Journey Cities
            antioch: {
                name: "Antioch",
                coords: [36.2012, 36.1611],
                type: "city",
                period: ["nt"],
                description: "First Gentile church, Paul's mission base",
                verses: ["Acts 11:26", "Acts 13:1"],
                layer: ["Paul's Journeys"]
            },
            athens: {
                name: "Athens",
                coords: [37.9755, 23.7348],
                type: "city",
                period: ["nt"],
                description: "Paul preached at the Areopagus",
                verses: ["Acts 17:16-34"],
                layer: ["Paul's Journeys"]
            },
            corinth: {
                name: "Corinth",
                coords: [37.9065, 22.8756],
                type: "city",
                period: ["nt"],
                description: "Paul established church and wrote letters",
                verses: ["Acts 18:1", "1 Corinthians 1:2"],
                layer: ["Paul's Journeys"]
            },
            ephesus: {
                name: "Ephesus",
                coords: [37.9495, 27.3517],
                type: "city",
                period: ["nt"],
                description: "Major center of Paul's ministry",
                verses: ["Acts 19:1", "Ephesians 1:1", "Revelation 2:1"],
                layer: ["Paul's Journeys"]
            },
            rome: {
                name: "Rome",
                coords: [41.9028, 12.4964],
                type: "city",
                period: ["nt"],
                description: "Capital of Roman Empire, Paul's final destination",
                verses: ["Acts 28:16", "Romans 1:7"],
                layer: ["Paul's Journeys"]
            },
            // Bodies of Water
            sea_of_galilee: {
                name: "Sea of Galilee",
                coords: [32.8219, 35.5881],
                type: "water",
                period: ["ot", "nt"],
                description: "Where Jesus called disciples and performed miracles",
                verses: ["Matthew 4:18", "Mark 6:47-52", "John 21:1"],
                layer: ["New Testament Cities", "Major Events"]
            },
            dead_sea: {
                name: "Dead Sea",
                coords: [31.5590, 35.4732],
                type: "water",
                period: ["ot", "nt"],
                description: "Salt sea, lowest point on earth",
                verses: ["Genesis 14:3", "Joshua 3:16"],
                layer: ["Old Testament Cities"]
            },
            jordan_river: {
                name: "Jordan River",
                coords: [32.0000, 35.5000],
                type: "water",
                period: ["ot", "nt"],
                description: "River where Jesus was baptized",
                verses: ["Joshua 3:17", "Matthew 3:13", "Mark 1:9"],
                layer: ["Old Testament Cities", "New Testament Cities"]
            },
            // Additional locations
            hebron: {
                name: "Hebron",
                coords: [31.5326, 35.0998],
                type: "city",
                period: ["ot"],
                description: "Where Abraham lived and was buried, David's first capital",
                verses: ["Genesis 23:2", "2 Samuel 2:11"],
                layer: ["Old Testament Cities"]
            },
            samaria: {
                name: "Samaria",
                coords: [32.2764, 35.1891],
                type: "city",
                period: ["ot", "nt"],
                description: "Capital of Northern Kingdom of Israel",
                verses: ["1 Kings 16:24", "John 4:4-9"],
                layer: ["Old Testament Cities", "New Testament Cities"]
            },
            caesarea: {
                name: "Caesarea",
                coords: [32.5014, 34.8944],
                type: "city",
                period: ["nt"],
                description: "Roman capital, where Paul was imprisoned",
                verses: ["Acts 10:1", "Acts 23:23"],
                layer: ["Paul's Journeys"]
            },
            philippi: {
                name: "Philippi",
                coords: [41.0136, 24.2919],
                type: "city",
                period: ["nt"],
                description: "First European city where Paul preached",
                verses: ["Acts 16:12", "Philippians 1:1"],
                layer: ["Paul's Journeys"]
            },
            thessalonica: {
                name: "Thessalonica",
                coords: [40.6403, 22.9439],
                type: "city",
                period: ["nt"],
                description: "Where Paul established a strong church",
                verses: ["Acts 17:1", "1 Thessalonians 1:1"],
                layer: ["Paul's Journeys"]
            }
        };
    }

    /**
     * Add all biblical locations to the map
     */
    addBiblicalLocations() {
        Object.entries(this.biblicalLocations).forEach(([key, location]) => {
            const marker = this.createLocationMarker(location);
            
            // Add marker to appropriate layers
            location.layer.forEach(layerName => {
                if (this.mapLayers[layerName]) {
                    this.mapLayers[layerName].addLayer(marker);
                }
            });
        });

        // Add all layers to map by default
        Object.values(this.mapLayers).forEach(layer => {
            layer.addTo(this.map);
        });
    }

    /**
     * Create a marker for a biblical location
     */
    createLocationMarker(location) {
        const icon = this.getLocationIcon(location.type);
        const marker = L.marker(location.coords, { icon: icon });

        // Create popup content
        const popupContent = this.createPopupContent(location);
        marker.bindPopup(popupContent, {
            maxWidth: 300,
            className: 'biblical-location-popup'
        });

        return marker;
    }

    /**
     * Get appropriate icon for location type
     */
    getLocationIcon(type) {
        const iconConfigs = {
            city: { color: '#8B4513', icon: '🏛️' },
            mountain: { color: '#8B7355', icon: '⛰️' },
            water: { color: '#4682B4', icon: '🌊' },
            temple: { color: '#DAA520', icon: '🕌' },
            event: { color: '#DC143C', icon: '✨' }
        };

        const config = iconConfigs[type] || iconConfigs.city;
        
        return L.divIcon({
            html: `<div style="background-color: ${config.color}; border-radius: 50%; width: 25px; height: 25px; display: flex; align-items: center; justify-content: center; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3);">
                     <span style="font-size: 12px;">${config.icon}</span>
                   </div>`,
            className: 'biblical-location-marker',
            iconSize: [25, 25],
            iconAnchor: [12, 12],
            popupAnchor: [0, -15]
        });
    }

    /**
     * Create popup content for a location
     */
    createPopupContent(location) {
        const verseLinks = location.verses.map(verse => 
            `<a href="/search?q=${encodeURIComponent(verse)}" style="color: #6d4bb3; text-decoration: none;">${verse}</a>`
        ).join(', ');

        return `
            <div style="font-family: 'Crimson Text', serif; color: #f5f5f5;">
                <h3 style="margin: 0 0 8px 0; color: #6d4bb3; font-size: 16px; border-bottom: 1px solid #2a2a2a; padding-bottom: 4px;">${location.name}</h3>
                <p style="margin: 8px 0; font-size: 14px; color: #a3a3a3;">${location.description}</p>
                <div style="margin-top: 10px; font-size: 12px; color: #737373;">
                    <strong>Key Verses:</strong><br>
                    ${verseLinks}
                </div>
            </div>
        `;
    }

    /**
     * Search for a location and center map on it
     */
    searchLocation(locationName) {
        const normalizedName = locationName.toLowerCase();
        const location = Object.values(this.biblicalLocations).find(loc => 
            loc.name.toLowerCase().includes(normalizedName)
        );

        if (location) {
            this.map.setView(location.coords, 10);
            // Find and open the marker popup
            Object.values(this.mapLayers).forEach(layer => {
                layer.eachLayer(marker => {
                    if (marker.getLatLng && marker.getLatLng().lat === location.coords[0] && 
                        marker.getLatLng().lng === location.coords[1]) {
                        marker.openPopup();
                    }
                });
            });
            return true;
        }
        return false;
    }

    /**
     * Show locations related to a Bible book
     */
    showBookLocations(bookName) {
        this.clearHighlights();
        const relevantLocations = this.getLocationsForBook(bookName);
        
        relevantLocations.forEach(locationKey => {
            const location = this.biblicalLocations[locationKey];
            if (location) {
                // Add highlight to marker
                this.highlightLocation(location);
            }
        });
    }

    /**
     * Get locations relevant to a specific Bible book
     */
    getLocationsForBook(bookName) {
        const bookLocations = {
            "Genesis": ["hebron", "egypt_memphis"],
            "Exodus": ["egypt_memphis", "mount_sinai"],
            "Joshua": ["jericho", "jordan_river"],
            "1 Samuel": ["bethlehem"],
            "2 Samuel": ["jerusalem", "hebron"],
            "1 Kings": ["jerusalem", "mount_carmel", "samaria"],
            "Psalms": ["jerusalem"],
            "Matthew": ["bethlehem", "nazareth", "capernaum", "jerusalem"],
            "Mark": ["capernaum", "sea_of_galilee", "jerusalem"],
            "Luke": ["nazareth", "bethlehem", "jericho", "jerusalem"],
            "John": ["capernaum", "sea_of_galilee", "jerusalem", "samaria"],
            "Acts": ["jerusalem", "damascus", "antioch", "athens", "corinth", "ephesus", "rome", "caesarea", "philippi", "thessalonica"],
            "Romans": ["rome"],
            "1 Corinthians": ["corinth"],
            "Ephesians": ["ephesus"],
            "Philippians": ["philippi"],
            "1 Thessalonians": ["thessalonica"],
            "Revelation": ["ephesus"]
        };

        return bookLocations[bookName] || [];
    }

    /**
     * Highlight a specific location
     */
    highlightLocation(location) {
        // This would add visual highlighting - implementation depends on specific needs
        console.log(`Highlighting ${location.name}`);
    }

    /**
     * Clear all highlights
     */
    clearHighlights() {
        // Clear any existing highlights
        console.log("Clearing highlights");
    }

    /**
     * Resize map (useful when container size changes)
     */
    resize() {
        if (this.map) {
            this.map.invalidateSize();
        }
    }

    /**
     * Destroy the map instance
     */
    destroy() {
        if (this.map) {
            this.map.remove();
            this.map = null;
        }
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Make BiblicalMaps available globally
    window.BiblicalMaps = BiblicalMaps;
    
    // Auto-initialize if map container exists
    const mapContainer = document.getElementById('biblical-map');
    if (mapContainer) {
        window.biblicalMapsInstance = new BiblicalMaps();
        window.biblicalMapsInstance.init('biblical-map');
    }
});