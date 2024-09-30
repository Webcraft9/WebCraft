document.getElementById('actualizarBtn').addEventListener('click', function() {
    // Ejemplo de actualización de información, esto se puede conectar a una API o base de datos
    document.getElementById('horaSalida').innerText = '15:45'; // Actualizar hora de salida
    document.getElementById('horaEntrega').innerText = '16:15'; // Actualizar hora de entrega
    document.getElementById('repartidor').innerText = 'María López'; // Actualizar repartidor
});
