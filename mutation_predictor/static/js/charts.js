window.onload = function () {
    const canvas = document.getElementById('scoreChart');
    if (!canvas) return;

    const score = parseFloat(canvas.dataset.score);
    const benign = 1 - score;

    new Chart(canvas, {
        type: 'bar',
        data: {
            labels: ['Benign', 'Pathogenic'],
            datasets: [{
                data: [benign, score],
                borderRadius: 14
            }]
        },
        options: {
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 1
                }
            }
        }
    });
};
