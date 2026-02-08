let user = JSON.parse(localStorage.getItem("currentUser"));
if (!user || user.role !== "admin") {
    window.location.href = "login.html";
}

let appointments = JSON.parse(localStorage.getItem("appointments")) || [];
let container = document.getElementById("appointments");

appointments.forEach(a => {
    container.innerHTML += `
        <div class="card">
            <p><b>Patient:</b> ${a.patient}</p>
            <p><b>Doctor:</b> ${a.doctor}</p>
            <p><b>Date:</b> ${a.date}</p>
        </div>
    `;
});
