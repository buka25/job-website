document.addEventListener("DOMContentLoaded", function () {
    const gallery = document.getElementById("scrollGallery");
    if (!gallery) return;

    let isDown = false;
    let startX;
    let scrollLeft;

    gallery.addEventListener("mousedown", (e) => {
        isDown = true;
        gallery.classList.add("dragging");
        startX = e.pageX - gallery.offsetLeft;
        scrollLeft = gallery.scrollLeft;
    });

    gallery.addEventListener("mouseleave", () => {
        isDown = false;
        gallery.classList.remove("dragging");
    });

    gallery.addEventListener("mouseup", () => {
        isDown = false;
        gallery.classList.remove("dragging");
    });

    gallery.addEventListener("mousemove", (e) => {
        if (!isDown) return;
        e.preventDefault();
        const x = e.pageX - gallery.offsetLeft;
        const walk = (x - startX) * 1.5;
        gallery.scrollLeft = scrollLeft - walk;
    });
});
