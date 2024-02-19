document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('googleSignInBtn').addEventListener('click', function() {
        // Redirect to Google authentication page
        window.location.href = '/auth/google';
    });
});
