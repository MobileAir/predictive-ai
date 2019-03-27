
function renderChart(data, labels) {
    var ctx = document.getElementById("stockChart").getContext('2d');
    Chart.defaults.global.defaultFontColor = 'white';
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                defaultFontColor: 'rbg(250,250,250)',
                label: 'closing price',
                data: data,
                precision: 2,
                backgroundColor: ['rgba(250, 250, 250, 1.0)'],
            }]
        },
        options: {
            legend: {
                display: false,
                labels: {
                    // This more specific font property overrides the global property
                    defaultFontSize: 18,
                    defaultFontFamily: "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif"
                }
            }
        }
    });
}
