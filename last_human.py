"""Table 2 and the date of the last human. Run: python last_human.py

Equation 7: t_L = t_s + T ln(N_s) / ln(1 / NRR), with NRR = TFR / 2.1 (Note 3).
"""

import datetime

import numpy as np

from common import UN_POPULATION, add_years, format_date, print_heading


# ===========================================================================
# Inputs
# ===========================================================================

# Start: UN projection for 1 July 2026.
START_DATE = datetime.date(2026, 7, 1)
START_YEAR = 2026.5
START_POPULATION = UN_POPULATION.loc[2026]

REPLACEMENT_TFR = 2.1

# Table 2: label, TFR, T (mean age of mothers at childbirth).
# Sources: Ministry of Data and Statistics (2026), Eurostat (2026), TurkStat (2026).
TABLE_2_ROWS = [
    ("South Korea, 2025", 0.80, 33.8),
    ("European Union, 2024", 1.34, 31.3),
    ("Türkiye, 2025", 1.42, 29.4),
]
WORLD_TFR_2023 = 2.25   # UN WPP 2024

_, KOREA_TFR, KOREA_T = TABLE_2_ROWS[0]   # South Korea, 2025
KOREA_TFR_2023 = 0.72


# ===========================================================================
# Equations
# ===========================================================================

def net_reproduction_rate(tfr):
    """NRR = TFR / 2.1."""
    return tfr / REPLACEMENT_TFR


def halving_time(tfr, T):
    """T ln 2 / ln(1 / NRR)."""
    return T * np.log(2) / np.log(1 / net_reproduction_rate(tfr))


def years_to_last_human(tfr, T, start_population=START_POPULATION):
    """T ln(N_s) / ln(1 / NRR)."""
    return T * np.log(start_population) / np.log(1 / net_reproduction_rate(tfr))


def year_of_last_human(tfr, T, start_year=START_YEAR, start_population=START_POPULATION):
    """Equation 7, as a decimal year."""
    return start_year + years_to_last_human(tfr, T, start_population)


def date_of_last_human(tfr, T):
    """Equation 7, as a date."""
    return add_years(START_DATE, years_to_last_human(tfr, T))


# ===========================================================================
# 1. The start
# ===========================================================================

def print_start():
    print_heading("1. The start")
    print(f"  N_s = {START_POPULATION / 1e9:.2f} billion in mid-2026 (UN projection)")
    print(f"  ln N_s = {np.log(START_POPULATION):.2f}")
    print(f"  Halvings from N_s to one person: log2 N_s = {np.log2(START_POPULATION):.1f}")


# ===========================================================================
# 2. Table 2
# ===========================================================================

def print_table_2():
    print_heading("2. Table 2. The last human under constant fertility")
    print(f"  {'Fertility held constant':24s} {'TFR':>5s} {'T':>5s} {'NRR':>6s}"
          f" {'Halving':>8s} {'t_L':>8s}   Population = 1 in")

    for label, tfr, T in TABLE_2_ROWS:
        t_last = year_of_last_human(tfr, T)
        print(f"  {label:24s} {tfr:5.2f} {T:5.1f} {net_reproduction_rate(tfr):6.3f}"
              f" {halving_time(tfr, T):8.1f} {t_last:8.1f}   {int(t_last)}")

    # NRR above 1: the population never reaches one person.
    nrr_world = net_reproduction_rate(WORLD_TFR_2023)
    print(f"  {'World, 2023':24s} {WORLD_TFR_2023:5.2f} {'-':>5s} {nrr_world:6.3f}"
          f" {'-':>8s} {'-':>8s}   never")


# ===========================================================================
# 3. The date
# ===========================================================================

def print_date():
    print_heading("3. The date (South Korea, 2025)")

    years = years_to_last_human(KOREA_TFR, KOREA_T)
    date = date_of_last_human(KOREA_TFR, KOREA_T)
    print(f"  {years:.2f} years after 1 July 2026: {format_date(date)}")

    # TFR 0.80 is rounded: the true value lies between 0.795 and 0.805.
    for tfr in (0.795, 0.805):
        print(f"  TFR {tfr}: {format_date(date_of_last_human(tfr, KOREA_T))}")


# ===========================================================================
# 4. Sensitivity
# ===========================================================================

def print_sensitivity():
    print_heading("4. Sensitivity (South Korea, 2025)")

    print(f"  T = 27: {year_of_last_human(KOREA_TFR, 27):.1f}")

    # UN projection to its peak, then Korean fertility.
    peak_population = UN_POPULATION.max()
    peak_year = UN_POPULATION[UN_POPULATION == peak_population].index[0]
    t_last = year_of_last_human(KOREA_TFR, KOREA_T,
                                start_year=peak_year + 0.5, start_population=peak_population)
    print(f"  UN projection to its peak ({peak_population / 1e9:.2f} billion in {peak_year}),"
          f" then TFR {KOREA_TFR:.2f}: {t_last:.1f}")

    # Korean TFR of 2023.
    t_last_2023 = year_of_last_human(KOREA_TFR_2023, KOREA_T)
    t_last_2025 = year_of_last_human(KOREA_TFR, KOREA_T)
    print(f"  TFR {KOREA_TFR_2023} (2023): {t_last_2023:.1f},"
          f" {t_last_2025 - t_last_2023:.0f} years earlier than with TFR {KOREA_TFR:.2f}")


# ===========================================================================
# 5. Conclusion
# ===========================================================================

def print_conclusion():
    """Great-great-grandchildren: four generations, one per (1 / NRR)**4 people."""
    print_heading("5. Conclusion")
    people_per_descendant = (1 / net_reproduction_rate(KOREA_TFR)) ** 4
    print(f"  At TFR {KOREA_TFR:.2f}: one great-great-grandchild"
          f" for every {people_per_descendant:.0f} people today")


# ===========================================================================
# Run
# ===========================================================================

def main():
    print_start()
    print_table_2()
    print_date()
    print_sensitivity()
    print_conclusion()


if __name__ == "__main__":
    main()
