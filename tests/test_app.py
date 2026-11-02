"""Focused checks using only the existing Python standard library and Flask."""

from copy import deepcopy
from decimal import Decimal
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch

import app as app_module
from opportunity_data import OPPORTUNITIES
from scoring import POLICY, assess, dashboard_opportunities, ranked_opportunities


class ScoringChecks(unittest.TestCase):
    def test_policy_and_independent_known_example(self):
        self.assertEqual(sum(p["weight"] for p in POLICY.values()), 100)
        for policy in POLICY.values():
            self.assertEqual(sum(weight for _, weight in policy["factors"].values()), 100)
        result = assess(OPPORTUNITIES[0])
        # D=45+20+0+10+10=85, W=40+30+15+5=90, F=33.75+18.75+20+7.5=80.
        self.assertEqual([g["lower"] for g in result["groups"]], [85, 90, 80])
        self.assertEqual(result["lower"], 85.5)
        self.assertEqual(result["upper"], 85.5)

    def test_every_displayed_contribution_reconciles(self):
        for record in OPPORTUNITIES:
            result = assess(record)
            for bound in ("lower", "upper"):
                displayed_sum = sum(Decimal(str(g[f"contribution_{bound}"])) for g in result["groups"])
                self.assertEqual(displayed_sum, Decimal(str(result[bound])), record["firm"])
                for group in result["groups"]:
                    factor_sum = sum(Decimal(str(f[bound])) for f in group["factors"])
                    self.assertEqual(max(0, factor_sum - group["deduction"]), Decimal(str(group[bound])))

    def test_unknown_is_not_absence_or_normalised_away(self):
        record = deepcopy(OPPORTUNITIES[0])
        record["factors"]["hiring"]["activity"] = (None, "No comparable baseline")
        unknown = assess(record)
        record["factors"]["hiring"]["activity"] = (0, "Confirmed no uplift")
        absent = assess(record)
        self.assertEqual(unknown["groups"][0]["coverage"], 80)
        self.assertEqual(absent["groups"][0]["coverage"], 100)
        self.assertGreater(unknown["upper"], absent["upper"])
        self.assertEqual(unknown["lower"], absent["lower"])
        self.assertTrue(unknown["meaningful"])

    def test_unscored_and_identity_gate(self):
        self.assertFalse(assess(OPPORTUNITIES[5])["meaningful"])
        headline = assess(OPPORTUNITIES[6])
        self.assertFalse(headline["meaningful"])
        self.assertEqual((headline["lower"], headline["upper"]), (0, 100))
        record = deepcopy(OPPORTUNITIES[0])
        record["identity_resolved"] = False
        self.assertFalse(assess(record)["meaningful"])

    def test_restriction_overrides_score_and_ranking_is_deterministic(self):
        ranked = ranked_opportunities(OPPORTUNITIES)
        self.assertEqual(ranked[0]["id"], "alder-vale")
        self.assertEqual(ranked[-1]["id"], "kingsley-hart")
        self.assertTrue(ranked[-1]["assessment"]["blocked"])
        self.assertGreater(ranked[-1]["assessment"]["lower"], ranked[0]["assessment"]["lower"])
        self.assertEqual([r["id"] for r in ranked], [r["id"] for r in ranked_opportunities(list(reversed(OPPORTUNITIES)))])
        active_scores = [r["assessment"]["lower"] for r in ranked if r["assessment"]["meaningful"] and not r["assessment"]["blocked"]]
        self.assertEqual(active_scores, sorted(active_scores, reverse=True))

    def test_contrary_evidence_and_duplicate_coverage(self):
        record = deepcopy(OPPORTUNITIES[4])
        with_contrary = assess(record)
        del record["contrary"]
        without_contrary = assess(record)
        self.assertEqual(without_contrary["lower"] - with_contrary["lower"], 5)
        record = deepcopy(OPPORTUNITIES[6])
        original = assess(record)
        record["evidence"][0]["source_count"] = 100
        record["deal_value"] = 1000000000000
        self.assertEqual(assess(record), original)
        for record in OPPORTUNITIES:
            ids = [e["event_id"] for e in record["evidence"]]
            self.assertEqual(len(ids), len(set(ids)))

    def test_contacts_and_candidate_records(self):
        for record in OPPORTUNITIES:
            self.assertEqual(record["contact"]["firm"], record["firm"])
            self.assertEqual(set(record["contact"]), {"name", "title", "firm", "email", "phone"})
            self.assertTrue(all(record["contact"].values()))
            self.assertTrue(record["contact"]["email"].endswith(".example"))
            self.assertRegex(record["contact"]["phone"], r"^(\+44 20 7946 0\d{3}|\+1 305 555 01\d{2})$")
            self.assertEqual(len(record["briefing"]), 3)
            self.assertTrue(record["candidate_note"])
            for candidate in record["candidates"]:
                self.assertTrue(all(candidate[key] for key in ("name", "level", "experience", "location", "availability", "verify")))

    def test_dashboard_only_includes_fully_assessed_active_scored_records(self):
        records = dashboard_opportunities(OPPORTUNITIES)
        self.assertEqual([o["id"] for o in records], ["alder-vale", "marlowe-pierce", "calder-rowe"])
        self.assertEqual([o["rank"] for o in records], [1, 2, 3])
        self.assertEqual({o["location"] for o in records}, {"London", "Miami"})
        self.assertEqual({o["practice"] for o in records}, {"Private credit", "Corporate / M&A", "Funds"})
        self.assertEqual({o["status"] for o in records}, {"confirmed"})
        # Every area, not just the overall judgement, must be fully assessed.
        for area, factor in [("hiring", "timing"), ("access", "position"), ("delivery", "availability")]:
            incomplete = deepcopy(OPPORTUNITIES[0])
            incomplete["factors"][area][factor] = (None, "Unchecked")
            self.assertEqual(dashboard_opportunities([incomplete]), [])
        paused = deepcopy(OPPORTUNITIES[0])
        paused["status"] = "paused"
        self.assertEqual(dashboard_opportunities([paused]), [])


