document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".action-toggle").forEach(function(toggle) {
        const arrow = toggle.querySelector(".toggle-arrow");
        const panel = toggle.parentElement.querySelector(".action-panel");

        if (!arrow || !panel) {
            return;
        }

        toggle.addEventListener("click", function() {
            panel.classList.toggle("open");
            arrow.classList.toggle("rotated");
        });
    });

    const allDropdowns = Array.from(document.querySelectorAll(".add-dropdown"));

    function closeDropdowns(exceptDropdown) {
        allDropdowns.forEach(function(dropdown) {
            if (dropdown !== exceptDropdown) {
                dropdown.classList.remove("open");
            }
        });
    }

    document.querySelectorAll(".add-menu").forEach(function(menu) {
        const addButton = menu.querySelector(".add-button");
        const addDropdown = menu.querySelector(".add-dropdown");

        if (!addButton || !addDropdown) {
            return;
        }

        addButton.addEventListener("click", function(event) {
            event.stopPropagation();
            const willOpen = !addDropdown.classList.contains("open");
            closeDropdowns(addDropdown);
            addDropdown.classList.toggle("open", willOpen);
        });

        addDropdown.addEventListener("click", function(event) {
            event.stopPropagation();
        });
    });

    document.addEventListener("click", function() {
        closeDropdowns(null);
    });
});