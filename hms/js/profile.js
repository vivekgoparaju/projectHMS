let user = JSON.parse(localStorage.getItem("currentUser"));
if (!user) window.location.href = "login.html";

name.innerText = user.name;
email.innerText = user.email;
