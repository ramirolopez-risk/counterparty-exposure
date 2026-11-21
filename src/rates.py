import numpy as np


def simulate_vasicek(r0, a, b, sigma, T, n_steps, n_paths, seed=None):
    """Simula trayectorias de la tasa corta con el modelo de Vasicek."""
    rng = np.random.default_rng(seed)
    dt = T / n_steps

    rates = np.zeros((n_paths, n_steps + 1))
    rates[:, 0] = r0

    for t in range(n_steps):
        z = rng.standard_normal(n_paths)
        rates[:, t + 1] = (rates[:, t]
                           + a * (b - rates[:, t]) * dt
                           + sigma * np.sqrt(dt) * z)

    times = np.linspace(0, T, n_steps + 1)
    return times, rates


def vasicek_mean(r0, a, b, t):
    """Media teórica de r(t)."""
    return b + (r0 - b) * np.exp(-a * t)


def vasicek_var(a, sigma, t):
    """Varianza teórica de r(t)."""
    return sigma**2 / (2 * a) * (1 - np.exp(-2 * a * t))


def vasicek_bond_price(r, a, b, sigma, tau):
    """Precio de un bono cupón cero que paga 1 dentro de tau años, dada la tasa corta r."""
    B = (1 - np.exp(-a * tau)) / a
    lnA = (B - tau) * (a**2 * b - sigma**2 / 2) / a**2 - sigma**2 * B**2 / (4 * a)
    return np.exp(lnA - B * r)
