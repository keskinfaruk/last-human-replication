# Data

Three CSV files, each with one header row. Population is in persons.

## vf1960_sources.csv

The estimates of world population behind Figure 1 of von Foerster, Mora and Amiot (1960). Each row is one value from one source, as in Table B1 of the commentary.

**Source.** Compiled for the commentary from the sources that the 1960 paper cites.

| Column | Contents |
|:--|:--|
| `year` | Year of the estimate (A.D.) |
| `population` | World population, from the source |
| `ref` | Source number in the reference list of the 1960 paper |
| `source` | Author, year, page and table of the source |

The fits leave out 1958, as the 1960 paper did.

## hyde35_world.csv

World population from HYDE 3.5, 10,000 BC to AD 2025.

**Source.** Klein Goldewijk, K. (2025). *HYDE Data for the Global Carbon Budget (2025)* (HYDE 3.5) [Data set]. Utrecht University. [doi:10.24416/UU01-F45D44](https://doi.org/10.24416/UU01-F45D44). The values are the "Total" row of `txt/popc_r.txt` in the download, rounded to whole persons.

| Column | Contents |
|:--|:--|
| `year` | Year. Negative years are BC |
| `base` | Baseline estimate |
| `lower` | Lower estimate (0 in 10,000 BC) |
| `upper` | Upper estimate |

## wpp2024_world.csv

World population on 1 July, 1950 to 2100.

**Source.** United Nations (2024). *World Population Prospects 2024*. [population.un.org/wpp](https://population.un.org/wpp/)

| Column | Contents |
|:--|:--|
| `year` | Year |
| `population` | World population on 1 July |
| `type` | `estimate` to 2023, `projection` (medium variant) from 2024 |

## License

- `vf1960_sources.csv`: © 2026 Faruk Keskin, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Please cite the commentary.
- `hyde35_world.csv` and `wpp2024_world.csv`: the terms of their providers. Please cite the original sources.
