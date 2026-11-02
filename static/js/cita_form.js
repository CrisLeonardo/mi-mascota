/**
 * Formulario de cita: carga con fetch las horas libres según servicio, veterinario y fecha.
 * El servidor vuelve a validar al guardar; esto solo mejora la experiencia.
 */
(function () {
  "use strict";
  const servicio = document.getElementById("id_servicio");
  const veterinario = document.getElementById("id_veterinario");
  const fecha = document.getElementById("id_fecha");
  const hora = document.getElementById("id_hora");
  if (!(servicio && veterinario && fecha && hora)) return;

  let ultimaPeticion = 0;

  function mensaje(texto) {
    hora.innerHTML = "";
    hora.add(new Option(texto, ""));
  }

  async function cargarHoras() {
    if (!(servicio.value && veterinario.value && fecha.value)) {
      mensaje("Elige fecha, veterinario y servicio");
      return;
    }
    const numero = ++ultimaPeticion; // evita que una respuesta lenta pise a una más reciente
    mensaje("Buscando horarios…");
    const params = new URLSearchParams({
      servicio: servicio.value,
      veterinario: veterinario.value,
      fecha: fecha.value,
    });
    if (hora.dataset.cita) params.set("cita", hora.dataset.cita); // al editar, su propio horario cuenta como libre
    try {
      const datos = await App.apiFetch(`/api/horarios-disponibles/?${params}`);
      if (numero !== ultimaPeticion) return;
      const inicial = hora.dataset.inicial;
      const horas = datos.horarios.slice();
      if (inicial && !horas.includes(inicial)) horas.push(inicial), horas.sort();
      hora.innerHTML = "";
      if (!horas.length) {
        mensaje("Sin horarios libres ese día");
        return;
      }
      hora.add(new Option("Selecciona una hora", ""));
      horas.forEach((h) => hora.add(new Option(h, h, false, h === inicial)));
    } catch (error) {
      if (numero === ultimaPeticion) mensaje("No se pudieron cargar los horarios");
      App.aviso(error.message, "danger");
    }
  }

  [servicio, veterinario, fecha].forEach((el) => el.addEventListener("change", () => {
    hora.dataset.inicial = ""; // si el usuario cambia algo, deja de conservarse la hora anterior
    cargarHoras();
  }));
  cargarHoras();
})();
