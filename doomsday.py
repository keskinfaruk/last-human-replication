"""Table 1 and the other doomsday fits. Run: python doomsday.py"""

import numpy as np
from scipy.optimize import brentq

from common import (
    FIT_POPULATION,
    FIT_YEARS,
    HYDE,
    RMS_1960,
    T0_1960,
    T0_1960_ERROR,
    UN_POPULATION,
    decimal_year_to_date,
    equation_5,
    fit_equation_3,
    hyde_base,
    k_1960,
    make_interpolator,
    points_with_un,
    print_heading,
)


# ===========================================================================
# 1. Table 1
# ===========================================================================

def print_table_1_row(label, years, population):
    """Fit Equation 3, print one row of Table 1, return the fit."""
    fit = fit_equation_3(years, population)
    print(f"  {label:42s} {fit['n']:6d}  {fit['t0']:7.2f} ± {fit['se_t0']:5.2f}"
          f"  {fit['k']:5.3f}  {100 * fit['rms']:7.1f}   {decimal_year_to_date(fit['t0'])}")
    return fit


def print_table_1():
    print_heading("1. Table 1. Doomsday refitted (least squares on ln N, ± is one standard error)")
    print(f"  {'Data':42s} {'Points':>6s}  {'Doomsday t0':>15s}  {'k':>5s}"
          f"  {'RMS (%)':>7s}   Date of t0")

    # Row 1. The published fit (not refitted).
    print(f"  {'Original paper (1960)':42s} {'-':>6s}  {T0_1960:7.2f} ± {T0_1960_ERROR:5.2f}"
          f"  {k_1960:5.3f}  {100 * RMS_1960:7.0f}")

    # Row 2. The 25 values of 1960.
    fit_1960 = print_table_1_row("1960 points, from their sources", FIT_YEARS, FIT_POPULATION)

    # Row 3. HYDE 3.5 at the same dates.
    values = [hyde_base(year) for year in FIT_YEARS]
    print_table_1_row("HYDE 3.5 at the same dates", FIT_YEARS, values)

    # Rows 4 and 5. HYDE 3.5 upper and lower estimates at the same dates.
    for estimate in ("upper", "lower"):
        hyde_estimate = make_interpolator(HYDE[estimate])
        values = [hyde_estimate(year) for year in FIT_YEARS]
        print_table_1_row(f"HYDE 3.5 {estimate} estimate, same dates", FIT_YEARS, values)

    # Row 6. The 1960 values, AD 0 replaced by HYDE 3.5.
    values = FIT_POPULATION.copy()
    values[FIT_YEARS == 0] = hyde_base(0)
    print_table_1_row("1960 points, AD 0 replaced by HYDE 3.5", FIT_YEARS, values)

    # Row 7. All HYDE 3.5 values from AD 0 to 1957.
    hyde_0_to_1957 = HYDE.loc[0:1957, "base"]
    print_table_1_row("HYDE 3.5, all values from AD 0 to 1957",
                      hyde_0_to_1957.index, hyde_0_to_1957)

    # Rows 8 to 10. The 1960 values plus UN estimates every five years.
    for last_year in (1980, 2000, 2020):
        years, values = points_with_un(last_year)
        print_table_1_row(f"1960 points + UN, 1960-{last_year}", years, values)

    # K of row 2 (section Replication).
    print()
    print(f"  K for the 1960 points, from their sources: {fit_1960['K'] / 1e11:.2f} x 10^11")


# ===========================================================================
# 2. The Same Model with Today's Estimates
# ===========================================================================

def year_equation_5_falls_below_un():
    """The year in which Equation 5 falls below the UN estimates (searched 1975-2010)."""
    un_years = UN_POPULATION.index + 0.5   # UN values are for 1 July
    un_values = UN_POPULATION.to_numpy()

    def log_difference(year):
        return np.log(equation_5(year)) - np.log(np.interp(year, un_years, un_values))

    return brentq(log_difference, 1975, 2010)


def print_todays_estimates():
    print_heading("2. The Same Model with Today's Estimates")

    higher = sum(hyde_base(year) > value for year, value in zip(FIT_YEARS, FIT_POPULATION))
    print(f"  HYDE 3.5 is higher than {higher} of the {len(FIT_YEARS)} values of 1960")

    value_1960 = FIT_POPULATION[FIT_YEARS == 0][0]
    print(f"  AD 0: HYDE 3.5 {hyde_base(0) / 1e6:.0f} million,"
          f" 1960 value {value_1960 / 1e6:.0f} million")
    print(f"  AD 0: HYDE 3.5 lower estimate {HYDE['lower'].loc[0] / 1e6:.0f} million,"
          f" upper estimate {HYDE['upper'].loc[0] / 1e6:.0f} million")

    print(f"  Equation 5 falls below the UN estimates in {year_equation_5_falls_below_un():.2f}")
    print(f"  1 July 2026: Equation 5 gives {equation_5(2026.5) / 1e9:.0f} billion,"
          f" the UN projection {UN_POPULATION.loc[2026] / 1e9:.2f} billion")


# ===========================================================================
# 3. What the Model Left Out
# ===========================================================================

def print_growth_rate_2023():
    """Equation 4, alpha = k / tau, in mid-2023."""
    print_heading("3. What the Model Left Out")
    alpha = k_1960 / (T0_1960 - 2023.5)
    print(f"  Equation 4, growth rate in mid-2023: {100 * alpha:.1f}% a year")


# ===========================================================================
# 4. Appendix A
# ===========================================================================

def print_doubling_time():
    """Equation A4: doubling time = (1 - 2**(-1/k)) tau."""
    print_heading("4. Appendix A")
    factor = 2 ** (-1 / k_1960)
    print(f"  2^(-1/k) = {factor:.3f}, so the doubling time is {1 - factor:.3f} tau")


# ===========================================================================
# Run
# ===========================================================================

def main():
    print_table_1()
    print_todays_estimates()
    print_growth_rate_2023()
    print_doubling_time()


if __name__ == "__main__":
    main()
