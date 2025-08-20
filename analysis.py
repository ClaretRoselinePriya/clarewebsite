# 23f3000663@ds.study.iitm.ac.in
# Purpose: Interactive, self-documenting correlation demo with reactive widgets.
# Data flow:
#   Cell A -> defines libs, RNG
#   Cell B -> defines UI (sliders)        [produces: n, slope, noise]
#   Cell C -> generates data from UI      [consumes: n, slope, noise] -> df
#   Cell D -> computes metrics            [consumes: df] -> corr
#   Cell E -> dynamic markdown summary    [consumes: n, slope, noise, corr]
#   Cell F -> plot scatter                [consumes: df]
#   Cell G -> preview table               [consumes: df]

import marimo as mo

app = mo.App(title="Interactive Correlation Explorer")

@app.cell
def _():
    # Cell A: imports and RNG (no dependencies)
    import numpy as np, pandas as pd
    import matplotlib.pyplot as plt
    rng = np.random.default_rng(42)
    return np, pd, plt, rng

@app.cell
def _(mo=np):
    # Cell B: UI widgets (source of truth for parameters)
    import marimo as mo
    n     = mo.ui.slider(50, 1000, value=200, step=50, label="Sample size (n)")
    slope = mo.ui.slider(-5.0, 5.0, value=2.0, step=0.5, label="Slope (β₁)")
    noise = mo.ui.slider(0.0, 5.0, value=1.0, step=0.2, label="Noise σ")
    # Display the controls together
    mo.hstack([n, slope, noise])
    return n, slope, noise

@app.cell
def _(np, pd, rng, n, slope, noise):
    # Cell C: data generator (depends on Cell B)
    x = rng.uniform(-3, 3, int(n.value))
    eps = rng.normal(0, float(noise.value), int(n.value))
    y = float(slope.value) * x + eps
    df = pd.DataFrame({"x": x, "y": y})
    return df

@app.cell
def _(np, df):
    # Cell D: derived metric (depends on Cell C)
    corr = float(np.corrcoef(df["x"], df["y"])[0, 1])
    return corr

@app.cell
def _(mo, n, slope, noise, corr):
    # Cell E: dynamic, self-documenting markdown (depends on Cells B & D)
    mo.md(f"""
### Current settings
- **n** = {n.value}, **β₁ (slope)** = {slope.value}, **σ (noise)** = {noise.value}
- **Estimated Pearson r** = {corr:.3f}

**Interpretation:** Increasing σ usually weakens |r|; larger |β₁| strengthens it.
""")

@app.cell
def _(plt, df, mo):
    # Cell F: visualization (depends on Cell C)
    fig, ax = plt.subplots()
    ax.scatter(df["x"], df["y"], alpha=0.6)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("y vs x (linear model with noise)")
    mo.mpl(fig)

@app.cell
def _(df, mo):
    # Cell G: data preview (depends on Cell C)
    mo.accordion({"Preview first 10 rows": mo.ui.table(df.head(10))})

if __name__ == "__main__":
    app.run()
