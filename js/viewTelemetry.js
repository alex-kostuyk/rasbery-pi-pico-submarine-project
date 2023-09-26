function updateData(data) {
    document.getElementById("data").textContent = data;
}

// Function to periodically update data from Python
async function fetchData() {
    while (true) {
        const response = await fetch("/get_data");  // Simulate an API call
        const data = await response.json();
        updateData(data);
        await new Promise(resolve => setTimeout(resolve, 20)); // 50 times per second
    }
}

// Start fetching data
fetchData();