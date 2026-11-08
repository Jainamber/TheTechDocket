import pathlib
import pytest

from engine.share import build_share_kit, _suggest_subreddits
from engine.build import _llms_txt, _robots_txt
from engine.util import load_config, all_articles


def test_suggest_subreddits_mapping():
    assert "pcmasterrace" in _suggest_subreddits("ai-tools")
    assert "LocalLLaMA" in _suggest_subreddits("ai-models")
    assert "technology" in _suggest_subreddits("unknown-hub")


def test_build_share_kit_generates_markdown():
    res = build_share_kit(slug="discord-kills-electron-rust-windows-11",
                          chosen_sub="developersIndia",
                          open_browser=False)
    assert res["slug"] == "discord-kills-electron-rust-windows-11"
    assert res["primary_sub"] == "developersIndia"
    assert "reddit.com/r/developersIndia/submit" in res["reddit_url"]
    assert "type=TEXT" in res["reddit_url"]
    path = pathlib.Path(res["path"])
    assert path.exists()
    content = path.read_text(encoding="utf-8")
    assert "https://thetechdocket.com/articles/discord-kills-electron-rust-windows-11/" in content
    assert "news.ycombinator.com/submitlink" in content
    assert "reddit.com/r/developersIndia/submit" in content
    assert "x.com/intent/tweet" in content
    assert "canonical_url:" in content


def test_llms_txt_and_robots_txt_spec():
    cfg = load_config()
    arts = all_articles()
    llms = _llms_txt(cfg, arts)
    assert "# The Tech Docket" in llms
    assert "https://thetechdocket.com/sitemap.xml" in llms
    assert "https://thetechdocket.com/docket/" in llms
    assert "https://thetechdocket.com/articles/discord-kills-electron-rust-windows-11/" in llms

    robots = _robots_txt(cfg)
    assert "User-agent: OAI-SearchBot" in robots
    assert "User-agent: PerplexityBot" in robots
    assert "User-agent: Claude-SearchBot" in robots
    assert "User-agent: Google-Extended" in robots
    assert "User-agent: Applebot-Extended" in robots
    assert "User-agent: Meta-ExternalAgent" in robots
