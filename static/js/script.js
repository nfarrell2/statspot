// You can add any interactivity here if needed
document.getElementById('loginBtn').addEventListener('click', function() {
    console.log('Spotify login clicked');
    window.location.href = '{{ url_for("login") }}';
});