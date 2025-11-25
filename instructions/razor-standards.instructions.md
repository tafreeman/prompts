---
applyTo: "**/*.cshtml,**/*.razor"
name: "razor-pages-ui-standards"
description: "Enforce security, accessibility, and performance standards for Razor Pages and Razor Components"
---

# Razor Pages and UI Standards

> Purpose: Ensure all Razor Pages and components meet enterprise security, accessibility (WCAG 2.1 AA), and performance requirements.

## Page Structure

- Use page-based organization with clear separation of concerns
- Implement proper model binding with validation attributes
- Use ViewModels for complex data presentation
- Follow RESTful routing conventions
- Use strongly-typed Razor views and components; avoid relying on dynamic or ViewBag for primary data

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

## Styling and Layout

- Implement responsive, mobile-first layouts for all new pages and components
- Use shared stylesheets and, where appropriate, CSS custom properties (variables) to support theming and consistency
- Do not use inline styles except in rare, well-justified cases; prefer reusable CSS classes instead

## JavaScript and UX Behavior

- Keep JavaScript in separate files or component-specific scripts; avoid inline <script> blocks in Razor views where possible
- Provide clear loading states for async or long-running user actions
- Display user-friendly error messages for failures; avoid exposing raw exception details or stack traces in the UI

### Example: Secure Form with CSRF and Validation

✅ **Correct Razor Page implementation:**

```cshtml
@page
@model RegisterModel

<form method="post" asp-antiforgery="true">
    <div class="form-group">
        <label asp-for="Email"></label>
        <input asp-for="Email" class="form-control" />
        <span asp-validation-for="Email" class="text-danger"></span>
    </div>
    <div class="form-group">
        <label asp-for="Password"></label>
        <input asp-for="Password" type="password" class="form-control" />
        <span asp-validation-for="Password" class="text-danger"></span>
    </div>
    <button type="submit" class="btn btn-primary">Register</button>
</form>
```

❌ **Avoid: Inline script and missing CSRF protection**

```cshtml
<form method="post">
    <input name="email" />
    <script>alert('inline script');</script>
</form>
```

## Constraints and Fallbacks

- Do NOT disable CSRF protection or HTML encoding without explicit security review and documented justification.
- When legacy JavaScript requires inline scripts, use nonce-based CSP and document the exception in the code review.
- If WCAG 2.1 AA compliance cannot be achieved for a specific component, document the accessibility gap, propose remediation steps, and escalate to the product owner.

## Response Format Expectations

When generating or reviewing Razor views/components, use this structure:

1. **Summary paragraph** – ≤3 sentences describing the UI feature and which standards it satisfies (security, accessibility, performance).
2. **Bullet list of compliance items** – map to specific sections above (e.g., "Security in Views – HTML encoding enabled", "Accessibility – ARIA labels added").
3. **Code example** – a short Razor snippet (≤2 blocks) showing the correct pattern.
4. **Deviations note** – if any standard cannot be met, explain why and propose the mitigation or waiver process.
