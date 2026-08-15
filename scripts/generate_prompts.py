#!/usr/bin/env python3
"""
Talent Search Prompt Generator
==============================
Generates specialized, high-conversion talent intelligence prompts
optimized for Gemini Enterprise App and other Agentic / Skill-based LLMs.
"""

from __future__ import annotations

import argparse
import sys
from typing import Dict, List


PROMPT_TEMPLATES: Dict[str, Dict[str, str]] = {
    "healthcare_cio": {
        "title": "Healthcare System CIOs driving AI & Cloud Modernization",
        "role": "Chief Information Officer / Chief Digital Officer",
        "industry": "Healthcare Systems & Academic Medical Centers",
        "count": "5",
        "focus": "Enterprise EHR transformation (Epic/Cerner), generative AI adoption, clinical workflow automation, and cybersecurity compliance (HITRUST/HIPAA).",
    },
    "chief_actuary": {
        "title": "Chief Actuaries in Health Insurance & Managed Care",
        "role": "Chief Actuary / Head of Actuarial Services",
        "industry": "Health Insurance / Payers (Medicare Advantage, Commercial, Medicaid)",
        "count": "5",
        "focus": "Predictive claims modeling, value-based risk adjustment (HCC), CMS Star ratings, and modern GLM/ML actuarial forecasting.",
    },
    "vp_healthcare_ai": {
        "title": "VPs of Healthcare Artificial Intelligence & Machine Learning",
        "role": "VP of Artificial Intelligence / Head of Applied Machine Learning",
        "industry": "HealthTech / BioPharma / Digital Health",
        "count": "5",
        "focus": "Large clinical multimodal models, ambient clinical intelligence, drug discovery AI pipelines, and FDA-cleared SaMD algorithms.",
    },
    "ciso_health": {
        "title": "Chief Information Security Officers (CISO) in Healthcare",
        "role": "Chief Information Security Officer (CISO)",
        "industry": "Enterprise Health Systems & Health Plans",
        "count": "5",
        "focus": "Medical device IoT security, zero-trust architectures, ransomware resilience, and HIPAA/HITECH risk governance.",
    },
    "chief_medical_officer": {
        "title": "Chief Medical Officers (CMO) driving Digital Clinical Transformation",
        "role": "Chief Medical Officer (CMO)",
        "industry": "Integrated Delivery Networks (IDNs) & Value-Based Care Organizations",
        "count": "5",
        "focus": "Physician AI adoption, clinical quality metrics, population health analytics, and reduction of clinician burnout through digital tools.",
    },
}


def build_system_and_user_prompt(
    role: str,
    industry: str,
    count: int = 5,
    focus: str = "",
    location: str = "United States",
    strict_table_only: bool = True,
) -> str:
    """Constructs a comprehensive, production-ready talent intelligence prompt."""
    focus_clause = f"\n- **Special Focus & Criteria:** {focus}" if focus else ""
    loc_clause = f"\n- **Geographic Scope:** {location}" if location else ""

    strict_instruction = (
        "Strict Requirement: Output ONLY the single Markdown table. Do not include introductory text, conversational greetings, commentary, or closing remarks."
        if strict_table_only
        else "Present findings in the standardized Markdown table accompanied by brief executive highlights."
    )

    prompt = f"""<talent_intelligence_request>
Identify and profile exactly {count} top-tier executive leaders matching the following criteria:

- **Target Role/Title:** {role}
- **Industry/Sector:** {industry}{loc_clause}{focus_clause}
- **Target Count (N):** {count}

<execution_guidelines>
1. Execute multi-angle targeted public searches across leadership pages, executive press releases, industry conferences, and verified business bios.
2. Ensure each profiled executive currently holds or recently held a verified senior leadership position in this domain.
3. Validate that all data points are derived from verifiable public sources.
4. Format the final output as a single Markdown table using the 7-column schema:
   `| # | Full Name | Current Position | Current Company | Relevant Background & Prior Experience | Key Expertise & Notable Achievements | Public Source URL |`
5. Ensure every Public Source URL is an active, clickable Markdown link formatted as `[Source Title / Domain](https://...)`.
</execution_guidelines>

<constraints>
- {strict_instruction}
- Do not include unverified or private personal information.
- All 7 columns are mandatory for each candidate.
</constraints>
</talent_intelligence_request>"""

    return prompt


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate specialized talent search prompts for Gemini Enterprise."
    )
    parser.add_argument(
        "--preset",
        choices=list(PROMPT_TEMPLATES.keys()),
        default=None,
        help="Use a pre-configured scenario preset",
    )
    parser.add_argument("--role", type=str, default="Chief Information Officer", help="Target executive role")
    parser.add_argument("--industry", type=str, default="Healthcare", help="Target industry")
    parser.add_argument("--count", type=int, default=5, help="Number of candidates (default: 5)")
    parser.add_argument("--focus", type=str, default="", help="Special technical or strategic focus areas")
    parser.add_argument("--location", type=str, default="United States", help="Geographic scope")
    parser.add_argument("--list-presets", action="store_true", help="List all available presets")
    parser.add_argument("--output", type=str, default=None, help="Save prompt to file")

    args = parser.parse_args()

    if args.list_presets:
        print("Available Preset Scenarios:")
        for key, p in PROMPT_TEMPLATES.items():
            print(f"  • {key:22}: {p['title']}")
        return 0

    if args.preset:
        preset = PROMPT_TEMPLATES[args.preset]
        prompt = build_system_and_user_prompt(
            role=preset["role"],
            industry=preset["industry"],
            count=int(preset["count"]),
            focus=preset["focus"],
        )
    else:
        prompt = build_system_and_user_prompt(
            role=args.role,
            industry=args.industry,
            count=args.count,
            focus=args.focus,
            location=args.location,
        )

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(prompt)
        print(f"Saved prompt to {args.output}", file=sys.stderr)
    else:
        print(prompt)

    return 0


if __name__ == "__main__":
    sys.exit(main())
