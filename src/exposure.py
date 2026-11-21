import numpy as np


def exposure(mtm):
    """Exposición = max(MtM, 0): solo perdés si te deben."""
    return np.maximum(mtm, 0)


def expected_exposure(mtm):
    """EE: promedio de la exposición en cada fecha."""
    return exposure(mtm).mean(axis=0)


def potential_future_exposure(mtm, q=0.95):
    """PFE: percentil q de la exposición en cada fecha."""
    return np.quantile(exposure(mtm), q, axis=0)


def expected_positive_exposure(ee):
    """EPE: promedio de la EE a lo largo del tiempo (fechas equiespaciadas)."""
    return ee.mean()
