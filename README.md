# Talent Search & Executive Intelligence Skill & Plugin

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Status: Production Ready](https://img.shields.io/badge/status-production--ready-green.svg)]()
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

An elite-level **Talent Intelligence Agent** skill and plugin designed for **Gemini Enterprise App**, **Antigravity**, and other LLM agent ecosystems. Sourcing, verifying, and profiling executive leadership from public data sources into standardized, C-suite ready reports.

---

## 📋 Executive Overview

Developed for high-visibility leadership benchmarking, executive talent acquisition, and Quarterly Business Reviews (QBRs), this skill transforms conversational requests into structured, verifiable executive intelligence tables.

```
                  ┌───────────────────────────────┐
                  │      User Prompt / Query      │
                  │   ("Top 5 Healthcare CIOs")   │
                  └──────────────┬────────────────┘
                                 │
                                 ▼
                  ┌───────────────────────────────┐
                  │    Talent Search SKILL.md     │
                  │   - Role & Scope Extraction   │
                  │   - Multi-Angle Dork Strategy │
                  └──────────────┬────────────────┘
                                 │
                                 ▼
                  ┌───────────────────────────────┐
                  │     Public Data Sourcing      │
                  │  - Leadership Bios            │
                  │  - Press Releases             │
                  │  - SEC DEF 14A Proxy Filings  │
                  │  - Industry Keynotes & Panels │
                  └──────────────┬────────────────┘
                                 │
                                 ▼
                  ┌───────────────────────────────┐
                  │    Standard Executive Table   │
                  │  - 7 Mandatory Columns        │
                  │  - Verified Public Source URLs│
                  │  - Zero Conversational Filler │
                  └───────────────────────────────┘
```

---

## 📁 Repository Structure

```text
talent-search-skill/
├── SKILL.md                          # Main Skill definition with YAML frontmatter & instructions
├── plugin.json                       # Plugin manifest for Antigravity / Gemini Plugin framework
├── pyproject.toml                    # Python project packaging specification
├── requirements.txt                  # Python dependencies
├── scripts/                          # Python CLI engines and automation tools
│   ├── __init__.py
│   ├── talent_search.py              # Sourcing engine, search strategy generator & exporter
│   ├── validate_output.py            # Strict table schema & constraints validator
│   └── generate_prompts.py           # Tailored prompt generator for various scenarios
├── references/                       # Reference manuals & search documentation
│   ├── search_strategies.md          # Boolean dorking cheat sheet & source directory
│   ├── table_schema.md               # 7-column schema definitions & rules
│   └── sample_prompts.md             # Curated, copy-pasteable prompt templates
├── examples/                         # Real-world outputs across formats
│   ├── sample_healthcare_cio_output.md
│   ├── sample_healthcare_cio_output.json
│   ├── sample_healthcare_cio_output.csv
│   ├── sample_chief_actuary_output.md
│   ├── sample_chief_actuary_output.json
│   └── sample_chief_actuary_output.csv
└── tests/                            # Automated unit tests
    ├── __init__.py
    ├── test_talent_search.py
    ├── test_validator.py
    └── test_generate_prompts.py
```

---

## 🚀 Quick Start & Integration

### 1. Using in Gemini Enterprise App / Antigravity

Place this directory in your agent's customization root or skills folder:
- **Workspace Skills Root:** `_agents/skills/talent-search/` or `skills/talent-search/`
- **Global Config:** `~/.gemini/config/skills/talent-search/`
- **Plugin Manifest:** Enable via `plugin.json`.

When the user requests executive sourcing (e.g., *"Find 5 Chief Actuaries in health insurance"*), the agent activates the skill instructions and adheres strictly to the 7-column format.

---

### 2. Command-Line Python Utilities

All Python scripts use the standard library with optional enhancements.

#### A. Generate Search Strategies & Export Data
```bash
# Generate targeted Boolean search dorks for web search
python3 scripts/talent_search.py --role "Chief Actuary" --industry "Health Insurance" --generate-queries-only

# Generate and export a Markdown table (using realistic curated data for demo/testing)
python3 scripts/talent_search.py --sample --role "Chief Information Officer" --industry "Healthcare" --count 5 --output report.md

# Export directly to JSON or CSV for analytics pipelines
python3 scripts/talent_search.py --sample --role "Chief Information Officer" --format json --output report.json
python3 scripts/talent_search.py --sample --role "Chief Information Officer" --format csv --output report.csv
```

#### B. Validate Generated Output Tables
```bash
# Validate that a report strictly complies with the 7-column schema and has no conversational filler
python3 scripts/validate_output.py --input report.md --min-candidates 5 --strict
```

#### C. Generate Specialized Prompts
```bash
# View available pre-built prompt scenarios
python3 scripts/generate_prompts.py --list-presets

# Generate a tailored prompt for a Healthcare CIO search
python3 scripts/generate_prompts.py --preset healthcare_cio
```

---

## 📊 Standard Executive Table Schema

All outputs conform strictly to the following 7-column structure:

| # | Full Name | Current Position | Current Company | Relevant Background & Prior Experience | Key Expertise & Notable Achievements | Public Source URL |
|---|---|---|---|---|---|---|
| 1 | Jane Doe, MD, MS, MBA | Chief Digital & Information Officer (CDIO) | Apex Health System | Former VP of Clinical Informatics at Metro Health; 20+ years in healthcare IT leadership. MD from State Medical University, MS Healthcare Informatics. | Enterprise cloud EHR modernization (Epic on Azure), clinical generative AI copilots, pediatric digital health transformation, and HITRUST cybersecurity. | [Apex Health Leadership](https://example.com/leadership/jane-doe) |
| 2 | Alex Morgan, MS | EVP, Chief Transformation & Digital Officer | Horizon Healthcare | Former Chief Digital Officer at Enterprise Logistics Corp; MS in Computer Science. Recognized healthcare digital innovation leader. | AI-powered patient triage systems, conversational AI in patient engagement, enterprise virtual care networks, and digital medicine ecosystem scaling. | [Horizon Executive Team](https://example.com/about-us/leadership) |
| 3 | Jordan Taylor | Executive Vice President & Chief Information Officer | Summit Health Network | 25-year technology veteran; led multi-region cloud migrations across large healthcare enterprise workloads. BS in Business Information Systems. | Multi-hospital EHR consolidation, large-scale healthcare cloud deployment, clinical ambient voice documentation rollout, and IT cost optimization. | [Summit Health Leadership](https://example.com/leadership) |
| 4 | Morgan Lee, MS, FASHP | Chief Information Officer & SVP | Vanguard Academic Medical Center | 30+ years in healthcare informatics and clinical operations; Fellow of Health-System Pharmacists. MS in Health Informatics. | Academic medical center digital transformation, federated clinical data registries, predictive sepsis analytics, and clinical research IT enablement. | [Vanguard Leadership](https://example.com/leadership/executive-team) |
| 5 | Taylor Reed, MBA, FACHE | Chief Digital & Information Officer | Integrated Health Partners | Former CDIO at Regional Health System and SVP & CIO at National Health Alliance. CHIME-HIMSS Healthcare Leadership recognition. | AI governance frameworks in health systems, integrated telehealth platforms, enterprise ERP/EHR merger integrations, and digital workforce enablement. | [Integrated Health Leadership](https://example.com/about/who-we-are/leadership) |

---

## 🎯 Sample Prompts for Enterprise Use

### Scenario 1: Healthcare CIOs driving Generative AI
> "Identify and profile 5 Chief Information Officers (CIOs) or Chief Digital Officers (CDOs) at major US health systems who are actively deploying generative AI or large-scale cloud modernization. Output strictly as the standardized 7-column Markdown table with public source URLs."

### Scenario 2: Chief Actuaries in Managed Care
> "Source and profile 5 Chief Actuaries at major US health plans (e.g., Elevance Health, Centene, Cigna, Humana, Oscar Health) with deep expertise in Medicare Advantage risk adjustment and predictive claims modeling. Provide only the Markdown table."

### Scenario 3: Large-Scale Talent Benchmarking (20+ candidates)
> To preserve maximum research depth and prevent output truncation, break searches into focused cohorts:
> - **Batch 1:** 5 CIOs from top Academic Medical Centers
> - **Batch 2:** 5 CIOs from Regional Integrated Delivery Networks (IDNs)
> - **Batch 3:** 5 CIOs from Specialized Pediatric / Cancer Centers
> - **Batch 4:** 5 CIOs from Tech-Forward Community Health Systems

---

## 🧪 Running Unit Tests

To run the automated test suite:

```bash
python3 -m unittest discover -s tests -v
```

Output:
```text
test_custom_prompt_generation ... ok
test_presets_exist ... ok
test_candidate_to_markdown_row ... ok
test_candidate_validation_failure ... ok
test_candidate_validation_success ... ok
test_json_and_csv_export ... ok
test_render_and_parse_markdown_table ... ok
test_search_strategy_generation ... ok
test_invalid_url_fails ... ok
test_missing_candidate_count ... ok
test_strict_mode_catches_filler ... ok
test_valid_table_passes ... ok

----------------------------------------------------------------------
Ran 12 tests in 0.004s

OK
```

---

## 🔒 Compliance & Data Integrity Guidelines

1. **Public Information Only:** All candidate data is sourced strictly from publicly available websites, official corporate directories, SEC filings, and news releases.
2. **Privacy Standards:** No private contact details (personal phone numbers, residential addresses, private emails) are ever harvested or output.
3. **Citation Integrity:** Every entry requires an active, verifiable public link.

---

## 📄 License

This project is licensed under the Apache License, Version 2.0 - see the [LICENSE](file:///usr/local/google/home/rolandmm/Projects/talent-search-skill/LICENSE) file for full terms and conditions.
