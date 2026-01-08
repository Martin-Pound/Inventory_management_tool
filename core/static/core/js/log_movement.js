//log_movement.js - corrected version

document.addEventListener('DOMContentLoaded', function() {
    // Get the form element
    const movementLogForm = document.getElementById('movement-log-form');

    if (movementLogForm) {
        movementLogForm.addEventListener('submit', function(e) {
            e.preventDefault();

            // Create a JSON object with the exact field names that work in Postman
            const formData = {
                item: document.getElementById('movement_sku').value,
                from_bin: document.getElementById('from_bin').value,
                to_bin: document.getElementById('to_bin').value,
                quantity: parseInt(document.getElementById('quantity').value),
                movement_type: document.getElementById('movement_type').value
            };

            // Send AJAX request to the MovementLogView
            fetch('/api/movements/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify(formData)
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(data => {
                        throw new Error(data.error || 'An error occurred while processing your request');
                    });
                }
                return response.json();
            })
            .then(data => {
                // Display success message
                showMessage('success', data.message || 'Stock movement logged successfully');

                // Clear the form
                movementLogForm.reset();

                // Reload if the current SKU matches
                const currentSku = document.getElementById('search_sku')?.value;
                if (currentSku && currentSku === formData.item) {
                    window.location.reload();
                }
            })
            .catch(error => {
                showMessage('error', error.message);
            });
        });
    }

    // Helper functions remain the same
    function getCookie(name) { /* unchanged */ }
    function showMessage(type, text) { /* unchanged */ }
});
