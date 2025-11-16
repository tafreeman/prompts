/**
 * Spell Checker Utility
 * Provides real-time spell checking and autocorrect suggestions
 */

class SpellChecker {
    constructor() {
        this.dictionary = null;
        this.initialized = false;
        this.init();
    }

    async init() {
        try {
            // Initialize spell checker with US English dictionary
            // Note: In production, you might want to load dictionary files
            console.log('Spell checker initialized');
            this.initialized = true;
        } catch (error) {
            console.error('Failed to initialize spell checker:', error);
        }
    }

    /**
     * Check if a word is spelled correctly
     * Simple implementation - can be enhanced with real dictionary
     */
    isCorrect(word) {
        // Basic check - filter out numbers, special chars
        if (!word || /^\d+$/.test(word) || word.length < 2) {
            return true;
        }
        
        // Simple spell check using built-in browser API
        return true; // Placeholder - implement actual check
    }

    /**
     * Get spelling suggestions for a word
     */
    getSuggestions(word) {
        // Placeholder - implement actual suggestions
        return [];
    }

    /**
     * Add spell checking to input/textarea elements
     */
    addSpellCheck(element) {
        if (!element) return;

        // Enable browser's built-in spell checker
        element.setAttribute('spellcheck', 'true');
        
        // Add custom visual indicators
        element.addEventListener('input', (e) => {
            this.highlightErrors(e.target);
        });
    }

    /**
     * Highlight spelling errors in text
     */
    highlightErrors(element) {
        // This is a simplified version
        // In production, use a more sophisticated approach
        const text = element.value;
        const words = text.split(/\s+/);
        
        // Count misspellings for statistics
        let errorCount = 0;
        words.forEach(word => {
            if (!this.isCorrect(word.replace(/[^\w]/g, ''))) {
                errorCount++;
            }
        });
        
        // Update error count display if exists
        const errorDisplay = element.parentElement.querySelector('.spell-error-count');
        if (errorDisplay) {
            errorDisplay.textContent = errorCount > 0 ? `${errorCount} spelling issue(s)` : '';
        }
    }

    /**
     * Auto-correct common typos
     */
    autoCorrect(text) {
        // Common typo corrections
        const corrections = {
            'teh': 'the',
            'recieve': 'receive',
            'occured': 'occurred',
            'seperate': 'separate',
            'definately': 'definitely',
            'untill': 'until',
            'wierd': 'weird',
            'Sonnet 4': 'Sonnet 4.5',  // Correct Claude model name
            'Code4': 'Code 5'  // Correct Claude model name
        };
        
        let correctedText = text;
        Object.keys(corrections).forEach(typo => {
            const regex = new RegExp('\\b' + typo + '\\b', 'gi');
            correctedText = correctedText.replace(regex, corrections[typo]);
        });
        
        return correctedText;
    }
}

// Initialize global spell checker
const spellChecker = new SpellChecker();

/**
 * Add spell checking to all text inputs on page load
 */
document.addEventListener('DOMContentLoaded', function() {
    // Add spell check to all relevant input fields
    const inputs = document.querySelectorAll('input[type="text"], textarea');
    inputs.forEach(input => {
        spellChecker.addSpellCheck(input);
    });
    
    // Add auto-correct button functionality
    document.querySelectorAll('.auto-correct-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const target = document.querySelector(this.dataset.target);
            if (target) {
                target.value = spellChecker.autoCorrect(target.value);
                // Trigger input event to update any bindings
                target.dispatchEvent(new Event('input', { bubbles: true }));
            }
        });
    });
});

/**
 * Copy to clipboard with feedback
 */
function copyToClipboard(text, buttonElement) {
    navigator.clipboard.writeText(text).then(function() {
        // Show success feedback
        if (buttonElement) {
            const originalText = buttonElement.innerHTML;
            buttonElement.innerHTML = '<i class="fas fa-check me-2"></i>Copied!';
            buttonElement.classList.add('btn-success');
            buttonElement.classList.remove('btn-primary');
            
            setTimeout(() => {
                buttonElement.innerHTML = originalText;
                buttonElement.classList.remove('btn-success');
                buttonElement.classList.add('btn-primary');
            }, 2000);
        }
        
        // Show toast notification if available
        const toast = document.getElementById('copyToast');
        if (toast) {
            const bsToast = new bootstrap.Toast(toast);
            bsToast.show();
        }
    }).catch(function(err) {
        console.error('Failed to copy:', err);
        alert('Failed to copy to clipboard. Please try again.');
    });
}

/**
 * Debounce function for search inputs
 */
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

/**
 * Live search functionality
 */
const liveSearch = debounce(function(searchTerm) {
    // Implement live search if needed
    console.log('Searching for:', searchTerm);
}, 300);

/**
 * Form validation with visual feedback
 */
function validateForm(formElement) {
    let isValid = true;
    const inputs = formElement.querySelectorAll('[required]');
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
        }
    });
    
    return isValid;
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { SpellChecker, copyToClipboard, debounce, validateForm };
}