class RouteChecks(unittest.TestCase):
    def setUp(self):
        self.client = app_module.app.test_client()

    def test_existing_routes(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "ok"})
        self.assertEqual(self.client.get("/roles").json, {"roles": [
            {"id": 1, "title": "Corporate Associate", "location": "London"},
            {"id": 2, "title": "Legal Counsel", "location": "Miami"},
        ], "count": 2})

    def test_api_records_match_selected_team(self):
        response = self.client.get("/api/opportunities")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["as_of"], "2026-11-02")
        self.assertEqual(len(response.json["opportunities"]), 3)
        source = {o["id"]: o for o in OPPORTUNITIES}
        for record in response.json["opportunities"]:
            self.assertTrue(record["assessment"]["meaningful"])
            self.assertFalse(record["assessment"]["blocked"])
            self.assertTrue(all(g["coverage"] == 100 for g in record["assessment"]["groups"]))
            self.assertEqual(record["evidence"], source[record["id"]]["evidence"])
            self.assertEqual(record["candidates"], source[record["id"]]["candidates"])
            self.assertEqual(record["contact"], source[record["id"]]["contact"])

    def test_built_frontend_and_hashed_assets(self):
        self.assertTrue((app_module.FRONTEND_DIST / "index.html").is_file(), "Run npm --prefix frontend run build before these checks")
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Cache-Control"], "no-cache")
        assets = re.findall(r'(?:src|href)="(/assets/[^\"]+)"', response.text)
        self.assertGreaterEqual(len(assets), 2)
        response.close()
        for asset in assets:
            response = self.client.get(asset)
            self.assertEqual(response.status_code, 200, asset)
            self.assertIn("max-age=31536000", response.headers["Cache-Control"])
            self.assertNotIn("text/html", response.content_type)
            response.close()
        self.assertEqual(self.client.get("/assets/missing.js").status_code, 404)
        self.assertEqual(self.client.get("/api/missing").status_code, 404)
        self.assertEqual(self.client.get("/assets/../app.py").status_code, 404)

    def test_clear_message_if_frontend_has_not_been_built(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(app_module, "FRONTEND_DIST", Path(directory)):
            response = self.client.get("/")
            self.assertEqual(response.status_code, 503)
            self.assertIn("Frontend build needed", response.text)
            self.assertEqual(self.client.get("/health").status_code, 200)


if __name__ == "__main__":
    unittest.main()
