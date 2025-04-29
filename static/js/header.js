document.addEventListener("DOMContentLoaded", function() {
    const dropdowns = document.querySelectorAll(".dropdown");

    dropdowns.forEach(dropdown => {
        dropdown.addEventListener("click", function() {
            let menu = this.querySelector(".dropdown-menu");
            menu.style.display = menu.style.display === "block" ? "none" : "block";
        });
    });

    
    document.addEventListener("click", function(event) {
        dropdowns.forEach(dropdown => {
            if (!dropdown.contains(event.target)) {
                dropdown.querySelector(".dropdown-menu").style.display = "none";
            }
        });
    });
});
