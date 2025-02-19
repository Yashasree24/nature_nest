document.addEventListener("DOMContentLoaded", () => {
    console.log("Nature Nest website loaded!");
});
// Fetch plants from Flask API and display them on the page
async function fetchPlants() {
    try {
        let response = await fetch("http://127.0.0.1:5000/api/plants"); // Adjust the API route
        let data = await response.json();

        let plantList = document.getElementById("plant-list");
        plantList.innerHTML = ""; // Clear previous content

        data.forEach(plant => {
            let plantItem = document.createElement("div");
            plantItem.classList.add("plant-item");
            plantItem.innerHTML = `
                <h3>${plant.name}</h3>
                <p>${plant.description}</p>
                <p><strong>Price:</strong> ₹${plant.price}</p>
                <img src="${plant.image_url}" alt="${plant.name}" width="150">
            `;
            plantList.appendChild(plantItem);
        });
    } catch (error) {
        console.error("Error fetching plants:", error);
    }
}

// Call the function when the page loads
document.addEventListener("DOMContentLoaded", fetchPlants);
async function placeOrder(plantId, quantity) {
    try {
        let response = await fetch("http://127.0.0.1:5000/api/orders", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ plant_id: plantId, quantity: quantity })
        });

        let result = await response.json();
        alert(result.message); // Show success message
    } catch (error) {
        console.error("Order failed:", error);
    }
}

