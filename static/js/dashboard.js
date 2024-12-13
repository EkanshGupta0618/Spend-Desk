document.addEventListener("DOMContentLoaded", () => {
  const monthlyCtx = document.getElementById("monthlyExpensesChart").getContext("2d");
  const monthlyExpensesChart = new Chart(monthlyCtx, {
      type: "bar",
      data: {
          labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'], // Example labels for weeks
          datasets: [{
              label: 'Monthly Expenses',
              data: [1200, 1500, 800, 2000], // Example data for monthly expenses
              backgroundColor: 'rgba(75, 192, 192, 0.6)',
              borderColor: 'rgba(75, 192, 192, 1)',
              borderWidth: 1
          }]
      },
      options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
              y: {
                  beginAtZero: true
              }
          },
          title: {
              display: true,
              text: "Monthly Expenses Overview"
          }
      }
  });

  const expenseCtx = document.getElementById("expenseDistributionChart").getContext("2d");
  const expenseDistributionChart = new Chart(expenseCtx, {
      type: "pie",
      data: {
          labels: categories, // Pass categories to the chart
          datasets: [{
              label: 'Expense Distribution',
              data: amounts, // Pass amounts to the chart
              backgroundColor: [
                  'rgba(255, 99, 132, 0.6)',
                  'rgba(54, 162, 235, 0.6)',
                  'rgba(255, 206, 86, 0.6)',
                  'rgba(75, 192, 192, 0.6)',
                  'rgba(153, 102, 255, 0.6)'
              ],
              borderColor: [
                  'rgba(255, 99, 132, 1)',
                  'rgba(54, 162, 235, 1)',
                  'rgba(255, 206, 86, 1)',
                  'rgba(75, 192, 192, 1)',
                  'rgba(153, 102, 255, 1)'
              ],
              borderWidth: 1
          }]
      },
      options: {
          responsive: true,
          maintainAspectRatio: false,
          title: {
              display: true,
              text: "Expense Distribution Overview"
          }
      }
  });
});