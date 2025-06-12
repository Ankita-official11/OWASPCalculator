document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('risk-form');

    // Handle form submission
    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(form);

        fetch('/calculate-risk', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            const resultDiv = document.getElementById('result');
            resultDiv.style.display = 'block';

            // Populate the result fields
            document.getElementById('risk-vulnerability').innerText = data.vulnerability;
            document.getElementById('risk-level').innerText = data.risk_level;
            document.getElementById('risk-mitigation').innerText = data.mitigation;
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while calculating the risk. Please try again.');
        });
    });

    // Handle Clear button functionality
    const clearButton = document.getElementById('clear-button');
    clearButton.addEventListener('click', function() {
        form.reset();  // Clear all input fields
        const resultDiv = document.getElementById('result');
        resultDiv.style.display = 'none';  // Hide the result section
    });
});
