// Basic JavaScript for interactivity and capturing user's geolocation

document.addEventListener("DOMContentLoaded", function() {
    console.log("JavaScript Loaded");

    // If the donation form has hidden fields for latitude and longitude, attempt to capture them.
    if (document.getElementById("latitude") && document.getElementById("longitude")) {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                document.getElementById("latitude").value = position.coords.latitude;
                document.getElementById("longitude").value = position.coords.longitude;
            }, function(error) {
                console.error("Error getting location: ", error);
            });
        } else {
            console.error("Geolocation is not supported by this browser.");
        }
    }
});
