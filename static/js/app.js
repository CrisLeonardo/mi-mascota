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
  const ICONOS_AVISO = { success: "bi-check-circle-fill", danger: "bi-x-octagon-fill", warning: "bi-exclamation-triangle-fill", info: "bi-info-circle-fill" };

  function aviso(mensaje, tipo = "success") {
    const cont = document.getElementById("toasts");
    const el = document.createElement("div");
    el.className = `toast toast-app toast-${tipo} border-0`;
    el.setAttribute("role", "alert");
    el.innerHTML = `<span class="t-icono"><i class="bi ${ICONOS_AVISO[tipo] || ICONOS_AVISO.info}"></i></span>
      <div class="toast-body"></div>
      <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Cerrar"></button>
      <span class="t-barra"></span>`;
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

  // ------------------------------------------------- barra de progreso superior
  const barra = document.getElementById("progreso");
  let tProgreso;
  const Progreso = {
    iniciar() {
      if (!barra) return;
      clearTimeout(tProgreso);
      barra.style.transition = "none";
      barra.style.width = "0";
      barra.classList.add("activo");
      void barra.offsetWidth; // fuerza el reflujo para reiniciar la transición
      barra.style.transition = "";
      barra.style.width = "70%";
    },
    terminar() {
      if (!barra) return;
      barra.style.width = "100%";
      tProgreso = setTimeout(() => { barra.classList.remove("activo"); barra.style.width = "0"; }, 350);
    },
  };

  window.App = { aviso, apiFetch, Progreso };

  // ------------------------------------------------------- búsqueda en vivo
  // <form data-busqueda data-destino="#contenedor"> ... </form>
  // Pide al servidor la misma URL con ?parcial=1 y reemplaza el contenido del destino.
  function iniciarBusqueda(form) {
    const destino = document.querySelector(form.dataset.destino);
    let temporizador;

    async function cargar(url) {
      destino.classList.add("cargando");
      Progreso.iniciar();
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
        Progreso.terminar();
      }
    }

    function urlDelFormulario() {
      const params = new URLSearchParams(new FormData(form));
      for (const [k, v] of [...params]) if (v === "") params.delete(k);
      params.set("parcial", "1");
      // form.action sin atributo devuelve la URL actual con su query string; se toma solo la ruta
      // para no acumular parámetros (?q=a?q=ab...) en cada búsqueda.
      const ruta = new URL(form.getAttribute("action") || location.pathname, location.href).pathname;
      return `${ruta}?${params}`;
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

  // ================================================================ efectos visuales
  const sinMovimiento = matchMedia("(prefers-reduced-motion: reduce)").matches;

  // ------------------------------------------------ modo claro / oscuro
  const raiz = document.documentElement;
  const botonTema = document.getElementById("btn-tema");
  if (botonTema) {
    botonTema.addEventListener("click", () => {
      const nuevo = raiz.getAttribute("data-bs-theme") === "dark" ? "light" : "dark";
      raiz.setAttribute("data-bs-theme", nuevo);
      try { localStorage.setItem("tema", nuevo); } catch (e) { /* modo privado: no se guarda */ }
      document.dispatchEvent(new Event("tema-cambiado")); // las gráficas se repintan
    });
  }

  // ------------------------------------------------ reloj de la barra superior
  const reloj = document.getElementById("reloj");
  if (reloj) {
    const pintar = () => { reloj.textContent = new Date().toLocaleTimeString("es-GT", { hour: "2-digit", minute: "2-digit" }); };
    pintar();
    setInterval(pintar, 15000);
  }

  // ------------------------------------------------ sombra de la barra al hacer scroll
  const topbar = document.getElementById("topbar");
  if (topbar) {
    const alScroll = () => topbar.classList.toggle("con-sombra", window.scrollY > 8);
    addEventListener("scroll", alScroll, { passive: true });
    alScroll();
  }

  // ------------------------------------------------ números que "suben" (data-contar)
  // El HTML ya trae el número final (sin JS se ve igual); aquí solo se anima de 0 hasta él.
  function contar(el) {
    const meta = parseFloat(el.dataset.contar);
    if (Number.isNaN(meta) || sinMovimiento) return;
    const prefijo = el.dataset.prefijo || "";
    const duracion = 1200;
    const inicio = performance.now();
    function paso(ahora) {
      const t = Math.min((ahora - inicio) / duracion, 1);
      const suave = 1 - Math.pow(1 - t, 4); // easeOutQuart
      el.textContent = prefijo + Math.round(meta * suave).toLocaleString("en-US");
      if (t < 1) requestAnimationFrame(paso);
    }
    el.textContent = prefijo + "0";
    requestAnimationFrame(paso);
  }
  document.querySelectorAll("[data-contar]").forEach(contar);

  // ------------------------------------------------ aparecer al hacer scroll (.reveal)
  const revelables = document.querySelectorAll(".reveal");
  if (revelables.length) {
    if ("IntersectionObserver" in window && !sinMovimiento) {
      const obs = new IntersectionObserver((entradas) => {
        entradas.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("visible"); obs.unobserve(e.target); } });
      }, { threshold: 0.12 });
      revelables.forEach((el) => obs.observe(el));
    } else {
      revelables.forEach((el) => el.classList.add("visible"));
    }
  }

  // ------------------------------------------------ onda al pulsar botones (ripple)
  document.addEventListener("click", (e) => {
    const b = e.target.closest(".btn");
    if (!b || sinMovimiento) return;
    const r = b.getBoundingClientRect();
    const d = Math.max(r.width, r.height);
    const onda = document.createElement("span");
    onda.className = "btn-ripple";
    onda.style.cssText = `width:${d}px;height:${d}px;left:${e.clientX - r.left - d / 2}px;top:${e.clientY - r.top - d / 2}px`;
    b.appendChild(onda);
    onda.addEventListener("animationend", () => onda.remove());
  });

  // ------------------------------------------------ progreso al cambiar de página
  document.addEventListener("click", (e) => {
    const a = e.target.closest("a[href]");
    if (!a || e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
    if (a.target === "_blank" || a.hasAttribute("download") || a.hasAttribute("data-bs-toggle")) return;
    const url = new URL(a.href, location.href);
    if (url.origin !== location.origin || url.protocol.startsWith("javascript") || url.pathname === location.pathname && url.hash) return;
    Progreso.iniciar();
  });
  addEventListener("pageshow", () => Progreso.terminar()); // al volver con "atrás" no se queda pegada

  // ------------------------------------------------ mostrar/ocultar contraseña
  document.querySelectorAll("[data-ver-password]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const campo = document.querySelector(btn.dataset.verPassword);
      const visible = campo.type === "text";
      campo.type = visible ? "password" : "text";
      btn.querySelector("i").className = visible ? "bi bi-eye" : "bi bi-eye-slash";
    });
  });
})();
