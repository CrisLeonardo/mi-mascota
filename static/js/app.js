/**
 * JavaScript común a todo el sistema.
 *  1. Utilidades: CSRF, avisos (toasts) y apiFetch() para llamar a la API REST.
 *  2. Búsqueda "en vivo": filtra tablas con fetch sin recargar la página.
 *  3. Validación de formularios en el cliente (Bootstrap).
 */
(function () {
  "use strict";

  // ---------------------------------------------------------------- utilidades
  const csrf = () => document.querySelector('meta[name="csrf-token"]').content;

  /** Muestra un aviso temporal (toast de Bootstrap). tipo: success | danger | warning | info */
  function aviso(mensaje, tipo = "success") {
    const cont = document.getElementById("toasts");
    const el = document.createElement("div");
    el.className = `toast align-items-center text-bg-${tipo} border-0`;
    el.setAttribute("role", "alert");
    el.innerHTML = `<div class="d-flex"><div class="toast-body"></div>
      <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Cerrar"></button></div>`;
    el.querySelector(".toast-body").textContent = mensaje; // textContent evita inyectar HTML (XSS)
    cont.appendChild(el);
    const toast = new bootstrap.Toast(el, { delay: 3500 });
    el.addEventListener("hidden.bs.toast", () => el.remove());
    toast.show();
  }

  /**
   * fetch() con lo necesario para hablar con la API de Django:
   *  - envía la cookie de sesión (credentials) y el token CSRF en métodos que modifican datos
   *  - si la respuesta no es 2xx, lanza un Error con el mensaje que devolvió el servidor
   */
  async function apiFetch(url, { method = "GET", body = null } = {}) {
    const opciones = {
      method,
      credentials: "same-origin",
      headers: { Accept: "application/json" },
    };
    if (method !== "GET") opciones.headers["X-CSRFToken"] = csrf();
    if (body !== null) {
      opciones.headers["Content-Type"] = "application/json";
      opciones.body = JSON.stringify(body);
    }
    const respuesta = await fetch(url, opciones);
    const datos = respuesta.status === 204 ? null : await respuesta.json().catch(() => null);
    if (!respuesta.ok) {
      const detalle = datos && (datos.detail || Object.values(datos).flat().join(" "));
      throw new Error(detalle || `Error ${respuesta.status}`);
    }
    return datos;
  }

  window.App = { aviso, apiFetch };

  // ------------------------------------------------------- búsqueda en vivo
  // <form data-busqueda data-destino="#contenedor"> ... </form>
  // Pide al servidor la misma URL con ?parcial=1 y reemplaza el contenido del destino.
  function iniciarBusqueda(form) {
    const destino = document.querySelector(form.dataset.destino);
    let temporizador;

    async function cargar(url) {
      destino.classList.add("cargando");
      try {
        const r = await fetch(url, { credentials: "same-origin", headers: { "X-Requested-With": "fetch" } });
        if (!r.ok) throw new Error(`Error ${r.status}`);
        destino.innerHTML = await r.text();
        // Mantiene la URL del navegador sin el parámetro técnico "parcial".
        const visible = new URL(url, location.href);
        visible.searchParams.delete("parcial");
        history.replaceState(null, "", visible.pathname + visible.search);
      } catch (e) {
        aviso("No se pudo actualizar la lista. Intenta de nuevo.", "danger");
      } finally {
        destino.classList.remove("cargando");
      }
    }

    function urlDelFormulario() {
      const params = new URLSearchParams(new FormData(form));
      for (const [k, v] of [...params]) if (v === "") params.delete(k);
      params.set("parcial", "1");
      return `${form.action || location.pathname}?${params}`;
    }

    form.addEventListener("input", (e) => {
      clearTimeout(temporizador);
      // Espera 300 ms tras la última tecla para no saturar al servidor.
      temporizador = setTimeout(() => cargar(urlDelFormulario()), e.target.type === "search" ? 300 : 0);
    });
    form.addEventListener("submit", (e) => { e.preventDefault(); cargar(urlDelFormulario()); });

    // La paginación vive dentro del destino: se intercepta con delegación de eventos.
    destino.addEventListener("click", (e) => {
      const enlace = e.target.closest("a.page-link");
      if (!enlace || !enlace.href) return;
      e.preventDefault();
      const url = new URL(enlace.href);
      url.searchParams.set("parcial", "1");
      cargar(url.toString());
    });

    // Para que otros scripts (p. ej. botones de estado) puedan refrescar la tabla actual.
    destino.recargar = () => cargar(urlDelFormulario());
  }
  document.querySelectorAll("form[data-busqueda]").forEach(iniciarBusqueda);

  // ------------------------------------------------ validación en el cliente
  document.querySelectorAll("form.needs-validation").forEach((form) => {
    form.addEventListener("submit", (e) => {
      if (!form.checkValidity()) {
        e.preventDefault();
        e.stopPropagation();
      }
      form.classList.add("was-validated");
    });
  });
})();
