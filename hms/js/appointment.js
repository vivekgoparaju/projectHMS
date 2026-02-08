function book() {
    let appointments = JSON.parse(localStorage.getItem("appointments")) || [];
    let user = JSON.parse(localStorage.getItem("currentUser"));

    appointments.push({
        patient: user.name,
        doctor: doctor.value,
        date: date.value
    });

    localStorage.setItem("appointments", JSON.stringify(appointments));
    alert("Appointment booked!");
}
