document.addEventListener('DOMContentLoaded', function() {
    // Initialize Google Sign-In
    gapi.load('auth2', function() {
        var auth2 = gapi.auth2.init({
            client_id: '431062006675-mohumg8orrinedqrv4s7a8c4bts0ampg.apps.googleusercontent.com', // Your client ID
            scope: 'openid https://www.googleapis.com/auth/business.manage'
        });

        // Attach click event handler to the sign-in button
        var signInBtn = document.getElementById('googleSignInBtn');
        auth2.attachClickHandler(signInBtn, {}, onSuccess, onFailure);
    });
});

// Callback function for successful sign-in
function onSuccess(user) {
    console.log('Signed in as ' + user.getBasicProfile().getName());
    // You can perform additional actions after successful sign-in
    // Redirect to the callback URL or handle token retrieval
    // For demonstration purposes, let's log the user's ID token
    console.log('ID Token:', user.getAuthResponse().id_token);
}

// Callback function for failed sign-in
function onFailure(error) {
    console.error('Sign-in failed:', error);
}
