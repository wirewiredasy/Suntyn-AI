// Header scroll improvement and navigation fixes
document.addEventListener('DOMContentLoaded', function() {
    'use strict';
    
    const header = document.querySelector('.sticky-header');
    let lastScrollY = window.scrollY;
    let isScrolling = false;
    
    // Throttled scroll handler for better performance
    function handleScroll() {
        if (!isScrolling) {
            window.requestAnimationFrame(() => {
                const currentScrollY = window.scrollY;
                
                if (header) {
                    if (currentScrollY > 10) {
                        header.classList.add('scrolled');
                        if (header && header.style) {
                            header.style.transform = 'translateY(0)';
                            header.style.backdropFilter = 'blur(20px)';
                        }
                    } else {
                        header.classList.remove('scrolled');
                        if (header && header.style) {
                            header.style.backdropFilter = 'blur(16px)';
                        }
                    }
                }
                
                lastScrollY = currentScrollY;
                isScrolling = false;
            });
        }
        isScrolling = true;
    }
    
    // Add scroll listener with passive option for better performance
    window.addEventListener('scroll', handleScroll, { passive: true });
    
    // Mobile menu toggle fix
    const mobileMenuBtn = document.querySelector('[data-mobile-menu-toggle]');
    const mobileMenu = document.querySelector('.mobile-menu');
    
    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', function() {
            mobileMenu.classList.toggle('open');
        });
        
        // Close mobile menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!mobileMenu.contains(e.target) && !mobileMenuBtn.contains(e.target)) {
                mobileMenu.classList.remove('open');
            }
        });
    }
    
    // Prevent double headers by hiding any additional navigation in dashboard
    const dashboardContent = document.querySelector('.dashboard-content');
    if (dashboardContent) {
        const extraNavs = dashboardContent.querySelectorAll('nav');
        extraNavs.forEach(nav => {
            if (nav && nav.style) {
                nav.style.display = 'none';
            }
        });
    }
    
    console.log('Header scroll fixes applied');
});