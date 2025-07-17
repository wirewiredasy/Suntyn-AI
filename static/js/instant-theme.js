
// Instant theme application to prevent flash
(function() {
    // Get saved theme immediately
    const savedTheme = localStorage.getItem('theme-preference') || 'system';
    let currentTheme = 'light';
    
    if (savedTheme === 'system') {
        currentTheme = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    } else {
        currentTheme = savedTheme;
    }
    
    // Apply theme instantly
    const html = document.documentElement;
    const body = document.body;
    
    html.style.transition = 'none';
    body.style.transition = 'none';
    
    if (currentTheme === 'dark') {
        html.classList.add('dark');
        html.style.backgroundColor = '#111827';
        body.style.backgroundColor = '#111827';
        body.style.color = '#e5e7eb';
    } else {
        html.classList.remove('dark');
        html.style.backgroundColor = '#f9fafb';
        body.style.backgroundColor = '#f9fafb';
        body.style.color = '#1f2937';
    }
    
    // Re-enable transitions after DOM is ready
    document.addEventListener('DOMContentLoaded', function() {
        setTimeout(() => {
            html.style.transition = '';
            body.style.transition = '';
        }, 100);
    });
})();
