# ZAI Genesis

**Researching market cycles by putting different explanatory models side by side.**

ZAI Genesis is a Python research program that assembles historical market data, current prices, news context, and seven rule-based analytical perspectives in a terminal workflow. It shows where those perspectives agree, where they disagree, and what a rule-based or optional model-assisted interpretation makes of the result.

It is **one program developed within Anteroom Studio**, the company founded by ZAI. It is not the ZAI intelligence project itself.

**[Join the methodology challenge](https://github.com/anteroom-studio/ZAI-Genesis/issues/1)** · **[Discuss research ideas](https://github.com/anteroom-studio/ZAI-Genesis/discussions)** · **[Explore the code](https://github.com/anteroom-studio/ZAI-Genesis)**

---

## From input to outcome

| Stage | What the program does | What you can inspect |
| --- | --- | --- |
| 1. Set up | Detects local hardware, creates data directories, and identifies available AI modes | Hardware report and chosen mode |
| 2. Gather context | Retrieves available historical datasets, market prices, and news | Locally stored data and source-dependent gaps |
| 3. Run engines | Evaluates Fibonacci position, Elliott-style heuristics, long economic cycles, solar/lunar timing, seasonality, and volatility psychology | Per-engine BULLISH / BEARISH / NEUTRAL signals with reasons |
| 4. Compare | Computes an unweighted agreement score from the seven directions | Signed agreement score and overall directional label |
| 5. Interpret | Builds a rule-based outlook or sends context to a configured AI provider/local model | Prediction summary, selected source, generated timestamp |
| 6. Observe | Saves prediction JSON and displays a periodically refreshed terminal dashboard | Latest saved output, signals, prices and news context |

The [launcher](zai_genesis.py), [data collector](data_collector.py), [seven engines](nature_engine.py), [interpretation layer](genesis_brain.py), and [dashboard](dashboard.py) expose the process for inspection.

### What the score actually means

In the current implementation, each engine contributes one of three labels. The Nature Agreement Score is:

```text
100 × (number of bullish engines − number of bearish engines)
      / number of engines
```

It measures **agreement among implemented heuristics**, not the probability of a future market move. The separate field currently called `confidence` reflects the share of engines taking a non-neutral position; it is **not statistically calibrated forecasting confidence**.

A worked *illustration* (not a recorded run): if four of seven engines are bullish, two bearish, and one neutral, the score is approximately +28.6. Readers can inspect the rationale behind each signal rather than accepting one final label.

---

## Run it

Use a Python environment with the requirements installed:

```bash
git clone https://github.com/anteroom-studio/ZAI-Genesis.git
cd ZAI-Genesis
python -m pip install -r requirements.txt
python3 zai_genesis.py
```

The first run can download datasets and requires network access for external data. Availability and returned history depend on the upstream sources. The launcher also attempts to install missing Python packages.

**Optional model access:** The current implementation reads `GROQ_KEY`, `GEMINI_KEY`, and `ANTHROPIC_KEY` from [`config.py`](config.py), **not automatically from `.env`**. You can run the rule-based fallback without a key or use an installed Ollama model where detected. Never commit your own credentials. The included `.env.example` is a template, but the present code does not load it automatically.

Saved outputs are written under the configured `DATA_PATH`, including `predictions/latest.json`. Inspect the `source` field to distinguish rule-based interpretation from the other modes.

---

## A research question worth challenging

**If several models agree, does that add independent evidence—or can correlated assumptions make agreement look stronger than it is?**

The current engines contain heuristics, including contested cycle-based hypotheses. Their inclusion is a subject of investigation, not an assertion that solar, lunar, or long-cycle models can predict markets reliably.

If you test Genesis, a useful contribution would be:

1. Identify one signal and the input data that produced it.
2. Compare it with a simple baseline over a fixed historical window, avoiding look-ahead.
3. Test whether changing one engine materially changes the overall score.
4. Report your dataset dates, reproducible method, failure cases, and what you would change.

[**Review the active experiment →**](https://github.com/anteroom-studio/ZAI-Genesis/issues/1) · [**Open a methodology discussion →**](https://github.com/anteroom-studio/ZAI-Genesis/discussions)  
[**Report a reproducible implementation bug →**](https://github.com/anteroom-studio/ZAI-Genesis/issues/new)

## Scope

This is research and educational software, not a validated forecasting service, trading signal, or financial recommendation. The public repository exposes an implementation and inspectable computations; it does not by itself establish predictive accuracy, causation, or profitability. Outputs can be incomplete or stale when data providers fail.

---

Developed within **Anteroom Studio**. Project: **ZAI Genesis**.
