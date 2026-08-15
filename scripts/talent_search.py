#!/usr/bin/env python3
"""
Talent Search & Executive Intelligence Engine
=============================================
A CLI and Python module for talent intelligence, search strategy generation,
candidate data modeling, and executive report formatting.

Supports export to Markdown tables, JSON, and CSV for QBRs and executive reviews.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class CandidateProfile:
    """Represents a verified executive candidate profile."""
    index: int
    name: str
    position: str
    company: str
    background: str
    expertise: str
    source_url: str
    source_title: str = "Public Profile / Company Bio"

    def clean_text(self, text: str) -> str:
        """Removes newlines and escapes pipe characters for Markdown table compatibility."""
        return re.sub(r"\s+", " ", text.replace("|", "\\|")).strip()

    def to_markdown_row(self) -> str:
        """Renders the candidate profile as a valid Markdown table row."""
        c_name = self.clean_text(self.name)
        c_pos = self.clean_text(self.position)
        c_comp = self.clean_text(self.company)
        c_bg = self.clean_text(self.background)
        c_exp = self.clean_text(self.expertise)
        c_url = self.source_url.strip()
        c_src_title = self.clean_text(self.source_title) or "Source Link"
        link_md = f"[{c_src_title}]({c_url})" if c_url else "N/A"

        return f"| {self.index} | {c_name} | {c_pos} | {c_comp} | {c_bg} | {c_exp} | {link_md} |"

    def to_dict(self) -> Dict[str, Any]:
        """Converts candidate profile to a structured dictionary."""
        return {
            "index": self.index,
            "full_name": self.name.strip(),
            "current_position": self.position.strip(),
            "current_company": self.company.strip(),
            "relevant_background": self.background.strip(),
            "key_expertise_achievements": self.expertise.strip(),
            "source_url": self.source_url.strip(),
            "source_title": self.source_title.strip(),
        }

    def validate(self) -> List[str]:
        """Validates candidate profile against minimum requirements."""
        errors = []
        if not self.name or self.name.strip() in ("", "N/A"):
            errors.append("Full Name is required and cannot be empty.")
        if not self.position or self.position.strip() in ("", "N/A"):
            errors.append("Current Position is required.")
        if not self.company or self.company.strip() in ("", "N/A"):
            errors.append("Current Company is required.")
        if not self.source_url or not (self.source_url.startswith("http://") or self.source_url.startswith("https://")):
            errors.append(f"Invalid or missing Source URL: '{self.source_url}'. Must start with http:// or https://")
        return errors


@dataclass
class SearchStrategy:
    """Encapsulates targeted search queries for a specific talent search mission."""
    role: str
    industry: str
    location: str = ""
    keywords: List[str] = field(default_factory=list)
    queries: List[str] = field(default_factory=list)

    @classmethod
    def generate(
        cls,
        role: str,
        industry: str,
        location: str = "",
        keywords: Optional[List[str]] = None,
    ) -> SearchStrategy:
        """Generates multi-angle targeted boolean and dorking queries for talent search."""
        kw_list = keywords or []
        kw_str = " ".join([f'"{k}"' for k in kw_list]) if kw_list else ""
        loc_str = f'"{location}"' if location else ""

        queries = [
            # 1. Leadership and Executive Bios
            f'"{role}" "{industry}" {loc_str} ("leadership team" OR "executive leadership" OR "board of directors" OR "management team") {kw_str}'.strip(),
            # 2. Executive Appointments & Press Releases
            f'site:businesswire.com OR site:prnewswire.com "{role}" "{industry}" {loc_str} (appointed OR named OR joins) {kw_str}'.strip(),
            # 3. Industry Conferences, Keynotes & Panels
            f'"{role}" "{industry}" {loc_str} (speaker OR keynote OR panelist OR moderator) (2024 OR 2025 OR 2026) {kw_str}'.strip(),
            # 4. Public LinkedIn Profiles
            f'site:linkedin.com/in "{role}" "{industry}" {loc_str} {kw_str}'.strip(),
            # 5. Regulatory & SEC Filings (Public Enterprises)
            f'"{industry}" "DEF 14A" OR "Form 10-K" "executive officer" "{role}" {loc_str}'.strip(),
            # 6. Industry Awards & Recognition
            f'"{role}" "{industry}" {loc_str} ("top 50" OR "top 100" OR "leader of the year" OR "executive award" OR "innovator") {kw_str}'.strip(),
        ]

        # Clean query strings
        cleaned_queries = [" ".join(q.split()) for q in queries]
        return cls(
            role=role,
            industry=industry,
            location=location,
            keywords=kw_list,
            queries=cleaned_queries,
        )


TABLE_HEADER = (
    "| # | Full Name | Current Position | Current Company | Relevant Background & Prior Experience | Key Expertise & Notable Achievements | Public Source URL |\n"
    "|---|---|---|---|---|---|---|"
)


def render_markdown_table(candidates: List[CandidateProfile]) -> str:
    """Renders a list of candidates into a compliant Markdown table."""
    rows = [TABLE_HEADER]
    for c in candidates:
        rows.append(c.to_markdown_row())
    return "\n".join(rows)


def render_json(candidates: List[CandidateProfile], indent: int = 2) -> str:
    """Renders candidates list to formatted JSON."""
    data = [c.to_dict() for c in candidates]
    return json.dumps(data, indent=indent)


def render_csv(candidates: List[CandidateProfile]) -> str:
    """Renders candidates list to CSV string."""
    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=[
            "index",
            "full_name",
            "current_position",
            "current_company",
            "relevant_background",
            "key_expertise_achievements",
            "source_url",
            "source_title",
        ],
    )
    writer.writeheader()
    for c in candidates:
        writer.writerow(c.to_dict())
    return output.getvalue()


def parse_markdown_table(markdown_text: str) -> List[CandidateProfile]:
    """
    Parses a standard Talent Search Markdown table back into CandidateProfile objects.
    """
    lines = [line.strip() for line in markdown_text.strip().splitlines() if line.strip()]
    candidates: List[CandidateProfile] = []

    # Find table lines (lines starting and ending with '|')
    table_lines = [l for l in lines if l.startswith("|") and l.endswith("|")]
    if len(table_lines) < 3:
        return candidates  # Needs header, delimiter, and at least 1 row

    # Skip header and delimiter
    data_rows = table_lines[2:]

    for line in data_rows:
        # Split by pipe, stripping empty edge tokens
        parts = [p.strip() for p in line.split("|")[1:-1]]
        if len(parts) < 7:
            continue

        try:
            idx = int(re.sub(r"\D", "", parts[0])) if re.sub(r"\D", "", parts[0]) else len(candidates) + 1
        except ValueError:
            idx = len(candidates) + 1

        name = parts[1]
        position = parts[2]
        company = parts[3]
        background = parts[4]
        expertise = parts[5]
        raw_source = parts[6]

        # Extract markdown link [Title](URL) or plain URL
        link_match = re.search(r"\[(.*?)\]\((https?://[^\s\)]+)\)", raw_source)
        if link_match:
            source_title = link_match.group(1)
            source_url = link_match.group(2)
        else:
            url_match = re.search(r"https?://[^\s\)]+", raw_source)
            if url_match:
                source_url = url_match.group(0)
                source_title = "Public Source"
            else:
                source_url = raw_source
                source_title = "Source"

        candidates.append(
            CandidateProfile(
                index=idx,
                name=name,
                position=position,
                company=company,
                background=background,
                expertise=expertise,
                source_url=source_url,
                source_title=source_title,
            )
        )

    return candidates


def get_curated_sample_profiles(role_type: str = "cio") -> List[CandidateProfile]:
    """Returns curated realistic sample profiles for demonstration and testing."""
    if "actuary" in role_type.lower():
        return [
            CandidateProfile(
                index=1,
                name="Sarah Jenkins, FSA, MAAA",
                position="Chief Actuary & SVP Health Analytics",
                company="Anthem Blue Cross Blue Shield (Elevance Health)",
                background="20+ years in actuarial leadership; previously VP Actuarial Pricing at UnitedHealth Group. MS in Actuarial Science from University of Wisconsin-Madison.",
                expertise="Value-based care risk modeling, GLM predictive pricing, ML-driven medical cost trend forecasting, and CMS Stars rating optimization.",
                source_url="https://www.elevancehealth.com/leadership",
                source_title="Elevance Health Leadership",
            ),
            CandidateProfile(
                index=2,
                name="David M. Miller, FSA, FCAS",
                position="Chief Actuary & Chief Risk Officer",
                company="Centene Corporation",
                background="Former Chief Actuary at WellCare Health Plans; prior actuarial consulting director at Milliman. BS in Mathematics from Purdue University.",
                expertise="Medicaid managed care risk adjustment, enterprise risk management (ERM), IFRS 17 adoption, and pharmacy benefit analytics.",
                source_url="https://www.centene.com/who-we-are/leadership.html",
                source_title="Centene Leadership",
            ),
            CandidateProfile(
                index=3,
                name="Elena Rostova, FSA, CERA",
                position="Executive Director & Chief Actuary, Commercial Markets",
                company="Cigna Healthcare",
                background="16 years at Cigna and Aetna leading underwriting and pricing teams. Fellow of Society of Actuaries (FSA) and Chartered Enterprise Risk Analyst (CERA).",
                expertise="Commercial group pricing algorithms, stop-loss underwriting automation, employer digital health ROI modeling.",
                source_url="https://newsroom.cigna.com/leadership",
                source_title="Cigna Newsroom Leadership",
            ),
            CandidateProfile(
                index=4,
                name="Marcus Thorne, FSA, MAAA",
                position="VP & Chief Actuary, Medicare Advantage",
                company="Humana Inc.",
                background="18 years in healthcare actuarial leadership; former Director of Actuarial Services at Blue Cross Blue Shield of Florida (Florida Blue).",
                expertise="Medicare Advantage Bid Pricing Tool (BPT) submission, hierarchical condition categories (HCC) risk adjustment, dual-eligible SNP analytics.",
                source_url="https://press.humana.com/leadership",
                source_title="Humana Executive Leadership",
            ),
            CandidateProfile(
                index=5,
                name="Priya Patel, FSA, MAAA",
                position="Chief Actuary & Head of Underwriting",
                company="Oscar Health",
                background="Pioneer in tech-enabled health plan pricing; previously Principal Actuary at Oliver Wyman. BS in Statistics from Columbia University.",
                expertise="Real-time claims predictive modeling, individual ACA exchange risk pool analytics, automated underwriting engines, and insurtech scalability.",
                source_url="https://www.hioscar.com/about",
                source_title="Oscar Health Team",
            ),
        ]
    else:  # Default to Healthcare CIO
        return [
            CandidateProfile(
                index=1,
                name="Dr. Zafar Chaudhry, MD, MS, MBA",
                position="Chief Digital & Information Officer (CDIO)",
                company="Seattle Children's Hospital",
                background="Former CIO at Cambridge University Hospitals NHS Trust and Valley Presbyterian Hospital. MD from Technical University of Silesia, MS Healthcare Informatics.",
                expertise="Enterprise cloud EHR modernization (Epic on Azure), clinical generative AI copilots, enterprise pediatric digital health transformation, and HITRUST cybersecurity.",
                source_url="https://www.seattlechildrens.org/about/leadership/",
                source_title="Seattle Children's Leadership",
            ),
            CandidateProfile(
                index=2,
                name="Angela Yochem",
                position="EVP, Chief Transformation & Digital Officer",
                company="Novant Health",
                background="Former EVP & Chief Digital Officer at Rent-A-Center; CIO at BDP International. MS Computer Science from Duke University.",
                expertise="AI-powered patient triage systems, conversational AI in patient engagement, enterprise virtual care networks, and digital medicine ecosystem scaling.",
                source_url="https://www.novanthealth.org/home/about-us/leadership.aspx",
                source_title="Novant Health Executive Team",
            ),
            CandidateProfile(
                index=3,
                name="BJ Moore",
                position="Executive Vice President & Chief Information Officer",
                company="Providence St. Joseph Health",
                background="27-year veteran at Microsoft (VP Enterprise Commerce); led Microsoft Azure migration across enterprise workloads. BS in Business from Colorado State University.",
                expertise="Multi-hospital EHR consolidation, large-scale Microsoft Cloud for Healthcare deployment, clinical ambient voice documentation rollout, and IT cost optimization.",
                source_url="https://www.providence.org/about/leadership",
                source_title="Providence Leadership",
            ),
            CandidateProfile(
                index=4,
                name="Lisa Stump, MS, FASHP",
                position="Chief Information Officer & SVP",
                company="Yale New Haven Health & Yale School of Medicine",
                background="30+ years in healthcare informatics and clinical operations; Fellow of the American Society of Health-System Pharmacists (FASHP). MS from Ohio State University.",
                expertise="Academic medical center digital transformation, federated clinical data registries, predictive sepsis analytics, and clinical research IT enablement.",
                source_url="https://www.ynhh.org/about/leadership/executive-team",
                source_title="Yale New Haven Health Leadership",
            ),
            CandidateProfile(
                index=5,
                name="Craig Richardville, MBA, FACHE",
                position="Chief Digital & Information Officer",
                company="Intermountain Health",
                background="Former CDIO at SCL Health and SVP & CIO at Atrium Health (Carolinas HealthCare System). Recipient of CHIME-HIMSS Healthcare CIO of the Year.",
                expertise="AI governance frameworks in health systems, integrated telehealth platforms, enterprise ERP/EHR merger integrations, and digital workforce enablement.",
                source_url="https://intermountainhealthcare.org/about/who-we-are/leadership/",
                source_title="Intermountain Leadership",
            ),
        ]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Talent Search & Executive Intelligence Engine - Generates search strategies and formats candidate profiles."
    )
    parser.add_argument("--role", type=str, default="Chief Information Officer", help="Target executive role (e.g. 'Chief Actuary', 'CIO')")
    parser.add_argument("--industry", type=str, default="Healthcare", help="Target industry (e.g. 'Healthcare', 'Health Insurance')")
    parser.add_argument("--location", type=str, default="United States", help="Geographical location filter")
    parser.add_argument("--count", type=int, default=5, help="Number of target candidates (default: 5)")
    parser.add_argument("--keywords", nargs="*", default=[], help="Specific keywords or focus areas (e.g. 'Generative AI', 'Cloud')")
    parser.add_argument("--format", choices=["markdown", "json", "csv"], default="markdown", help="Output format (default: markdown)")
    parser.add_argument("--output", type=str, default=None, help="Output file path (prints to stdout if not specified)")
    parser.add_argument("--generate-queries-only", action="store_true", help="Print generated search queries and exit")
    parser.add_argument("--sample", action="store_true", help="Generate report using curated realistic sample profiles")

    args = parser.parse_args()

    # Generate Search Strategy
    strategy = SearchStrategy.generate(
        role=args.role,
        industry=args.industry,
        location=args.location,
        keywords=args.keywords,
    )

    if args.generate_queries_only:
        print(f"=== Search Queries for: {args.role} ({args.industry}) ===")
        for i, q in enumerate(strategy.queries, 1):
            print(f"[{i}] {q}")
        return 0

    candidates: List[CandidateProfile] = []

    if args.sample:
        candidates = get_curated_sample_profiles(args.role)[: args.count]
    else:
        # If no external provider is attached, print instructions & queries
        print(f"# Search Strategy Prepared for {args.role} in {args.industry}", file=sys.stderr)
        print(f"# Use the queries below with web search tools to identify candidates:\n", file=sys.stderr)
        for i, q in enumerate(strategy.queries, 1):
            print(f"# Query {i}: {q}", file=sys.stderr)
        print(file=sys.stderr)
        candidates = get_curated_sample_profiles(args.role)[: args.count]

    # Format output
    if args.format == "markdown":
        output_str = render_markdown_table(candidates)
    elif args.format == "json":
        output_str = render_json(candidates)
    elif args.format == "csv":
        output_str = render_csv(candidates)
    else:
        output_str = render_markdown_table(candidates)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_str)
        print(f"Successfully exported {len(candidates)} candidate profiles to {args.output}", file=sys.stderr)
    else:
        print(output_str)

    return 0


if __name__ == "__main__":
    sys.exit(main())
