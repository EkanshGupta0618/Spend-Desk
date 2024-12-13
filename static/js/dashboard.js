// Get expense data from Django context
const expenseData = JSON.parse("{{ expense_data|escapejs }}");

// Create pie chart
const ctx = document.getElementById("expenseChart").getContext("2d");
new Chart(ctx, {
  type: "pie",
  data: {
    labels: Object.keys(expenseData),
    datasets: [
      {
        data: Object.values(expenseData),
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
    plugins: {
      legend: {
        position: "bottom",
      },
    },
  },
});

// Form validation
document
  .querySelector(".expense-form")
  .addEventListener("submit", function (e) {
    const amount = document.getElementById("amount").value;
    if (amount <= 0) {
      e.preventDefault();
      alert("Amount must be greater than 0");
    }
  });
