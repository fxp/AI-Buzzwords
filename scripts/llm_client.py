#!/usr/bin/env python3
"""
Provider-agnostic LLM client used by freshness_check.py and other agents.

Supported providers (env-configurable):
  - anthropic (default): ANTHROPIC_API_KEY, model claude-sonnet-4-6
  - bigmodel:            BIGMODEL_API_KEY, model glm-5.1
  - openai:              OPENAI_API_KEY,   model gpt-5

Env vars:
  UPDATE_AGENT_PROVIDER  — anthropic | bigmodel | openai (default: anthropic)
  UPDATE_AGENT_MODEL     — overrides default model name for the provider
"""
import json
import os
import sys
import time
import urllib.request
import urllib.error


PROVIDER_DEFAULTS = {
    "anthropic": {
        "endpoint": "https://api.anthropic.com/v1/messages",
        "model": "claude-sonnet-4-6",
        "api_key_env": "ANTHROPIC_API_KEY",
        "version_header": "2023-06-01",
    },
    "bigmodel": {
        "endpoint": "https://api.z.ai/api/paas/v4/chat/completions",
        "model": "glm-5.1",
        "api_key_env": "BIGMODEL_API_KEY",
    },
    "openai": {
        "endpoint": "https://api.openai.com/v1/chat/completions",
        "model": "gpt-5",
        "api_key_env": "OPENAI_API_KEY",
    },
}


def get_provider_config():
    provider = os.environ.get("UPDATE_AGENT_PROVIDER", "anthropic").lower()
    if provider not in PROVIDER_DEFAULTS:
        raise ValueError(f"Unknown provider: {provider}")
    cfg = dict(PROVIDER_DEFAULTS[provider])
    cfg["provider"] = provider
    cfg["model"] = os.environ.get("UPDATE_AGENT_MODEL") or cfg["model"]
    cfg["api_key"] = os.environ.get(cfg["api_key_env"], "")
    return cfg


def _post_json(url, headers, payload, timeout=600, max_retries=3):
    body = json.dumps(payload).encode("utf-8")
    last_err = None
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, data=body, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            last_err = f"HTTP {e.code}: {e.read().decode('utf-8', errors='ignore')[:500]}"
            time.sleep(2 ** attempt)
        except Exception as e:
            last_err = str(e)
            time.sleep(2 ** attempt)
    raise RuntimeError(f"LLM call failed after {max_retries}: {last_err}")


def chat(system_prompt: str, user_prompt: str, max_tokens: int = 4096) -> str:
    """Single-turn chat. Returns assistant message content as string."""
    cfg = get_provider_config()
    if not cfg["api_key"]:
        raise RuntimeError(f"{cfg['api_key_env']} not set")

    if cfg["provider"] == "anthropic":
        headers = {
            "x-api-key": cfg["api_key"],
            "anthropic-version": cfg["version_header"],
            "Content-Type": "application/json",
        }
        payload = {
            "model": cfg["model"],
            "max_tokens": max_tokens,
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_prompt}],
        }
        data = _post_json(cfg["endpoint"], headers, payload)
        # Anthropic response: content is list of blocks; we want first text block
        for block in data.get("content", []):
            if block.get("type") == "text":
                return block.get("text", "")
        return ""
    else:
        # OpenAI / BigModel — both OpenAI-compatible
        headers = {
            "Authorization": f"Bearer {cfg['api_key']}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": cfg["model"],
            "max_tokens": max_tokens,
            "temperature": 0.2,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }
        data = _post_json(cfg["endpoint"], headers, payload)
        return data["choices"][0]["message"]["content"]


def info():
    cfg = get_provider_config()
    has_key = bool(cfg["api_key"])
    return {
        "provider": cfg["provider"],
        "model": cfg["model"],
        "endpoint": cfg["endpoint"],
        "api_key_set": has_key,
    }


if __name__ == "__main__":
    print(json.dumps(info(), indent=2))
