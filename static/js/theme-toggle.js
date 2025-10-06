document.addEventListener('DOMContentLoaded', () => {
    // 1. Selecciona todos los elementos necesarios para el cambio de tema.
    const themeToggleBtn = document.getElementById('theme-toggle');
    const body = document.body;
    const moonIcon = document.querySelector('.moon-icon');
    const sunIcon = document.querySelector('.sun-icon');
    
    // Selecciona los elementos principales que cambian de color.
    // **NOTA DE CORRECCIÓN:** Se actualizó la clase del header a '.header-foursweets' para que coincida con el HTML.
    const header = document.querySelector('.header-foursweets');
    const main = document.querySelector('.main');
    const footer = document.querySelector('.footer');
    const cards = document.querySelectorAll('.card');

    // 2. Define una función para aplicar o quitar el tema.
    // Esta función se encarga de añadir o quitar la clase 'dark-mode' de los elementos.
    const applyTheme = (theme) => {
        const isDarkMode = theme === 'dark';
        
        // Aplica o quita la clase 'dark-mode' al cuerpo de la página.
        body.classList.toggle('dark-mode', isDarkMode);
        
        // Se añade una verificación 'if' para asegurar que el elemento existe antes de intentar modificar su clase.
        // Esto previene errores en caso de que algún elemento no se encuentre en la página.
        if (header) {
            header.classList.toggle('dark-mode', isDarkMode);
        }
        if (main) {
            main.classList.toggle('dark-mode', isDarkMode);
        }
        if (footer) {
            footer.classList.toggle('dark-mode', isDarkMode);
        }
        
        // Itera sobre todas las tarjetas para aplicar el estilo a cada una.
        cards.forEach(card => card.classList.toggle('dark-mode', isDarkMode));
        
        // Muestra el ícono correcto (luna para modo oscuro, sol para modo claro).
        moonIcon.classList.toggle('hidden', isDarkMode);
        sunIcon.classList.toggle('hidden', !isDarkMode);
    };

    // 3. Obtén el tema guardado en el navegador o el tema preferido por el sistema operativo.
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const currentTheme = savedTheme || (prefersDark ? 'dark' : 'light');
    applyTheme(currentTheme);

    // 4. Agrega un evento de clic al botón de cambio de tema.
    // Cuando se hace clic, se determina el nuevo tema, se guarda en el almacenamiento local y se aplica.
    themeToggleBtn.addEventListener('click', () => {
        const newTheme = body.classList.contains('dark-mode') ? 'light' : 'dark';
        localStorage.setItem('theme', newTheme);
        applyTheme(newTheme);
    });
});