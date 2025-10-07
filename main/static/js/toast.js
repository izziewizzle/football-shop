function showToast(title, message, type = 'normal', duration = 3000) {
    const toast = document.getElementById('toast-component');
    const icon = document.getElementById('toast-icon');
    const titleEl = document.getElementById('toast-title');
    const messageEl = document.getElementById('toast-message');

    if (!toast) return;

    // Reset style
    toast.style.backgroundColor = 'white';
    toast.style.borderColor = 'var(--leaf)';
    icon.innerHTML = '';

    // Default teks
    titleEl.textContent = title;
    messageEl.textContent = message;
    titleEl.style.color = 'var(--leaf)';
    messageEl.style.color = '#6B7280'; // abu lembut (gray-500)

    // Show animation
    toast.classList.remove('opacity-0', 'translate-y-8');
    toast.classList.add('opacity-100', 'translate-y-0');

    // Hide automatically
    setTimeout(() => {
        toast.classList.remove('opacity-100', 'translate-y-0');
        toast.classList.add('opacity-0', 'translate-y-8');
    }, duration);
}
