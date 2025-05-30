/**
 * Advanced Tree Layout Options for KJV Study Family Tree
 * Provides multiple visualization modes beyond the standard hierarchical tree
 */

class AdvancedTreeLayouts {
    constructor(svg, familyData) {
        this.svg = svg;
        this.familyData = familyData;
        this.currentLayout = 'hierarchical';
        this.width = 800;
        this.height = 600;
        this.simulation = null;
        this.zoom = null;
        this.g = null;
        
        this.initializeZoom();
    }

    initializeZoom() {
        this.zoom = d3.zoom()
            .scaleExtent([0.1, 3])
            .on("zoom", (event) => {
                if (this.g) {
                    this.g.attr("transform", event.transform);
                }
            });
        
        this.svg.call(this.zoom);
        this.g = this.svg.append("g");
    }

    updateDimensions() {
        const rect = this.svg.node().getBoundingClientRect();
        this.width = rect.width;
        this.height = rect.height;
    }

    /**
     * Radial Tree Layout - Shows generations in concentric circles
     */
    renderRadialLayout(rootPersonId, maxGenerations = 4) {
        this.currentLayout = 'radial';
        this.updateDimensions();
        
        const treeData = this.buildRadialTreeData(rootPersonId, maxGenerations);
        if (!treeData) return;

        this.g.selectAll("*").remove();

        const centerX = this.width / 2;
        const centerY = this.height / 2;
        const maxRadius = Math.min(this.width, this.height) / 2 - 60;

        // Calculate positions for each generation
        const generations = this.getGenerationLevels(treeData);
        const radiusStep = maxRadius / Math.max(generations.length - 1, 1);

        // Position nodes in concentric circles
        generations.forEach((generation, genIndex) => {
            const radius = genIndex * radiusStep;
            const angleStep = (2 * Math.PI) / Math.max(generation.length, 1);
            
            generation.forEach((node, nodeIndex) => {
                const angle = nodeIndex * angleStep - Math.PI / 2; // Start from top
                node.x = centerX + radius * Math.cos(angle);
                node.y = centerY + radius * Math.sin(angle);
            });
        });

        this.drawRadialConnections(treeData);
        this.drawNodes(treeData.nodes, rootPersonId);
        
        // Add generation labels
        this.addGenerationLabels(generations, centerX, centerY, radiusStep);
    }

