/**
 * FamilySearch-Style Interactive Family Tree
 * Recreates the FamilySearch family tree experience with person cards,
 * smooth animations, and their signature layout
 */

class FamilySearchStyleTree {
    constructor(containerId, familyData) {
        this.container = document.getElementById(containerId);
        this.familyData = familyData;
        this.currentPersonId = null;
        this.treeData = {};
        this.scale = 1;
        this.translateX = 0;
        this.translateY = 0;
        this.isDragging = false;
        
        this.cardWidth = 200;
        this.cardHeight = 120;
        this.generationSpacing = 180;
        this.siblingSpacing = 220;
        
        this.init();
    }

    init() {
        this.createTreeContainer();
        this.setupEventListeners();
        this.initializeWithFirstPerson();
    }

    createTreeContainer() {
        this.container.innerHTML = `
            <div class="fs-tree-wrapper">
                <div class="fs-tree-controls">
                    <div class="fs-control-group">
                        <button class="fs-btn fs-btn-icon" onclick="fsTree.zoomIn()" title="Zoom In">
                            <i class="fas fa-plus"></i>
                        </button>
                        <button class="fs-btn fs-btn-icon" onclick="fsTree.zoomOut()" title="Zoom Out">
                            <i class="fas fa-minus"></i>
                        </button>
                        <button class="fs-btn fs-btn-icon" onclick="fsTree.centerTree()" title="Center">
                            <i class="fas fa-crosshairs"></i>
                        </button>
                    </div>
                    <div class="fs-control-group">
                        <button class="fs-btn fs-btn-compact" onclick="fsTree.switchView('ancestors')" title="Focus on Ancestors">
                            <i class="fas fa-arrow-up"></i> Ancestors
                        </button>
                        <button class="fs-btn fs-btn-compact" onclick="fsTree.switchView('family')" title="Focus on Family">
                            <i class="fas fa-users"></i> Family
                        </button>
                        <button class="fs-btn fs-btn-compact" onclick="fsTree.switchView('descendants')" title="Focus on Descendants">
                            <i class="fas fa-arrow-down"></i> Descendants
                        </button>
                    </div>
                    <div class="fs-control-group">
                        <div class="fs-breadcrumb">
                            <span id="fs-breadcrumb-text">Biblical Family Tree</span>
                        </div>
                    </div>
                </div>
                
                <div class="fs-tree-viewport" id="fs-tree-viewport">
                    <svg class="fs-tree-svg" id="fs-tree-svg">
                        <defs>
                            <filter id="fs-shadow" x="-50%" y="-50%" width="200%" height="200%">
                                <feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="#000" flood-opacity="0.1"/>
                            </filter>
                            <linearGradient id="fs-male-gradient" x1="0%" y1="0%" x2="0%" y2="100%">
                                <stop offset="0%" style="stop-color:#4A90E2;stop-opacity:1" />
                                <stop offset="100%" style="stop-color:#357ABD;stop-opacity:1" />
                            </linearGradient>
                            <linearGradient id="fs-female-gradient" x1="0%" y1="0%" x2="0%" y2="100%">
                                <stop offset="0%" style="stop-color:#E85D8A;stop-opacity:1" />
                                <stop offset="100%" style="stop-color:#D1477A;stop-opacity:1" />
                            </linearGradient>
                        </defs>
                        <g class="fs-tree-content" id="fs-tree-content"></g>
                    </svg>
                </div>
            </div>
        `;
    }

    setupEventListeners() {
        const viewport = document.getElementById('fs-tree-viewport');
        
        // Mouse wheel zoom
        viewport.addEventListener('wheel', (e) => {
            e.preventDefault();
            const delta = e.deltaY * -0.001;
            const newScale = Math.max(0.1, Math.min(3, this.scale + delta));
            this.setZoom(newScale, e.clientX, e.clientY);
        });

        // Pan functionality
        let startX, startY;
        viewport.addEventListener('mousedown', (e) => {
            if (e.target.classList.contains('fs-person-card') || e.target.closest('.fs-person-card')) return;
            this.isDragging = true;
            startX = e.clientX - this.translateX;
            startY = e.clientY - this.translateY;
            viewport.style.cursor = 'grabbing';
        });

        document.addEventListener('mousemove', (e) => {
            if (!this.isDragging) return;
            this.translateX = e.clientX - startX;
            this.translateY = e.clientY - startY;
            this.updateTransform();
        });

        document.addEventListener('mouseup', () => {
            this.isDragging = false;
            viewport.style.cursor = 'grab';
        });
    }

