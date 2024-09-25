// dropdown.js

function toggleDropdown() {
    var dropdown = document.getElementById('dropdown');
    dropdown.classList.toggle('show');
}

function openLoginModal() {
    document.getElementById('loginModal').classList.remove('hidden');
}

function closeLoginModal() {
    document.getElementById('loginModal').classList.add('hidden');
}

