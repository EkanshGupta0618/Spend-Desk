const ctx = document.getElementById("expenseChart").getContext("2d");
const expenseChart = new Chart(ctx, {
  type: "pie",
  data: {
    labels: categories, // Pass categories to the chart
    datasets: [
      {
        data: amounts, // Pass amounts to the chart
        backgroundColor: [
          "#FF6384",
          "#36A2EB",
          "#FFCE56",
          "#4BC0C0",
          "#9966FF",
        ],
      },
    ],
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    title: {
      display: true,
      text: "Expense Distribution by Category",
    },
  },
});
