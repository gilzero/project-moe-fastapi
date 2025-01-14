/**
 * @fileoverview Enhanced JavaScript functionality for the Multi-Agent Orchestration System
 */

'use strict';

// Constants
const CONFIG = {
    MAX_QUERY_LENGTH: 1000,
    ERROR_DISPLAY_DURATION: 5000,
    DEBOUNCE_DELAY: 100,
    ENDPOINTS: {
        ANALYZE: '/analyze'
    }
};

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips if jQuery is available
    if (typeof $ !== 'undefined') {
        $('[data-toggle="tooltip"]').tooltip();
    }

    // Form elements
    const form = document.getElementById('queryForm');
    const queryInput = document.getElementById('query');
    const submitButton = document.getElementById('submitBtn');
    const charCount = document.getElementById('charCount');
    const exampleButtons = document.querySelectorAll('.btn-example');

    // Debounce function
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // Update character count
    function updateCharCount() {
        const currentLength = queryInput.value.length;
        charCount.textContent = `${currentLength}/${CONFIG.MAX_QUERY_LENGTH} characters`;
        submitButton.disabled = currentLength === 0 || currentLength > CONFIG.MAX_QUERY_LENGTH;
    }

    // Handle example query clicks
    exampleButtons.forEach(button => {
        button.addEventListener('click', () => {
            if (!button.dataset.query) return;
            queryInput.value = button.dataset.query;
            updateCharCount();
            queryInput.focus();
        });
    });

    // Add input listener with debounce
    queryInput.addEventListener('input', debounce(() => {
        updateCharCount();
    }, CONFIG.DEBOUNCE_DELAY));

    // Form submission handler
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();

            // Validate input
            const query = queryInput.value.trim();
            if (!query) {
                showError('Please enter a query');
                return;
            }

            if (query.length > CONFIG.MAX_QUERY_LENGTH) {
                showError(`Query must be ${CONFIG.MAX_QUERY_LENGTH} characters or less`);
                return;
            }

            try {
                setLoadingState(true);
                const response = await fetch(CONFIG.ENDPOINTS.ANALYZE, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: new URLSearchParams({ query })
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const html = await response.text();
                document.documentElement.innerHTML = html;
                window.history.pushState({}, '', CONFIG.ENDPOINTS.ANALYZE);
            } catch (error) {
                console.error('Error:', error);
                showError('An error occurred while processing your request');
            } finally {
                setLoadingState(false);
            }
        });
    }

    // Show error message
    function showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.innerHTML = `
            <i class="fas fa-exclamation-circle" aria-hidden="true"></i>
            <span role="alert">${message}</span>
        `;

        const existingError = form.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }

        form.insertBefore(errorDiv, form.firstChild);

        setTimeout(() => {
            errorDiv.remove();
        }, CONFIG.ERROR_DISPLAY_DURATION);
    }

    // Set loading state
    function setLoadingState(isLoading) {
        const buttonText = submitButton.querySelector('.button-text');
        const buttonLoader = submitButton.querySelector('.button-loader');
        const form = document.getElementById('queryForm');

        if (isLoading) {
            buttonText.classList.add('d-none');
            buttonLoader.classList.remove('d-none');
            submitButton.disabled = true;
            queryInput.disabled = true;
            form.classList.add('loading');
            
            // Add loading overlay
            const loadingOverlay = document.createElement('div');
            loadingOverlay.className = 'loading-overlay';
            loadingOverlay.innerHTML = `
                <div class="loading-spinner">
                    <div class="button-loader"></div>
                    <p>Analyzing your query...</p>
                </div>
            `;
            form.appendChild(loadingOverlay);
        } else {
            buttonText.classList.remove('d-none');
            buttonLoader.classList.add('d-none');
            submitButton.disabled = false;
            queryInput.disabled = false;
            form.classList.remove('loading');
            
            // Remove loading overlay
            const loadingOverlay = form.querySelector('.loading-overlay');
            if (loadingOverlay) {
                loadingOverlay.remove();
            }
        }
    }

    // Initialize character count
    updateCharCount();
});