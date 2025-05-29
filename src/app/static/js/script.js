document.addEventListener('DOMContentLoaded', () => {
    fetch('/predict')
        .then(response => response.json())
        .then(data => {
            document.getElementById('prediction').innerText = `Predicted Price: $${data.prediction.toFixed(2)}`;
        });

    fetch('/data')
        .then(response => response.json())
        .then(data => {
            document.getElementById('data').innerText = `Latest Price: $${data.price.toFixed(2)} (Timestamp: ${data.timestamp})`;
        });
});