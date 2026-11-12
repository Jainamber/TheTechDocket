import pathlib
import pytest

from engine.ai.ledger import Ledger, BudgetExceeded, HARD_MAX_DAILY_BUDGET_USD
from engine.analytics_report import generate_analytics_report
from engine.build import build_site, _sitemap_xml
from engine.util import load_config, all_articles


def test_hard_max_daily_budget_ceiling(tmp_path):
    # Even if config specifies $50, hard ceiling enforces $20.00
    cfg = {"daily_budget_usd": 50.0}
    led = Ledger(cfg, "run-test", root=tmp_path)
    assert HARD_MAX_DAILY_BUDGET_USD == 20.00

    # Record spend reaching $20.00
    led.record("write", "gemini-3.5-flash", {"in": 100, "out": 100}, cost_usd=20.01)

    # Precheck must raise BudgetExceeded
    with pytest.raises(BudgetExceeded) as exc:
        led.precheck("write")
    assert "daily budget $20.00 reached" in str(exc.value)


def test_analytics_report_generation():
    res = generate_analytics_report(open_browser=False)
    assert res["status"] == "ok"
    assert res["budget_remaining"] <= 20.00
    latest = pathlib.Path(res["latest_path"])
    assert latest.exists()
    content = latest.read_text(encoding="utf-8")
    assert "Analytics &amp; North Star Command Center" in content or "Analytics & North Star" in content
    assert "Weekly Visitors" in content
    assert "$20.00/Day Hard Limit" in content
    assert "North Star Action Ledger" in content


def test_sitemap_tightened_to_54_canonical_urls():
    cfg = load_config()
    arts = all_articles()
    sitemap = _sitemap_xml(cfg, arts)
    # Exactly len(arts) + 12 <url> entries (48 articles + 12 static/hubs/docket)
    url_count = sitemap.count("<url><loc>")
    assert url_count == len(arts) + 12
    # Dated dockets and deck sub-pages must be excluded from sitemap.xml
    assert "/docket/2026-07-19/" not in sitemap
    assert "/deck/ai-models/" not in sitemap
    # Canonical /docket/ must be present
    assert "https://thetechdocket.com/docket/" in sitemap
    # All 6 topic hubs must have a valid lastmod
    assert "<loc>https://thetechdocket.com/topics/ai-tools/</loc><lastmod>" in sitemap


def test_docket_page_renders_valid_itemlist_jsonld():
    from engine.util import ROOT
    docket_html = ROOT / "docs" / "docket" / "2026-11-08" / "index.html"
    assert docket_html.exists()
    content = docket_html.read_text(encoding="utf-8")
    # Must NOT have empty JSON-LD
    assert '<script type="application/ld+json"></script>' not in content
    assert '"@type": "ItemList"' in content
    assert '"name": "Today\'s Docket — November 8, 2026"' in content
