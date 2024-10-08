    const o = [1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7];

const e = [[1], [2], [2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6], [2, 7], [2, 8], [2, 8, 1], [2, 8, 2], [2, 8, 3], [2, 8, 4], [2, 8, 5], [2, 8, 6], [2, 8, 7], [2, 8, 8], [2, 8, 8, 1], [2, 8, 8, 2], [2, 8, 8, 3], [2, 8, 8, 4], [2, 8, 8, 5], [2, 8, 8, 6], [2, 8, 8, 7], [2, 8, 8, 8], [2, 8, 18, 1], [2, 8, 18, 2], [2, 8, 18, 3], [2, 8, 18, 4], [2, 8, 18, 5], [2, 8, 18, 6], [2, 8, 18, 7], [2, 8, 18, 8], [2, 8, 18, 9], [2, 8, 18, 10], [2, 8, 18, 11], [2, 8, 18, 12], [2, 8, 18, 13], [2, 8, 18, 14], [2, 8, 18, 15], [2, 8, 18, 16], [2, 8, 18, 17], [2, 8, 18, 18], [2, 8, 18, 18, 1], [2, 8, 18, 18, 2], [2, 8, 18, 18, 3], [2, 8, 18, 18, 4], [2, 8, 18, 18, 5], [2, 8, 18, 18, 6], [2, 8, 18, 18, 7], [2, 8, 18, 18, 8], [2, 8, 18, 18, 9], [2, 8, 18, 18, 10], [2, 8, 18, 18, 11], [2, 8, 18, 18, 12], [2, 8, 18, 18, 13], [2, 8, 18, 18, 14], [2, 8, 18, 18, 15], [2, 8, 18, 18, 16], [2, 8, 18, 18, 17], [2, 8, 18, 18, 18]]; // Number of electrons in each shell

const p = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118];
// Number of protons for first five elements

const n = [0, 2, 4, 5, 6, 6, 7, 8, 10, 10, 12, 12, 14, 14, 16, 16, 18, 18, 20, 20, 22, 22, 24, 24, 26, 28, 30, 31, 33, 34, 36, 37, 39, 40, 42, 43, 45, 46, 48, 49, 51, 52, 54, 55, 57, 58, 60, 61, 63, 64, 66, 67, 69, 70, 72, 73, 75, 76, 78, 79, 81, 82, 84, 85, 87, 88, 90, 91, 93, 94, 96, 97, 99, 100, 102, 103, 105, 106, 108, 109, 111, 112, 114, 115, 117, 118, 120, 121, 123, 124, 126, 127, 129, 130, 132, 133, 135, 136, 138, 139, 141, 142, 144, 145, 147, 148, 150, 151, 153, 154, 156, 157, 159, 160];
 // Number of neutrons for first five elements

    let numOrbits = 1;
    let numElectrons = [1];
    let numProtons = 1;
    let numNeutrons = 0;
    let angles = [];
    const orbitSpeeds = [0.02, 0.015, 0.01, 0.007, 0.007, 0.01, 0.015]; // Default speeds

    function displayElement(index) {
        numOrbits = o[index];
        numElectrons = e[index];
        numProtons = p[index];
        numNeutrons = n[index];
        angles = Array(numOrbits).fill(0); // Reset angles array to default values
        updateCanvas(); // Redraw orbits with new data
    }

    const canvas = document.getElementById('atomCanvas');
    const context = canvas.getContext('2d');
    let centerX, centerY;
    const canvasWidthPercentage = 0.2; // 20% of screen width
    const canvasHeightPercentage = 0.4; // 40% of screen height

    function updateCanvasSize() {
        canvas.width = window.innerWidth * canvasWidthPercentage;
        canvas.height = window.innerHeight * canvasHeightPercentage;
        centerX = canvas.width / 2;
        centerY = canvas.height / 2;
    }

    const baseRadius = 80 * canvasWidthPercentage; // Scale base radius
    const ringWidth = 4 * canvasWidthPercentage; // Scale ring width
    const electronRadius = 7 * canvasWidthPercentage; // Scale electron radius
    const nucleusRadius = 70 * canvasWidthPercentage; // Scale nucleus radius
    const protonRadius = 12 * canvasWidthPercentage; // Scale proton radius
    const neutronRadius = 12 * canvasWidthPercentage; // Scale neutron radius

    function generateStructuredPoints(numPoints, radius) {
        const points = [];
        const phiStep = Math.PI * (3 - Math.sqrt(5)); // Golden angle approximation
        const thetaStep = Math.sqrt(5) * 2 * Math.PI / numPoints; // Radial step
        
        for (let i = 0; i < numPoints; i++) {
            const theta = i * thetaStep;
            const phi = phiStep * i;
            
            const x = radius * Math.sin(phi) * Math.cos(theta);
            const y = radius * Math.sin(phi) * Math.sin(theta);
            const z = radius * Math.cos(phi);
            
            points.push({ x, y, z });
        }
        return points;
    }

    function project3DTo2D(x, y, z) {
        const scale = 200 / (200 + z);
        return { x: centerX + x * scale, y: centerY - y * scale };
    }

    function drawCircle(x, y, radius, color, filled = false) {
        context.beginPath();
        context.arc(x, y, radius, 0, 2 * Math.PI);
        context.fillStyle = filled ? color : 'transparent';
        context.strokeStyle = !filled ? color : 'transparent';
        context.lineWidth = filled ? 0 : 1;
        context.shadowBlur = 8;
        context.shadowColor = color;
        context.fill();
        context.stroke();
        context.shadowBlur = 0; // Reset shadow
    }

    function drawElectron(x, y) {
        drawCircle(x, y, electronRadius, 'black', true);
    }

    function drawNucleus() {
        const protons = generateStructuredPoints(numProtons, nucleusRadius);
        const neutrons = generateStructuredPoints(numNeutrons, nucleusRadius);

        protons.forEach(({ x, y, z }) => {
            const { x: x2D, y: y2D } = project3DTo2D(x, y, z);
            drawCircle(x2D, y2D, protonRadius, 'rgba(255, 0, 0, 0.8)', true);
        });

        neutrons.forEach(({ x, y, z }) => {
            const { x: x2D, y: y2D } = project3DTo2D(x, y, z);
            drawCircle(x2D, y2D, neutronRadius, 'rgba(0, 0, 255, 0.8)', true);
        });
    }

    function drawOrbits() {
        context.clearRect(0, 0, canvas.width, canvas.height);

        for (let i = 0; i < numOrbits; i++) {
            const radius = baseRadius + i * 100 * canvasWidthPercentage; // Adjust radius for scaling
            drawCircle(centerX, centerY, radius, 'rgba(0, 0, 255, 0.5)', false, ringWidth); // Semi-transparent blue for orbits

            for (let j = 0; j < numElectrons[i]; j++) {
                const angle = angles[i] + (j / numElectrons[i]) * 2 * Math.PI;
                const x = centerX + radius * Math.cos(angle);
                const y = centerY + radius * Math.sin(angle);
                drawElectron(x, y);
            }
            angles[i] += orbitSpeeds[i]; // Update angle for orbit speed
        }

        drawNucleus();

        requestAnimationFrame(drawOrbits); // Request next frame
    }

    function updateCanvas() {
        updateCanvasSize();
        drawOrbits(); // Start the animation loop
    }

    window.onload = function() {
        updateCanvasSize();
        updateCanvas(); // Initialize the canvas and start animation
    };

    window.addEventListener('resize', () => {
        updateCanvasSize();
    });