    /**
     * Force-Directed Layout - Dynamic positioning based on relationships
     */
    renderForceDirectedLayout(rootPersonId, includeExtended = true) {
        this.currentLayout = 'force-directed';
        this.updateDimensions();
        
        const graphData = this.buildGraphData(rootPersonId, includeExtended);
        if (!graphData.nodes.length) return;

        this.g.selectAll("*").remove();

        // Create force simulation
        this.simulation = d3.forceSimulation(graphData.nodes)
            .force("link", d3.forceLink(graphData.links)
                .id(d => d.id)
                .distance(d => this.getLinkDistance(d))
                .strength(d => this.getLinkStrength(d)))
            .force("charge", d3.forceManyBody()
                .strength(-300)
                .distanceMax(200))
            .force("center", d3.forceCenter(this.width / 2, this.height / 2))
            .force("collision", d3.forceCollide().radius(25));

        // Draw links
        const links = this.g.selectAll('.force-link')
            .data(graphData.links)
            .enter()
            .append('line')
            .attr('class', d => `force-link ${d.type}`)
            .attr('stroke-width', d => d.type === 'marriage' ? 3 : 2)
            .attr('stroke', d => this.getLinkColor(d.type));

        // Draw nodes
        const nodes = this.g.selectAll('.force-node')
            .data(graphData.nodes)
            .enter()
            .append('g')
            .attr('class', d => `force-node ${d.gender} ${d.id === rootPersonId ? 'current' : ''}`)
            .call(d3.drag()
                .on("start", (event, d) => this.dragStarted(event, d))
                .on("drag", (event, d) => this.dragged(event, d))
                .on("end", (event, d) => this.dragEnded(event, d)))
            .on('click', (event, d) => {
                this.selectPerson(d.id);
            });

        nodes.append('circle')
            .attr('r', d => d.id === rootPersonId ? 12 : 8)
            .attr('fill', d => this.getNodeColor(d, rootPersonId));

        nodes.append('text')
            .attr('dy', '.35em')
            .attr('text-anchor', 'middle')
            .style('font-size', '10px')
            .style('font-weight', d => d.id === rootPersonId ? 'bold' : 'normal')
            .text(d => this.truncateName(d.name, 12));

        // Update positions on simulation tick
        this.simulation.on("tick", () => {
            links
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);

            nodes.attr("transform", d => `translate(${d.x},${d.y})`);
        });
    }

    /**
     * Timeline Tree Layout - Shows family relationships across biblical timeline
     */
    renderTimelineLayout(rootPersonId) {
        this.currentLayout = 'timeline';
        this.updateDimensions();
        
        const timelineData = this.buildTimelineData(rootPersonId);
        if (!timelineData.length) return;

        this.g.selectAll("*").remove();

        // Sort by estimated birth year
        timelineData.sort((a, b) => (a.estimatedYear || 0) - (b.estimatedYear || 0));

        const padding = 50;
        const timelineWidth = this.width - 2 * padding;
        const timelineHeight = this.height - 2 * padding;

        // Create time scale
        const years = timelineData.map(d => d.estimatedYear || 0).filter(y => y > 0);
        const minYear = Math.min(...years) || 4000;
        const maxYear = Math.max(...years) || 1;
        
        const xScale = d3.scaleLinear()
            .domain([minYear, maxYear])
            .range([padding, this.width - padding]);

        // Group by generation for y-positioning
        const generations = this.groupByGeneration(timelineData);
        const yScale = d3.scaleBand()
            .domain(Object.keys(generations))
            .range([padding, this.height - padding])
            .paddingInner(0.2);

        // Draw timeline axis
        this.drawTimelineAxis(xScale, minYear, maxYear);

        // Position and draw nodes
        Object.entries(generations).forEach(([generation, persons]) => {
            const y = yScale(generation) + yScale.bandwidth() / 2;
            
            persons.forEach((person, index) => {
                const x = person.estimatedYear ? 
                    xScale(person.estimatedYear) : 
                    padding + (index * 30); // Fallback positioning
                
                person.x = x;
                person.y = y;
            });
        });

        this.drawTimelineConnections(timelineData);
        this.drawNodes(timelineData, rootPersonId);
        this.addGenerationLabels(generations, 20, 0, yScale.bandwidth());
    }

    /**
     * Circular Pedigree Layout - Traditional pedigree chart in circular form
     */
    renderCircularPedigreeLayout(rootPersonId) {
        this.currentLayout = 'circular-pedigree';
        this.updateDimensions();
        
        const pedigreeData = this.buildPedigreeData(rootPersonId, 5);
        if (!pedigreeData) return;

        this.g.selectAll("*").remove();

        const centerX = this.width / 2;
        const centerY = this.height / 2;
        const maxRadius = Math.min(this.width, this.height) / 2 - 60;

        // Calculate positions for pedigree chart
        this.positionPedigreeNodes(pedigreeData, centerX, centerY, maxRadius);
        
        this.drawPedigreeConnections(pedigreeData);
        this.drawNodes([pedigreeData], rootPersonId);
    }

    // Helper Methods

    buildRadialTreeData(rootPersonId, maxGenerations) {
        const nodes = [];
        const visited = new Set();
        
        const traverse = (personId, generation) => {
            if (!personId || visited.has(personId) || generation > maxGenerations) return null;
            
            visited.add(personId);
            const person = this.familyData[personId];
            if (!person) return null;

            const node = {
                id: personId,
                name: person.name,
                data: person,
                gender: this.determineGender(person),
                generation: generation,
                children: []
            };

            nodes.push(node);

            // Add children
            if (person.children && generation < maxGenerations) {
                person.children.forEach(childId => {
                    const child = traverse(childId, generation + 1);
                    if (child) node.children.push(child);
                });
            }

            return node;
        };

        const rootNode = traverse(rootPersonId, 0);
        return { root: rootNode, nodes: nodes };
    }

    buildGraphData(rootPersonId, includeExtended) {
        const nodes = [];
        const links = [];
        const visited = new Set();
        const maxDepth = includeExtended ? 3 : 2;

        const traverse = (personId, depth) => {
            if (!personId || visited.has(personId) || depth > maxDepth) return;
            
            visited.add(personId);
            const person = this.familyData[personId];
            if (!person) return;

            const node = {
                id: personId,
                name: person.name,
                data: person,
                gender: this.determineGender(person)
            };
            nodes.push(node);

            // Add family links
            if (person.spouse) {
                const spouseId = this.findPersonIdByName(person.spouse);
                if (spouseId && !visited.has(spouseId)) {
                    traverse(spouseId, depth);
                    links.push({
                        source: personId,
                        target: spouseId,
                        type: 'marriage'
                    });
                }
            }

            // Add parent-child links
            if (person.children && depth < maxDepth) {
                person.children.forEach(childId => {
                    traverse(childId, depth + 1);
                    links.push({
                        source: personId,
                        target: childId,
                        type: 'parent-child'
                    });
                });
            }

            // Add parent links
            if (person.parents && depth < maxDepth) {
                person.parents.forEach(parentId => {
                    traverse(parentId, depth + 1);
                    links.push({
                        source: parentId,
                        target: personId,
                        type: 'parent-child'
                    });
                });
            }
        };

        traverse(rootPersonId, 0);
        return { nodes, links };
    }

    buildTimelineData(rootPersonId) {
        const persons = [];
        const visited = new Set();

        const traverse = (personId, generation = 0) => {
            if (!personId || visited.has(personId)) return;
            
            visited.add(personId);
            const person = this.familyData[personId];
            if (!person) return;

            const estimatedYear = this.estimateBirthYear(person);
            persons.push({
                id: personId,
                name: person.name,
                data: person,
                gender: this.determineGender(person),
                generation: generation,
                estimatedYear: estimatedYear
            });

            // Traverse family members
            if (person.children) {
                person.children.forEach(childId => traverse(childId, generation + 1));
            }
            if (person.parents) {
                person.parents.forEach(parentId => traverse(parentId, generation - 1));
            }
        };

        traverse(rootPersonId);
        return persons;
    }

    getGenerationLevels(treeData) {
        const generations = {};
        
        const addToGeneration = (node) => {
            const gen = node.generation || 0;
            if (!generations[gen]) generations[gen] = [];
            generations[gen].push(node);
            
            if (node.children) {
                node.children.forEach(addToGeneration);
            }
        };

        if (treeData.nodes) {
            treeData.nodes.forEach(addToGeneration);
        }

        return Object.values(generations);
    }

    drawRadialConnections(treeData) {
        // Draw curved connections between generations
        const connections = [];
        
        const addConnections = (node) => {
            if (node.children) {
                node.children.forEach(child => {
                    connections.push({ source: node, target: child });
                    addConnections(child);
                });
            }
        };

        if (treeData.root) addConnections(treeData.root);

        this.g.selectAll('.radial-link')
            .data(connections)
            .enter()
            .append('path')
            .attr('class', 'radial-link')
            .attr('d', d => {
                const midX = (d.source.x + d.target.x) / 2;
                const midY = (d.source.y + d.target.y) / 2;
                return `M${d.source.x},${d.source.y} Q${midX},${midY} ${d.target.x},${d.target.y}`;
            })
            .attr('stroke', '#666')
            .attr('stroke-width', 2)
            .attr('fill', 'none');
    }

    drawNodes(nodes, currentPersonId) {
        const nodeSelection = this.g.selectAll('.tree-node')
            .data(nodes)
            .enter()
            .append('g')
            .attr('class', d => `tree-node ${d.gender} ${d.id === currentPersonId ? 'current' : ''}`)
            .attr('transform', d => `translate(${d.x},${d.y})`)
            .on('click', (event, d) => {
                if (this.selectPerson) this.selectPerson(d.id);
            });

        nodeSelection.append('circle')
            .attr('r', d => d.id === currentPersonId ? 10 : 6)
            .attr('fill', d => this.getNodeColor(d, currentPersonId));

        nodeSelection.append('text')
            .attr('dy', '.35em')
            .attr('text-anchor', 'middle')
            .style('font-size', '10px')
            .style('font-weight', d => d.id === currentPersonId ? 'bold' : 'normal')
            .text(d => this.truncateName(d.name, 12));
    }

    // Utility Methods

    determineGender(person) {
        const name = person.name.toLowerCase();
        const femaleNames = ['eve', 'sarah', 'rebekah', 'rachel', 'leah', 'mary', 'elizabeth'];
        return femaleNames.includes(name) ? 'female' : 'male';
    }

    getNodeColor(node, currentPersonId) {
        if (node.id === currentPersonId) return '#007bff';
        return node.gender === 'female' ? '#e91e63' : '#2196f3';
    }

    getLinkColor(type) {
        switch(type) {
            case 'marriage': return '#4caf50';
            case 'parent-child': return '#666';
            default: return '#999';
        }
    }

    getLinkDistance(link) {
        return link.type === 'marriage' ? 80 : 120;
    }

    getLinkStrength(link) {
        return link.type === 'marriage' ? 0.8 : 0.5;
    }

    truncateName(name, maxLength) {
        return name.length > maxLength ? name.substring(0, maxLength) + '...' : name;
    }

    estimateBirthYear(person) {
        // Simple estimation based on biblical timeline
        // This would need more sophisticated logic based on actual biblical data
        const birthYear = person.birth_year;
        if (birthYear && birthYear !== "Unknown") {
            const match = birthYear.match(/\d+/);
            return match ? parseInt(match[0]) : null;
        }
        return null;
    }

    findPersonIdByName(name) {
        return Object.keys(this.familyData).find(id => 
            this.familyData[id].name === name
        );
    }

    // Force simulation event handlers
    dragStarted(event, d) {
        if (!event.active) this.simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    dragged(event, d) {
        d.fx = event.x;
        d.fy = event.y;
    }

    dragEnded(event, d) {
        if (!event.active) this.simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }

    // Public API
    setSelectPersonCallback(callback) {
        this.selectPerson = callback;
    }

    getCurrentLayout() {
        return this.currentLayout;
    }

    centerView() {
        const bounds = this.g.node().getBBox();
        const parent = this.svg.node().getBoundingClientRect();
        const fullWidth = parent.width;
        const fullHeight = parent.height;
        const width = bounds.width;
        const height = bounds.height;
        const midX = bounds.x + width / 2;
        const midY = bounds.y + height / 2;
        
        const scale = 0.8 / Math.max(width / fullWidth, height / fullHeight);
        const translate = [fullWidth / 2 - scale * midX, fullHeight / 2 - scale * midY];
        
        this.svg.transition()
            .duration(750)
            .call(this.zoom.transform, d3.zoomIdentity.translate(translate[0], translate[1]).scale(scale));
    }

    destroy() {
        if (this.simulation) {
            this.simulation.stop();
        }
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AdvancedTreeLayouts;
}