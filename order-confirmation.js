document.addEventListener("DOMContentLoaded", () => {
    let params = new URLSearchParams(window.location.search);
    let orderId = params.get("order_id");
    let plantName = params.get("plant_name");
    let quantity = params.get("quantity");

    document.getElementById("order-id").textContent = orderId;
    document.getElementById("plant-name").textContent = plantName;
    document.getElementById("order-quantity").textContent = quantity;
});
