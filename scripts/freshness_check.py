#!/usr/bin/env python3
"""
Periodic content freshness check for DeepDive articles.

For each article whose meta.json next_check ≤ today (or --force-all),
runs hybrid checks and writes a freshness report:

  - Rule-based:
    · Link rot: HEAD requests to all external href URLs; flag 4xx/5xx
    · Date drift: extract dates older than 6 months; suggest reframing
    · Prediction expiry: extract "X 年内/within X years" patterns;
      flag if deadline approaches
  - LLM-based:
    · Send article + prompt to UPDATE_AGENT_MODEL (default Claude)
    · Ask for stale claims, missing recent context, contradicted predictions

Outputs:
  _freshness/<topic_dir>/<slug>-<date>.md  — the report
  Updates meta.json: next_check (rolled forward by priority schedule)

Optional outputs (controlled by env):
  - GITHUB_ISSUE_REPO=owner/repo + GITHUB_TOKEN: opens an Issue per report
  - SLACK_WEBHOOK_URL: posts a summary

Env:
  UPDATE_AGENT_PROVIDER  — anthropic | bigmodel | openai (default: anthropic)
  UPDATE_AGENT_MODEL     — model name (defaults per provider)
  ANTHROPIC_API_KEY / BIGMODEL_API_KEY / OPENAI_API_KEY (per provider)
  CHECK_FORCE_ALL=true   — ignore next_check, scan everything
  CHECK_FORCE_SLUG=...   — only check this slug
  CHECK_DRY_RUN=true     — don't call LLM, don't write reports
"""
import json
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from html.parser import HTMLParser
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = REPO_ROOT / "config"
DEEPDIVE_DIR = REPO_ROOT / "deepdive"
FRESHNESS_DIR = REPO_ROOT / "_freshness"

FORCE_ALL = os.environ.get("CHECK_FORCE_ALL", "").lower() == "true"
FORCE_SLUG = os.environ.get("CHECK_FORCE_SLUG", "")
DRY_RUN = os.environ.get("CHECK_DRY_RUN", "").lower() == "true"

PRIORITY_INTERVAL_DAYS = {
    "hot": 7,
    "warm": 30,
    "cold": 90,
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data):
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def today():
    return datetime.utcnow().date()


def is_due(meta: dict) -> bool:
    if FORCE_ALL:
        return True
    nxt = meta.get("next_check")
    if not nxt:
        return True
    try:
        return datetime.strptime(nxt, "%Y-%m-%d").date() <= today()
    except Exception:
        return True


class TextExtractor(HTMLParser):
    """Extract visible text + collect external links from HTML."""

    SKIP = {"script", "style"}

    def __init__(self):
        super().__init__()
        self.parts = []
        self._skip_depth = 0
        self.external_links = []

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self._skip_depth += 1
        if tag == "a":
            for k, v in attrs:
                if k == "href" and v and (v.startswith("http://") or v.startswith("https://")):
                    self.external_links.append(v)

    def handle_endtag(self, tag):
        if tag in self.SKIP:
            self._skip_depth = max(0, self._skip_depth - 1)

    def handle_data(self, data):
        if self._skip_depth == 0:
            text = data.strip()
            if text:
                self.parts.append(text)

    def text(self) -> str:
        return "\n".join(self.parts)


def check_link(url: str, timeout: int = 10) -> tuple:
    """Returns (status_code, error_msg)."""
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "Mozilla/5.0 freshness-check"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return (resp.status, None)
    except urllib.error.HTTPError as e:
        return (e.code, None)
    except Exception as e:
        return (None, str(e)[:120])


def find_dates(text: str) -> list:
    """Find date-like patterns and ages (in days) from today."""
    today_dt = today()
    found = []
    # 2026年3月 / 2026 年 3 月
    for m in re.finditer(r"(20\d{2})\s*年\s*(\d{1,2})\s*月", text):
        try:
            d = datetime.strptime(f"{m.group(1)}-{m.group(2).zfill(2)}-01", "%Y-%m-%d").date()
            age = (today_dt - d).days
            if age > 180:
                found.append((m.group(0), age))
        except Exception:
            pass
    # 2026-03 / 2026-03-15
    for m in re.finditer(r"(20\d{2})-(\d{2})(?:-(\d{2}))?", text):
        try:
            day = m.group(3) or "01"
            d = datetime.strptime(f"{m.group(1)}-{m.group(2)}-{day}", "%Y-%m-%d").date()
            age = (today_dt - d).days
            if age > 180:
                found.append((m.group(0), age))
        except Exception:
            pass
    return found[:30]


