# news-image-20261117 — The World in One Day

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/Chapo1245/news-image-20261117-chapo124574/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/Chapo1245/news-image-20261117-chapo124574/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

A one-page newspaper front page summing up world news on **Tuesday, 17 November 2026** — eight stories from around the world, drawn entirely by code.

## What it shows

- **US–Iran:** US jets strike a missile site on Qeshm Island after Iran fires drones at a US radar base in Bahrain.
- **Kerch Bridge:** Ukraine hits the Crimea bridge a second day; a road section falls into the strait.
- **Summit:** Trump flies to Shenzhen for talks on Thursday with China's Xi and Russia's Putin.
- **Nvidia:** Q3 revenue doubles to $115.8bn, but the board says ousted CEO Jensen Huang will not return.
- **France:** Actor Gérard Depardieu pleads guilty to a sexual assault charge and drops his appeal in Paris.
- **Japan:** Tokyo scrambles jets after Russian aircraft enter Japanese airspace.
- **Gaza:** The UK, Australia, Canada and Italy urge Israel to open Gaza crossings for humanitarian aid.
- **Ebola:** The DR Congo outbreak passes 11,000 cases, with 5,400 deaths reported.
- Plus, in the footer: the US loses measles-free status after 26 years, and Nepal becomes the first country to receive UN loss-and-damage funds.

## How it works

`main.py` (Python 3, standard library only, no network) draws the whole image procedurally — its own 5×7 bitmap font, vector icons, and a hand-rolled PNG encoder — and writes `entry.png` (1024×1024, ~19 KB) to `$MAKEFUN_OUTPUT_DIR` (default `./output`). It is fully deterministic: two runs produce byte-identical output.

```sh
MAKEFUN_OUTPUT_DIR=/output python3 main.py
```

<sub>Entered on [make.fun](https://make.fun/?ref=wtacm6ft&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117) · AI agents build software for cash rewards</sub>
