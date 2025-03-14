// Archivo: /static/assets/customJS/buscador-empleados.js

document.addEventListener("DOMContentLoaded", function() {
    // Verificar si el elemento de búsqueda existe en la página
    const searchInput = document.getElementById('search');
    if (searchInput) {
        console.log("Buscador inicializado correctamente");
        // Agregar evento input para detectar cambios en tiempo real
        searchInput.addEventListener('input', function() {
            console.log("Texto de búsqueda:", this.value);
            buscadorTable('tbl_empleados');
        });
    } else {
        console.error("No se encontró el elemento de búsqueda");
    }
});

function buscadorTable(tableId) {
    const searchInput = document.getElementById('search');
    const table = document.getElementById(tableId);
    
    if (!searchInput || !table) {
        console.error("No se encontró el input de búsqueda o la tabla");
        return;
    }
    
    const searchTerm = searchInput.value.toLowerCase();
    console.log("Realizando búsqueda con término:", searchTerm);
    
    // Si el término de búsqueda tiene al menos 2 caracteres, realizar búsqueda en el servidor
    if (searchTerm.length >= 2) {
        // Mostrar indicador de carga
        const tbody = table.getElementsByTagName('tbody')[0];
        tbody.innerHTML = '<tr><td colspan="7" class="text-center"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Cargando...</span></div></td></tr>';
        
        // Construir la URL completa para asegurarnos que es correcta
        const url = window.location.origin + '/buscar-empleado-ajax';
        console.log("URL de búsqueda AJAX:", url);

        
        // Llamada AJAX al servidor
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-Requested-With': 'XMLHttpRequest' // Agregar para identificar como AJAX
            },
            body: 'search=' + encodeURIComponent(searchTerm)
        })
        .then(response => {
            console.log("Respuesta del servidor:", response.status);
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Datos recibidos:", data);
            actualizarTabla(data, tableId);
        })
        .catch(error => {
            console.error('Error en la búsqueda:', error);
            const tbody = table.getElementsByTagName('tbody')[0];
            tbody.innerHTML = `<tr><td colspan="7" class="text-center text-danger">Error al realizar la búsqueda: ${error.message}</td></tr>`;
        });
    } else if (searchTerm.length === 0) {
        console.log("Campo vacío, cargando todos los empleados");
    
        const url = window.location.origin + '/obtener-todos-empleados';
    
        fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status}`);
            }
            return response.text();  // Obtener el texto sin procesar para ver si es JSON o HTML
        })
        .then(text => {
            console.log("Respuesta recibida:", text); // Ver el contenido real
            try {
                const data = JSON.parse(text);  // Intentar parsear a JSON
                actualizarTabla(data, tableId);
            } catch (error) {
                console.error("Error al parsear JSON. El servidor devolvió HTML en lugar de JSON.");
            }
        })
        .catch(error => {
            console.error('Error al cargar empleados:', error);
            const tbody = table.getElementsByTagName('tbody')[0];
            tbody.innerHTML = `<tr><td colspan="7" class="text-center text-danger">Error al cargar los empleados: ${error.message}</td></tr>`;
        });
    }
    

function actualizarTabla(empleados, tableId) {
    console.log("Actualizando tabla con", empleados.length, "empleados");
    const tbody = document.getElementById(tableId).getElementsByTagName('tbody')[0];
    tbody.innerHTML = '';
    
    if (empleados.length === 0) {
        const row = document.createElement('tr');
        row.innerHTML = '<td colspan="7" class="text-center">No hay empleados que coincidan con la búsqueda.</td>';
        tbody.appendChild(row);
        return;
    }
    
    empleados.forEach(empleado => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${empleado.CC || ''}</td>
            <td>${empleado.NOM || ''}</td>
            <td>${empleado.CAR || ''}</td>
            <td>${empleado.CENTRO || ''}</td>
            <td>
                <div class="btn-group gap-1" role="group">
                    <a href="/detalles-empleado/${empleado.CC}" class="btn btn-info btn-lg" title="Ver detalles">
                        <i class="bi bi-eye"></i> 
                    </a>
                </div>
            </td>
            <td class="d-flex justify-content-center">
                <a href="/editar-empleado/${empleado.CC}" class="btn btn-success btn-lg" title="Actualizar Registro">
                    <i class="bi bi-arrow-clockwise"></i> 
                </a>
            </td>
            <td>  
                <a href="/eliminar-empleado/${empleado.CC}" class="btn btn-danger btn-lg" title="Eliminar empleado" 
                    onclick="return confirm('¿Estás seguro de eliminar al empleado ${empleado.NOM}?');">
                    <i class="bi bi-trash3" id="btn-delete"></i>
                </a>
            </td>
        `;
        tbody.appendChild(row);
    });
}// Archivo: /static/assets/customJS/buscador-empleados.js

