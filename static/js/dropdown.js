// dropdown.js

function toggleDropdown() {
    var dropdown = document.getElementById('dropdown');
    dropdown.classList.toggle('show');
}

function openLoginModal() {
    const modal = document.getElementById('loginModal');
    modal.classList.remove('hidden'); // Show the modal
    modal.classList.add('flex'); // Make it a flex container to center items
}

function closeLoginModal() {
    const modal = document.getElementById('loginModal');
    modal.classList.add('hidden'); // Hide the modal
    modal.classList.remove('flex'); // Remove flex class when hidden
}

function toggleLoginModal() {
    const modal = document.getElementById('loginModal');
    modal.classList.toggle('hidden'); // Toggle visibility of the modal
    modal.classList.toggle('flex'); // Toggle flex class for centering
}

// Add event listeners for modal actions
document.addEventListener('DOMContentLoaded', function () {
    const loginBtn = document.querySelector('.login-btn'); // Update if necessary
    const closeModal = document.getElementById('closeModal');

    // Show the modal when the login button is clicked
    if (loginBtn) {
        loginBtn.addEventListener('click', openLoginModal);
    }

    // Hide the modal when the close button is clicked
    if (closeModal) {
        closeModal.addEventListener('click', closeLoginModal);
    }

    // Hide the modal when clicking outside of it
    window.addEventListener('click', function (event) {
        const modal = document.getElementById('loginModal');
        if (event.target === modal) {
            closeLoginModal();
        }
    });
});
