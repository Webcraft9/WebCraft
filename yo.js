
    document.addEventListener('DOMContentLoaded', function () {
        // Toggle for orders
        const toggleOrdersBtn = document.getElementById('toggle-orders');
        const ordersTable = document.getElementById('orders-table');

        toggleOrdersBtn.addEventListener('click', function () {
            ordersTable.classList.toggle('hidden');
            toggleOrdersBtn.textContent = ordersTable.classList.contains('hidden') ? 'Mostrar Pedidos' : 'Ocultar Pedidos';
        });

        // Toggle for pending orders
        const togglePendingBtn = document.getElementById('toggle-pending');
        const pendingOrdersTable = document.getElementById('pending-orders-table');

        togglePendingBtn.addEventListener('click', function () {
            pendingOrdersTable.classList.toggle('hidden');
            togglePendingBtn.textContent = pendingOrdersTable.classList.contains('hidden') ? 'Mostrar Pedidos Pendientes' : 'Ocultar Pedidos Pendientes';
        });
    });

