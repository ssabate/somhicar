/*This file contains utility functions for the application*/
function aplicarTamanyText() {

    // Selecciona todos los elementos con id que comienza con "segon";
    let elementos= document.querySelectorAll('[id^="titol"]');
    for (const elemento of elementos) {
        // Limpia clases previas de tamaño
        elemento.classList.remove('text-2xl', 'text-4xl');
        // Detecta móvil y aplica clase correspondiente
        if (/Mobi|Android/i.test(navigator.userAgent)) {
            elemento.classList.add('text-6xl'); // Tamaño para móvil
        } else {
            elemento.classList.add('text-4xl'); // Tamaño para PC
        }
    }

    // Selecciona todos los elementos con id que comienza con "segon";
    elementos= document.querySelectorAll('[id^="subtitol"]');
    for (const elemento of elementos) {
        // Limpia clases previas de tamaño
        elemento.classList.remove('text-2xl', 'text-4xl');
        // Detecta móvil y aplica clase correspondiente
        if (/Mobi|Android/i.test(navigator.userAgent)) {
            elemento.classList.add('text-5xl'); // Tamaño para móvil
        } else {
            elemento.classList.add('text-3xl'); // Tamaño para PC
        }
    }

    // Selecciona todos los elementos con id que comienza con "segon";
    elementos= document.querySelectorAll('[id^="fila"]');
    for (const elemento of elementos) {
        // Limpia clases previas de tamaño
        elemento.classList.remove('text-2xl', 'text-4xl');
        // Detecta móvil y aplica clase correspondiente
        if (/Mobi|Android/i.test(navigator.userAgent)) {
            elemento.classList.add('text-4xl'); // Tamaño para móvil
        } else {
            elemento.classList.add('text-2xl'); // Tamaño para PC
        }
    }

     // Selecciona todos los elementos con id que comienza con "segon";
    elementos= document.querySelectorAll('[id^="subfila"]');
    for (const elemento of elementos) {
        // Limpia clases previas de tamaño
        elemento.classList.remove('text-2xl', 'text-4xl');
        // Detecta móvil y aplica clase correspondiente
        if (/Mobi|Android/i.test(navigator.userAgent)) {
            elemento.classList.add('text-3xl'); // Tamaño para móvil
        } else {
            elemento.classList.add('text-xl'); // Tamaño para PC
        }
    }

    // Selecciona todos los elementos con id que comienza con "segon";
    elementos= document.querySelectorAll('[id^="boto"]');
    for (const elemento of elementos) {
        // Limpia clases previas de tamaño
        elemento.classList.remove('text-2xl', 'text-4xl');
        // Detecta móvil y aplica clase correspondiente
        if (/Mobi|Android/i.test(navigator.userAgent)) {
            elemento.classList.add('text-2xl'); // Tamaño para móvil
        } else {
            elemento.classList.add('text-lg'); // Tamaño para PC
        }
    }

    // Selecciona todos los elementos con id que comienza con "segon";
    elementos= document.querySelectorAll('[id^="boto_gran_movil"]');
    for (const elemento of elementos) {
        // Limpia clases previas de tamaño
        elemento.classList.remove('text-2xl', 'text-4xl');
        // Detecta móvil y aplica clase correspondiente
        if (/Mobi|Android/i.test(navigator.userAgent)) {
            elemento.classList.add('text-4xl'); // Tamaño para móvil
        } else {
            elemento.classList.add('text-lg'); // Tamaño para PC
        }
    }
}

aplicarTamanyText();
window.addEventListener('resize', aplicarTamanyText);