    initializeWithFirstPerson() {
        const firstPersonId = Object.keys(this.familyData)[0];
        if (firstPersonId) {
            this.loadPerson(firstPersonId);
        }
    }

    loadPerson(personId) {
        this.currentPersonId = personId;
        this.treeData = this.buildTreeData(personId);
        this.renderTree();
        this.updateBreadcrumb();
        this.centerTree();
    }

    buildTreeData(rootId) {
        const tree = {
            person: this.familyData[rootId],
            id: rootId,
            ancestors: this.buildAncestors(rootId, 3),
            descendants: this.buildDescendants(rootId, 2),
            siblings: this.buildSiblings(rootId),
            spouse: this.findSpouse(rootId)
        };
        return tree;
    }

    buildAncestors(personId, generations) {
        if (generations <= 0) return null;
        
        const person = this.familyData[personId];
        if (!person || !person.parents || person.parents.length === 0) return null;

        const ancestors = {
            generation: generations,
            parents: []
        };

        person.parents.forEach(parentId => {
            if (this.familyData[parentId]) {
                const parentData = {
                    person: this.familyData[parentId],
                    id: parentId,
                    ancestors: this.buildAncestors(parentId, generations - 1),
                    spouse: this.findSpouse(parentId)
                };
                ancestors.parents.push(parentData);
            }
        });

        return ancestors.parents.length > 0 ? ancestors : null;
    }

    buildDescendants(personId, generations) {
        if (generations <= 0) return null;
        
        const person = this.familyData[personId];
        if (!person || !person.children || person.children.length === 0) return null;

        const descendants = [];
        person.children.forEach(childId => {
            if (this.familyData[childId]) {
                const childData = {
                    person: this.familyData[childId],
                    id: childId,
                    descendants: this.buildDescendants(childId, generations - 1),
                    spouse: this.findSpouse(childId)
                };
                descendants.push(childData);
            }
        });

        return descendants.length > 0 ? descendants : null;
    }

    buildSiblings(personId) {
        const person = this.familyData[personId];
        if (!person || !person.parents || person.parents.length === 0) return [];

        const siblings = [];
        const parentId = person.parents[0];
        const parent = this.familyData[parentId];
        
        if (parent && parent.children) {
            parent.children.forEach(siblingId => {
                if (siblingId !== personId && this.familyData[siblingId]) {
                    siblings.push({
                        person: this.familyData[siblingId],
                        id: siblingId,
                        spouse: this.findSpouse(siblingId)
                    });
                }
            });
        }

        return siblings;
    }

    findSpouse(personId) {
        const person = this.familyData[personId];
        if (!person || !person.spouse) return null;

        const spouseId = Object.keys(this.familyData).find(id => 
            this.familyData[id].name === person.spouse
        );

        return spouseId ? {
            person: this.familyData[spouseId],
            id: spouseId
        } : null;
    }

    renderTree() {
        const content = document.getElementById('fs-tree-content');
        content.innerHTML = '';

        const centerX = 0;
        const centerY = 0;

        // Render main person at center
        this.renderPersonCard(content, this.treeData, centerX, centerY, 'main');

        // Render spouse next to main person
        if (this.treeData.spouse) {
            this.renderPersonCard(content, this.treeData.spouse, centerX + this.cardWidth + 20, centerY, 'spouse');
            this.renderMarriageLine(content, centerX, centerY, centerX + this.cardWidth + 20, centerY);
        }

        // Render ancestors (parents, grandparents, etc.)
        if (this.treeData.ancestors) {
            this.renderAncestors(content, this.treeData.ancestors, centerX, centerY - this.generationSpacing);
        }

        // Render descendants (children, grandchildren)
        if (this.treeData.descendants) {
            this.renderDescendants(content, this.treeData.descendants, centerX, centerY + this.generationSpacing);
        }

        // Render siblings
        if (this.treeData.siblings && this.treeData.siblings.length > 0) {
            this.renderSiblings(content, this.treeData.siblings, centerX, centerY);
        }
    }

