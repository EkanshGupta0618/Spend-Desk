function showEditForm(id, description, category, amount) {
    document.getElementById('edit-expense-id').value = id;
    document.getElementById('edit-description').value = description;
    document.getElementById('edit-amount').value = amount;

    // Set the selected category in the dropdown
    var categorySelect = document.getElementById('edit-category');
    categorySelect.value = category; // Set the selected value

    document.getElementById('edit-form').style.display = 'block';
}

function hideEditForm() {
    document.getElementById('edit-form').style.display = 'none';
}