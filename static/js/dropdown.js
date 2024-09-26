
let isDarkMode = false;

// Toggle dropdown menu visibility
function toggleDropdown() {
    const dropdown = document.getElementById('dropdown');
    dropdown.classList.toggle('show'); // Adjusted from 'hidden' to 'show' based on your existing logic
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
    const notifModal = document.getElementById('notifModal');

    // Check if the login modal is active and if the click is outside of it
    if (loginModal.classList.contains('active') && event.target === loginModal) {
        closeLoginModal();
    }

    // Check if the signup modal is active and if the click is outside of it
    if (signupModal.classList.contains('active') && event.target === signupModal) {
        closeSignupModal();
    }

    if (notifModal.classList.contains('active') && event.target === notifModal) {
        closeNotifModal();
    }
});

// Logout function
function logout() {
    window.location.href = '/logout/';
}

// Dark mode toggle functionality
document.getElementById('toggleDarkMode').addEventListener('click', function() {
    isDarkMode = !isDarkMode;
    document.body.classList.toggle('bg-gray-900', isDarkMode);
    document.body.classList.toggle('text-white', isDarkMode);
    document.body.classList.toggle('bg-white', !isDarkMode);
    document.body.classList.toggle('text-black', !isDarkMode);
});

// Attach event listeners for modal close buttons
document.addEventListener('DOMContentLoaded', function() {
    // Close login modal button
    const closeLoginButton = document.querySelector('#loginModal .close-button');
    if (closeLoginButton) {
        closeLoginButton.addEventListener('click', closeLoginModal);
    }

    // Close signup modal button
    const closeSignupButton = document.querySelector('#signupModal .close-button');
    if (closeSignupButton) {
        closeSignupButton.addEventListener('click', closeSignupModal);
    }

    const closeNotifButton = document.querySelector('#notifModal .close-button');
    if (closeNotifButton) {
        closeNotifButton.addEventListener('click', closeNotifModal);
    }

    // Initialize dark mode toggle button if it exists
    const darkModeToggle = document.getElementById('darkModeToggle');
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode'); // Implement your dark mode functionality
        });
    }
});


function openNotifModal() {
    const modal = document.getElementById('notifModal');
    modal.classList.add('active');
}

// Close the notif modal
function closeNotifModal() {
    const modal = document.getElementById('notifModal');
    modal.classList.remove('active'); // Hide the modal
}