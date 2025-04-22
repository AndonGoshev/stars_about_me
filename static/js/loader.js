document.addEventListener("DOMContentLoaded", function () {
    console.log("DOMContentLoaded event fired");

    // Wait for the window to load completely
    window.addEventListener("load", function () {
        const loader = document.getElementById("loader");

        if (loader) {
            console.log("Loader is visible now.");
            loader.style.visibility = "visible";  // Make loader visible
            loader.style.opacity = 1;  // Fade in the loader

            // Wait for a specified time before hiding the loader
            setTimeout(function () {
                loader.style.opacity = 0;  // Fade out the loader
                loader.style.visibility = "hidden";  // Hide it completely after fade
            }, 500); // Adjust the delay as per your requirement (e.g., 2 seconds)
        } else {
            console.log("Loader element not found!");
        }
    });
});