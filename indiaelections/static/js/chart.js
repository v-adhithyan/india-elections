function generateDoughnutChart(elementId, data) {
  var ctx = document.getElementById(elementId);
  var myChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ["Positive", "Negative", 'Neutral'],
      datasets: [{
        label: '# tweet sentiments',
        data: data,
        backgroundColor: [
          'rgba(75, 192, 192, 0.2)',
          'rgba(255, 99, 132, 0.2)',
          'rgba(241, 90, 34, 0.2)'
        ],
        borderColor: [
          'rgba(75, 192, 192, 1)',
          'rgba(255,99,132,1)',
          'rgba(241, 90, 34, 1)'
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

function generateBarChart(elementId, data) {
  var ctx = document.getElementById(elementId);
  var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ["Female", "Male"],
      datasets: [{
        label: '# tweet counts by gender',
        data: data,
        backgroundColor: [
          'rgba(255, 192, 203, 0.2)',
          'rgba(0, 0, 255, 0.2)'
        ],
        borderColor: [
          'rgba(255, 192, 203, 1)',
          'rgba(0, 0, 255, 1)',
        ],
        borderWidth: 1
      }]
    },

  });
}

function generateTimeseriesData(elementId, data, label) {
  var s1 = {
    label: 'label',
    borderColor: 'blue',
    data: data
  };
  var ctx = document.getElementById(elementId);
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      datasets: [s1]
    },
    options: {
      scales: {
        xAxes: [{
          type: 'time'
        }]
      }
    }
  })
}

function plotTimeseriesData(elementId, data1, data2, label1, label2) {
  var s1 = {
    label: label1,
    borderColor: 'blue',
    data: data1
  };
  var s2 = {
    label: label2,
    borderColor: 'red',
    data: data2
  };
  var ctx = document.getElementById(elementId);
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      datasets: [s1, s2]
    },
    options: {
      scales: {
        xAxes: [{
          type: 'time'
        }]
      }
    }
  })
}