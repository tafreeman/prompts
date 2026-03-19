# Playwright Automated Testing — Self-Guided Training Prompt

Use this prompt with Claude or any AI assistant to get interactive, hands-on Playwright training. Copy the whole thing, or pick a specific section.

---

## The Prompt

```
I'm a tester learning to write automated E2E tests with Playwright and TypeScript. I need hands-on, practical training — not theory. Teach me by building real tests together.

My skill level: [BEGINNER / INTERMEDIATE / ADVANCED — pick one]

Teach me in this order, with working code examples for each topic. After each section, give me a small exercise to write myself, then review my answer.

### PHASE 1: FOUNDATIONS (Beginner)

1. **Setup & First Test**
   - How to install Playwright (`npm init playwright@latest`)
   - The anatomy of a test file: `import`, `test.describe`, `test`, `async/await`
   - `page.goto()` — navigating to a URL
   - `expect().toBeVisible()` — the most basic assertion
   - `toHaveURL()` and `toHaveTitle()` — quick page-level checks, often your first assertions
   - Running tests: `npx playwright test`, `--headed`, `--debug`, `-g "name"`

2. **Finding Elements (Selectors)**
   - The selector priority pyramid (best to worst):
     1. `getByRole()` — buttons, links, headings, cells (BEST — accessible and resilient)
     2. `getByText()` — visible text content
     3. `getByPlaceholder()` — input placeholders
     4. `getByLabel()` — form labels
     5. `getByTitle()` — title attributes
     6. `locator(".css-class")` — CSS selectors (LAST RESORT)
   - Why `getByRole()` is king: survives CSS refactors, matches what users see
   - `{ exact: true }` — when "Add" also matches "Add Staffing"
   - `{ name: /pattern/ }` — regex matching for flexible selectors

3. **Common Assertions**
   - `toBeVisible()` / `not.toBeVisible()` — is it on screen?
   - `toHaveText()` / `toContainText()` — text content checks
   - `toHaveValue()` — form input values
   - `toBeEnabled()` / `toBeDisabled()` — button/input states
   - `toHaveCount()` — number of matching elements
   - `toHaveURL()` / `toHaveTitle()` — verify navigation landed on the right page
   - `toHaveAttribute()` — check `href`, `disabled`, `data-*` attributes
   - **Presence vs. accuracy**: `toBeVisible()` checks something exists; `toContainText("$4,030,000")` checks the value is correct. Always test accuracy for computed data — don't just verify labels are on screen.
   - **Soft assertions**: `expect.soft()` reports ALL failures in one run instead of stopping at the first. Use when checking multiple values on a page (e.g., a dashboard with 10 stat cards). The test still fails, but you see every problem at once — saves re-running 10 times.

4. **User Actions**
   - `click()` — clicking buttons and links
   - `fill()` — typing into inputs (clears first, unlike `type()`)
   - `selectOption()` — choosing from dropdowns
   - `press("Enter")` / `press("Control+Enter")` — keyboard shortcuts
   - `check()` / `uncheck()` — checkboxes

5. **Anti-Patterns to Recognize (Especially in AI-Generated Code)**
   - AI assistants sometimes generate code with these mistakes — you MUST catch them:
   - Never use `page.waitForTimeout(5000)` — hardcoded sleeps make tests slow and flaky. Use web-first assertions (`toBeVisible()`, `toHaveText()`) which auto-wait.
   - Never use `{ force: true }` on clicks — if a user can't click it, the test shouldn't either. This hides real bugs.
   - Never use `expect(await locator.isVisible()).toBe(true)` — this doesn't retry! Use `await expect(locator).toBeVisible()` instead (the retrying form).
   - Never rely on `waitForLoadState('networkidle')` for page readiness — wait for a specific visible element instead.
   - When reviewing AI-generated tests, check for these patterns FIRST.

### PHASE 2: REAL-WORLD PATTERNS (Intermediate)

6. **Handling Ambiguous Selectors (Strict Mode)**
   - What "strict mode violation" means and why it happens
   - Fix #1: Make selectors more specific (`{ exact: true }`, regex)
   - Fix #2: Scope to a container with `page.locator(".parent", { has: ... })`
   - Fix #3: Use `.first()`, `.nth(1)`, `.last()` (least preferred)
   - **Table row scoping**: `page.locator("tr", { has: getByRole("cell", { name: "Alice" }) })` — find a row by one cell, then assert on sibling cell values. Essential for any data table.
   - **Card scoping**: `page.locator(".card", { has: getByText("Total Budget") })` — tie a value assertion to its label container

7. **Waiting for Async Data**
   - Playwright auto-waits for elements (no manual `sleep()` needed!)
   - `waitForResponse()` — wait for a specific API call to finish
   - `toBeVisible({ timeout: 10000 })` — custom timeouts for slow operations
   - Anti-pattern: never use `page.waitForTimeout()` (it's a code smell)

8. **Testing Forms & CRUD**
   - Fill a form, submit, verify the result appears
   - Delete something, verify it disappears
   - `page.on("dialog", d => d.accept())` — handling confirm() dialogs
   - Testing that validation errors appear for bad input

9. **Authentication with `storageState`**
   - Almost every real app has login — Playwright handles this with `storageState`
   - **Setup project**: Create a `setup` project in `playwright.config.ts` that logs in once and saves cookies/localStorage to a JSON file
   - **Reuse across tests**: Other projects declare `dependencies: ['setup']` and `use: { storageState: '.auth/user.json' }` — every test starts already logged in
   - **Multiple roles**: Save different state files for different user roles (admin vs. viewer) and assign them to different test projects
   - **Why not log in every test?** Logging in per test is slow and flaky. `storageState` runs login once, then reuses the session — tests are faster and more reliable.
   - **Global setup file pattern**:
     ```
     // auth.setup.ts
     test('authenticate', async ({ page }) => {
       await page.goto('/login');
       await page.getByLabel('Email').fill('user@example.com');
       await page.getByLabel('Password').fill('password');
       await page.getByRole('button', { name: 'Sign in' }).click();
       await page.waitForURL('/dashboard');
       await page.context().storageState({ path: '.auth/user.json' });
     });
     ```

10. **The AAA Pattern (Arrange → Act → Assert)**
   - Every test follows this structure — learn to think in these three steps
   - **Arrange**: Set up preconditions (navigate, open a form, seed data, set up mocks)
   - **Act**: Perform the user action being tested (click, fill, submit)
   - **Assert**: Verify the expected outcome (element visible, value correct, item gone)
   - Sometimes Act is implicit — e.g., a dashboard that loads data on navigation
   - Label the sections in your test with comments (`// ── ARRANGE ──`, `// ── ACT ──`, `// ── ASSERT ──`) until the habit is automatic
   - When directing Copilot, describe your test in AAA terms: "Arrange: go to Staffing tab. Act: add a person. Assert: they appear in the table."

