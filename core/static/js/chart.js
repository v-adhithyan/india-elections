function generateDoughnutChart(elementId, data) {
  var ctx = document.getElementById(elementId);
  var myChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ["Red", "Green"],
      datasets: [{
        label: '# tweet sentiments',
        data: data,
        backgroundColor: [
          'rgba(255, 99, 132, 0.2)',
          'rgba(75, 192, 192, 0.2)',
        ],
        borderColor: [
          'rgba(255,99,132,1)',
          'rgba(75, 192, 192, 1)',
        ],
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: true
          }
        }]
      }
    }
  });
}
