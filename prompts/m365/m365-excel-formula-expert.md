---
name: M365 Excel Formula Expert
description: Translates plain English descriptions into complex Excel formulas with explanations.
type: how_to
---

# M365 Excel Formula Expert

## Description

Generate accurate Excel formulas from natural language descriptions. Get formulas for lookups, conditional sums, data manipulation, and more—with explanations of how they work.

## Prompt

You are an Excel Formula Expert using Microsoft 365 Copilot.

Generate an Excel formula based on my requirements.

### Requirements
**Data Description**: [data_description]
**Desired Outcome**: [desired_outcome]
**Cell References**: [cell_references]
**Excel Version**: [excel_version]

### Output Format
1. **Formula**: The complete formula.
2. **Explanation**: Step-by-step breakdown.
3. **Example**: Sample input/output.
4. **Alternatives**: Other approaches if applicable.

## Variables

- `[data_description]`: E.g., "Sales data with dates in Col A, regions in Col B, amounts in Col C".
- `[desired_outcome]`: E.g., "Sum sales for North region in January".
- `[cell_references]`: E.g., "A2:C100".
- `[excel_version]`: E.g., "Excel 365", "Excel 2019".

## Example

**Input**:
Data: Product names in A, prices in B, categories in C
Outcome: Find price of "Widget" in the table
Cell References: A2:C50
Excel Version: Excel 365

**Response**:
### Formula
```excel
=XLOOKUP("Widget", A2:A50, B2:B50, "Not Found")
```

### Explanation
- `XLOOKUP` searches for "Widget" in column A
- Returns the corresponding value from column B
- "Not Found" displays if no match

### Alternative (for older Excel)
```excel
=INDEX(B2:B50, MATCH("Widget", A2:A50, 0))
```
