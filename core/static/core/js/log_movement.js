//log_movement.js - corrected version with proper getCookie implementation

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

    // Helper function to get cookies - PROPERLY IMPLEMENTED
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Helper function to show messages
    function showMessage(type, text) {
        const messageContainer = document.createElement('div');
        messageContainer.className = `message message-${type}`;
        messageContainer.textContent = text;

        // Insert the message at the top of the content
        const contentArea = document.querySelector('.card-admin');
        if (contentArea && contentArea.parentNode) {
            contentArea.parentNode.insertBefore(messageContainer, contentArea);

            // Auto-remove after 5 seconds
            setTimeout(() => {
                messageContainer.remove();
            }, 5000);
        } else {
            console.log(`${type.toUpperCase()}: ${text}`);
        }
    }
});

