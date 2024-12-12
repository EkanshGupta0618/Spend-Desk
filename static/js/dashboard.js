// Initialize Chart
const ctx = document.getElementById("expenseChart").getContext("2d");
const expenseChart = new Chart(ctx, {
  type: "doughnut",
  data: {
    labels: ["Food", "Transport", "Utilities", "Entertainment", "Other"],
    datasets: [
      {
        data: [0, 0, 0, 0, 0],
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
  },
});

// Handle Budget Form
document.getElementById("budgetForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const formData = new FormData(e.target);
  try {
    const response = await fetch("/api/set-budget/", {
      method: "POST",
      body: formData,
    });
    const data = await response.json();
    document.getElementById("currentBudget").textContent = data.budget;
  } catch (error) {
    console.error("Error:", error);
  }
});

// Handle Expense Form
document.getElementById("expenseForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const formData = new FormData(e.target);
  try {
    const response = await fetch("/api/add-expense/", {
      method: "POST",
      body: formData,
    });
    const data = await response.json();
    updateExpenseList();
    updateChart();
    e.target.reset();
  } catch (error) {
    console.error("Error:", error);
  }
});

// Update Expense List
async function updateExpenseList() {
  try {
    const response = await fetch("/api/expenses/");
    const expenses = await response.json();
    const expenseList = document.getElementById("expenseList");
    expenseList.innerHTML = expenses
      .map(
        (expense) => `
                    <div class="expense-item">
                        <div>
                            <strong>${expense.description}</strong>
                            <span>$${expense.amount}</span>
                            <span>${expense.category}</span>
                        </div>
                        <div class="expense-actions">
                            <button onclick="editExpense(${expense.id})">Edit</button>
                            <button onclick="deleteExpense(${expense.id})">Delete</button>
                        </div>
                    </div>
                `
      )
      .join("");
  } catch (error) {
    console.error("Error:", error);
  }
}

// Update Chart
async function updateChart() {
  try {
    const response = await fetch("/api/expense-summary/");
    const data = await response.json();
    expenseChart.data.datasets[0].data = [
      data.food,
      data.transport,
      data.utilities,
      data.entertainment,
      data.other,
    ];
    expenseChart.update();
  } catch (error) {
    console.error("Error:", error);
  }
}

// Delete Expense
async function deleteExpense(id) {
  if (confirm("Are you sure you want to delete this expense?")) {
    try {
      await fetch(`/api/delete-expense/${id}/`, {
        method: "DELETE",
      });
      updateExpenseList();
      updateChart();
    } catch (error) {
      console.error("Error:", error);
    }
  }
}

// Edit Expense
async function editExpense(id) {
  // Implement edit functionality
  const newAmount = prompt("Enter new amount:");
  if (newAmount) {
    try {
      await fetch(`/api/edit-expense/${id}/`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ amount: newAmount }),
      });
      updateExpenseList();
      updateChart();
    } catch (error) {
      console.error("Error:", error);
    }
  }
}

// Initial load
updateExpenseList();
updateChart();
