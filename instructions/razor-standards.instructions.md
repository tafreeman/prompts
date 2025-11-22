---
applyTo: "**/*.cshtml,**/*.razor"
---

# Razor Pages and UI Standards

## Page Structure
- Use page-based organization with clear separation of concerns
- Implement proper model binding with validation attributes
- Use ViewModels for complex data presentation
- Follow RESTful routing conventions

## Security in Views
- Always use HTML encoding for user-generated content
- Implement CSRF protection on all forms
- Use Content Security Policy (CSP) headers
- Validate and sanitize all user inputs

## Accessibility Requirements
- Implement WCAG 2.1 AA compliance for Section 508
- Use semantic HTML elements and proper ARIA attributes
- Ensure keyboard navigation and screen reader compatibility
- Provide alternative text for images and media

## Performance Optimization
- Minimize HTTP requests and optimize resource loading
- Use bundling and minification for CSS/JavaScript
- Implement proper caching strategies
- Optimize images and media files for web delivery