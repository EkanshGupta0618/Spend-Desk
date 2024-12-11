let expenses = JSON.parse(localStorage.getItem("expenses")) || [];
let monthlyBudget = 2000;

// Initialize Chart
const ctx = document.getElementById("expense-chart").getContext("2d");
let expenseChart = new Chart(ctx, {
  type: "doughnut",
  data: {
    labels: ["Food", "Transportation", "Utilities", "Entertainment", "Other"],
    datasets: [
      {
        data: [0, 0, 0, 0, 0],
        backgroundColor: [
          "#1a73e8",
          "#ea4335",
          "#34a853",
          "#fbbc04",
          "#9aa0a6",
        ],
      },
    ],
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
  },
});

// Update Stats
function updateStats() {
  const totalExpenses = expenses.reduce(
    (total, expense) => total + expense.amount,
    0
  );
  const remainingBudget = monthlyBudget - totalExpenses;

  document.getElementById(
    "total-expenses"
  ).textContent = `$${totalExpenses.toFixed(2)}`;
  document.getElementById(
    "remaining-budget"
  ).textContent = `$${remainingBudget.toFixed(2)}`;

  // Update chart data
  const categoryTotals = {
    food: 0,
    transportation: 0,
    utilities: 0,
    entertainment: 0,
    other: 0,
  };

  expenses.forEach((expense) => {
    categoryTotals[expense.category] += expense.amount;
  });

  expenseChart.data.datasets[0].data = Object.values(categoryTotals);
  expenseChart.update();
}

// Display Expenses
// Modify the displayExpenses function to include edit and delete buttons
function displayExpenses() {
  const container = document.getElementById("expenses-container");
  container.innerHTML = "";

  expenses.sort((a, b) => new Date(b.date) - new Date(a.date));

  expenses.forEach((expense, index) => {
    const expenseElement = document.createElement("div");
    expenseElement.className = "expense-item";
    expenseElement.innerHTML = `
            <div class="expense-info">
                <h4>${expense.title}</h4>
                <p>${expense.category} - ${expense.date}</p>
            </div>
            <div class="expense-actions">
                <span class="expense-amount">$${expense.amount.toFixed(
                  2
                )}</span>
                <button class="btn edit-btn" onclick="editExpense(${index})">Edit</button>
                <button class="btn delete-btn" onclick="deleteExpense(${index})">Delete</button>
            </div>
        `;
    container.appendChild(expenseElement);
  });
}

// Edit expense function
function editExpense(index) {
  const expense = expenses[index];

  // Populate the form with the existing expense details
  document.getElementById("expense-title").value = expense.title;
  document.getElementById("expense-amount").value = expense.amount;
  document.getElementById("expense-category").value = expense.category;
  document.getElementById("expense-date").value = expense.date;

  // Remove the existing expense from the list temporarily
  expenses.splice(index, 1);
  localStorage.setItem("expenses", JSON.stringify(expenses));

  // Update the display and stats
  updateStats();
  displayExpenses();
}

// Delete expense function
function deleteExpense(index) {
  // Remove the expense from the list
  expenses.splice(index, 1);
  localStorage.setItem("expenses", JSON.stringify(expenses));

  // Update the display and stats
  updateStats();
  displayExpenses();
}

// Functionality to set monthly budget
function setMonthlyBudget() {
  const newBudget = parseFloat(
    prompt("Enter your monthly budget:", monthlyBudget)
  );
  if (!isNaN(newBudget) && newBudget > 0) {
    localStorage.setItem("monthlyBudget", newBudget);
    monthlyBudget = newBudget;
    updateStats();
    alert(`Monthly budget updated to $${newBudget.toFixed(2)}`);
  } else {
    alert("Invalid budget value. Please try again.");
  }
}

// Initialize monthly budget from local storage or use default
monthlyBudget = parseFloat(localStorage.getItem("monthlyBudget")) || 2000;

document.addEventListener("DOMContentLoaded", () => {
  const setBudgetBtn = document.createElement("button");
  setBudgetBtn.textContent = "Set Monthly Budget";
  setBudgetBtn.className = "btn";
  setBudgetBtn.style.marginBottom = "1rem";
  setBudgetBtn.addEventListener("click", setMonthlyBudget);

  const container = document.querySelector(".header");
  container.appendChild(setBudgetBtn);

  updateStats();
  displayExpenses();
});

// Handle Form Submission
document
  .getElementById("expense-form")
  .addEventListener("submit", function (e) {
    e.preventDefault();

    const expense = {
      title: document.getElementById("expense-title").value,
      amount: parseFloat(document.getElementById("expense-amount").value),
      category: document.getElementById("expense-category").value,
      date: document.getElementById("expense-date").value,
    };

    expenses.push(expense);
    localStorage.setItem("expenses", JSON.stringify(expenses));

    updateStats();
    displayExpenses();

    this.reset();
  });

// Initial render
updateStats();
displayExpenses();