    renderPersonCard(container, personData, x, y, type = 'normal') {
        const person = personData.person;
        const gender = this.determineGender(person);
        
        // Create card group
        const cardGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        cardGroup.setAttribute('class', `fs-person-card fs-card-${type} fs-gender-${gender}`);
        cardGroup.setAttribute('transform', `translate(${x}, ${y})`);
        cardGroup.style.cursor = 'pointer';

        // Card background
        const cardBg = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
        cardBg.setAttribute('width', this.cardWidth);
        cardBg.setAttribute('height', this.cardHeight);
        cardBg.setAttribute('rx', '8');
        cardBg.setAttribute('ry', '8');
        cardBg.setAttribute('fill', gender === 'female' ? 'url(#fs-female-gradient)' : 'url(#fs-male-gradient)');
        cardBg.setAttribute('stroke', type === 'main' ? '#FFD700' : 'rgba(255,255,255,0.3)');
        cardBg.setAttribute('stroke-width', type === 'main' ? '3' : '1');
        cardBg.setAttribute('filter', 'url(#fs-shadow)');

        // Profile circle
        const profileCircle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        profileCircle.setAttribute('cx', '30');
        profileCircle.setAttribute('cy', '30');
        profileCircle.setAttribute('r', '20');
        profileCircle.setAttribute('fill', 'rgba(255,255,255,0.2)');
        profileCircle.setAttribute('stroke', 'rgba(255,255,255,0.5)');
        profileCircle.setAttribute('stroke-width', '2');

        // Profile icon
        const profileIcon = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        profileIcon.setAttribute('x', '30');
        profileIcon.setAttribute('y', '37');
        profileIcon.setAttribute('text-anchor', 'middle');
        profileIcon.setAttribute('fill', 'white');
        profileIcon.setAttribute('font-family', 'FontAwesome');
        profileIcon.setAttribute('font-size', '16');
        profileIcon.textContent = gender === 'female' ? '\uf182' : '\uf183';

        // Name text
        const nameText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        nameText.setAttribute('x', '65');
        nameText.setAttribute('y', '25');
        nameText.setAttribute('fill', 'white');
        nameText.setAttribute('font-family', 'Arial, sans-serif');
        nameText.setAttribute('font-size', '14');
        nameText.setAttribute('font-weight', 'bold');
        nameText.textContent = this.truncateText(person.name, 18);

        // Title text
        const titleText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        titleText.setAttribute('x', '65');
        titleText.setAttribute('y', '42');
        titleText.setAttribute('fill', 'rgba(255,255,255,0.8)');
        titleText.setAttribute('font-family', 'Arial, sans-serif');
        titleText.setAttribute('font-size', '11');
        titleText.textContent = this.truncateText(person.title || 'Biblical Figure', 20);

        // Dates text
        const datesText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        datesText.setAttribute('x', '10');
        datesText.setAttribute('y', '75');
        datesText.setAttribute('fill', 'rgba(255,255,255,0.7)');
        datesText.setAttribute('font-family', 'Arial, sans-serif');
        datesText.setAttribute('font-size', '10');
        const birthYear = person.birth_year && person.birth_year !== 'Unknown' ? person.birth_year : '?';
        const deathYear = person.death_year && person.death_year !== 'Unknown' ? person.death_year : '?';
        datesText.textContent = `${birthYear} - ${deathYear}`;

        // Expand button
        const expandBtn = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        expandBtn.setAttribute('cx', this.cardWidth - 20);
        expandBtn.setAttribute('cy', '20');
        expandBtn.setAttribute('r', '12');
        expandBtn.setAttribute('fill', 'rgba(255,255,255,0.2)');
        expandBtn.setAttribute('stroke', 'rgba(255,255,255,0.5)');
        expandBtn.setAttribute('stroke-width', '1');
        expandBtn.style.cursor = 'pointer';

        const expandIcon = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        expandIcon.setAttribute('x', this.cardWidth - 20);
        expandIcon.setAttribute('y', '25');
        expandIcon.setAttribute('text-anchor', 'middle');
        expandIcon.setAttribute('fill', 'white');
        expandIcon.setAttribute('font-family', 'FontAwesome');
        expandIcon.setAttribute('font-size', '10');
        expandIcon.textContent = '\uf065';

        // Add all elements to card
        cardGroup.appendChild(cardBg);
        cardGroup.appendChild(profileCircle);
        cardGroup.appendChild(profileIcon);
        cardGroup.appendChild(nameText);
        cardGroup.appendChild(titleText);
        cardGroup.appendChild(datesText);
        cardGroup.appendChild(expandBtn);
        cardGroup.appendChild(expandIcon);

        // Add click handler
        cardGroup.addEventListener('click', () => {
            this.selectPerson(personData.id);
        });

        // Add hover effects
        cardGroup.addEventListener('mouseenter', () => {
            cardBg.setAttribute('stroke-width', '2');
            cardGroup.style.transform = `translate(${x}px, ${y}px) scale(1.02)`;
        });

        cardGroup.addEventListener('mouseleave', () => {
            if (type !== 'main') cardBg.setAttribute('stroke-width', '1');
            cardGroup.style.transform = `translate(${x}px, ${y}px) scale(1)`;
        });

        container.appendChild(cardGroup);
        return cardGroup;
    }

