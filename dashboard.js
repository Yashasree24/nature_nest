document.addEventListener("DOMContentLoaded", () => {
    fetchUserProfile();
    fetchUserOrders();

    document.getElementById("profile-form").addEventListener("submit", updateProfile);
});

// Fetch user profile
async function fetchUserProfile() {
    try {
        let token = localStorage.getItem("token");
        if (!token) {
            alert("Please log in to access the dashboard.");
            window.location.href = "login.html";
            return;
        }

        let response = await fetch("http://127.0.0.1:5000/api/users/profile", {
            method: "GET",
            headers: { "Authorization": `Bearer ${token}` }
        });

        let data = await response.json();
        if (response.ok) {
            document.getElementById("name").value = data.name;
            document.getElementById("email").value = data.email;
            document.getElementById("address").value = data.address || "";
        } else {
            alert(data.error);
        }
    } catch (error) {
        console.error("Error fetching profile:", error);
    }
}

// Update user profile
async function updateProfile(event) {
    event.preventDefault();
    
    let token = localStorage.getItem("token");
    let name = document.getElementById("name").value;
    let address = document.getElementById("address").value;
    let password = document.getElementById("password").value;

    let updateData = { name, address };
    if (password) updateData.password = password;

    try {
        let response = await fetch("http://127.0.0.1:5000/api/users/profile/update", {
            method: "PUT",
            headers: { 
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify(updateData)
        });

        let result = await response.json();
        alert(result.message);
    } catch (error) {
        console.error("Profile update failed:", error);
    }
}

// Fetch user order history
async function fetchUserOrders() {
    try {
        let token = localStorage.getItem("token");

        let response = await fetch("http://127.0.0.1:5000/api/users/orders", {
            method: "GET",
            headers: { "Authorization": `Bearer ${token}` }
        });

        let data = await response.json();
        let ordersTable = document.getElementById("orders-table");
        ordersTable.innerHTML = "";

        data.forEach(order => {
            let row = document.createElement("tr");
            row.innerHTML = `
                <td>${order.id}</td>
                <td>${order.plant_name}</td>
                <td>${order.quantity}</td>
                <td>${order.status}</td>
            `;
            ordersTable.appendChild(row);
        });
    } catch (error) {
        console.error("Error fetching orders:", error);
    }
}
