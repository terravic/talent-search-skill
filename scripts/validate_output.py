#!/usr/bin/env python3
"""
Talent Search Output Validator
==============================
Validates that generated talent intelligence tables strictly comply with
executive formatting, column schema, link validity, and strict output constraints.
"""

from __future__ import annotations

import argparse
import re
import sys
from typing import List, Tuple


REQUIRED_HEADERS = [
    "#",
    "full name",
    "current position",
    "current company",
    "relevant background",
    "key expertise",
    "public source url",
]


def validate_markdown_output(
    content: str,
    min_candidates: int = 1,
    strict_no_filler: bool = False,
) -> Tuple[bool, List[str], List[str]]:
    """
    Validates Markdown table content against Talent Intelligence Agent standards.

    Returns:
        (is_valid, error_messages, warning_messages)
    """
    errors: List[str] = []
    warnings: List[str] = []

    lines = content.strip().splitlines()
    if not lines:
        errors.append("Input content is empty.")
        return False, errors, warnings

    # 1. Strict filler check (No non-table conversational text)
    if strict_no_filler:
        non_table_lines = [
            l.strip()
            for l in lines
            if l.strip() and not (l.strip().startswith("|") and l.strip().endswith("|"))
        ]
        if non_table_lines:
            errors.append(
                f"Strict Mode Violation: Found {len(non_table_lines)} non-table lines (e.g., conversational filler, preamble, or footer). "
                f"First non-table line: '{non_table_lines[0]}'"
            )

    # 2. Extract Table lines
    table_lines = [
        l.strip()
        for l in lines
        if l.strip().startswith("|") and l.strip().endswith("|")
    ]

    if len(table_lines) < 3:
        errors.append(
            f"Insufficient table rows found. Expected at least header, separator, and 1 data row. Found {len(table_lines)} rows."
        )
        return False, errors, warnings

    # 3. Check Header Columns
    header_line = table_lines[0]
    header_cols = [c.strip().lower() for c in header_line.split("|")[1:-1]]

    if len(header_cols) < 7:
        errors.append(
            f"Table header must have exactly 7 columns. Found {len(header_cols)}: {header_cols}"
        )
    else:
        for idx, req in enumerate(REQUIRED_HEADERS):
            if req not in header_cols[idx]:
                warnings.append(
                    f"Header column {idx+1} is '{header_cols[idx]}', expected match for '{req}'"
                )

    # 4. Check Separator Row
    separator_line = table_lines[1]
    sep_cols = [c.strip() for c in separator_line.split("|")[1:-1]]
    if not all(re.match(r"^:?-+:?$", s) for s in sep_cols if s):
        errors.append(f"Invalid Markdown table delimiter row: '{separator_line}'")

    # 5. Check Data Rows
    data_rows = table_lines[2:]
    if len(data_rows) < min_candidates:
        errors.append(
            f"Insufficient candidate profiles. Expected at least {min_candidates}, found {len(data_rows)}."
        )

    for row_idx, row in enumerate(data_rows, start=1):
        cols = [c.strip() for c in row.split("|")[1:-1]]
        if len(cols) != 7:
            errors.append(
                f"Row {row_idx} has {len(cols)} columns instead of the required 7. Line: '{row}'"
            )
            continue

        idx_val, name, pos, comp, bg, exp, src = cols

        # Check required fields
        if not name or name.upper() == "N/A":
            errors.append(f"Row {row_idx}: 'Full Name' cannot be empty.")
        if not pos or pos.upper() == "N/A":
            errors.append(f"Row {row_idx}: 'Current Position' cannot be empty.")
        if not comp or comp.upper() == "N/A":
            errors.append(f"Row {row_idx}: 'Current Company' cannot be empty.")

        # Check URL validity
        url_match = re.search(r"https?://[^\s\)\>]+", src)
        if not url_match:
            errors.append(
                f"Row {row_idx}: 'Public Source URL' must contain a valid HTTP/HTTPS URL. Found: '{src}'"
            )
        else:
            url = url_match.group(0)
            if not ("http://" in url or "https://" in url):
                errors.append(f"Row {row_idx}: Malformed URL: '{url}'")

        # Check link markdown formatting recommendation
        if not re.search(r"\[.+?\]\(https?://[^\s\)]+\)", src):
            warnings.append(
                f"Row {row_idx}: Public Source URL '{src}' should ideally be formatted as a Markdown link `[Source Title](URL)`."
            )

    is_valid = len(errors) == 0
    return is_valid, errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate Markdown output against Talent Intelligence Agent standards."
    )
    parser.add_argument(
        "--input",
        type=str,
        default=None,
        help="Path to Markdown file to validate (reads from stdin if omitted)",
    )
    parser.add_argument(
        "--min-candidates",
        type=int,
        default=1,
        help="Minimum number of candidate rows expected (default: 1)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Enforce zero conversational filler / preambles / footers outside the Markdown table",
    )

    args = parser.parse_args()

    if args.input:
        try:
            with open(args.input, "r", encoding="utf-8") as f:
                content = f.read()
        except OSError as e:
            print(f"Error reading file '{args.input}': {e}", file=sys.stderr)
            return 1
    else:
        content = sys.stdin.read()

    is_valid, errors, warnings = validate_markdown_output(
        content=content,
        min_candidates=args.min_candidates,
        strict_no_filler=args.strict,
    )

    print("=" * 60)
    print(" Talent Search Output Validation Report")
    print("=" * 60)

    if warnings:
        print(f"\n[!] Warnings ({len(warnings)}):")
        for w in warnings:
            print(f"  - {w}")

    if errors:
        print(f"\n[X] Validation Failed with {len(errors)} error(s):")
        for e in errors:
            print(f"  - {e}")
        print("\nStatus: FAILED")
        return 1
    else:
        print("\n[✓] Validation Passed! Table strictly complies with executive specifications.")
        print("Status: PASSED")
        return 0


if __name__ == "__main__":
    sys.exit(main())
