"""
Unit tests for Output Validator.
"""

import unittest
from scripts.validate_output import validate_markdown_output
from scripts.talent_search import render_markdown_table, get_curated_sample_profiles


class TestOutputValidator(unittest.TestCase):

    def setUp(self):
        self.valid_candidates = get_curated_sample_profiles("cio")
        self.valid_table = render_markdown_table(self.valid_candidates)

    def test_valid_table_passes(self):
        is_valid, errors, warnings = validate_markdown_output(
            content=self.valid_table,
            min_candidates=5,
            strict_no_filler=True,
        )
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)

    def test_strict_mode_catches_filler(self):
        table_with_filler = f"Here is the executive talent table you requested:\n\n{self.valid_table}\n\nHope this helps with your QBR!"
        is_valid, errors, warnings = validate_markdown_output(
            content=table_with_filler,
            min_candidates=5,
            strict_no_filler=True,
        )
        self.assertFalse(is_valid)
        self.assertTrue(any("Strict Mode Violation" in e for e in errors))

    def test_missing_candidate_count(self):
        is_valid, errors, warnings = validate_markdown_output(
            content=self.valid_table,
            min_candidates=10,  # Only 5 exist
            strict_no_filler=False,
        )
        self.assertFalse(is_valid)
        self.assertTrue(any("Insufficient candidate profiles" in e for e in errors))

    def test_invalid_url_fails(self):
        malformed_table = (
            "| # | Full Name | Current Position | Current Company | Relevant Background & Prior Experience | Key Expertise & Notable Achievements | Public Source URL |\n"
            "|---|---|---|---|---|---|---|\n"
            "| 1 | Jane Doe | VP Engineering | Acme Health | 15 yrs exp | AI systems | [No URL](invalid-url) |"
        )
        is_valid, errors, warnings = validate_markdown_output(
            content=malformed_table,
            min_candidates=1,
            strict_no_filler=False,
        )
        self.assertFalse(is_valid)
        self.assertTrue(any("Public Source URL" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
