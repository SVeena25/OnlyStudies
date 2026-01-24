/**
 * Cloudinary Admin Integration
 * Enhances the Django admin panel with Cloudinary upload functionality
 */

(function() {
    'use strict';

    document.addEventListener('DOMContentLoaded', function() {
        // Find all Cloudinary upload inputs
        const cloudinaryInputs = document.querySelectorAll('input[data-cloudinary="true"]');
        
        if (cloudinaryInputs.length === 0) {
            // Fallback: find inputs in Cloudinary upload containers
            const containers = document.querySelectorAll('.cloudinary-upload-container');
            containers.forEach(container => {
                const input = container.querySelector('input[type="text"]');
                if (input) {
                    enhanceCloudinaryInput(input);
                }
            });
        } else {
            cloudinaryInputs.forEach(enhanceCloudinaryInput);
        }

        function enhanceCloudinaryInput(input) {
            // Add event listener for validation
            input.addEventListener('change', function() {
                validateCloudinaryUrl(this);
            });

            // Add paste event handling
            input.addEventListener('paste', function(e) {
                // Validate pasted URL
                setTimeout(() => {
                    validateCloudinaryUrl(this);
                }, 100);
            });
        }

        function validateCloudinaryUrl(input) {
            const url = input.value.trim();
            
            if (!url) {
                removeValidationIndicator(input);
                return;
            }

            if (url.includes('cloudinary.com')) {
                showValidation(input, true, 'Valid Cloudinary URL');
            } else if (url.match(/^https?:\/\//)) {
                showValidation(input, false, 'Invalid: Use a Cloudinary image URL');
            }
        }

        function showValidation(input, isValid, message) {
            removeValidationIndicator(input);
            
            const container = input.parentElement;
            const indicator = document.createElement('span');
            indicator.className = 'cloudinary-validation-' + (isValid ? 'success' : 'error');
            indicator.textContent = (isValid ? '✓ ' : '✗ ') + message;
            indicator.style.cssText = `
                display: block;
                margin-top: 5px;
                font-size: 12px;
                color: ${isValid ? '#28a745' : '#dc3545'};
                font-weight: 500;
            `;
            
            container.appendChild(indicator);
        }

        function removeValidationIndicator(input) {
            const container = input.parentElement;
            const indicator = container.querySelector('[class*="cloudinary-validation-"]');
            if (indicator) {
                indicator.remove();
            }
        }

        // Add Cloudinary widget scripts if not already loaded
        if (!window.cloudinary) {
            const script = document.createElement('script');
            script.src = 'https://widget.cloudinary.com/v2.0/global/all.js';
            script.async = true;
            document.head.appendChild(script);
        }
    });
})();
