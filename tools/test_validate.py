#!/usr/bin/env python3
from pathlib import Path
import shutil
import tempfile
import unittest
import validate as v


class Tests(unittest.TestCase):
    def test_current_lists(self):
        data = v.validate()
        self.assertEqual(set(data), set(v.NAMES))
        self.assertEqual([len(data[n]) for n in v.NAMES], [41, 15, 4])

    def test_merge_preserves_exact_order_and_coverage(self):
        before = []
        for name in v.COMPAT_NAMES:
            before.extend(v.parse((v.ROOT / "rules" / name).read_text()))
        self.assertEqual(v.validate()["Claude.list"], before)

    def test_merge_guard_rejects_missing_reordered_and_edited_compat(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(v.ROOT / "rules", root / "rules")
            merged = root / "rules" / "Claude.list"
            original = merged.read_text()
            for modified in (
                original.replace("DOMAIN-SUFFIX,anthropic.com\n", ""),
                original.replace(
                    "DOMAIN-SUFFIX,anthropic.com\nDOMAIN-SUFFIX,anthropic.team",
                    "DOMAIN-SUFFIX,anthropic.team\nDOMAIN-SUFFIX,anthropic.com"),
            ):
                merged.write_text(modified)
                with self.assertRaises(ValueError):
                    v.validate(root)
            merged.write_text(original)
            compat = root / "rules" / v.COMPAT_NAMES[0]
            compat.write_text(compat.read_text() + "# edited\n")
            with self.assertRaises(ValueError):
                v.validate(root)

    def test_invalid_or_unsafe_rules(self):
        for text in (
            "", "DOMAIN-SUFFIX,example.com,DIRECT", "DOMAIN-KEYWORD,claude",
            "IP-CIDR,10.0.0.0/8,no-resolve", "IP-CIDR,8.8.8.0/24",
            "IP-ASN,0,no-resolve", "IP-CIDR6,8.8.8.0/24,no-resolve",
            "DOMAIN,https://example.com", "FINAL,Proxy",
        ):
            with self.subTest(text=text), self.assertRaises(ValueError):
                v.parse(text)

    def test_duplicates(self):
        with self.assertRaises(ValueError):
            v.parse("DOMAIN,example.com\nDOMAIN,example.com\n")

    def test_comments_and_parameters(self):
        self.assertEqual(v.parse("# example\nIP-ASN,399358,no-resolve\n"),
                         [("IP-ASN", "399358", "no-resolve")])


if __name__ == "__main__":
    unittest.main()
