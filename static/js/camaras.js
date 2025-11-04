let currentView = 'both'; 

function showSingleCamera(cameraId) {
    const container = document.getElementById('container');
    const camera1 = document.getElementById('camera1');
    const camera2 = document.getElementById('camera2');
    const toggleButton = document.getElementById('toggleView');

    // Cambiar a vista con una sola cámara
    container.classList.add('single-view');
    
    if (cameraId === 'camera1') {
        camera1.classList.remove('hidden');
        camera2.classList.add('hidden');
        currentView = 'camera1';
    } else {
        camera1.classList.add('hidden');
        camera2.classList.remove('hidden');
        currentView = 'camera2';
    }

    // Mostrar botón para volver a vista dual
    toggleButton.classList.add('active');
}

function showBothCameras() {
    const container = document.getElementById('container');
    const camera1 = document.getElementById('camera1');
    const camera2 = document.getElementById('camera2');
    const toggleButton = document.getElementById('toggleView');

    // Volver a vista dual
    container.classList.remove('single-view');
    camera1.classList.remove('hidden');
    camera2.classList.remove('hidden');
    
    // Ocultar botón
    toggleButton.classList.remove('active');
    
    currentView = 'both';
}

// Actualizar tiempo
function updateTimestamps() {
    const now = new Date();
    const timeString = now.toLocaleTimeString('es-CO', { hour12: false });
    document.getElementById('time1').textContent = timeString;
    document.getElementById('time2').textContent = timeString;
}

// Actualizar contadores de personas
async function updatePeopleCounts() {
    try {
        const response = await fetch('/people_count');
        const data = await response.json();
        document.getElementById('count1').textContent = data.camera1 || 0;
        document.getElementById('count2').textContent = data.camera2 || 0;
    } catch (error) {
        console.error('Error al obtener conteo:', error);
    }
}

// Inicializar cuando la página carga
setInterval(updateTimestamps, 1000);
setInterval(updatePeopleCounts, 500);
updateTimestamps();
updatePeopleCounts();