"""Forecast GTA VI's launch-day Twitch viewers hour by hour.

Reads every case file (<id>.in) from the input directory, forecasts
hours 2 to 24 as five quantiles each with the launch-day ratio model
in model.py, and writes one <id>.out per case to the output directory.

Runs with Python 3.13, standard library only, no network. The grader
runs `python3 /bot/main.py` with /input and /output; locally, set
MAKEFUN_INPUT_DIR and MAKEFUN_OUTPUT_DIR:

    mkdir -p out && MAKEFUN_INPUT_DIR=input MAKEFUN_OUTPUT_DIR=out python3 main.py

The program is deterministic: same case in, same bytes out, every run.
If a case cannot be fitted for any reason, the output still falls back
to the persistence forecast, so no case is ever left invalid.
"""

import json
import os
import sys
from pathlib import Path

# The grader runs with -P, which leaves this file's directory off
# sys.path; put it back first so `import model` finds model.py beside it.
sys.path.insert(0, str(Path(__file__).resolve().parent))

import model

INPUT_DIR = Path(os.environ.get("MAKEFUN_INPUT_DIR", "/input"))
OUTPUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def forecast_case(case):
    """One case dict -> the output object for it."""
    try:
        quantiles = model.forecast_quantiles(case)
    except Exception:
        # Never leave a case without an output: persistence is always valid.
        known = case.get("known") or []
        p1 = 1.0
        for row in known:
            if row.get("hour") == 1 and row.get("viewers"):
                p1 = max(1.0, float(row["viewers"]))
                break
        quantiles = model.persistence_quantiles(p1)
    hours = [row["hour"] for row in case.get("forecast") or []]
    if not hours:
        hours = list(range(2, 25))
    rows = [{"hour": h, "q": quantiles[h]} for h in sorted(set(hours))]
    return {"hours": rows}


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    cases = sorted(INPUT_DIR.glob("*.in"))
    if not cases:
        # A run with no case files would silently produce nothing and
        # the entry would score as invalid; fail loudly instead.
        raise SystemExit(f"no .in case files in {INPUT_DIR}")
    # Every case file, in name order, so two runs write the same bytes.
    for path in cases:
        case = json.loads(path.read_text(encoding="utf-8"))
        out = forecast_case(case)
        (OUTPUT_DIR / f"{path.stem}.out").write_text(
            json.dumps(out, separators=(",", ":")) + "\n", encoding="utf-8"
        )


if __name__ == "__main__":
    main()
