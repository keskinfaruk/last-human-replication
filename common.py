"""Data and functions shared by doomsday.py, last_human.py and figures.py."""

import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit


# ===========================================================================
# 1. Data
# ===========================================================================

DATA_FOLDER = Path(__file__).parent / "data"

# --- 1a. The 1960 estimates (Table B1). 1958 is left out, as in 1960: 25 values.
vf1960 = pd.read_csv(DATA_FOLDER / "vf1960_sources.csv")
in_fit = vf1960[vf1960["year"] != 1958]
FIT_YEARS = in_fit["year"].to_numpy()
FIT_POPULATION = in_fit["population"].to_numpy(float)

# --- 1b. HYDE 3.5: columns base, lower, upper. Example: HYDE["base"].loc[1800].
HYDE = pd.read_csv(DATA_FOLDER / "hyde35_world.csv", index_col="year")

# --- 1c. UN WPP 2024, 1 July. Example: UN_POPULATION.loc[2026].
UN_POPULATION = pd.read_csv(DATA_FOLDER / "wpp2024_world.csv", index_col="year")["population"]


# --- 1d. The 1960 values plus UN estimates every five years (Table 1, Figure 2)

def points_with_un(last_year):
    """Return years and population: the 25 values of 1960 and UN 1960, 1965, ..., last_year."""
    un_years = list(range(1960, last_year + 1, 5))   # empty before 1960
    years = np.concatenate([FIT_YEARS, un_years])
    population = np.concatenate([FIT_POPULATION, UN_POPULATION.loc[un_years]])
    return years, population


# ===========================================================================
# 2. The 1960 fit (Equation 5)
# ===========================================================================

T0_1960 = 2026.87
K_1960 = 1.79e11
k_1960 = 0.99

T0_1960_ERROR = 5.50   # published ± of t0
RMS_1960 = 0.07        # published RMS error, about 7%


def equation_5(year):
    """N = K / (t0 - t)**k with the 1960 values."""
    tau = T0_1960 - np.asarray(year, float)
    return K_1960 / tau ** k_1960


# ===========================================================================
# 3. Functions
# ===========================================================================

# --- 3a. Values between HYDE dates (Note 2)

def make_interpolator(population):
    """Return a function for the population in any year (constant growth between dates)."""
    positive = population[population > 0].sort_index()   # ln 0 does not exist
    years = positive.index.to_numpy()
    log_values = np.log(positive.to_numpy())

    def population_in(year):
        return float(np.exp(np.interp(year, years, log_values)))

    return population_in


hyde_base = make_interpolator(HYDE["base"])   # HYDE 3.5 baseline in any year


# --- 3b. The least-squares fit of Equation 3

def log_equation_3(t, log_K, k, t0):
    """Equation 3 in logarithms: ln N = ln K - k ln(t0 - t)."""
    return log_K - k * np.log(t0 - t)


def fit_equation_3(years, population):
    """Fit Equation 3 by least squares on ln N. Return t0, k, K, se_t0, rms and n."""
    t = np.asarray(years, float)
    log_n = np.log(np.asarray(population, float))

    # Start near the 1960 result. t0 must come after the last data year.
    start = [np.log(1.8e11), 1.0, t.max() + 30]
    bounds = ([0, 0.05, t.max() + 0.01], [300, 50, 1e6])

    # Best ln K, k and t0, and their covariance matrix.
    (log_K, k, t0), covariance = curve_fit(log_equation_3, t, log_n, p0=start, bounds=bounds)
    standard_errors = np.sqrt(np.diag(covariance))

    errors = log_equation_3(t, log_K, k, t0) - log_n

    return {
        "t0": t0,
        "k": k,
        "K": np.exp(log_K),
        "se_t0": standard_errors[2],
        "rms": np.sqrt(np.mean(errors ** 2)),
        "n": len(t),
    }


# --- 3c. Dates

DAYS_PER_YEAR = 365.2425   # mean Gregorian year


def add_years(start_date, years):
    """The date a number of years after start_date."""
    return start_date + datetime.timedelta(days=years * DAYS_PER_YEAR)


def decimal_year_to_date(decimal_year):
    """1997.8 -> a date in 1997."""
    year = int(np.floor(decimal_year))
    return add_years(datetime.date(year, 1, 1), decimal_year - year)


def format_date(date):
    """Example: Friday 29 May 2826."""
    return f"{date:%A} {date.day} {date:%B %Y}"


# --- 3d. Printed output

def print_heading(title):
    """Print a title with a line under it."""
    print()
    print(title)
    print("-" * len(title))
