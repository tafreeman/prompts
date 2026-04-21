import json
import os
import re

theme_path = "presentation/src/tokens/raw-themes/doom-64.json"
out_path = "presentation/src/tokens/raw-themes/preview.html"

with open(theme_path, encoding="utf-8") as f:
    data = json.load(f)

variables = data.get("variables", {})

html_content = rf"""<!DOCTYPE html>
<html lang="en" class="{data.get('classes', '')}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Theme Preview: {data.get('themeName', 'Custom')}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {{
{chr(10).join(f"  {k}: {v};" for k, v in variables.items())}
}}

body {{
    /* Using var directly since V0 usually provides explicit color formats inside */
    background-color: var(--background, #fff);
    color: var(--foreground, #000);
    font-family: var(--font-sans, 'Inter', sans-serif);
    margin: 0;
    padding: 3rem;
    display: flex;
    gap: 2rem;
    flex-wrap: wrap;
}}

/* For HSL fallbacks if needed */
body.hsl-mode {{
    background-color: hsl(var(--background));
    color: hsl(var(--foreground));
}}

.card {{
    background-color: var(--card, #fff);
    color: var(--card-foreground, #000);
    border: 1px solid var(--border, #e5e7eb);
    border-radius: var(--radius, 0.5rem);
    padding: 1.5rem;
    width: 380px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}}

.primary-btn {{
    background-color: var(--primary, #000);
    color: var(--primary-foreground, #fff);
    border: none;
    border-radius: calc(var(--radius, 0.5rem) - 2px);
    padding: 0.6rem 1rem;
    font-weight: 500;
    cursor: pointer;
    width: 100%;
    margin-top: 1rem;
}}

.secondary-btn {{
    background-color: var(--secondary, #f3f4f6);
    color: var(--secondary-foreground, #000);
    border: none;
    border-radius: calc(var(--radius, 0.5rem) - 2px);
    padding: 0.6rem 1rem;
    font-weight: 500;
    cursor: pointer;
    flex: 1;
}}

.input {{
    background-color: var(--input, #fff);
    color: var(--foreground, #000);
    border: 1px solid var(--border, #e5e7eb);
    border-radius: calc(var(--radius, 0.5rem) - 2px);
    padding: 0.6rem;
    width: 100%;
    box-sizing: border-box;
    margin-bottom: 1rem;
}}

.label {{
    font-size: 0.875rem;
    font-weight: 500;
    margin-bottom: 0.4rem;
    display: block;
}}

.muted-text {{
    color: var(--muted-foreground, #6b7280);
    font-size: 0.875rem;
    margin: 0;
}}

.title {{
    font-size: 1.5rem;
    font-weight: 600;
    margin: 0 0 0.5rem 0;
}}

.stat {{
    font-size: 2.5rem;
    font-weight: 700;
    margin: 0.5rem 0;
}}

.flex-row {{
    display: flex;
    gap: 0.5rem;
    margin-top: 1rem;
    margin-bottom: 1.5rem;
}}

</style>
<!-- Inline script to patch hsl vs pure okoklch raw configs -->
<script>
    document.addEventListener("DOMContentLoaded", () => {{
        const bg = getComputedStyle(document.documentElement).getPropertyValue('--background').trim();
        // If it's just raw numbers like "222.2 47.4% 11.2%", we enable hsl mode
        if (bg.match(/^[0-9]+(\.[0-9]+)?\s+[0-9]+(\.[0-9]+)?%\s+[0-9]+(\.[0-9]+)?%$/)) {{
            document.body.classList.add('hsl-mode');
            
            // Add hsl injection to stylesheet dynamically
            const style = document.createElement('style');
            style.innerHTML = `
                .card {{ background-color: hsl(var(--card)); color: hsl(var(--card-foreground)); border-color: hsl(var(--border)); }}
                .primary-btn {{ background-color: hsl(var(--primary)); color: hsl(var(--primary-foreground)); }}
                .secondary-btn {{ background-color: hsl(var(--secondary)); color: hsl(var(--secondary-foreground)); }}
                .input {{ background-color: hsl(var(--background)); border-color: hsl(var(--border)); color: hsl(var(--foreground)); }}
                .muted-text {{ color: hsl(var(--muted-foreground)); }}
            `;
            document.head.appendChild(style);
        }}
    }});
</script>
</head>
<body>

<div class="card">
    <h3 class="title">Total Revenue</h3>
    <p class="stat">$15,231.89</p>
    <p class="muted-text">+20.1% from last month</p>
    <!-- Little mock chart line relying on primary color -->
    <div style="height: 80px; margin-top: 2rem; border-bottom: 3px solid var(--primary, #000); position: relative;">
        <!-- Simulated chart dots -->
        <div style="position:absolute; bottom: -4px; left: 10%; width: 6px; height: 6px; border-radius: 50%; background: var(--primary, #000);"></div>
        <div style="position:absolute; bottom: 20px; left: 40%; width: 6px; height: 6px; border-radius: 50%; background: var(--primary, #000);"></div>
        <div style="position:absolute; bottom: 40px; left: 70%; width: 6px; height: 6px; border-radius: 50%; background: var(--primary, #000);"></div>
        <div style="position:absolute; bottom: 60px; left: 90%; width: 6px; height: 6px; border-radius: 50%; background: var(--primary, #000);"></div>
    </div>
</div>

<div class="card">
    <div style="margin-bottom: 1.5rem;">
        <h3 class="title" style="font-size: 1.25rem;">Create an account</h3>
        <p class="muted-text">Enter your email below to create your account</p>
    </div>
    
    <div class="flex-row">
        <button class="secondary-btn">GitHub</button>
        <button class="secondary-btn">Google</button>
    </div>
    
    <div style="text-align: center; margin-bottom: 1.5rem; position: relative;">
        <hr style="border: 0; border-top: 1px solid var(--border, #e5e7eb); position: absolute; top: 10px; width: 100%; z-index: -1;">
        <span class="muted-text" style="background: var(--card, #fff); padding: 0 10px; font-size: 0.75rem; text-transform: uppercase;">Or continue with</span>
    </div>
    
    <label class="label">Email</label>
    <input type="text" class="input" placeholder="m@example.com">
    
    <label class="label">Password</label>
    <input type="password" class="input" placeholder="••••••••">
    
    <button class="primary-btn">Create account</button>
</div>

</body>
</html>
"""

with open(out_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Preview generated. Absolute Path: {os.path.abspath(out_path)}")
