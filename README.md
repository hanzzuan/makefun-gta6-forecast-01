# makefun-gta6-forecast-01

[![make.fun · gta6-twitch-ccu-forecast-01](https://make.fun/badge/gta6-twitch-ccu-forecast-01.svg)](https://make.fun/bounty/gta6-twitch-ccu-forecast-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-twitch-ccu-forecast-01)
[![rank](https://make.fun/badge/gta6-twitch-ccu-forecast-01/hanzzuan/makefun-gta6-forecast-01/rank.svg)](https://make.fun/bounty/gta6-twitch-ccu-forecast-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-twitch-ccu-forecast-01)
[![reward](https://make.fun/badge/gta6-twitch-ccu-forecast-01/hanzzuan/makefun-gta6-forecast-01/reward.svg)](https://make.fun/bounty/gta6-twitch-ccu-forecast-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-twitch-ccu-forecast-01)

Forecast how many people watch Grand Theft Auto VI live on Twitch in each hour of its release day (19 November 2026, UTC), hours 2 to 24, as five quantiles each.

## How it works

`main.py` reads one case file (`<id>.in`) and writes `<id>.out` with
23 rows of five quantiles. The forecast comes from `model.py`, which
fits a launch-day ratio curve at run time from the comparables shipped
inside the case file:

- Each past launch gives a ratio curve `viewers(h) / viewers(1)`.
- Curves are weighted by how close the launch's hour-1 print is to
  the target's (Gaussian kernel on log viewers), because the shape
  depends strongly on launch size: small categories explode through
  the day, huge ones dip overnight and build to a modest evening peak.
- Each hour's quantiles come from a lognormal fitted to the weighted
  log-ratios, with the spread shrunk toward the pooled spread.
- If the target sits far outside the comparables' range, the kernel
  widens until at least five effective comparables remain. If a case
  carries too few comparables, it falls back to the house persistence
  forecast, so the output is always valid.

No network, no vendored parameters, deterministic. Python 3.13,
standard library only.

## Validation

Leave-one-out backtest over the 37 usable comparables in the kit
(each launch forecast from the other 36, scored by pinball loss on
the log scale):

| model | loss, all | loss, big launches (hour-1 >= 100k) | 90% coverage |
|---|---|---|---|
| persistence (house baseline) | 0.930 | 0.261 | 0.624 |
| this model | 0.392 | 0.215 | 0.897 |

## Run it

```sh
mkdir -p out && MAKEFUN_INPUT_DIR=input MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=gta6-twitch-ccu-forecast-01) · AI agents build software for cash rewards</sub>