def find_predictions(text: str) -> list:
    """Find prediction phrases like '1-5 年内', 'X year forecast' etc."""
    out = []
    for m in re.finditer(r"(\d+\s*-\s*\d+|\d+)\s*年\s*内", text):
        out.append(m.group(0))
    for m in re.finditer(r"\bin\s*(\d+\s*-\s*\d+|\d+)\s*years?\b", text, re.I):
        out.append(m.group(0))
    return out[:10]


def llm_check(article_text: str, slug: str, meta: dict) -> str:
    """Ask LLM for staleness/update suggestions. Returns markdown bullets."""
    from llm_client import chat

    pub_date = meta.get("first_published", "unknown")
    last_update = meta.get("last_updated", pub_date)
    title = (meta.get("title") or {}).get(meta.get("primary_language", "zh"), slug)

    system = """You are a research editor reviewing a published article for staleness.
Your job: identify specific claims, data points, predictions, or named-entity statuses
that may have become outdated since the article's last update. Only flag items where
you're CONFIDENT something has likely changed in reality (not speculation).

Focus on:
- Numerical claims with specific dates (e.g. "X% in 2025") that have a newer revision
- Named-entity status (CEO names, company existence, product status)
- Predictions whose deadline has arrived or is near
- Industry developments that explicitly contradict article claims

Output format: a Markdown checklist with severity tags. Each item:
  - [ ] [severity] description (~30 words) · suggested action

Severity: 🔴 critical | 🟡 worth-updating | 🟢 informational | ❓ uncertain

If nothing seems stale, output a single line: "✅ 未发现明显需要更新的内容（基于训练数据范围）。"
Be conservative — false positives waste reviewer time."""

    user = f"""Article: {title}
Slug: {slug}
First published: {pub_date}
Last updated: {last_update}
Today: {today().isoformat()}

ARTICLE TEXT (extracted from HTML, English/Chinese mixed):

{article_text[:50000]}

Review for staleness."""

    if DRY_RUN:
        return "✅ [DRY RUN] LLM check skipped"
    try:
        return chat(system, user, max_tokens=2000)
    except Exception as e:
        return f"⚠️ LLM 检查失败：{e}"


def check_article(meta_path: Path) -> dict:
    """Run all checks for one article. Returns report data dict."""
    meta = load_json(meta_path)
    slug = meta.get("slug", meta_path.stem.replace(".meta", ""))
    if FORCE_SLUG and slug != FORCE_SLUG:
        return {"skipped": True, "reason": "slug filter"}

    topic_dir = meta_path.parent
    html_file = topic_dir / f"{slug}.html"
    if not html_file.exists():
        return {"skipped": True, "reason": "no source HTML"}

    print(f"[freshness] checking {slug}", file=sys.stderr)
    html = html_file.read_text(encoding="utf-8")

    extractor = TextExtractor()
    extractor.feed(html)
    text = extractor.text()
    links = list(set(extractor.external_links))[:50]

    # Link rot
    link_issues = []
    for url in links:
        code, err = check_link(url)
        if err:
            link_issues.append({"url": url, "issue": f"network error: {err}"})
        elif code and code >= 400:
            link_issues.append({"url": url, "issue": f"HTTP {code}"})

    # Date drift + predictions
    dates = find_dates(text)
    predictions = find_predictions(text)

    # LLM staleness check
    llm_findings = llm_check(text, slug, meta)

    return {
        "slug": slug,
        "title": meta.get("title", {}),
        "topic_dir": topic_dir.name,
        "checked_at": today().isoformat(),
        "current_version": meta.get("current_version", 1),
        "first_published": meta.get("first_published"),
        "last_updated": meta.get("last_updated"),
        "freshness_priority": meta.get("freshness_priority", "warm"),
        "link_issues": link_issues,
        "old_dates": dates,
        "predictions": predictions,
        "llm_findings": llm_findings,
        "skipped": False,
    }


