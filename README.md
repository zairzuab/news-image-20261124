# The World Today — 24 November 2026

[![news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/zairzuab/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/zairzuab/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

Entry for the [make.fun bounty "Sum up 24 November's world news in one image"](https://make.fun/bounty/news-image-20261124) (news-image-20261124).

## What it is

A dense newspaper front page — **"THE WORLD TODAY — 24 November 2026"** — summing up
Tuesday 24 November 2026 in 40 stories across 7 sections:

- **Lead:** COP31 climate talks collapse without a deal in Antalya
- **Featured:** Jensen Huang reinstated as Nvidia CEO; Russian strikes kill 15 in the Kyiv region
- **Americas, Europe, Middle East, Asia-Pacific, Africa, Tech & Science, Sport & Culture** — from the US sanctions on Iran's shadow banking and the US naval blockade, to the Indonesia factory fire, the Modi–Nepal package, Alcaraz's first ATP Finals title, and Gukesh's world chess title defence opening in Geneva — plus a footer ticker with the Sensex slide, Lahore's air pollution, the supermoon, and the FIFA Women's World Cup hosts.

## How it works

`main.py` (Python 3.13, PIL only) draws the whole front page with PIL — masthead, lead story, two featured stories, three columns of region sections, and a footer ticker — and writes it to `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR/entry.png` outside the grader). No network, no randomness, no timestamps: two runs produce byte-identical output.

```
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Output: a 1024×1024 PNG, well under the 1 MiB gate limit.

## Files

- `main.py` — the program that draws the front page
- `entry.png` — the generated front page (also produced by running `main.py`)
- `LICENSE` — MIT

Built by Muse for [@zairzuab](https://github.com/zairzuab) for make.fun bounty `news-image-20261124`.
