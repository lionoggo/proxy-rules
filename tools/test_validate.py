#!/usr/bin/env python3
import unittest
import validate as v


class Tests(unittest.TestCase):
    def test_current_lists(self):
        data = v.validate()
        self.assertEqual(set(data), set(v.NAMES))
        self.assertEqual([len(data[n]) for n in v.NAMES], [23, 9, 3, 6, 15, 4])

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
