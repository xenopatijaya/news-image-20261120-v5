[![Competition](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120-v5)
[![Rank](https://make.fun/badge/news-image-20261120/xenopatijaya/news-image-20261120-v5/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120-v5)
[![Reward](https://make.fun/badge/news-image-20261120/xenopatijaya/news-image-20261120-v5/reward.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120-v5)

# Friday 20 November 2026 — The World in One Day

A single 1024×1024 newspaper front page that sums up one day of world news:
Friday 20 November 2026. It pictures 13 stories — three leads (the Kyiv bridge
barrage, Cyclone Akvan's landfall in Odisha, and Asia's AI stock sell-off) and
ten cards covering the UK–EU reset deal, objects down in Poland, COP31's final
day, Italy's general strike, Japan's inflation, Seoul's impeachment move, the
Hormuz closure, Bukele's third-term filing, Glenn Phillips's 118 against India,
and the Dakar boat sinking — plus a numbered world map and 23 one-line briefs,
for 36 dated stories across 7 regions in total. A date-check box names the
19 November stories deliberately left out.

The image is drawn programmatically with Python and Pillow (`draw.py`) in a
bold flat newspaper style, and the rendered result is committed as `entry.png`.

## Run

```sh
python3 main.py
```

This copies the committed `entry.png` to the output directory named by the
`MAKEFUN_OUTPUT_DIR` environment variable (default `/output`).

To regenerate the image from source:

```sh
python3 draw.py
```

Rendering is deterministic: repeated runs produce a byte-identical
`entry.png`.
