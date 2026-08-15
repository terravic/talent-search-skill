# Executive Talent Table Schema & Formatting Standard

This document details the exact 7-column schema required by the **Talent Intelligence Agent** for executive reporting and QBR presentations.

---

## 1. Column Specifications

| # | Column Name | Mandatory | Data Type | Description & Guidelines |
|---|---|:---:|---|---|
| 1 | `#` | Yes | Integer | Sequential index ($1$ to $N$). |
| 2 | `Full Name` | Yes | String | Candidate's complete professional name with standard credentials (e.g., "Sarah Jenkins, FSA, MAAA" or "Dr. Zafar Chaudhry, MD, MS"). |
| 3 | `Current Position` | Yes | String | Full formal executive title (e.g., "Chief Digital & Information Officer"). |
| 4 | `Current Company` | Yes | String | Full name of the employer / health system / enterprise. |
| 5 | `Relevant Background & Prior Experience` | Yes | String | 2-3 concise sentences covering prior leadership roles, prominent past employers, and degrees/certifications. |
| 6 | `Key Expertise & Notable Achievements` | Yes | String | 2-3 concise sentences detailing core domain proficiencies, technology initiatives, AI/digital transformations, or business impact. |
| 7 | `Public Source URL` | Yes | Markdown Link | Direct public web citation formatted as `[Source Title / Domain](https://...)`. |

---

## 2. Formatting Rules & Best Practices

1. **Escaping Special Characters:**
   - Any pipe characters (`|`) occurring inside cell text must be escaped (`\|`) to prevent table breakage.
   - Do not insert raw newline characters (`\n`) within table cells; use continuous sentences or HTML `<br>` if multi-line is strictly necessary.
2. **Link Formatting:**
   - Always format URLs as clickable Markdown links with descriptive source names:
     - `[Seattle Children's Leadership](https://www.seattlechildrens.org/about/leadership/)`
     - `[SEC DEF 14A Filing](https://www.sec.gov/edgar/...)`
3. **Conciseness for Executive Presentation:**
   - Cell text should be punchy and data-dense. Avoid narrative fluff or informal prose.
   - Focus on quantifiable metrics where available (e.g., "$50M cost reduction", "10-hospital EHR deployment", "HIPAA-compliant LLM implementation").
