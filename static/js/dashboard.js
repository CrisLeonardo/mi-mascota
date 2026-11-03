/**
 * Gráficas del panel. Los datos se piden a la API REST (/api/estadisticas/) con fetch
 * y se dibujan con Chart.js (barras con degradado y dona con el total al centro, ambas animadas).
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

  // Colores que se adaptan al modo claro/oscuro
  const oscuro = () => document.documentElement.getAttribute("data-bs-theme") === "dark";
  const estilo = getComputedStyle(document.documentElement);
  const colorTexto = () => (oscuro() ? "#8ba3ab" : "#62767d");
  const colorRejilla = () => (oscuro() ? "rgba(255,255,255,.06)" : "rgba(15,55,60,.07)");
  Chart.defaults.font.family = '"Plus Jakarta Sans", system-ui, sans-serif';
  Chart.defaults.font.weight = 600;

  const dias = ["dom", "lun", "mar", "mié", "jue", "vie", "sáb"];
  const etiquetaDia = (iso) => {
    const [a, m, d] = iso.split("-").map(Number);
    const fecha = new Date(a, m - 1, d);
    return `${dias[fecha.getDay()]} ${d}`;
  };

  // ---------------------------------------------------------- barras (7 días)
  const lienzoDias = document.getElementById("grafica-dias");
  const graficaDias = new Chart(lienzoDias, {
    type: "bar",
    data: {
      labels: datos.citas_proximos_dias.map((x) => etiquetaDia(x.fecha)),
      datasets: [{
        label: "Citas",
        data: datos.citas_proximos_dias.map((x) => x.total),
        // degradado vertical: se calcula con el tamaño real del área de dibujo
        backgroundColor: (ctx) => {
          const { chartArea, ctx: c } = ctx.chart;
          if (!chartArea) return "#14b8a6";
          const g = c.createLinearGradient(0, chartArea.bottom, 0, chartArea.top);
          g.addColorStop(0, "#0f766e");
          g.addColorStop(1, "#2dd4bf");
          return g;
        },
        hoverBackgroundColor: "#f59e0b",
        borderRadius: 10,
        borderSkipped: false,
        maxBarThickness: 46,
      }],
    },
    options: {
      maintainAspectRatio: false,
      animation: { duration: 1100, easing: "easeOutQuart", delay: (ctx) => ctx.dataIndex * 90 },
      plugins: {
        legend: { display: false },
        tooltip: { backgroundColor: "#0d2a33", padding: 12, cornerRadius: 10, displayColors: false, titleFont: { weight: 700 } },
      },
      scales: {
        y: { beginAtZero: true, ticks: { precision: 0, color: colorTexto() }, grid: { color: colorRejilla() }, border: { display: false } },
        x: { ticks: { color: colorTexto() }, grid: { display: false }, border: { display: false } },
      },
    },
  });

  // ---------------------------------------------------------- dona (por estado)
  const colores = { PENDIENTE: "#f59e0b", CONFIRMADA: "#0ea5e9", ATENDIDA: "#16a34a", CANCELADA: "#94a3b8", NO_ASISTIO: "#dc2626" };
  const totalEstados = datos.citas_por_estado.reduce((s, x) => s + x.total, 0);

  // Plugin propio: escribe el total de citas en el centro de la dona.
  const textoCentro = {
    id: "textoCentro",
    afterDraw(chart) {
      const { ctx, chartArea: a } = chart;
      const x = (a.left + a.right) / 2, y = (a.top + a.bottom) / 2;
      ctx.save();
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillStyle = oscuro() ? "#e5f0f2" : "#14262c";
      ctx.font = '800 30px "Plus Jakarta Sans", sans-serif';
      ctx.fillText(totalEstados, x, y - 8);
      ctx.fillStyle = colorTexto();
      ctx.font = '600 12px "Plus Jakarta Sans", sans-serif';
      ctx.fillText("citas en total", x, y + 17);
      ctx.restore();
    },
  };

  const graficaEstados = new Chart(document.getElementById("grafica-estados"), {
    type: "doughnut",
    data: {
      labels: datos.citas_por_estado.map((x) => x.estado),
      datasets: [{
        data: datos.citas_por_estado.map((x) => x.total),
        backgroundColor: datos.citas_por_estado.map((x) => colores[x.clave]),
        borderWidth: 4,
        borderColor: estilo.getPropertyValue("--superficie").trim() || "#fff",
        hoverOffset: 12,
        borderRadius: 8,
        spacing: 2,
      }],
    },
    options: {
      maintainAspectRatio: false,
      cutout: "70%",
      animation: { animateRotate: true, animateScale: true, duration: 1300, easing: "easeOutCubic" },
      plugins: {
        legend: { position: "bottom", labels: { usePointStyle: true, pointStyle: "circle", boxWidth: 8, padding: 14, color: colorTexto() } },
        tooltip: { backgroundColor: "#0d2a33", padding: 12, cornerRadius: 10 },
      },
    },
    plugins: [textoCentro],
  });

  // Al cambiar entre modo claro y oscuro se repintan con los colores nuevos.
  document.addEventListener("tema-cambiado", () => {
    graficaDias.options.scales.y.ticks.color = colorTexto();
    graficaDias.options.scales.x.ticks.color = colorTexto();
    graficaDias.options.scales.y.grid.color = colorRejilla();
    graficaEstados.options.plugins.legend.labels.color = colorTexto();
    graficaEstados.data.datasets[0].borderColor = getComputedStyle(document.documentElement).getPropertyValue("--superficie").trim();
    graficaDias.update("none");
    graficaEstados.update("none");
  });
})();
