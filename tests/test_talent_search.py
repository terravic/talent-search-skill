"""
Unit tests for Talent Search CLI & Data Engine.
"""

import json
import unittest
from scripts.talent_search import (
    CandidateProfile,
    SearchStrategy,
    render_markdown_table,
    render_json,
    render_csv,
    parse_markdown_table,
    get_curated_sample_profiles,
)


class TestTalentSearchEngine(unittest.TestCase):

    def setUp(self):
        self.sample_candidate = CandidateProfile(
            index=1,
            name="Jane Doe, PhD",
            position="VP of Clinical AI",
            company="HealthCorp Global",
            background="Former Director of AI at MedTech Inc. PhD in Computer Science from MIT.",
            expertise="Large Language Models in EHR, ambient scribe development, HIPAA-compliant cloud architectures.",
            source_url="https://example.com/leadership/jane-doe",
            source_title="HealthCorp Leadership Bio",
        )

    def test_candidate_to_markdown_row(self):
        row = self.sample_candidate.to_markdown_row()
        self.assertTrue(row.startswith("| 1 | Jane Doe, PhD | VP of Clinical AI |"))
        self.assertIn("[HealthCorp Leadership Bio](https://example.com/leadership/jane-doe)", row)
        self.assertEqual(row.count("|"), 8)

    def test_candidate_validation_success(self):
        errors = self.sample_candidate.validate()
        self.assertEqual(len(errors), 0)

    def test_candidate_validation_failure(self):
        invalid_candidate = CandidateProfile(
            index=1,
            name="",
            position="VP",
            company="",
            background="Test",
            expertise="Test",
            source_url="not-a-url",
        )
        errors = invalid_candidate.validate()
        self.assertGreaterEqual(len(errors), 3)
        self.assertTrue(any("Full Name" in e for e in errors))
        self.assertTrue(any("Current Company" in e for e in errors))
        self.assertTrue(any("Source URL" in e for e in errors))

    def test_search_strategy_generation(self):
        strategy = SearchStrategy.generate(
            role="Chief Information Security Officer",
            industry="Healthcare",
            location="United States",
            keywords=["Zero Trust", "HITRUST"],
        )
        self.assertEqual(strategy.role, "Chief Information Security Officer")
        self.assertEqual(strategy.industry, "Healthcare")
        self.assertEqual(len(strategy.queries), 6)
        self.assertTrue(any("site:businesswire.com" in q for q in strategy.queries))
        self.assertTrue(any("site:linkedin.com/in" in q for q in strategy.queries))
        self.assertTrue(any("HITRUST" in q for q in strategy.queries))

    def test_render_and_parse_markdown_table(self):
        candidates = get_curated_sample_profiles("cio")
        self.assertEqual(len(candidates), 5)

        table_md = render_markdown_table(candidates)
        self.assertIn("| # | Full Name | Current Position |", table_md)

        # Parse back
        parsed = parse_markdown_table(table_md)
        self.assertEqual(len(parsed), 5)
        self.assertEqual(parsed[0].name, candidates[0].name)
        self.assertEqual(parsed[0].company, candidates[0].company)
        self.assertTrue(parsed[0].source_url.startswith("https://"))

    def test_json_and_csv_export(self):
        candidates = get_curated_sample_profiles("actuary")
        json_out = render_json(candidates)
        data = json.loads(json_out)
        self.assertEqual(len(data), 5)
        self.assertEqual(data[0]["current_position"], candidates[0].position)

        csv_out = render_csv(candidates)
        self.assertIn("full_name,current_position", csv_out)
        self.assertIn("Sarah Jenkins", csv_out)


if __name__ == "__main__":
    unittest.main()
