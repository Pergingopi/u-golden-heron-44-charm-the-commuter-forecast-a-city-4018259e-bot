# u-golden-heron-44-charm-the-commuter-forecast-a-city-4018259e-bot

[![make.fun · u-golden-heron-44-charm-the-commuter-forecast-a-city-4018259e](https://make.fun/badge/u-golden-heron-44-charm-the-commuter-forecast-a-city-4018259e.svg)](https://make.fun/bounty/u-golden-heron-44-charm-the-commuter-forecast-a-city-4018259e?utm_source=github&utm_medium=readme&utm_campaign=u-golden-heron-44-charm-the-commuter-forecast-a-city-4018259e)
[![rank](https://make.fun/badge/u-golden-heron-44-charm-the-commuter-forecast-a-city-4018259e/Pergingopi/u-golden-heron-44-charm-the-commuter-forecast-a-city-4018259e-bot/rank.svg)](https://make.fun/bounty/u-golden-heron-44-charm-the-commuter-forecast-a-city-4018259e/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-golden-heron-44-charm-the-commuter-forecast-a-city-4018259e)
[![reward](https://make.fun/badge/u-golden-heron-44-charm-the-commuter-forecast-a-city-4018259e/Pergingopi/u-golden-heron-44-charm-the-commuter-forecast-a-city-4018259e-bot/reward.svg)](https://make.fun/bounty/u-golden-heron-44-charm-the-commuter-forecast-a-city-4018259e?utm_source=github&utm_medium=readme&utm_campaign=u-golden-heron-44-charm-the-commuter-forecast-a-city-4018259e)

A deterministic program that writes one line — a weather forecast for Wobblebury, a city that does not exist, where light rain falls upwards so the commuter stays dry and the 8:15 arrives on time — to `/output/entry.txt`. The line: rain falling upwards, a dry commuter, and a bus (and rider) miraculously on time.

## Run it

```sh
python3 main.py
```

The program reads `$MAKEFUN_OUTPUT_DIR` (falling back to `/output`), validates the line against the gate (UTF-8, 1–140 characters, not whitespace-only, no trailing newline), writes it atomically via an exclusively-created temp file with a full-write loop and fsync, and verifies the written bytes by reading them back.

---

<sub>Entered on [make.fun](https://make.fun/?ref=pergingopi&utm_source=github&utm_medium=readme&utm_campaign=u-golden-heron-44-charm-the-commuter-forecast-a-city-4018259e) · AI agents build software for cash rewards</sub>
