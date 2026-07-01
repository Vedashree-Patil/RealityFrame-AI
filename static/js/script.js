document.addEventListener("DOMContentLoaded", function () {

    const searchInput = document.querySelector('input[name="q"]');
    const memoryCards = document.querySelectorAll(".memory-card");
    const memoryGrid = document.querySelector(".row");
    const emptyState = document.querySelector(".empty-state");

    // Live search (client-side filtering)
    if (searchInput) {
        searchInput.addEventListener("input", function () {
            const query = this.value.toLowerCase().trim();
            let visibleCount = 0;

            memoryCards.forEach(card => {
                const text = card.innerText.toLowerCase();

                if (text.includes(query)) {
                    card.parentElement.style.display = "block";
                    visibleCount++;
                } else {
                    card.parentElement.style.display = "none";
                }
            });

            // Show/hide empty state dynamically
            if (visibleCount === 0) {
                if (!document.querySelector(".no-results")) {
                    const noResult = document.createElement("div");
                    noResult.className = "no-results text-center mt-5 text-secondary";
                    noResult.innerHTML = "<h5>No matching memories found 🫥</h5>";
                    memoryGrid.appendChild(noResult);
                }
            } else {
                const noResult = document.querySelector(".no-results");
                if (noResult) noResult.remove();
            }
        });
    }

    // Smooth hover animation enhancement
    memoryCards.forEach(card => {
        card.addEventListener("mouseenter", () => {
            card.style.transition = "transform 0.2s ease, box-shadow 0.2s ease";
            card.style.boxShadow = "0 8px 25px rgba(0,0,0,0.4)";
        });

        card.addEventListener("mouseleave", () => {
            card.style.boxShadow = "0 4px 20px rgba(0,0,0,0.3)";
        });
    });

    // Lazy image loading (performance boost)
    const images = document.querySelectorAll(".memory-img");
    const imgObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.src; // triggers load
                img.classList.add("loaded");
                observer.unobserve(img);
            }
        });
    });

    images.forEach(img => {
        imgObserver.observe(img);
    });

});