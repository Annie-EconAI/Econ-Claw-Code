# Romano-Wolf Multiple Hypothesis Testing Correction
# Based on Romano & Wolf (2005, 2016)

import numpy as np
import pandas as pd
from scipy import stats


def romano_wolf(
    outcomes: list[str],
    treatment: str,
    data: pd.DataFrame,
    controls: list[str] | None = None,
    n_bootstrap: int = 1000,
    alpha: float = 0.05,
    seed: int = 42,
) -> pd.DataFrame:
    """Romano-Wolf stepdown adjusted p-values for multiple hypothesis testing.

    Parameters
    ----------
    outcomes : list of outcome variable names
    treatment : treatment variable name
    data : DataFrame with all variables
    controls : optional list of control variable names
    n_bootstrap : number of bootstrap replications
    alpha : significance level
    seed : random seed

    Returns
    -------
    DataFrame with columns: outcome, coef, se, p_unadj, p_rw
    """
    rng = np.random.default_rng(seed)
    n = len(data)
    k = len(outcomes)

    # Step 1: Compute original t-statistics
    orig_stats = []
    for y in outcomes:
        coef, se, p = _ols_coef(data, y, treatment, controls)
        orig_stats.append({'outcome': y, 'coef': coef, 'se': se, 'p_unadj': p, 't': abs(coef / se)})

    # Step 2: Bootstrap under the null
    boot_t = np.zeros((n_bootstrap, k))
    for b in range(n_bootstrap):
        idx = rng.choice(n, size=n, replace=True)
        boot_data = data.iloc[idx].copy()
        # Permute treatment to impose null
        boot_data[treatment] = rng.permutation(boot_data[treatment].values)
        for j, y in enumerate(outcomes):
            coef, se, _ = _ols_coef(boot_data, y, treatment, controls)
            boot_t[b, j] = abs(coef / se) if se > 0 else 0

    # Step 3: Stepdown procedure
    orig_t = np.array([s['t'] for s in orig_stats])
    p_rw = _stepdown(orig_t, boot_t)

    # Build results
    results = []
    for j, s in enumerate(orig_stats):
        results.append({
            'outcome': s['outcome'],
            'coef': round(s['coef'], 4),
            'se': round(s['se'], 4),
            'p_unadj': round(s['p_unadj'], 4),
            'p_rw': round(p_rw[j], 4),
        })
    return pd.DataFrame(results)


def _ols_coef(
    data: pd.DataFrame,
    y: str,
    treatment: str,
    controls: list[str] | None,
) -> tuple[float, float, float]:
    """Simple OLS to get treatment coefficient, SE, and p-value."""
    X_cols = [treatment] + (controls or [])
    mask = data[[y] + X_cols].dropna().index
    Y = data.loc[mask, y].values
    X = data.loc[mask, X_cols].values
    X = np.column_stack([np.ones(len(X)), X])

    try:
        beta = np.linalg.lstsq(X, Y, rcond=None)[0]
        resid = Y - X @ beta
        sigma2 = np.sum(resid**2) / (len(Y) - X.shape[1])
        var_beta = sigma2 * np.linalg.inv(X.T @ X)
        coef = beta[1]  # treatment coefficient
        se = np.sqrt(var_beta[1, 1])
        t_stat = coef / se
        p = 2 * (1 - stats.t.cdf(abs(t_stat), df=len(Y) - X.shape[1]))
        return coef, se, p
    except (np.linalg.LinAlgError, ValueError):
        return 0.0, 1.0, 1.0


def _stepdown(orig_t: np.ndarray, boot_t: np.ndarray) -> np.ndarray:
    """Romano-Wolf stepdown procedure."""
    k = len(orig_t)
    p_rw = np.ones(k)
    remaining = list(range(k))

    # Sort by original t-stat descending
    order = np.argsort(-orig_t)

    for step in range(k):
        if not remaining:
            break
        idx = [j for j in order if j in remaining]
        # Max bootstrap t over remaining hypotheses
        boot_max = boot_t[:, idx].max(axis=1)
        for j in idx:
            p_rw[j] = max(p_rw[j], np.mean(boot_max >= orig_t[j]))
        # Remove rejected hypotheses
        newly_removed = [j for j in idx if p_rw[j] > 0.05]
        if not newly_removed:
            break
        remaining = [j for j in remaining if j not in newly_removed]

    # Enforce monotonicity
    for i in range(1, k):
        j = order[i]
        j_prev = order[i - 1]
        p_rw[j] = max(p_rw[j], p_rw[j_prev])

    return p_rw
