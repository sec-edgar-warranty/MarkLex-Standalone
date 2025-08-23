// MarkLex Desktop Website JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add scroll effect to navigation
    let lastScrollTop = 0;
    const header = document.querySelector('header');
    
    window.addEventListener('scroll', function() {
        let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > lastScrollTop && scrollTop > 100) {
            // Scrolling down
            header.style.transform = 'translateY(-100%)';
        } else {
            // Scrolling up
            header.style.transform = 'translateY(0)';
        }
        lastScrollTop = scrollTop;
    });

    // Add animation to feature cards on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe all cards for animation
    document.querySelectorAll('.feature-card, .download-card, .step, .application, .doc-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });

    // Download button click tracking (for analytics if needed later)
    document.querySelectorAll('.btn-download').forEach(button => {
        button.addEventListener('click', function() {
            const platform = this.closest('.download-card').querySelector('h3').textContent;
            console.log(`Download clicked: ${platform}`);
            // Add analytics tracking here if needed
        });
    });

    // Mobile navigation toggle (if you add a hamburger menu later)
    const navToggle = document.querySelector('.nav-toggle');
    const navLinks = document.querySelector('.nav-links');
    
    if (navToggle) {
        navToggle.addEventListener('click', function() {
            navLinks.classList.toggle('nav-active');
            navToggle.classList.toggle('toggle');
        });
    }

    // Check if user is on mobile and adjust hero text
    function adjustHeroText() {
        const heroTitle = document.querySelector('.hero-content h1');
        if (window.innerWidth < 768 && heroTitle) {
            heroTitle.style.fontSize = '2.5rem';
        }
    }

    // Run on load and resize
    adjustHeroText();
    window.addEventListener('resize', adjustHeroText);

    // Add loading state for external links
    document.querySelectorAll('a[target="_blank"]').forEach(link => {
        link.addEventListener('click', function() {
            // Add a subtle loading indicator if needed
            this.style.opacity = '0.7';
            setTimeout(() => {
                this.style.opacity = '1';
            }, 1000);
        });
    });

    // Simple feature to detect OS and highlight appropriate download
    function detectOS() {
        const userAgent = window.navigator.userAgent.toLowerCase();
        const downloadCards = document.querySelectorAll('.download-card');
        
        let preferredOS = '';
        if (userAgent.includes('mac')) {
            preferredOS = 'macos';
        } else if (userAgent.includes('win')) {
            preferredOS = 'windows';
        } else if (userAgent.includes('linux')) {
            preferredOS = 'linux';
        }

        // Highlight the preferred OS download card
        downloadCards.forEach(card => {
            const osName = card.querySelector('h3').textContent.toLowerCase();
            if (preferredOS && osName.includes(preferredOS.replace('os', ''))) {
                card.style.border = '2px solid var(--primary-color)';
                card.style.transform = 'scale(1.05)';
                
                // Add a "Recommended" badge
                const badge = document.createElement('div');
                badge.textContent = 'Recommended';
                badge.style.cssText = `
                    position: absolute;
                    top: 10px;
                    right: 10px;
                    background: var(--primary-color);
                    color: white;
                    padding: 4px 8px;
                    border-radius: 4px;
                    font-size: 0.75rem;
                    font-weight: 600;
                `;
                card.style.position = 'relative';
                card.appendChild(badge);
            }
        });
    }

    // Run OS detection
    detectOS();
});