"""Figures 1 and 2, written to figures/. Run: python figures.py"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")   # write files, open no window
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FixedLocator, NullLocator

from common import (
    FIT_POPULATION,
    FIT_YEARS,
    K_1960,
    T0_1960,
    UN_POPULATION,
    fit_equation_3,
    hyde_base,
    k_1960,
    points_with_un,
    print_heading,
)

OUTPUT_FOLDER = Path(__file__).parent / "figures"

# Black and white, serif font, 600 dpi.
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "font.size": 10,
    "axes.linewidth": 0.6,
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
    "savefig.dpi": 600,
})


def dooms_time(year):
    """tau = t0 - t."""
    return T0_1960 - np.asarray(year, float)


def save(fig, file_name):
    fig.tight_layout()
    fig.savefig(OUTPUT_FOLDER / file_name)
    plt.close(fig)


# ===========================================================================
# Figure 1
# ===========================================================================

def draw_figure_1():
    """Population against dooms-time, both on log scales."""
    fig, ax = plt.subplots(figsize=(6.0, 4.2))

    # Equation 5 (line).
    tau = np.geomspace(1, 2100, 300)
    ax.plot(tau, K_1960 / tau ** k_1960, "k-", lw=0.9,
            label="Equation 5 (1960 fit)")

    # 1960 values (open circles).
    ax.plot(dooms_time(FIT_YEARS), FIT_POPULATION, "o", mfc="white", mec="k", ms=5, mew=0.8,
            label="1960 estimates")

    # HYDE 3.5 at the same dates (filled circles).
    hyde_values = [hyde_base(year) for year in FIT_YEARS]
    ax.plot(dooms_time(FIT_YEARS), hyde_values, "o", mfc="k", mec="k", ms=3,
            label="HYDE 3.5, same dates")

    # UN every five years, 1960-2020 (crosses).
    un_years = list(range(1960, 2021, 5))
    un_values = UN_POPULATION.loc[un_years]
    ax.plot(dooms_time(un_years), un_values, "x", color="k", ms=5, mew=0.9,
            label="UN WPP 2024, 1960–2020")

    # Log axes. Dooms-time falls from left to right.
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(2100, 1.5)
    ax.set_ylim(5e7, 2e11)

    # Bottom axis: calendar years.
    year_ticks = [0, 1000, 1500, 1800, 1900, 1950, 2000, 2020]
    ax.xaxis.set_major_locator(FixedLocator(list(dooms_time(year_ticks))))
    ax.xaxis.set_minor_locator(NullLocator())
    ax.set_xticklabels([str(year) for year in year_ticks])
    ax.set_xlabel("Year (A.D.)")

    # Top axis: dooms-time.
    top = ax.secondary_xaxis("top")
    top.set_xticks([1000, 100, 10, 2])
    top.set_xticklabels(["1000", "100", "10", "2"])
    top.xaxis.set_minor_locator(NullLocator())
    top.set_xlabel(f"Dooms-time τ = {T0_1960} − t (years)")

    ax.set_ylabel("World population N")
    ax.legend(frameon=False, loc="upper left", fontsize=9)
    save(fig, "fig1.png")


# ===========================================================================
# Figure 2
# ===========================================================================

def refit_as_data_accumulate():
    """t0 and its SE for the 1960 values plus UN data up to 1956, 1960, ..., 2020."""
    last_years = [1956] + list(range(1960, 2021, 5))
    t0_values = []
    t0_errors = []

    for last_year in last_years:
        fit = fit_equation_3(*points_with_un(last_year))
        t0_values.append(fit["t0"])
        t0_errors.append(fit["se_t0"])

    return last_years, t0_values, t0_errors


def draw_figure_2():
    """Estimated doomsday against the last year of data used."""
    last_years, t0_values, t0_errors = refit_as_data_accumulate()

    print_heading("Figure 2. Doomsday refitted as data accumulate")
    print("  Years ahead = doomsday t0 minus the last year of data.")
    print()
    print("  Last year   Doomsday t0 ± 1 SE   Years ahead")
    for last_year, t0, error in zip(last_years, t0_values, t0_errors):
        print(f"  {last_year:9d}   {t0:11.1f} ± {error:4.1f}   {t0 - last_year:11.1f}")

    fig, ax = plt.subplots(figsize=(6.0, 3.8))
    ax.errorbar(last_years, t0_values, yerr=t0_errors, fmt="o", color="k", mfc="k", ms=4,
                capsize=2, lw=0.8, label="Estimated doomsday ± 1 SE")
    ax.axhline(T0_1960, color="k", lw=0.6, ls=":", label=f"1960 estimate ({T0_1960})")
    ax.set_xlim(1950, 2030)
    ax.set_ylim(1950, 2070)
    ax.set_xlabel("Last year of data used")
    ax.set_ylabel("Estimated doomsday t$_0$")
    ax.legend(frameon=False, loc="upper left", fontsize=9)
    save(fig, "fig2.png")


# ===========================================================================
# Run
# ===========================================================================

def main():
    OUTPUT_FOLDER.mkdir(exist_ok=True)
    draw_figure_1()
    draw_figure_2()
    print()
    print(f"Figures written to {OUTPUT_FOLDER}")


if __name__ == "__main__":
    main()
