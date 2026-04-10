document.addEventListener('DOMContentLoaded', async () => {
    const scenarioSelect = document.getElementById('scenarioSelect');
    const healthScore = document.getElementById('healthScore');
    const container = document.getElementById('graphContainer');
    
    let appData = null;
    let simulation = null;

    try {
        const resp = await fetch('data/gravity_results.json');
        appData = await resp.json();
    } catch (e) {
        console.error('Failed to load gravity data:', e);
        return;
    }

    const width = container.clientWidth;
    const height = container.clientHeight;

    const svg = d3.select("#graphContainer").append("svg")
        .attr("width", "100%")
        .attr("height", "100%")
        .attr("viewBox", [0, 0, width, height]);

    // Defs for arrows
    svg.append("defs").selectAll("marker")
        .data(["end"])
        .join("marker")
        .attr("id", "arrow")
        .attr("viewBox", "0 -5 10 10")
        .attr("refX", 25)
        .attr("refY", 0)
        .attr("markerWidth", 6)
        .attr("markerHeight", 6)
        .attr("orient", "auto")
        .append("path")
        .attr("fill", "#475569")
        .attr("d", "M0,-5L10,0L0,5");

    const link = svg.append("g")
        .selectAll("line")
        .data(appData.graph.edges)
        .join("line")
        .attr("class", "link")
        .attr("marker-end", "url(#arrow)");

    const node = svg.append("g")
        .selectAll("g")
        .data(appData.graph.nodes)
        .join("g")
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));

    const circles = node.append("circle")
        .attr("class", "node-circle")
        .attr("r", 20);

    const labels = node.append("text")
        .attr("class", "node-text")
        .attr("dy", 35)
        .text(d => d.label);
        
    const reliabilityText = node.append("text")
        .attr("class", "node-text")
        .attr("dy", 5)
        .attr("font-weight", "bold");

    simulation = d3.forceSimulation(appData.graph.nodes)
        .force("link", d3.forceLink(appData.graph.edges).id(d => d.id).distance(150))
        .force("charge", d3.forceManyBody().strength(-800))
        .force("center", d3.forceCenter(width / 2, height / 2))
        .on("tick", () => {
            link.attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);
            node.attr("transform", d => `translate(${d.x},${d.y})`);
        });

    function updateScenario(scenarioId) {
        const scenario = appData.scenarios.find(s => s.id === scenarioId);
        if(!scenario) return;

        // Update Health
        healthScore.textContent = scenario.portfolio_health.toFixed(1) + '%';
        healthScore.style.color = scenario.portfolio_health > 90 ? '#10b981' : (scenario.portfolio_health > 60 ? '#facc15' : '#ef4444');

        // Update Nodes
        circles.attr("fill", d => {
            const rel = scenario.node_reliabilities[d.id];
            if(rel === 1.0) return '#10b981'; // Green
            if(rel === 0.0) return '#ef4444'; // Red (Shock origin)
            return '#facc15'; // Yellow (Collateral damage)
        });
        
        reliabilityText.text(d => {
            const rel = scenario.node_reliabilities[d.id];
            return (rel * 100).toFixed(0) + '%';
        });
    }

    scenarioSelect.addEventListener('change', (e) => {
        updateScenario(e.target.value);
    });

    // Init
    updateScenario('baseline');

    // Drag functions
    function dragstarted(event) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        event.subject.fx = event.subject.x;
        event.subject.fy = event.subject.y;
    }
    function dragged(event) {
        event.subject.fx = event.x;
        event.subject.fy = event.y;
    }
    function dragended(event) {
        if (!event.active) simulation.alphaTarget(0);
        event.subject.fx = null;
        event.subject.fy = null;
    }
});
