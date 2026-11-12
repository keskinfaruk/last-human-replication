# The Last Human: data and code

Data and code for

> Keskin, F. (2026). The Last Human: Friday, 29 May, A.D. 2826. A commentary on von Foerster, Mora and Amiot (1960). Submitted to *The Turkish Journal of Population Studies*.

The commentary refits the doomsday equation of von Foerster, Mora and Amiot (1960, *Science* 132, 1291–1295, [doi:10.1126/science.132.3436.1291](https://doi.org/10.1126/science.132.3436.1291)) and dates the last human under constant fertility. Equation, table, figure and note numbers below refer to the commentary.

## Files

| File | Contents |
|:--|:--|
| `doomsday.py` | Table 1 and the doomsday fits |
| `last_human.py` | Table 2 and the date of the last human |
| `figures.py` | Figures 1 and 2 |
| `common.py` | Data loading and the least-squares fit, used by the three scripts |
| `data/vf1960_sources.csv` | The estimates of 1960, from the sources cited in their Figure 1 (Table B1) |
| `data/hyde35_world.csv` | World population from HYDE 3.5, 10,000 BC to AD 2025 |
| `data/wpp2024_world.csv` | World population from UN World Population Prospects 2024, 1950 to 2100 |
| `figures/` | Figures 1 and 2 |

[`data/README.md`](data/README.md) describes each data file, its columns and its source.

## How to run

You need Python 3. The results were made with Python 3.13.

```
pip install -r requirements.txt
python doomsday.py
python last_human.py
python figures.py
```

Each script runs in a few seconds. It prints its results under headings that follow the sections of the commentary. `figures.py` also writes `figures/fig1.png` and `figures/fig2.png`.

## License

- Code: MIT License (see `LICENSE`).
- `data/vf1960_sources.csv`: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Please cite the commentary.
- HYDE 3.5 and WPP 2024 data: the terms of their providers. Please cite the original sources.
