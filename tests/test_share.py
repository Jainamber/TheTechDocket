import pathlib
import pytest

from engine.share import build_share_kit, _suggest_subreddits, _get_flair
from engine.reddit_api import is_configured, find_matching_flair_id
from engine.build import _llms_txt, _robots_txt
from engine.util import load_config, all_articles


def test_suggest_subreddits_mapping():
    assert "pcmasterrace" in _suggest_subreddits("ai-tools")
    assert "LocalLLaMA" in _suggest_subreddits("ai-models")
    assert "technology" in _suggest_subreddits("unknown-hub")


def test_reddit_flair_mapping_and_api():
    assert _get_flair("developersIndia") == "News"
    assert _get_flair("pcmasterrace") == "Discussion"
    assert not is_configured()  # when env vars are unset
    flairs = [{"id": "uuid-1", "text": "Discussion"}, {"id": "uuid-2", "text": "News"}]
    assert find_matching_flair_id(flairs, "News") == "uuid-2"
    assert find_matching_flair_id(flairs, "Discussion") == "uuid-1"


def test_build_share_kit_generates_markdown():
    res = build_share_kit(slug="discord-kills-electron-rust-windows-11",
                          chosen_sub="developersIndia",
                          open_browser=False)
    assert res["slug"] == "discord-kills-electron-rust-windows-11"
    assert res["primary_sub"] == "developersIndia"
    assert res["flair"] == "News"
    assert "reddit.com/r/developersIndia/submit" in res["reddit_url"]
    assert "type=TEXT" in res["reddit_url"]
    path = pathlib.Path(res["path"])
    assert path.exists()
    content = path.read_text(encoding="utf-8")
    assert "https://thetechdocket.com/articles/discord-kills-electron-rust-windows-11/" in content
    assert "news.ycombinator.com/submitlink" in content
    assert "reddit.com/r/developersIndia/submit" in content
    assert "Required Post Flair:" in content
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