11. **Test Organization & Tagging**
   - `test.describe()` — grouping related tests
   - `test.beforeEach()` — shared setup (navigate, log in, etc.)
   - Test isolation: each test should work independently
   - Cleanup: leave the database the way you found it
   - **Test tagging**: Add `@smoke`, `@regression`, `@slow` tags to test titles or via `{ tag: '@smoke' }`
   - Filter at the CLI: `--grep @smoke` to run only smoke tests, `--grep-invert @slow` to skip slow ones
   - Built-in annotations: `test.skip('reason')`, `test.fixme('bug-123')`, `test.slow()` — communicate test status to the team

12. **API Mocking with `page.route()`**
   - WHY mock: no flaky external services, test error states, run fast
   - `page.route("**/api/endpoint", route => route.fulfill({...}))` — fake a response
   - Mocking errors: `route.fulfill({ status: 500, body: ... })`
   - Mocking slow responses: add a `setTimeout` before `route.fulfill`
   - Mock ONLY what you need — let other requests pass through to the real server

13. **Flaky Test Management**
    - Configure retries: `retries: 2` in CI, `retries: 0` locally — Playwright auto-labels tests as "flaky" (failed then passed on retry) in the HTML report
    - Capture traces on retry: `trace: 'on-first-retry'` gives you a full replay of what happened during the failure
    - Open traces: `npx playwright show-trace trace.zip` — see DOM snapshots, network calls, console logs, and action timing at each step
    - Quarantine strategy: tag flaky tests with `@flaky`, run them separately, create tickets to fix root causes. Flaky tests destroy team trust in the suite.

