
    const ctxEventCategories = document.getElementById('eventCategoriesChart').getContext('2d');
    const eventCategoriesChart = new Chart(ctxEventCategories, {
        type: 'bar',
        data: {
            labels: JSON.parse(document.getElementById('eventCategoriesLabels').textContent),
            datasets: [{
                label: 'Number of Events',
                data: JSON.parse(document.getElementById('eventCategoriesData').textContent),
                backgroundColor: 'rgba(90, 45, 159, 0.7)',
                borderColor: 'rgba(90, 45, 159, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    precision: 0
                }
            }
        }
    });

    const ctxCustomerGrowth = document.getElementById('customerGrowthChart').getContext('2d');
    const customerGrowthChart = new Chart(ctxCustomerGrowth, {
        type: 'line',
        data: {
            labels: JSON.parse(document.getElementById('customerGrowthLabels').textContent),
            datasets: [{
                label: 'Customer Growth',
                data: JSON.parse(document.getElementById('customerGrowthData').textContent),
                fill: false,
                borderColor: 'rgba(90, 45, 159, 1)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    precision: 0
                }
            }
        }
    });
