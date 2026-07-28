"""
Chat client for the Ministral 3 Worker API.

Usage:
    python chat_client.py                           # Interactive
    python chat_client.py -m "Hello"                # One-shot
    python chat_client.py --api http://localhost:8742
"""

import argparse
import json
import sys
from typing import Optional

import requests


def send_message(
    text: str,
    api_url: str = "http://localhost:8742",
    temperature: float = 0.1,
    max_tokens: int = 2048,
    system_prompt: Optional[str] = None,
    history: Optional[list] = None,
) -> str:
    messages = history or []
    messages.append({"role": "user", "content": text})

    payload = {
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if system_prompt:
        payload["system_prompt"] = system_prompt

    resp = requests.post(
        f"{api_url}/v1/chat/completions",
        json=payload,
        timeout=300,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"]


def interactive(api_url: str):
    print(f"Ministral 3 — Chat ({api_url})")
    print("/quit to exit, /sys <prompt> to set system prompt, /clear to reset history")
    print()

    sys_prompt = None
    history = []

    while True:
        try:
            line = input(">>> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not line:
            continue
        if line == "/quit":
            break
        if line == "/clear":
            history = []
            print("[history cleared]")
            continue
        if line.startswith("/sys "):
            sys_prompt = line[5:]
            print(f"[system prompt set]")
            continue

        try:
            reply = send_message(line, api_url, history=history, system_prompt=sys_prompt)
            chat_history = history + [{"role": "user", "content": line}]
            if reply:
                print(reply)
                history = chat_history + [{"role": "assistant", "content": reply}]
                if len(history) > 20:
                    history = history[-20:]
        except requests.exceptions.ConnectionError:
            print("[error] Cannot connect to worker. Is it running?")
            print(f"        Start with: python model_worker.py")
        except Exception as e:
            print(f"[error] {e}")


def main():
    parser = argparse.ArgumentParser(description="Ministral 3 Chat Client")
    parser.add_argument("--api", default="http://localhost:8742", help="Worker API URL")
    parser.add_argument("-m", "--message", help="One-shot message (non-interactive)")
    parser.add_argument("-t", "--temperature", type=float, default=0.1)
    parser.add_argument("--max-tokens", type=int, default=2048)
    args = parser.parse_args()

    if args.message:
        reply = send_message(args.message, args.api, args.temperature, args.max_tokens)
        print(reply)
    else:
        interactive(args.api)


if __name__ == "__main__":
    main()
