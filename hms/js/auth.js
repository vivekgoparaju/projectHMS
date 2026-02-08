function signup() {
    let users = JSON.parse(localStorage.getItem("users")) || [];

    let user = {
        name: name.value,
        email: email.value,
        password: password.value,
        role: role.value
    };

    users.push(user);
    localStorage.setItem("users", JSON.stringify(users));
    alert("Signup successful!");
    window.location.href = "login.html";
}

function login() {
    let users = JSON.parse(localStorage.getItem("users")) || [];

    let user = users.find(u =>
        u.email === email.value && u.password === password.value
    );

    if (!user) {
        alert("Invalid credentials");
        return;
    }

    localStorage.setItem("currentUser", JSON.stringify(user));

    if (user.role === "admin") {
        window.location.href = "dashboard.html";
    } else {
        window.location.href = "profile.html";
    }
}