    renderAncestors(container, ancestors, centerX, startY) {
        if (!ancestors || !ancestors.parents) return;

        const parentSpacing = this.cardWidth + 40;
        const startX = centerX - (ancestors.parents.length - 1) * parentSpacing / 2;

        ancestors.parents.forEach((parent, index) => {
            const x = startX + index * parentSpacing;
            const y = startY;

            // Render parent card
            this.renderPersonCard(container, parent, x, y, 'ancestor');

            // Render spouse if exists
            if (parent.spouse) {
                const spouseX = x + this.cardWidth + 20;
                this.renderPersonCard(container, parent.spouse, spouseX, y, 'ancestor');
                this.renderMarriageLine(container, x, y, spouseX, y);
            }

            // Draw connection line to main person
            this.renderConnectionLine(container, 
                x + this.cardWidth / 2, y + this.cardHeight,
                centerX + this.cardWidth / 2, startY + this.generationSpacing
            );

            // Recursively render grandparents
            if (parent.ancestors) {
                this.renderAncestors(container, parent.ancestors, x, y - this.generationSpacing);
            }
        });
    }

    renderDescendants(container, descendants, centerX, startY) {
        if (!descendants || descendants.length === 0) return;

        const childSpacing = this.cardWidth + 30;
        const startX = centerX - (descendants.length - 1) * childSpacing / 2;

        descendants.forEach((child, index) => {
            const x = startX + index * childSpacing;
            const y = startY;

            // Render child card
            this.renderPersonCard(container, child, x, y, 'descendant');

            // Render spouse if exists
            if (child.spouse) {
                const spouseX = x + this.cardWidth + 20;
                this.renderPersonCard(container, child.spouse, spouseX, y, 'descendant');
                this.renderMarriageLine(container, x, y, spouseX, y);
            }

            // Draw connection line to main person
            this.renderConnectionLine(container,
                centerX + this.cardWidth / 2, startY - this.generationSpacing,
                x + this.cardWidth / 2, y
            );

            // Recursively render grandchildren
            if (child.descendants) {
                this.renderDescendants(container, child.descendants, x, y + this.generationSpacing);
            }
        });
    }

    renderSiblings(container, siblings, centerX, centerY) {
        if (!siblings || siblings.length === 0) return;

        const siblingSpacing = this.cardWidth + 30;
        const startX = centerX - siblingSpacing * Math.ceil(siblings.length / 2);

        siblings.forEach((sibling, index) => {
            const x = startX + index * siblingSpacing - this.cardWidth;
            const y = centerY + this.cardHeight + 40;

            this.renderPersonCard(container, sibling, x, y, 'sibling');

            if (sibling.spouse) {
                const spouseX = x + this.cardWidth + 20;
                this.renderPersonCard(container, sibling.spouse, spouseX, y, 'sibling');
                this.renderMarriageLine(container, x, y, spouseX, y);
            }
        });
    }

    renderConnectionLine(container, x1, y1, x2, y2) {
        const line = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        const midY = (y1 + y2) / 2;
        
        line.setAttribute('d', `M ${x1} ${y1} L ${x1} ${midY} L ${x2} ${midY} L ${x2} ${y2}`);
        line.setAttribute('stroke', '#c0c0c0');
        line.setAttribute('stroke-width', '2');
        line.setAttribute('fill', 'none');
        line.setAttribute('stroke-linecap', 'round');
        
        container.appendChild(line);
    }

    renderMarriageLine(container, x1, y1, x2, y2) {
        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        line.setAttribute('x1', x1 + this.cardWidth);
        line.setAttribute('y1', y1 + this.cardHeight / 2);
        line.setAttribute('x2', x2);
        line.setAttribute('y2', y2 + this.cardHeight / 2);
        line.setAttribute('stroke', '#FFD700');
        line.setAttribute('stroke-width', '3');
        line.setAttribute('stroke-linecap', 'round');
        
        container.appendChild(line);
    }

    selectPerson(personId) {
        if (personId === this.currentPersonId) return;
        
        // Smooth transition effect
        const content = document.getElementById('fs-tree-content');
        content.style.opacity = '0.3';
        content.style.transition = 'opacity 0.3s ease';
        
        setTimeout(() => {
            this.loadPerson(personId);
            content.style.opacity = '1';
        }, 150);
    }

