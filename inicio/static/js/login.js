$(document).ready(function () {
    // Hide spinner initially
    $('#loading-spinner').hide();

    // Handle form submission
    $('#login-form').on('submit', function (e) {
        // Show spinner when button is clicked
        $('#loading-spinner').show();

        // Hide the submit button to avoid multiple clicks
        $('#submit-btn').hide();

        // Simulate form submission (you can replace this with actual submission logic)
        setTimeout(function () {
            // Simulate a successful submission and hide the spinner
            $('#loading-spinner').hide();
            // Submit the form after the delay (simulating)
            $('#login-form')[0].submit();
        }, 2000); // Simulating a 2-second delay (you can remove this in production)
        
        // Prevent default form submission while the spinner is showing
        e.preventDefault();
    });
});
