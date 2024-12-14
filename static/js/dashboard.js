function showEditForm(id, description, category, amount) {
  document.getElementById("edit-expense-id").value = id;
  document.getElementById("edit-description").value = description;
  document.getElementById("edit-amount").value = amount;

  // Set the selected category in the dropdown
  var categorySelect = document.getElementById("edit-category");
  categorySelect.value = category; // Set the selected value

  document.getElementById("edit-form").style.display = "block";
}

function hideEditForm() {
  document.getElementById("edit-form").style.display = "none";
}
console.log("Categories:", "{{ categories|safe }}");
console.log("Amounts:", "{{ amounts|safe }}");

// Parse the data
const categories = JSON.parse("{{ categories|safe }}");
const amounts = JSON.parse("{{ amounts|safe }}");

// Log parsed data
console.log("Parsed Categories:", categories);
console.log("Parsed Amounts:", amounts);

// Initialize Chart.js
const ctx = document.getElementById("expenseChart").getContext("2d");
new Chart(ctx, {
  type: "doughnut",
  data: {
    labels: categories,
    datasets: [
      {
        data: amounts,
        backgroundColor: [
          "#FF6384",
          "#36A2EB",
          "#FFCE56",
          "#4BC0C0",
          "#9966FF",
        ],
        hoverOffset: 4,
      },
    ],
  },
  options: {
    responsive: true,
    plugins: {
      legend: {
        position: "top",
      },
      title: {
        display: true,
        text: "Expenses by Category",
      },
    },
  },
});
if (categories.length === 0 || amounts.length === 0) {
  document.querySelector(".chart-container").innerHTML =
    "<p>No expense data available to display the chart.</p>";
}

new Chart(ctx, {
  type: "doughnut",
  data: {
    labels: ["Food", "Transport", "Utilities"],
    datasets: [
      {
        data: [10, 20, 30],
        backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56"],
      },
    ],
  },
});
