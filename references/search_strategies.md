# Executive Talent Search Strategies & Sourcing Guide

This reference manual provides boolean operators, search query templates, and verification workflows for the **Talent Intelligence Agent**.

---

## 1. High-Confidence Public Sourcing Channels

When researching executive talent, prioritize authoritative public sources:

| Source Category | Target Domains & Databases | Data Extracted |
|---|---|---|
| **Official Leadership Bios** | `company.com/about/leadership`, `/executive-team`, `/about-us` | Current exact title, board roles, official bio, credentials |
| **Regulatory & SEC Filings** | `sec.gov/edgar` (DEF 14A Proxy Statements, 10-K filings) | Named Executive Officers (NEOs), career history, official disclosures |
| **Press Releases & Wires** | `businesswire.com`, `prnewswire.com`, `globenewswire.com` | Executive appointments, tenure announcements, organizational restructuring |
| **Healthcare Trade Media** | `beckershospitalreview.com`, `modernhealthcare.com`, `fiercehealthcare.com` | Industry rankings ("Top 50 CIOs to know"), interviews, panels |
| **Professional Associations** | `himss.org`, `chimecentral.org`, `soa.org` (Society of Actuaries), `casact.org` | Fellow designations, keynote speakers, working group chairs |
| **Public Profiles** | `linkedin.com/in`, Google Scholar, Crunchbase | Career trajectory, education, patents, publications |

---

## 2. Advanced Search Operators & Boolean Dorking

Use these search templates to quickly locate top leadership candidates:

### A. Leadership & Executive Bios
```text
"[Target Title]" "[Industry]" ("leadership team" OR "executive leadership" OR "board of directors" OR "management team") -jobs -careers -salary
```
*Example:*
```text
"Chief Information Officer" "healthcare system" ("leadership team" OR "executive leadership") -jobs -careers
```

### B. Recent Executive Appointments (2024–2026)
```text
site:businesswire.com OR site:prnewswire.com "[Target Title]" "[Industry]" (appointed OR named OR "joins as") (2024 OR 2025 OR 2026)
```
*Example:*
```text
site:businesswire.com OR site:prnewswire.com "Chief Actuary" "health insurance" (appointed OR named OR joins)
```

### C. Industry Conference Speakers & Keynotes
```text
"[Target Title]" "[Industry]" (speaker OR keynote OR panelist OR "fireside chat") (CHIME OR HIMSS OR ViVE OR HLTH OR "Society of Actuaries")
```

### D. Public Profile Search (LinkedIn Dorking)
```text
site:linkedin.com/in "[Target Title]" "[Industry]" "[Key Skill/Technology]" -intitle:profiles
```
*Example:*
```text
site:linkedin.com/in "VP Artificial Intelligence" "healthcare" ("generative AI" OR "clinical LLM")
```

---

## 3. Verification & Currency Checklist

Before adding a candidate to the executive table, perform the following verification:

1. **Active Title Check:** Verify that the executive currently holds the role or left within the last 3-6 months. Check recent news announcements.
2. **Entity Validation:** Ensure the company is an active organization (not an acquired or defunct entity without clarifying notes).
3. **Public URL Integrity:** Ensure the public source link is valid, direct, and publicly readable without requiring private credentials.
4. **Credential Accuracy:** Ensure degrees, certifications (e.g., MD, MBA, FSA, MAAA, CISSP, FACHE), and accolades are factual.
