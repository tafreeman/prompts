---
title: "M365 Excel Formula Expert"
description: "Translates plain English descriptions of data problems into complex Excel formulas, explaining the logic and syntax."
category: "analysis"
tags: ["m365", "excel", "data-analysis", "formulas", "productivity"]
author: "GitHub Copilot"
version: "1.0"
date: "2025-11-18"
difficulty: "Intermediate"
platform: "Microsoft 365 Copilot"
---

## Description

This prompt acts as an expert Excel consultant. It helps users who know what they want to calculate but don't know the specific function syntax. It generates the correct formula (e.g., XLOOKUP, INDEX/MATCH, nested IFs) and explains how it works so the user can learn.

## Goal

To generate accurate, efficient Excel formulas from natural language descriptions and provide a clear explanation of the logic.

## Inputs

- **Data Description**: [data_description]
- **Desired Outcome**: [desired_outcome]
- **Column/Cell References**: [cell_references]
- **Excel Version**: [excel_version]

## Prompt

You are an expert Excel Data Analyst. I need a formula to solve a specific problem in my spreadsheet.

Here is the scenario:

- **Data Structure**: [data_description]
- **What I want to calculate**: [desired_outcome]
- **Relevant Cells/Columns**: [cell_references]
- **My Excel Version**: [excel_version]

Please provide:

1. The **exact formula** I can copy and paste.
2. A **breakdown** of how the formula works, step-by-step.
3. An **alternative approach** if a more efficient function exists (e.g., XLOOKUP vs VLOOKUP).
4. **Error handling**: How to modify the formula to handle missing data or errors (e.g., IFERROR).

## Variables

- `[data_description]`: Description of the dataset (e.g., "Sales data with dates in Col A and amounts in Col B").
- `[desired_outcome]`: What you are trying to find (e.g., "Sum of sales for 'North' region in January").
- `[cell_references]`: Specific ranges (e.g., "A2:A100", "Sheet1!B:B").
- `[excel_version]`: e.g., "Excel 365", "Excel 2019" (important for function availability).

## Example Usage

**Input:**

- `[data_description]`: "Employee list with IDs in Col A and Names in Col B. Another sheet has IDs in Col A and I need Names."
- `[desired_outcome]`: "Match the ID in the second sheet to the Name in the first sheet."
- `[cell_references]`: "Sheet1!A:B, Sheet2!A2"
- `[excel_version]`: "Excel 365"

**Output:**

### Recommended Formula

```excel
=XLOOKUP(A2, Sheet1!A:A, Sheet1!B:B, "Not Found")
```

### Explanation

- **Lookup_value (A2)**: The ID you are searching for in the current sheet.
- **Lookup_array (Sheet1!A:A)**: The column in the source sheet containing the IDs.
- **Return_array (Sheet1!B:B)**: The column in the source sheet containing the Names you want to retrieve.
- **"Not Found"**: A custom message if the ID doesn't exist (built-in error handling).

## Tips

- Always specify your Excel version, as newer functions like `XLOOKUP` or `FILTER` are not available in older versions.
- If your data is in an Excel Table, mention the Table Name for cleaner structured references (e.g., `Table1[Amount]`).

## Related Prompts

- `m365-data-insights-assistant`
- `data-analysis-specialist`

## Changelog

- 2025-11-18: Initial version created.
