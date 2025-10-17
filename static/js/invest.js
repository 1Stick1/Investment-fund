
const atx = document.getElementById('investmentChart').getContext('2d');

const investmentChart = new Chart(atx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [
            {
                label: 'S&P 500 (USA)',
                data: [],
                borderColor: '#d9a441',
                backgroundColor: 'rgba(217,164,65,0.15)',
                borderWidth: 3,
                tension: 0.4,
                fill: true
            },
            {
                label: 'Bund (Europa)',
                data: [],
                borderColor: '#3b82f6',
                backgroundColor: 'rgba(59,130,246,0.15)',
                borderWidth: 3,
                tension: 0.4,
                fill: true
            }
        ]
    },
    options: {
        responsive: true,
        animation: {
            duration: 1000,
            easing: 'easeOutCubic'
        },
        plugins: {
            legend: {
                labels: { color: '#333', font: { size: 14 } }
            }
        },
        scales: {
            x: {
                ticks: { color: '#555', font: { size: 12 } },
                grid: { color: '#eee' }
            },
            y: {
                ticks: { color: '#555', font: { size: 12 } },
                grid: { color: '#eee' },
                beginAtZero: false
            }
        }
    }
});

let prevUSA = null;
let prevEU = null;

async function updateChart() {
    const response = await fetch("/data");
    const newData = await response.json();

    investmentChart.data.labels = newData.map(p => p.time);
    investmentChart.data.datasets[0].data = newData.map(p => p.usa);
    investmentChart.data.datasets[1].data = newData.map(p => p.eu);
    investmentChart.update();

    const lastPoint = newData[newData.length - 1];
    const usaVal = document.getElementById("usaValue");
    const euVal = document.getElementById("euValue");

    usaVal.textContent = lastPoint.usa.toFixed(2);
    euVal.textContent = lastPoint.eu.toFixed(2);

    if (prevUSA !== null) {
        usaVal.className = "value " + (lastPoint.usa > prevUSA ? "up" : "down");
    }
    if (prevEU !== null) {
        euVal.className = "value " + (lastPoint.eu > prevEU ? "up" : "down");
    }

    prevUSA = lastPoint.usa;
    prevEU = lastPoint.eu;
}

updateChart();
setInterval(updateChart, 10000);



 const ctx = document.getElementById('fundWalletChart').getContext('2d');
                    const fundWalletChart = new Chart(ctx, {
                    type: 'pie', 
                    data: {
                        labels: ['Akcje S&P 500 (USA)', 'Obligacje Bund (EU)'],
                        datasets: [{
                            data: [60, 40],
                            backgroundColor: ['#f0c060', '#9f7030'],
                            borderWidth: 0,
                            borderColor: 'transparent' 
                        }]
                    },
                    options: {
                        responsive: false,
                        plugins: {
                            legend: {
                                display: false
                            }
                        }
                    }
                    });


