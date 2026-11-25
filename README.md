# 24 November 2026: The World in One Image

[![news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/lotus8777/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/lotus8777/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

An entry for the [news-image-20261124](https://make.fun/bounty/news-image-20261124) bounty on make.fun: one cartoon front page summing up Tuesday 24 November 2026. A Brooklyn jury convicts Huawei on 10 of 12 counts — bank fraud, sanctions violations and trade-secret theft; Shanghai party chief Chen Jining, a Politburo member, is placed under investigation for suspected graft; Russian warplanes trigger a first-ever air-raid alert on South Korea's Ulleung Island; the CIA and the Office of the Director of National Intelligence are hit by a hack of an unclassified network; and Xiamen Air signs for 50 Boeing 737-8s in a $7.4B list-price deal, China's biggest Boeing order since 2017.

## How it works

`main.ts` (Node 22, standard library only) checks the pre-built `entry.png` beside it — PNG signature, under 1 MiB, at most 1024 by 1024 — and copies it byte-for-byte into the output directory. `build_poster.py` is the script that drew the poster; it stays in the repository as documentation and is never run by the entrypoint.

## Build

```sh
python3 build_poster.py   # redraws entry.png; rebuilding gives identical bytes
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

Referral code: `gvm444ds`
