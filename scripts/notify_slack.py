#!/usr/bin/env python3
"""
Send Slack notification via incoming webhook.

Usage:
  echo '{"title":"...","fields":[{"name":"...","value":"..."}]}' | python notify_slack.py
  # OR via flags:
  python notify_slack.py --title "..." --field name=value --field name=value

Env:
  SLACK_WEBHOOK_URL — required
"""
import argparse
import json
import os
import sys
import urllib.request


def send(payload: dict):
    url = os.environ.get("SLACK_WEBHOOK_URL", "")
    if not url:
        print("[notify_slack] SLACK_WEBHOOK_URL not set; skipping", file=sys.stderr)
        return
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        if resp.status != 200:
            print(f"[notify_slack] HTTP {resp.status}", file=sys.stderr)


def from_args(argv):
    p = argparse.ArgumentParser()
    p.add_argument("--title", required=True)
    p.add_argument("--text", default="")
    p.add_argument("--field", action="append", default=[],
                   help='name=value (or "name=value with spaces")')
    p.add_argument("--color", default="#7fb88b")
    args = p.parse_args(argv)

    fields = []
    for f in args.field:
        if "=" in f:
            n, v = f.split("=", 1)
            fields.append({"title": n, "value": v, "short": False})

    payload = {
        "text": args.title,
        "attachments": [
            {
                "color": args.color,
                "title": args.title,
                "text": args.text,
                "fields": fields,
                "mrkdwn_in": ["text", "fields"],
            }
        ],
    }
    return payload


def from_stdin():
    raw = sys.stdin.read().strip()
    if not raw:
        return None
    return json.loads(raw)


if __name__ == "__main__":
    payload = from_stdin() if not sys.stdin.isatty() else None
    if not payload:
        payload = from_args(sys.argv[1:])
    send(payload)
