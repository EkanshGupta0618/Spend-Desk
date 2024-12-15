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
