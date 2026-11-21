import numpy as np
from .rates import vasicek_bond_price


def swap_payment_dates(maturity, freq):
    """Fechas de pago del swap, en años. freq = pagos por año."""
    n = int(maturity * freq)
    return np.arange(1, n + 1) / freq


def par_swap_rate(r0, a, b, sigma, maturity, freq):
    """Tasa fija que hace que el swap valga 0 hoy."""
    dates = swap_payment_dates(maturity, freq)
    P = vasicek_bond_price(r0, a, b, sigma, dates)
    return (1 - P[-1]) / (P.sum() / freq)


def swap_mtm(t, r_t, r_reset, a, b, sigma, fixed_rate, maturity, freq, notional=1_000_000):
    """MtM en la fecha t, para cada escenario, de quien PAGA fija y RECIBE variable.

    r_reset: tasa corta en la última fecha de reajuste (fija el próximo cupón variable).
    """
    dates = swap_payment_dates(maturity, freq)
    remaining = dates[dates > t + 1e-9]          # pagos que todavía no ocurrieron

    if len(remaining) == 0:                      # el swap ya venció
        return np.zeros_like(r_t)

    delta = 1 / freq
    tau = remaining - t
    P = vasicek_bond_price(r_t[:, None], a, b, sigma, tau[None, :])

    # Tasa variable fijada en el último reajuste, para el próximo pago
    P_reset = vasicek_bond_price(r_reset, a, b, sigma, delta)
    L = (1 / P_reset - 1) / delta

    fixed_leg = notional * fixed_rate * delta * P.sum(axis=1)
    float_leg = notional * ((1 + L * delta) * P[:, 0] - P[:, -1])
    return float_leg - fixed_leg


def simulate_swap_mtm(times, rates, a, b, sigma, fixed_rate, maturity, freq, notional=1_000_000):
    """MtM del swap en todas las fechas y escenarios simulados (tabla n_paths x n_fechas)."""
    mtm = np.zeros_like(rates)
    dt_sim = times[1] - times[0]

    for i, t in enumerate(times):
        t_reset = np.floor(t * freq + 1e-9) / freq      # última fecha de reajuste
        j = int(round(t_reset / dt_sim))                # su columna en la tabla de tasas
        mtm[:, i] = swap_mtm(t, rates[:, i], rates[:, j], a, b, sigma,
                             fixed_rate, maturity, freq, notional)
    return mtm


def simulate_swap_mtm(times, rates, a, b, sigma, fixed_rate, maturity, freq, notional=1_000_000):
    """MtM del swap en todas las fechas y escenarios simulados (tabla n_paths x n_fechas)."""
    mtm = np.zeros_like(rates)
    dt_sim = times[1] - times[0]

    for i, t in enumerate(times):
        t_reset = np.floor(t * freq + 1e-9) / freq      # última fecha de reajuste
        j = int(round(t_reset / dt_sim))                # su columna en la tabla de tasas
        mtm[:, i] = swap_mtm(t, rates[:, i], rates[:, j], a, b, sigma,
                             fixed_rate, maturity, freq, notional)
    return mtm
