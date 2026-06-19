#!/usr/bin/env python3
from pathlib import Path


root = Path(__file__).resolve().parents[1]
skill = root / "SKILL.md"
text = skill.read_text(encoding="utf-8")
assert text.startswith("---\n"), "SKILL.md is missing YAML frontmatter"
frontmatter = text.split("---", 2)[1]
required = {"name", "description"}
seen = set()
for line in frontmatter.splitlines():
    if not line.strip() or line.strip().startswith("#"):
        continue
    key = line.split(":", 1)[0].strip()
    if key:
        seen.add(key)
missing = required - seen
assert not missing, f"SKILL.md missing frontmatter keys: {', '.join(sorted(missing))}"
print("frontmatter ok")
