function addDoctor() {
    let doctors = JSON.parse(localStorage.getItem("doctors")) || [];

    doctors.push({
        name: docName.value,
        specialization: specialization.value
    });

    localStorage.setItem("doctors", JSON.stringify(doctors));
    alert("Doctor added!");
}