document.addEventListener("DOMContentLoaded", function() {
    // Verificar si el elemento de búsqueda existe en la página
    const searchInput = document.getElementById('search');
    if (searchInput) {
        console.log("Buscador inicializado correctamente");
        // Agregar evento input para detectar cambios en tiempo real
        searchInput.addEventListener('input', debounce(function() {
            console.log("Texto de búsqueda:", this.value);
            buscadorTable('tbl_empleados');
        }, 500));
    } else {
        console.error("No se encontró el elemento de búsqueda");
    }
});

function buscadorTable(tableId) {
    const searchInput = document.getElementById('search');
    const table = document.getElementById(tableId);
    
    if (!searchInput || !table) {
        console.error("No se encontró el input de búsqueda o la tabla");
        return;
    }
    
    const searchTerm = searchInput.value.trim().toLowerCase();
    console.log("Realizando búsqueda con término:", searchTerm);
    
    // Si el término de búsqueda tiene al menos 2 caracteres, realizar búsqueda en el servidor
    if (searchTerm.length >= 2) {
        // Mostrar indicador de carga
        const tbody = table.getElementsByTagName('tbody')[0];
        tbody.innerHTML = '<tr><td colspan="7" class="text-center"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Cargando...</span></div></td></tr>';
        
        // Construir la URL completa para asegurarnos que es correcta
        const url = window.location.origin + '/buscar-empleado-ajax';
        console.log("URL de búsqueda AJAX:", url);

        // Llamada AJAX al servidor
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-Requested-With': 'XMLHttpRequest' // Agregar para identificar como AJAX
            },
            body: 'search=' + encodeURIComponent(searchTerm)
        })
        .then(response => {
            console.log("Respuesta del servidor:", response.status);
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Datos recibidos:", data);
            actualizarTabla(data, tableId);
        })
        .catch(error => {
            console.error('Error en la búsqueda:', error);
            const tbody = table.getElementsByTagName('tbody')[0];
            tbody.innerHTML = `<tr><td colspan="7" class="text-center text-danger">Error al realizar la búsqueda: ${error.message}</td></tr>`;
        });
    } else if (searchTerm.length === 0) {
        console.log("Campo vacío, cargando todos los empleados");
    
        const url = window.location.origin + '/obtener-todos-empleados';
    
        fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status}`);
            }
            return response.text();  // Obtener el texto sin procesar para ver si es JSON o HTML
        })
        .then(text => {
            console.log("Respuesta recibida:", text); // Ver el contenido real
            try {
                const data = JSON.parse(text);  // Intentar parsear a JSON
                actualizarTabla(data, tableId);
            } catch (error) {
                console.error("Error al parsear JSON. El servidor devolvió HTML en lugar de JSON.");
            }
        })
        .catch(error => {
            console.error('Error al cargar empleados:', error);
            const tbody = table.getElementsByTagName('tbody')[0];
            tbody.innerHTML = `<tr><td colspan="7" class="text-center text-danger">Error al cargar los empleados: ${error.message}</td></tr>`;
        });
    }
}

function actualizarTabla(empleados, tableId) {
    console.log("Actualizando tabla con", empleados.length, "empleados");
    const tbody = document.getElementById(tableId).getElementsByTagName('tbody')[0];
    tbody.innerHTML = '';
    
    if (empleados.length === 0) {
        const row = document.createElement('tr');
        row.innerHTML = '<td colspan="7" class="text-center">No hay empleados que coincidan con la búsqueda.</td>';
        tbody.appendChild(row);
        return;
    }
    
    empleados.forEach(empleado => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${empleado.CC || ''}</td>
            <td>${empleado.NOM || ''}</td>
            <td>${empleado.CAR || ''}</td>
            <td>${empleado.CENTRO || ''}</td>
            <td>
                <div class="btn-group gap-1" role="group">
                    <a href="/detalles-empleado/${empleado.CC}" class="btn btn-info btn-lg" title="Ver detalles">
                        <i class="bi bi-eye"></i> 
                    </a>
                </div>
            </td>
            <td class="d-flex justify-content-center">
                <a href="/editar-empleado/${empleado.CC}" class="btn btn-success btn-lg" title="Actualizar Registro">
                    <i class="bi bi-arrow-clockwise"></i> 
                </a>
            </td>
            <td>  
                <a href="/eliminar-empleado/${empleado.CC}" class="btn btn-danger btn-lg" title="Eliminar empleado" 
                    onclick="return confirm('¿Estás seguro de eliminar al empleado ${empleado.NOM}?');">
                    <i class="bi bi-trash3" id="btn-delete"></i>
                </a>
            </td>
        `;
        tbody.appendChild(row);
    });
}

function debounce(func, wait) {
    let timeout;
    return function() {
        const context = this;
        const args = arguments;
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            func.apply(context, args);
        }, wait);
    };
}}