const sidebar = document.querySelector(".sidebar");
const toggle = document.getElementById("sidebarToggle");

if (toggle) {
    toggle.addEventListener("click", () => {
        sidebar.classList.toggle("collapsed");
    });
}