14. **Visual Regression Testing (Screenshot Comparison)**
    - `await expect(page).toHaveScreenshot()` — full-page comparison against a saved baseline image
    - `await expect(locator).toHaveScreenshot()` — component-level comparison (e.g., just the header or a chart)
    - Configure tolerance: `maxDiffPixels` or `threshold` to avoid false positives from anti-aliasing
    - Update baselines: `--update-snapshots` when visual changes are intentional
    - Critical: screenshots must be generated on the same OS/browser as CI (run in Docker or generate on CI)

15. **Accessibility Testing (a11y)**
    - Install `@axe-core/playwright`, run `new AxeBuilder({ page }).analyze()` after page loads
    - Filter by WCAG standard: `.withTags(['wcag2a', 'wcag2aa'])` for compliance levels
    - Scope scans to specific regions: `.include('#main-content')` and `.exclude('#known-issue')`
    - Attach violation reports to test results: `testInfo.attach()` for team review
    - WHY: accessibility bugs are real bugs. Automated a11y scans catch missing alt text, broken ARIA, and contrast issues without requiring a11y expertise.

### PHASE 3: PROFESSIONAL PATTERNS (Advanced)

16. **Page Object Model (POM)**
    - Encapsulating page interactions in reusable classes
    - When POM helps (large test suites) vs. when it's overkill (small projects)

17. **Test Data Management**
    - Using seeded databases vs. creating data in tests
    - API-level setup: `request.post()` to create test data before UI tests
    - Cleaning up: delete what you create, restore what you change
    - **Deterministic seed data**: When the app seeds the same data every run, expected values are constants — calculate them once, verify they make sense, then hardcode them. If a value changes, that's a real regression, not flakiness.
    - **Deriving expected values**: Trace the data flow from seed → database query → API response → UI formatting. The formatted string on screen (e.g., `"$199,830"`) is what you assert on, not the raw number.

18. **API Testing with `request` Context (No Browser Needed)**
    - Playwright can test REST APIs directly — no browser, no page, just HTTP requests
    - Use `test({ request })` to get a built-in API client that shares cookies and baseURL with your browser tests
    - **When to use**: Testing backend endpoints, setting up test data before UI tests, verifying side effects after UI actions
    - **Example**:
      ```
      test('GET /api/users returns user list', async ({ request }) => {
        const response = await request.get('/api/users');
        expect(response.ok()).toBeTruthy();
        const users = await response.json();
        expect(users.length).toBeGreaterThan(0);
        expect(users[0]).toHaveProperty('email');
      });
      ```
    - **Multipart file uploads**: Playwright's `request` handles file uploads natively — useful for testing import endpoints
      ```
      const response = await request.post('/api/import', {
        multipart: {
          file: { name: 'data.xlsx', mimeType: 'application/...', buffer: fileBuffer }
        }
      });
      ```
    - **Hybrid tests**: Use `request` to seed data via API, then `page` to verify it renders in the UI — combines speed of API setup with confidence of UI verification
    - **WHY learn this**: API tests run 10-50x faster than browser tests. Use them for thorough backend coverage, and save browser tests for critical user journeys.

19. **CI/CD Integration**
    - Running tests in GitHub Actions / Azure DevOps
    - Playwright's built-in reporters: list, html, json
    - Screenshots and traces on failure: `use: { screenshot: 'only-on-failure', trace: 'retain-on-failure' }`
    - Parallelization: `workers: 4` for speed, `workers: 1` for stability

20. **Debugging Failing Tests**
    - `npx playwright test --debug` — step through interactively
    - `npx playwright show-report` — view the HTML report
    - `page.screenshot({ path: 'debug.png' })` — capture state mid-test
    - Trace viewer: `npx playwright show-trace trace.zip`
    - Reading error messages: "strict mode violation", "timeout", "locator not found"

