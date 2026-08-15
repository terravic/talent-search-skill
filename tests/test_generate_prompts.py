"""
Unit tests for Prompt Generator.
"""

import unittest
from scripts.generate_prompts import build_system_and_user_prompt, PROMPT_TEMPLATES


class TestPromptGenerator(unittest.TestCase):

    def test_custom_prompt_generation(self):
        prompt = build_system_and_user_prompt(
            role="Chief Medical Officer",
            industry="Integrated Delivery Networks",
            count=5,
            focus="Ambient AI clinical documentation",
            location="United States",
            strict_table_only=True,
        )
        self.assertIn("Chief Medical Officer", prompt)
        self.assertIn("Integrated Delivery Networks", prompt)
        self.assertIn("Ambient AI clinical documentation", prompt)
        self.assertIn("Output ONLY the single Markdown table", prompt)
        self.assertIn("<talent_intelligence_request>", prompt)

    def test_presets_exist(self):
        self.assertIn("healthcare_cio", PROMPT_TEMPLATES)
        self.assertIn("chief_actuary", PROMPT_TEMPLATES)
        self.assertIn("vp_healthcare_ai", PROMPT_TEMPLATES)


if __name__ == "__main__":
    unittest.main()
