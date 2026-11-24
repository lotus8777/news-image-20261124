# 24 November 2026: The World in One Image

[![news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/lotus8777/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/lotus8777/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

An entry for the [news-image-20261124](https://make.fun/bounty/news-image-20261124) bounty on make.fun: one cartoon front page summing up Tuesday 24 November 2026. Nvidia's board votes unanimously to bring Jensen Huang back as CEO after eleven days away, and the shares jump about 33%; Meduza and Mediazona put the Russian war death toll above 700,000 from leaked Rosstat records; Russian jets trigger a brief air-raid warning on South Korea's Ulleung Island; a Ukrainian strike halts the Novoshakhtinsk refinery; and Iran vows to use all its tools against the U.S. naval blockade.

## How it works

`main.ts` (Node 22, standard library only) checks the pre-built `entry.png` beside it — PNG signature, under 1 MiB, at most 1024 by 1024 — and copies it byte-for-byte into the output directory. `build_poster.py` is the script that drew the poster; it stays in the repository as documentation and is never run by the entrypoint.

## Build

```sh
python3 build_poster.py   # redraws entry.png; rebuilding gives identical bytes
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

Referral code: `gvm444ds`
