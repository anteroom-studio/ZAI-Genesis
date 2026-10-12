#!/usr/bin/env python3
"""Inspect Genesis' directional agreement and leave-one-engine-out sensitivity.

This is a deterministic methodology probe, NOT a forecast or backtest.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from nature_engine import calculate_agreement_score

EXAMPLE = {
    "fibonacci": "BULLISH",
    "elliott": "BEARISH",
    "kondratiev": "BULLISH",
    "sunspots": "NEUTRAL",
    "lunar": "BULLISH",
    "seasonal": "BULLISH",
    "psychology": "BEARISH",
}
VALID = {"BULLISH", "BEARISH", "NEUTRAL"}


def normalized_signals(raw):
    """Accept engine_signals, a nested 'signals' map, or a simple name:label map."""
    if not isinstance(raw, dict):
        raise ValueError("Input must be a JSON object")
    if "engine_signals" in raw:
        raw = raw["engine_signals"]
    elif "signals" in raw:
        raw = raw["signals"]
    if not isinstance(raw, dict) or not raw:
        raise ValueError("Expected a non-empty signal mapping")
    out = {}
    for name, value in raw.items():
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Every engine needs a non-empty name")
        if isinstance(value, dict):
            value = value.get("signal")
        if not isinstance(value, str) or value not in VALID:
            raise ValueError(f"Invalid label for {name!r}: {value!r}")
        out[name] = {"signal": value}
    return out


def report(raw):
    signals = normalized_signals(raw)
    score, direction, active_fraction = calculate_agreement_score(signals)
    sensitivity = {}
    for removed in signals:
        remainder = {k: v for k, v in signals.items() if k != removed}
        loo_score, loo_direction, _ = calculate_agreement_score(remainder)
        sensitivity[removed] = {
            "score_without_engine": loo_score,
            "direction_without_engine": loo_direction,
            "score_change": round(loo_score - score, 1),
        }
    return {
        "engine_count": len(signals),
        "signals": {k: v["signal"] for k, v in signals.items()},
        "agreement_score": score,
        "direction": direction,
        "non_neutral_fraction_pct": active_fraction,
        "note": "Agreement and non-neutral fraction are NOT predictive probabilities.",
        "leave_one_engine_out": sensitivity,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, help="JSON signal mapping or saved Genesis prediction JSON")
    args = parser.parse_args()
    try:
        raw = json.loads(args.input.read_text(encoding="utf-8")) if args.input else EXAMPLE
        result = report(raw)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    if not args.input:
        print("SYNTHETIC DEMONSTRATION — NOT OBSERVED MARKET DATA")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
