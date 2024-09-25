// Toggle dropdown menu visibility
function toggleDropdown() {
    var dropdown = document.getElementById('dropdown');
    dropdown.classList.toggle('show');
}

// Open the login modal
function openLoginModal() {
    const modal = document.getElementById('loginModal');
    modal.classList.add('active'); // Show the modal
}

// Close the login modal
function closeLoginModal() {
    const modal = document.getElementById('loginModal');
    modal.classList.remove('active'); // Hide the modal
}

// Open the signup modal
function openSignupModal() {
    const modal = document.getElementById('signupModal');
    modal.classList.add('active'); // Show the modal
}

// Close the signup modal
function closeSignupModal() {
    const modal = document.getElementById('signupModal');
    modal.classList.remove('active'); // Hide the modal
}

// Close modals when clicking outside of them
window.addEventListener('click', function (event) {
    const loginModal = document.getElementById('loginModal');
    const signupModal = document.getElementById('signupModal');

    // Check if the login modal is active and if the click is outside of it
    if (loginModal.classList.contains('active') && event.target === loginModal) {
        closeLoginModal();
    }

    // Check if the signup modal is active and if the click is outside of it
    if (signupModal.classList.contains('active') && event.target === signupModal) {
        closeSignupModal();
    }
});

function logout() {
    // Redirect to logout URL
    window.location.href = '/logout/';
}

// Attach event listeners for modal close buttons inside the script
document.addEventListener('DOMContentLoaded', function() {
    // Close login modal button
    document.querySelector('#loginModal .close-button').addEventListener('click', closeLoginModal);

    // Close signup modal button
    document.querySelector('#signupModal .close-button').addEventListener('click', closeSignupModal);
});

