document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('googleSignInBtn').addEventListener('click', function() {
        // Redirect to Google authentication page
        window.location.href = 'https://accounts.google.com/o/oauth2/v2/auth?client_id=431062006675-mohumg8orrinedqrv4s7a8c4bts0ampg.apps.googleusercontent.com&redirect_uri=https://sachin4b4.github.io/google_business/auth/callback&response_type=code&scope=openid%20https://www.googleapis.com/auth/business.manage';
    });
});
