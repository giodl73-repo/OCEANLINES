import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROLES = ROOT / ".roles"
EXPECTED = {
    "current": ("physical-oceanographer", 1),
    "sounder": ("climate-data-steward", 2),
    "chart": ("ocean-cartographer", 3),
    "beacon": ("public-science-editor", 4),
    "harbor": ("accessibility-reviewer", 5),
    "keel": ("reproducibility-engineer", 6),
    "logbook": ("repository-steward", 7),
    "orbit": ("planetary-comparison-reviewer", 8),
}


class RoleRosterTests(unittest.TestCase):
    def test_index_names_every_role(self):
        index = (ROLES / "ROLE.md").read_text(encoding="utf-8")
        for role in EXPECTED:
            self.assertIn(f"**{role.upper()}**", index)

    def test_roster_is_exact_and_functional(self):
        files = {path.stem for path in ROLES.glob("*.md") if path.name != "ROLE.md"}
        self.assertEqual(files, set(EXPECTED))

    def test_role_contracts(self):
        positions = []
        for role, (archetype, position) in EXPECTED.items():
            text = (ROLES / f"{role}.md").read_text(encoding="utf-8")
            self.assertTrue(text.startswith("---\n"))
            self.assertIn(f"name: {role}", text)
            self.assertIn(f"archetype: {archetype}", text)
            self.assertIn(f"tiebreaker_position: {position}", text)
            self.assertIn("## Verify", text)
            self.assertIn("## Key question", text)
            checks = re.findall(r"^- ", text, flags=re.MULTILINE)
            self.assertGreaterEqual(len(checks), 6)
            positions.append(position)
        self.assertEqual(sorted(positions), list(range(1, len(EXPECTED) + 1)))


if __name__ == "__main__":
    unittest.main()
