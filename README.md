# Ivory Tempo

[![make.fun](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/Aman404Found/ivory-tempo/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard)
[![reward](https://make.fun/badge/tiny-chess-01/Aman404Found/ivory-tempo/reward.svg)](https://make.fun/bounty/tiny-chess-01)

A deterministic Python chess engine. It searches successively deeper trees, reordering the root after each completed iteration. Captures are searched beyond the nominal horizon. Only moves supplied as legal by the environment can be played.

## Run

Set `MAKEFUN_ENV_URL` to the competition environment endpoint and run `python3.13 main.py`, or run `node cli/makefun.mjs grade-local --kit . --bot <repo> --driver docker --instances 3` inside the official kit.

[Entered on make.fun](https://make.fun/?ref=vwvfcna2&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
