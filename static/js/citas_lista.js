/**
 * Lista de citas: botones de cambio de estado sin recargar la página.
 * Cada botón trae data-url (endpoint de la API) y data-estado (nuevo estado).
 */
(function () {
  "use strict";
  const contenedor = document.getElementById("resultados");

  contenedor.addEventListener("click", async (e) => {
    const boton = e.target.closest("button[data-estado]");
    if (!boton) return;

    if (boton.dataset.confirmar && !confirm(boton.dataset.confirmar)) return;

    boton.disabled = true;
    try {
      const cita = await App.apiFetch(boton.dataset.url, { method: "POST", body: { estado: boton.dataset.estado } });
      App.aviso(`Cita de ${cita.mascota_nombre}: ${cita.estado_display.toLowerCase()}.`);
      contenedor.recargar(); // vuelve a pedir la tabla con los mismos filtros
    } catch (error) {
      App.aviso(error.message, "danger");
      boton.disabled = false;
    }
  });
})();
