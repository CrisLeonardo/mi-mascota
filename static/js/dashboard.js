/**
 * Gráficas del panel. Los datos se piden a la API REST (/api/estadisticas/) con fetch
 * y se dibujan con Chart.js.
 */
(async function () {
  "use strict";
  if (typeof Chart === "undefined") return; // sin conexión a la CDN el panel sigue funcionando sin gráficas

  let datos;
  try {
    datos = await App.apiFetch("/api/estadisticas/");
  } catch (error) {
    App.aviso("No se pudieron cargar las gráficas.", "warning");
    return;
  }

  const dias = ["dom", "lun", "mar", "mié", "jue", "vie", "sáb"];
  const etiquetaDia = (iso) => {
    const [a, m, d] = iso.split("-").map(Number);
    const fecha = new Date(a, m - 1, d);
    return `${dias[fecha.getDay()]} ${d}`;
  };

  new Chart(document.getElementById("grafica-dias"), {
    type: "bar",
    data: {
      labels: datos.citas_proximos_dias.map((x) => etiquetaDia(x.fecha)),
      datasets: [{ label: "Citas", data: datos.citas_proximos_dias.map((x) => x.total), backgroundColor: "#0f766e", borderRadius: 6 }],
    },
    options: { plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, ticks: { precision: 0 } } } },
  });

  const colores = { PENDIENTE: "#f59e0b", CONFIRMADA: "#0ea5e9", ATENDIDA: "#16a34a", CANCELADA: "#94a3b8", NO_ASISTIO: "#dc2626" };
  new Chart(document.getElementById("grafica-estados"), {
    type: "doughnut",
    data: {
      labels: datos.citas_por_estado.map((x) => x.estado),
      datasets: [{ data: datos.citas_por_estado.map((x) => x.total), backgroundColor: datos.citas_por_estado.map((x) => colores[x.clave]) }],
    },
    options: { plugins: { legend: { position: "bottom" } } },
  });
})();
