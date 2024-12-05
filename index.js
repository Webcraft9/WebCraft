


        // Array of searchable items
        const searchableItems = [
            "Dorilocos", "Salchilocura", "Choriloco", "Alitas BBQ", "Alitas Bufalo",
            "De la casa", "Salchipapa", "Perro caliente", "Especiales",
            "Inicio de sesión", "Registrarse", "Carrito de compras",
            "Puntos físicos", "Seguir mi pedido", "Mi perfil"
        ];

        const searchInput = document.getElementById('searchInput');
        const searchResults = document.getElementById('searchResults');

        searchInput.addEventListener('input', function() {
            const input = this.value.toLowerCase();
            const filteredItems = searchableItems.filter(item => 
                item.toLowerCase().includes(input)
            );

            displayResults(filteredItems);
        });

        function displayResults(results) {
            searchResults.innerHTML = '';
            if (results.length > 0 && searchInput.value !== '') {
                results.forEach(item => {
                    const div = document.createElement('div');
                    div.textContent = item;
                    div.className = 'search-item';
                    div.addEventListener('click', function() {
                        searchInput.value = item;
                        searchResults.innerHTML = '';
                    });
                    searchResults.appendChild(div);
                });
            }
        }

        // Close search results when clicking outside
        document.addEventListener('click', function(e) {
            if (e.target !== searchInput && e.target !== searchResults) {
                searchResults.innerHTML = '';
            }
        });

