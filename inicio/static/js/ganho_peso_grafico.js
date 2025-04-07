document.addEventListener('DOMContentLoaded', function () {
  const semanas = Array.from({ length: 31 }, (_, i) => i + 10); // Semana 10 a 40
  const ganhoRecomendadoMin = {
      "Baixo peso": 9.7,
      "Eutrofia": 11.5,
      "Sobrepeso": 7.0,
      "Obesidade": 5.0
  };
  const ganhoRecomendadoMax = {
      "Baixo peso": 12.2,
      "Eutrofia": 16.0,
      "Sobrepeso": 11.5,
      "Obesidade": 9.0
  };

  const classificacao = "{{ resultado.classificacao }}";
  const ganhoUsuario = parseFloat("{{ resultado.ganho }}");
  const semanaAtual = parseInt("{{ resultado.semana }}");

  const ganhoMin = ganhoRecomendadoMin[classificacao];
  const ganhoMax = ganhoRecomendadoMax[classificacao];

  const ganhoMinPorSemana = semanas.map((_, i) => (ganhoMin / 30) * i);
  const ganhoMaxPorSemana = semanas.map((_, i) => (ganhoMax / 30) * i);
  const ganhoUsuarioPontos = semanas.map((_, i) => i === semanaAtual - 10 ? ganhoUsuario : null);

  const ctx = document.getElementById('graficoGanhoPeso').getContext('2d');
  new Chart(ctx, {
      type: 'line',
      data: {
          labels: semanas,
          datasets: [
              {
                  label: 'Ganho mínimo recomendado',
                  data: ganhoMinPorSemana,
                  borderColor: 'rgba(0, 123, 255, 0.6)',
                  fill: false,
                  tension: 0.3
              },
              {
                  label: 'Ganho máximo recomendado',
                  data: ganhoMaxPorSemana,
                  borderColor: 'rgba(40, 167, 69, 0.6)',
                  fill: '-1',
                  backgroundColor: 'rgba(0, 255, 0, 0.05)',
                  tension: 0.3
              },
              {
                  label: 'Ganho da gestante',
                  data: ganhoUsuarioPontos,
                  borderColor: 'red',
                  backgroundColor: 'red',
                  pointRadius: 6,
                  type: 'scatter',
                  showLine: false
              }
          ]
      },
      options: {
          plugins: {
              title: {
                  display: true,
                  text: 'Gráfico de Ganho de Peso x Semana de Gestação'
              }
          },
          scales: {
              x: {
                  title: {
                      display: true,
                      text: 'Semana de Gestação'
                  }
              },
              y: {
                  title: {
                      display: true,
                      text: 'Ganho de Peso (kg)'
                  },
                  beginAtZero: true
              }
          }
      }
  });
});