    // Utility methods
    determineGender(person) {
        const name = person.name.toLowerCase();
        const femaleNames = ['eve', 'sarah', 'rebekah', 'rachel', 'leah', 'mary', 'elizabeth', 'ruth', 'naomi'];
        return femaleNames.some(fname => name.includes(fname)) ? 'female' : 'male';
    }

    truncateText(text, maxLength) {
        return text.length > maxLength ? text.substring(0, maxLength - 3) + '...' : text;
    }

    updateBreadcrumb() {
        const breadcrumb = document.getElementById('fs-breadcrumb-text');
        const person = this.familyData[this.currentPersonId];
        breadcrumb.textContent = person ? person.name : 'Biblical Family Tree';
    }

    // Zoom and pan methods
    zoomIn() {
        this.setZoom(Math.min(3, this.scale * 1.2));
    }

    zoomOut() {
        this.setZoom(Math.max(0.1, this.scale / 1.2));
    }

    setZoom(newScale, centerX = null, centerY = null) {
        const viewport = document.getElementById('fs-tree-viewport');
        const rect = viewport.getBoundingClientRect();
        
        const cx = centerX || rect.width / 2;
        const cy = centerY || rect.height / 2;
        
        this.scale = newScale;
        this.updateTransform();
    }

    centerTree() {
        this.translateX = 0;
        this.translateY = 0;
        this.scale = 1;
        this.updateTransform();
    }

    updateTransform() {
        const content = document.getElementById('fs-tree-content');
        content.setAttribute('transform', 
            `translate(${this.translateX}, ${this.translateY}) scale(${this.scale})`
        );
    }

    switchView(viewType) {
        // Remove active state from all buttons
        document.querySelectorAll('.fs-btn-compact').forEach(btn => {
            btn.classList.remove('active');
        });
        
        // Add active state to clicked button
        event.target.classList.add('active');
        
        // Adjust tree focus based on view type
        switch(viewType) {
            case 'ancestors':
                this.focusOnAncestors();
                break;
            case 'family':
                this.centerTree();
                break;
            case 'descendants':
                this.focusOnDescendants();
                break;
        }
    }

    focusOnAncestors() {
        this.translateY = 200;
        this.updateTransform();
    }

    focusOnDescendants() {
        this.translateY = -200;
        this.updateTransform();
    }
}

// CSS for FamilySearch-style tree (to be added to the page)
const familySearchCSS = `
<style>
.fs-tree-wrapper {
    width: 100%;
    height: 600px;
    position: relative;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

.fs-tree-controls {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    background: rgba(255,255,255,0.95);
    backdrop-filter: blur(10px);
    padding: 12px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(0,0,0,0.1);
    z-index: 10;
}

.fs-control-group {
    display: flex;
    gap: 8px;
    align-items: center;
}

.fs-btn {
    padding: 8px 12px;
    border: 1px solid #ddd;
    background: white;
    border-radius: 6px;
    cursor: pointer;
    font-size: 12px;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    gap: 4px;
}

.fs-btn:hover {
    background: #f8f9fa;
    border-color: #007bff;
    transform: translateY(-1px);
}

.fs-btn.active {
    background: #007bff;
    color: white;
    border-color: #007bff;
}

.fs-btn-icon {
    width: 32px;
    height: 32px;
    padding: 8px;
    justify-content: center;
}

.fs-btn-compact {
    font-size: 11px;
    padding: 6px 10px;
}

.fs-breadcrumb {
    font-weight: 600;
    color: #495057;
    font-size: 14px;
}

.fs-tree-viewport {
    position: absolute;
    top: 60px;
    left: 0;
    right: 0;
    bottom: 0;
    cursor: grab;
    overflow: hidden;
}

.fs-tree-viewport:active {
    cursor: grabbing;
}

.fs-tree-svg {
    width: 100%;
    height: 100%;
}

.fs-tree-content {
    transform-origin: center;
    transition: opacity 0.3s ease;
}

.fs-person-card {
    transition: all 0.2s ease;
}

.fs-person-card:hover {
    transform: scale(1.02) !important;
}

.fs-card-main .fs-person-card rect {
    stroke: #FFD700;
    stroke-width: 3;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.fs-person-card {
    animation: fadeInUp 0.3s ease forwards;
}
</style>
`;

// Auto-inject CSS
document.head.insertAdjacentHTML('beforeend', familySearchCSS);

// Global instance for easy access
let fsTree = null;

// Initialize function
function initializeFamilySearchTree(containerId, familyData) {
    fsTree = new FamilySearchStyleTree(containerId, familyData);
    return fsTree;
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { FamilySearchStyleTree, initializeFamilySearchTree };
}