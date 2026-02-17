#!/usr/bin/env python3
"""Regression checks for NDR live-submit guard matching logic."""

import importlib.util
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "fdr-ndr-fill.py"
SPEC = importlib.util.spec_from_file_location("fdr_ndr_fill", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load script module from {SCRIPT_PATH}")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class SubmitGuardMatcherTests(unittest.TestCase):
    def test_blocks_ndr_post_details(self):
        self.assertTrue(
            MODULE.should_block_live_submit_request(
                "ndr",
                "POST",
                "https://start.nationaldebtrelief.com/details?debtAmountLow=20000",
            )
        )

    def test_allows_ndr_get_details_navigation(self):
        self.assertFalse(
            MODULE.should_block_live_submit_request(
                "ndr",
                "GET",
                "https://start.nationaldebtrelief.com/details?debtAmountLow=20000",
            )
        )

    def test_allows_non_details_posts(self):
        self.assertFalse(
            MODULE.should_block_live_submit_request(
                "ndr",
                "POST",
                "https://start.nationaldebtrelief.com/personalizesavings",
            )
        )

    def test_allows_non_ndr_hosts(self):
        self.assertFalse(
            MODULE.should_block_live_submit_request(
                "ndr",
                "POST",
                "https://api.example.com/details",
            )
        )

    def test_only_ndr_offer_uses_guard(self):
        self.assertFalse(
            MODULE.should_block_live_submit_request(
                "fdr",
                "POST",
                "https://start.nationaldebtrelief.com/details",
            )
        )


if __name__ == "__main__":
    unittest.main()
