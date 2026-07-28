"""
Ministral 3.3B Worker — Inference server for Ministral-3-3B-Instruct-2512.

Usage:
    python model_worker.py                   # Start API server (default port 8742)
    python model_worker.py --cli             # Interactive CLI mode
    python model_worker.py --text "Hello"    # One-shot inference

Environment:
    FLUX_WORKER_PORT     — Server port (default: 8742)
    FLUX_WORKER_MODEL    — Model path/ID (default: mistralai/Ministral-3-3B-Instruct-2512)
    FLUX_WORKER_DEVICE   — Device override (auto-detect if unset)
"""

import argparse
import json
import os
import sys
import threading
from pathlib import Path
from typing import Optional

import requests

MODEL_ID = os.environ.get(
    "FLUX_WORKER_MODEL",
    "mistralai/Ministral-3-3B-Instruct-2512",
)
DEVICE = os.environ.get("FLUX_WORKER_DEVICE", "")
PORT = int(os.environ.get("FLUX_WORKER_PORT", "8742"))

HF_TOKEN = os.environ.get("HF_TOKEN", None)

_SYSTEM_PROMPT = (
    "You are Ministral 3, a helpful, efficient, and concise AI assistant "
    "created by Mistral AI. You answer in the language the user uses. "
    "You are precise, factual, and brief."
)


# ─── Model Loader ─────────────────────────────────────────────────────────

_model = None
_tokenizer = None
_lock = threading.Lock()


def load_model():
    global _model, _tokenizer
    with _lock:
        if _model is not None:
            return _model, _tokenizer

    print(f"[worker] Loading {MODEL_ID}...")
    import torch
    from transformers import (
        Mistral3ForConditionalGeneration,
        MistralCommonBackend,
    )

    device = DEVICE or ("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[worker] Device: {device}")

    tokenizer = MistralCommonBackend.from_pretrained(
        MODEL_ID, token=HF_TOKEN,
    )
    model = Mistral3ForConditionalGeneration.from_pretrained(
        MODEL_ID,
        device_map=device,
        torch_dtype=torch.bfloat16 if device == "cuda" else torch.float32,
        token=HF_TOKEN,
    )

    if device == "cpu":
        model = model.to(torch.float32)

    _model = model
    _tokenizer = tokenizer
    print(f"[worker] Model ready — {sum(p.numel() for p in model.parameters()):,} params")
    return model, tokenizer


def unload_model():
    global _model, _tokenizer
    with _lock:
        _model = None
        _tokenizer = None
    import gc, torch
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    print("[worker] Model unloaded")


# ─── Inference ────────────────────────────────────────────────────────────

def generate(
    messages,
    temperature=0.1,
    max_tokens=2048,
    system_prompt=None,
):
    model, tokenizer = load_model()

    if system_prompt:
        messages = [
            {"role": "system", "content": system_prompt},
            *[m for m in messages if m.get("role") != "system"],
        ]

    tokenized = tokenizer.apply_chat_template(
        messages, return_tensors="pt", return_dict=True,
    )

    import torch
    device = next(model.parameters()).device
    tokenized["input_ids"] = tokenized["input_ids"].to(device)
    if "pixel_values" in tokenized:
        tokenized["pixel_values"] = tokenized["pixel_values"].to(
            dtype=torch.bfloat16 if device.type == "cuda" else torch.float32,
            device=device,
        )

    image_sizes = None
    if "pixel_values" in tokenized:
        image_sizes = [tokenized["pixel_values"].shape[-2:]]

    out = model.generate(
        **tokenized,
        image_sizes=image_sizes,
        max_new_tokens=max_tokens,
        temperature=temperature,
        do_sample=temperature > 0,
        pad_token_id=tokenizer.eos_token_id,
    )

    decoded = tokenizer.decode(out[0][len(tokenized["input_ids"][0]):])
    return decoded.strip()


# ─── CLI Mode ──────────────────────────────────────────────────────────────

def cli_mode():
    print(f"Ministral 3 Worker — CLI")
    print(f"Model: {MODEL_ID}")
    print("Type /quit to exit, /unload to free memory, /sys <prompt> to set system prompt")
    print()

    sys_prompt = _SYSTEM_PROMPT
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
        if line == "/unload":
            unload_model()
            print("[done]")
            continue
        if line.startswith("/sys "):
            sys_prompt = line[5:]
            print(f"[system prompt set]")
            continue

        messages = [{"role": "user", "content": line}]
        if history:
            messages = history + messages

        print("[generating...]", end=" ", flush=True)
        try:
            reply = generate(messages, system_prompt=sys_prompt)
            print()
            print(reply)
            history.append({"role": "user", "content": line})
            history.append({"role": "assistant", "content": reply})
            if len(history) > 20:
                history = history[-20:]
        except Exception as e:
            print(f"\n[error] {e}")

    unload_model()


# ─── API Server ────────────────────────────────────────────────────────────

def api_server():
    from flask import Flask, request, jsonify
    from flask_cors import CORS

    app = Flask(__name__)
    CORS(app)

    @app.route("/v1/chat/completions", methods=["POST"])
    def chat():
        data = request.get_json(force=True)
        messages = data.get("messages", [])
        temperature = data.get("temperature", 0.1)
        max_tokens = data.get("max_tokens", 2048)
        system_prompt = data.get("system_prompt", _SYSTEM_PROMPT)
        stream = data.get("stream", False)

        try:
            reply = generate(messages, temperature, max_tokens, system_prompt)
            return jsonify({
                "id": "ministral-3-3b",
                "object": "chat.completion",
                "choices": [{
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": reply,
                    },
                    "finish_reason": "stop",
                }],
                "usage": {
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0,
                },
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/v1/models", methods=["GET"])
    def list_models():
        return jsonify({
            "object": "list",
            "data": [{
                "id": MODEL_ID.split("/")[-1],
                "object": "model",
                "created": 0,
                "owned_by": "mistralai",
            }],
        })

    @app.route("/health", methods=["GET"])
    def health():
        import torch
        gpu = torch.cuda.is_available() if hasattr(torch, "cuda") else False
        return jsonify({
            "status": "ok",
            "model": MODEL_ID,
            "gpu": gpu,
            "device": DEVICE or ("cuda" if gpu else "cpu"),
        })

    print(f"[worker] API server on http://0.0.0.0:{PORT}")
    print(f"[worker] Endpoints:")
    print(f"   POST /v1/chat/completions  — Chat completion")
    print(f"   GET  /v1/models            — List models")
    print(f"   GET  /health               — Health check")
    app.run(host="0.0.0.0", port=PORT, threaded=True)


# ─── One-shot ──────────────────────────────────────────────────────────────

def oneshot(text):
    msg = [{"role": "user", "content": text}]
    reply = generate(msg, system_prompt=_SYSTEM_PROMPT)
    print(reply)
    unload_model()


# ─── Main ──────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Ministral 3 Worker")
    parser.add_argument("--cli", action="store_true", help="Interactive CLI mode")
    parser.add_argument("--text", type=str, help="One-shot inference")
    parser.add_argument("--unload", action="store_true", help="Unload model and exit")
    args = parser.parse_args()

    if args.unload:
        unload_model()
        return
    if args.cli:
        cli_mode()
    elif args.text:
        oneshot(args.text)
    else:
        api_server()


if __name__ == "__main__":
    main()