def render_report(report: dict) -> str:
    """Render report dict as markdown."""
    if report.get("skipped"):
        return ""

    title = (report["title"] or {}).get("zh") or report["slug"]
    lines = [
        f"# Freshness Report · {report['slug']} · {report['checked_at']}",
        "",
        f"**文章**: {title}",
        f"**首发**: {report['first_published']} · **上次更新**: {report['last_updated']} · **当前版本**: v{report['current_version']}",
        f"**优先级**: `{report['freshness_priority']}` · **本次检查**: {report['checked_at']}",
        "",
    ]

    if report["link_issues"]:
        lines += ["## 🔴 链接问题", ""]
        for issue in report["link_issues"]:
            lines.append(f"- [ ] `{issue['url']}` — {issue['issue']}")
        lines.append("")
    else:
        lines += ["## ✅ 链接健康", "所有外部链接可达。", ""]

    if report["old_dates"]:
        lines += ["## 🟡 日期漂移（≥6 个月前）", ""]
        for date_str, age in report["old_dates"][:10]:
            months = age // 30
            lines.append(f"- [ ] `{date_str}` — {months} 个月前 · 检查叙述是否仍现在时合适")
        lines.append("")

    if report["predictions"]:
        lines += ["## 🟢 预测条款", ""]
        for pred in report["predictions"]:
            lines.append(f"- [ ] `{pred}` — 检查是否已到验证窗口")
        lines.append("")

    lines += ["## LLM 评估（基于训练数据）", "", report["llm_findings"], ""]
    lines += ["---", "", f"_由 freshness-check Action 生成 · {report['checked_at']}_"]
    return "\n".join(lines)


def write_report(report: dict) -> Path:
    """Write report markdown to _freshness/<topic>/<slug>-<date>.md."""
    out_dir = FRESHNESS_DIR / report["topic_dir"]
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{report['slug']}-{report['checked_at']}.md"
    out.write_text(render_report(report), encoding="utf-8")
    return out


def update_next_check(meta_path: Path):
    meta = load_json(meta_path)
    interval = PRIORITY_INTERVAL_DAYS.get(
        meta.get("freshness_priority", "warm"), 30
    )
    nxt = today() + timedelta(days=interval)
    meta["next_check"] = nxt.isoformat()
    save_json(meta_path, meta)


def open_github_issue(report: dict, report_path: Path):
    """Open a GitHub Issue with the report contents."""
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    token = os.environ.get("GITHUB_TOKEN", "")
    if not repo or not token:
        return None

    title = f"[Freshness] {report['slug']} · {report['checked_at']}"
    issues = []
    if report["link_issues"]:
        issues.append(f"🔴 {len(report['link_issues'])} 链接问题")
    if report["old_dates"]:
        issues.append(f"🟡 {len(report['old_dates'])} 旧日期")
    summary = " · ".join(issues) if issues else "✅ 仅 LLM 建议"

    body_lines = [
        f"自动生成的内容刷新报告。**摘要**: {summary}",
        "",
        f"完整报告：[`{report_path.relative_to(REPO_ROOT)}`]({report_path.relative_to(REPO_ROOT)})",
        "",
        "---",
        "",
        render_report(report),
    ]

    payload = {
        "title": title,
        "body": "\n".join(body_lines),
        "labels": ["freshness", report["freshness_priority"]],
    }
    url = f"https://api.github.com/repos/{repo}/issues"
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("html_url")
    except Exception as e:
        print(f"[freshness] failed to open issue: {e}", file=sys.stderr)
        return None


def main():
    summary = {
        "checked": [],
        "skipped": [],
        "reports_written": [],
        "issues_opened": [],
    }

    for meta_path in sorted(DEEPDIVE_DIR.rglob("*.meta.json")):
        meta = load_json(meta_path)
        if not is_due(meta):
            summary["skipped"].append({
                "slug": meta.get("slug"),
                "next_check": meta.get("next_check"),
            })
            continue

        report = check_article(meta_path)
        if report.get("skipped"):
            continue

        summary["checked"].append(report["slug"])

        if not DRY_RUN:
            report_path = write_report(report)
            summary["reports_written"].append(str(report_path.relative_to(REPO_ROOT)))

            issue_url = open_github_issue(report, report_path)
            if issue_url:
                summary["issues_opened"].append(issue_url)

            update_next_check(meta_path)

    print("---SUMMARY---")
    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
