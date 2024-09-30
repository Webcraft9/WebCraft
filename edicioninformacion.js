
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('edit-form');

    form.addEventListener('submit', function (event) {
        event.preventDefault(); // Evita el envío del formulario por defecto

        // Aquí podrías hacer una llamada al servidor para guardar los cambios
        alert('Cambios guardados exitosamente.');

        // Para demostrar, vamos a limpiar el formulario después de la simulación
        form.reset();
    });
});