21. **Working with AI Code Assistants (Copilot / Claude)**
    - Your job is to DIRECT the AI — tell it WHAT to test, not HOW to write Playwright code
    - Describe tests in AAA terms: "Arrange: navigate to Settings. Act: change model, click Save, reload page. Assert: saved model persists."
    - Review generated selectors against the priority pyramid — reject CSS selectors when `getByRole` would work
    - The AI writes the code; YOU verify: Are the expected values correct? Is the right thing being tested? Does it scope assertions to the right container?
    - When the AI generates a test, run it once and read the output — don't blindly trust hardcoded expected values
    - If the AI uses `page.waitForTimeout()`, flag it — that's always a code smell

### RULES FOR TEACHING ME:

- Show me WORKING code, not pseudocode
- Explain WHY, not just HOW — I need to understand the principle
- When I make a mistake, show me the error message I'd see and how to fix it
- Give me exercises that build on the app we're testing
- If I ask about a concept, show me a before/after: bad code → good code
- Keep examples under 30 lines — I can always ask for more detail
```

---

## Quick-Reference Commands

```bash
# Install Playwright
npm init playwright@latest

# Run all tests
npx playwright test

# Run with browser visible
npx playwright test --headed

# Step-through debugger
npx playwright test --debug

# Run one specific test by name
npx playwright test -g "adds and removes"

# Run one specific file
npx playwright test tests/e2e/ui/app.spec.ts

# View the HTML report after a run
npx playwright show-report

# Update Playwright browsers
npx playwright install
```

## Quick-Reference Selectors (Best to Worst)

```typescript
// BEST: Role-based (survives refactors)
page.getByRole("button", { name: "Save" })
page.getByRole("cell", { name: "Project Alpha" })
page.getByRole("columnheader", { name: "Budget" })
page.getByRole("link", { name: "Home" })

// GOOD: Text/placeholder/label
page.getByText("Total Budget")
page.getByPlaceholder("Enter email")
page.getByLabel("Username")
page.getByTitle("Remove")

// OK: Scoped locators (when text appears multiple times)
page.locator(".card", { has: page.getByText("Rate Card") })
     .getByRole("cell", { name: "Lead Architect" })

// LAST RESORT: CSS selectors
page.locator("select.input-field")
page.locator("tr", { has: page.getByRole("cell", { name: "Alice" }) })
```

## Quick-Reference Assertions (Pin This)

```typescript
// ── ELEMENT STATE ──
await expect(locator).toBeVisible();          // element is on screen
await expect(locator).not.toBeVisible();      // element is NOT on screen
await expect(locator).toBeEnabled();          // button/input is clickable
await expect(locator).toBeDisabled();         // button/input is greyed out
await expect(locator).toBeChecked();          // checkbox is checked
await expect(locator).toBeFocused();          // element has keyboard focus
await expect(locator).toBeHidden();           // element exists in DOM but hidden
await expect(locator).toBeAttached();         // element exists in DOM (visible or not)

// ── TEXT CONTENT ──
await expect(locator).toHaveText("exact");            // exact full text match
await expect(locator).toContainText("partial");       // text contains substring
await expect(locator).toHaveText(/regex/i);           // regex match (case-insensitive)

// ── FORM VALUES ──
await expect(locator).toHaveValue("input value");     // input/select current value
await expect(locator).toHaveValues(["a", "b"]);       // multi-select values

// ── ATTRIBUTES & CSS ──
await expect(locator).toHaveAttribute("href", "/home"); // HTML attribute
await expect(locator).toHaveClass(/active/);             // CSS class (regex)
await expect(locator).toHaveCSS("color", "rgb(0,0,0)"); // computed CSS property

// ── COUNTING ──
await expect(locator).toHaveCount(5);         // exactly 5 matching elements

// ── PAGE-LEVEL ──
await expect(page).toHaveURL(/\/dashboard/);  // current URL matches
await expect(page).toHaveTitle("My App");     // page <title> tag

// ── VISUAL ──
await expect(locator).toHaveScreenshot();     // screenshot comparison
await expect(page).toHaveScreenshot();        // full-page screenshot

// ── API RESPONSE ──
expect(response.ok()).toBeTruthy();           // status 200-299
expect(response.status()).toBe(201);          // exact status code

// ── SOFT ASSERTIONS (report all failures, don't stop at first) ──
expect.soft(locator1).toHaveText("A");
expect.soft(locator2).toHaveText("B");
expect.soft(locator3).toHaveText("C");
// test continues even if locator1 fails — you see ALL 3 results
```
