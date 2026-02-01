/**
 * Student Performance Predictor - JavaScript
 * Interactive form handling and animations
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initNavbar();
    initFormValidation();
    initScoreInputs();
    initAnimations();
});

/**
 * Navbar scroll effect
 */
function initNavbar() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;

    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
}

/**
 * Form validation with visual feedback
 */
function initFormValidation() {
    const form = document.querySelector('form');
    if (!form) return;

    const inputs = form.querySelectorAll('.form-control');
    
    inputs.forEach(input => {
        // Add focus effects
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });

        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
            validateInput(this);
        });

        // Real-time validation for selects
        if (input.tagName === 'SELECT') {
            input.addEventListener('change', function() {
                validateInput(this);
            });
        }
    });

    // Form submission
    form.addEventListener('submit', function(e) {
        let isValid = true;
        
        inputs.forEach(input => {
            if (!validateInput(input)) {
                isValid = false;
            }
        });

        if (isValid) {
            showLoadingState(form);
        } else {
            e.preventDefault();
            shakeForm(form);
        }
    });
}

/**
 * Validate individual input
 */
function validateInput(input) {
    const formGroup = input.closest('.form-group');
    if (!formGroup) return true;

    let isValid = true;

    if (input.required && !input.value) {
        isValid = false;
        formGroup.classList.add('error');
        formGroup.classList.remove('success');
    } else if (input.type === 'number') {
        const value = parseFloat(input.value);
        if (isNaN(value) || value < 0 || value > 100) {
            isValid = false;
            formGroup.classList.add('error');
            formGroup.classList.remove('success');
        } else {
            formGroup.classList.remove('error');
            formGroup.classList.add('success');
        }
    } else if (input.value) {
        formGroup.classList.remove('error');
        formGroup.classList.add('success');
    }

    return isValid;
}

/**
 * Score input enhancements
 */
function initScoreInputs() {
    const scoreInputs = document.querySelectorAll('input[type="number"]');
    
    scoreInputs.forEach(input => {
        // Create value display
        const wrapper = input.parentElement;
        if (!wrapper.classList.contains('score-input-wrapper')) {
            const newWrapper = document.createElement('div');
            newWrapper.className = 'score-input-wrapper';
            input.parentNode.insertBefore(newWrapper, input);
            newWrapper.appendChild(input);
        }

        // Update display on input
        input.addEventListener('input', function() {
            let value = parseInt(this.value);
            
            // Clamp value between 0 and 100
            if (value < 0) this.value = 0;
            if (value > 100) this.value = 100;
            
            // Update visual feedback
            updateScoreVisual(this);
        });
    });
}

/**
 * Update score visual feedback
 */
function updateScoreVisual(input) {
    const value = parseInt(input.value) || 0;
    const wrapper = input.closest('.score-input-wrapper');
    
    // Update border color based on score
    if (value >= 80) {
        input.style.borderColor = 'var(--success)';
    } else if (value >= 60) {
        input.style.borderColor = 'var(--accent-primary)';
    } else if (value >= 40) {
        input.style.borderColor = 'var(--warning)';
    } else if (value > 0) {
        input.style.borderColor = 'var(--danger)';
    } else {
        input.style.borderColor = 'var(--glass-border)';
    }
}

/**
 * Show loading state on form submission
 */
function showLoadingState(form) {
    const btn = form.querySelector('.btn-submit');
    if (!btn) return;

    const originalText = btn.textContent;
    btn.innerHTML = '<span class="spinner"></span> Predicting...';
    btn.disabled = true;
    btn.classList.add('loading');
}

/**
 * Shake form on validation error
 */
function shakeForm(form) {
    form.classList.add('shake');
    setTimeout(() => form.classList.remove('shake'), 500);
}

/**
 * Initialize scroll animations
 */
function initAnimations() {
    // Intersection Observer for fade-in animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all animatable elements
    document.querySelectorAll('.feature-card, .glass-card').forEach(el => {
        el.classList.add('animate-on-scroll');
        observer.observe(el);
    });

    // Result animation
    const resultContainer = document.querySelector('.result-container');
    if (resultContainer) {
        animateResult(resultContainer);
    }
}

/**
 * Animate result value
 */
function animateResult(container) {
    const valueEl = container.querySelector('.result-value');
    if (!valueEl) return;

    const finalValue = parseFloat(valueEl.textContent);
    if (isNaN(finalValue)) return;

    let currentValue = 0;
    const duration = 1000;
    const increment = finalValue / (duration / 16);

    const animate = () => {
        currentValue += increment;
        if (currentValue < finalValue) {
            valueEl.textContent = Math.round(currentValue);
            requestAnimationFrame(animate);
        } else {
            valueEl.textContent = finalValue.toFixed(1);
        }
    };

    animate();
}

/**
 * Add CSS for shake animation
 */
const style = document.createElement('style');
style.textContent = `
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
        20%, 40%, 60%, 80% { transform: translateX(5px); }
    }
    
    .shake {
        animation: shake 0.5s ease-in-out;
    }
    
    .animate-on-scroll {
        opacity: 0;
        transform: translateY(30px);
        transition: opacity 0.6s ease, transform 0.6s ease;
    }
    
    .animate-in {
        opacity: 1;
        transform: translateY(0);
    }
    
    .form-group.error .form-control {
        border-color: var(--danger);
    }
    
    .form-group.success .form-control {
        border-color: var(--success);
    }
    
    .btn.loading {
        opacity: 0.7;
    }
`;
document.head.appendChild(style);
