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
function logout() {
    // Redirect to logout URL
    window.location.href = '/logout/';
}

// Add event listeners for modal actions
document.addEventListener('DOMContentLoaded', function () {
    const closeModal = document.getElementById('closeModal');

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
