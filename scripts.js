document.addEventListener("DOMContentLoaded", () => {
    console.log("Nature Nest website loaded!");
});
// Fetch plants from Flask API and display them on the page
async function loginUser(email, password) {
    try {
        let response = await fetch("http://127.0.0.1:5000/api/users/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        let result = await response.json();
        if (response.ok) {
            localStorage.setItem("token", result.token); // Store token
            alert("Login successful!");
        } else {
            alert(result.error);
        }
    } catch (error) {
        console.error("Login failed:", error);
    }
}

async function fetchPlants() {
    try {
        let response = await fetch("http://127.0.0.1:5000/api/plants");
        let data = await response.json();

        let plantList = document.getElementById("plant-list");
        plantList.innerHTML = "";

        data.forEach(plant => {
            let plantItem = document.createElement("div");
            plantItem.classList.add("plant-item");
            plantItem.innerHTML = `
                <img src="${plant.image_url}" alt="${plant.name}" width="150">
                <h3>${plant.name}</h3>
                <p><strong>Category:</strong> ${plant.category}</p>
                <p><strong>Price:</strong> ₹${plant.price}</p>
                <p><strong>Stock:</strong> ${plant.stock} available</p>
                <p>${plant.description}</p>
                <button onclick="viewPlantDetails('${plant.id}')">View Details</button>
            `;
            plantList.appendChild(plantItem);
        });
    } catch (error) {
        console.error("Error fetching plants:", error);
    }
}

// Fetch plant details when clicking "View Details"
async function viewPlantDetails(plantId) {
    try {
        let response = await fetch(`http://127.0.0.1:5000/api/plants/${plantId}`);
        let plant = await response.json();

        alert(`🌱 ${plant.name}\nCategory: ${plant.category}\nPrice: ₹${plant.price}\nStock: ${plant.stock}\n\n${plant.description}`);
    } catch (error) {
        console.error("Error fetching plant details:", error);
    }
}

// Load plants on page load
document.addEventListener("DOMContentLoaded", fetchPlants);


// Call the function when the page loads
document.addEventListener("DOMContentLoaded", fetchPlants);
async function placeOrder(plantId, plantName, quantity) {
    try {
        let token = localStorage.getItem("token");
        if (!token) {
            alert("Please log in to place an order.");
            return;
        }

        let response = await fetch("http://127.0.0.1:5000/api/orders/place", {
            method: "POST",
            headers: { 
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ plant_id: plantId, quantity: quantity, address: "User Address" })
        });

        let result = await response.json();
        if (response.ok) {
            // Redirect to order confirmation page with order details
            window.location.href = `order-confirmation.html?order_id=${result.order_id}&plant_name=${plantName}&quantity=${quantity}`;
        } else {
            alert(result.error);
        }
    } catch (error) {
        console.error("Order failed:", error);
    }
}


