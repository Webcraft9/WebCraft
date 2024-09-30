document.addEventListener('DOMContentLoaded', () => {
    const logoutButton = document.getElementById('logout-button');
    const cancelButton = document.getElementById('cancel-button');

    logoutButton.addEventListener('click', () => {
        if (confirm('¿Estás seguro de que deseas cerrar sesión?')) {
            // Redirige a la página de cierre de sesión o realiza una acción específica
            window.location.href = 'logout.php'; // Cambia esta URL a la ruta correcta para el cierre de sesión
        }
    });

    cancelButton.addEventListener('click', () => {
        // Redirige a la página principal o a la página que estaba antes
        window.location.href = 'yo.html'; // Cambia esta URL a la ruta correcta
    });
});
