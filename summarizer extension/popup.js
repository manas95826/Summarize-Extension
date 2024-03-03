document.getElementById('checkButton').addEventListener('click', async () => {    
    const resultDiv = document.getElementById('result');
    resultDiv.style.display = 'none';
    console.log('Check button clicked'); // Log when the button is clicked

    try {
        const response = await fetch('http://localhost:8000/summarize_url', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({url: document.getElementById('urlInput').value}),
        });
        const data = await response.json();
        resultDiv.textContent = data.result;
        if (data.result.includes('error')) {
            resultDiv.classList.add('alert-danger');
        } else {
            resultDiv.classList.add('alert-success');
        }
        resultDiv.style.display = 'block';
    } catch (error) {
        console.error('Error:', error); // Log any errors encountered during fetch
        resultDiv.textContent = 'Error checking URL.';
        resultDiv.classList.add('alert-danger');
        resultDiv.style.display = 'block';
    }
});
