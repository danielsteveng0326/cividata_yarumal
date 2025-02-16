function updateClock() {
    const now = new Date();
    
    // Formatear la hora
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const timeString = `${hours}:${minutes}`;
    
    // Formatear la fecha
    const options = { 
        weekday: 'short', 
        day: 'numeric', 
        month: 'short'
    };
    const dateString = now.toLocaleDateString('es-ES', options);
    
    // Actualizar los elementos
    document.getElementById('clock-time').textContent = timeString;
    document.getElementById('clock-date').textContent = dateString.toUpperCase();
}

// Iniciar el reloj cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    updateClock(); // Primera actualización
    setInterval(updateClock, 60000); // Actualizar cada minuto
});