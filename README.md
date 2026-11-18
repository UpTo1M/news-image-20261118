# World News — Wednesday, 18 November 2026

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/UpTo1M/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/UpTo1M/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

A one-image front page summing up the world news of Wednesday, 18 November 2026.

## What it does

`main.py` draws a 1024x1024 newspaper front page with Pillow (Python standard
library + PIL only) and writes it to `/output/entry.png`. It also saves a
local copy as `entry.png` in this directory.

Stories covered:

1. US-Iran war escalates in the Gulf
2. Ukraine hits the Kerch Bridge again
3. North Korea fires a missile
4. UN warns of Gaza cold deaths
5. COP31 climate talks enter the decisive phase
6. Trump in Manila, Xi hosts APEC

Plus two brief items in the footer strip.

## How to run

```bash
python3 main.py
```

The program is deterministic: running it twice produces byte-identical
`entry.png` output. It makes no network calls.
