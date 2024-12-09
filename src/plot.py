import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar

from my_formatter import multiple_formatter

plt.style.use(["grid", "science", "notebook", "mylegend"])

SAVE_FIGURES = True


def check_stability(a: float, sigma: float) -> bool:
    """Check if the Kapitza pendulum is stable according to the Multiscale Method."""
    return a**2 > 2 * sigma


def preprocess_stability(tol: float = 1e-2) -> pd.DataFrame:
    """Preprocess the stability data."""

    df = pd.read_csv("data/stability.csv")

    df["stability"] = df["endpoint"] < tol
    df["is_stable"] = check_stability(df["a"], df["sigma"])

    return df


def num_errors(tol: float, df: pd.DataFrame) -> int:
    """Count the number of errors in the stability data."""
    df["stability"] = df["endpoint"] < tol
    return np.sum(df["stability"] != df["is_stable"])


def optimize_tol() -> float:
    """Find the tolerance (to determine the numerical stability) that minimizes the
    number of errors."""

    df = preprocess_stability(-1)

    result = minimize_scalar(
        num_errors, args=(df,), bounds=(1e-8, 1e-6), method="bounded"
    )

    if not result.success:
        raise ValueError(f"Optimization failed: {result.message}")

    return result.x


def plot_stability(tol: float = 1e-2, skip: int = 1) -> None:
    """Plots the stability of the Kapitza pendulum on the a-sigma plane."""

    df = preprocess_stability(tol)[::skip]

    stable_index = df["stability"]
    stable = df[stable_index]
    unstable = df[~stable_index]

    fig, ax = plt.subplots(1, 1)

    # Plot multiscale method separation line and stability regions
    a_max = np.sqrt(2 * df["sigma"].max())
    a = np.linspace(df["a"].min(), a_max)
    ax.plot(a, 0.5 * a**2, c="k", zorder=-1)
    ax.fill_between(
        a,
        0.5 * a**2,
        color="green",
        linewidth=0,
        alpha=0.15,
        label="Stable",
    )
    ax.fill_between(
        np.linspace(a_max, df["a"].max()),
        df["sigma"].max(),
        color="green",
        linewidth=0,
        alpha=0.15,
    )
    ax.fill_between(
        a,
        0.5 * a**2,
        y2=df["sigma"].max(),
        color="red",
        linewidth=0,
        alpha=0.15,
        label="Unstable",
    )

    # Plot numerical stability points
    ax.scatter(
        stable["a"],
        stable["sigma"],
        color="green",
        label="Numerically stable",
        marker="o",
    )
    ax.scatter(
        unstable["a"],
        unstable["sigma"],
        color="red",
        label="Numerically unstable",
        marker="o",
    )

    ax.set_title(f"Stability of the Kapitza pendulum (tol = {tol:.3g})")
    ax.set_xlabel(r"$a = b/l$")
    ax.set_ylabel(r"$\sigma = g / l \omega^2$")

    ax.legend(loc="lower right", framealpha=1)

    fig.tight_layout()

    if SAVE_FIGURES:
        fig.savefig(f"images/stability_{tol:.3g}.png", dpi=200)


def plot_trajectories(tol: float = 1e-2, skip: int = 2) -> None:
    """Plots the numerically stable trajectories of the Kapitza pendulum for various
    values of a-sigma."""

    df = pd.read_csv("data/trajectory.csv")

    theta_max: float = 0

    fig, ax = plt.subplots(1, 1)
    for a in df["a"].unique()[::skip]:
        for sigma in df["sigma"].unique()[::skip]:
            filt = (df["a"] == a) & (df["sigma"] == sigma)
            traj = df[filt]
            is_stable = check_stability(a, sigma)
            if abs(traj["theta"].iloc[-1]) < tol:
                theta_max = max(theta_max, abs(traj["theta"]).max())
                ax.plot(
                    traj["t"],
                    traj["theta"],
                    ls="--" if not is_stable else "-",
                    alpha=0.5 if not is_stable else 1,
                )

    ax.set_title(
        f"Numerically stable trajectories\nof the Kapitza pendulum (tol = {tol:.3g})"
    )
    ax.set_xlabel(r"$t$")
    ax.set_ylabel(r"$\theta(t)$")

    if theta_max > np.pi / 6:
        ax.yaxis.set_major_locator(plt.MultipleLocator(np.pi / 6))
        ax.yaxis.set_major_formatter(plt.FuncFormatter(multiple_formatter(6)))

    fig.tight_layout()

    if SAVE_FIGURES:
        fig.savefig(f"images/stable_trajs_{tol:.3g}.png", dpi=200)


def plot_errors(tol: float = 1e-2, skip: int = 2) -> None:
    """Plots the numerically unstable but analitically stable trajectories of the
    Kapitza pendulum for various values of a-sigma."""

    df = pd.read_csv("data/trajectory.csv")

    theta_max: float = 0

    fig, ax = plt.subplots(1, 1)
    for a in df["a"].unique()[::skip]:
        for sigma in df["sigma"].unique()[::skip]:
            filt = (df["a"] == a) & (df["sigma"] == sigma)
            traj = df[filt]
            is_stable = check_stability(a, sigma)
            if abs(traj["theta"].iloc[-1]) > tol:
                if is_stable:
                    theta_max = max(theta_max, abs(traj["theta"]).max())
                    ax.plot(traj["t"], traj["theta"])

    ax.set_title(
        f"Numerically unstable but actually stable trajectories\n"
        f"of the Kapitza pendulum (tol = {tol:.3g})"
    )
    ax.set_xlabel(r"$t$")
    ax.set_ylabel(r"$\theta(t)$")

    if theta_max > np.pi / 6:
        ax.yaxis.set_major_locator(plt.MultipleLocator(np.pi / 6))
        ax.yaxis.set_major_formatter(plt.FuncFormatter(multiple_formatter(6)))

    fig.tight_layout()

    if SAVE_FIGURES:
        fig.savefig(f"images/errors_{tol:.3g}.png", dpi=200)


def main() -> None:
    """Main function."""

    opt_tol = optimize_tol()
    print(f"Optimal tolerance: {opt_tol:.3g}")
    phys_tol = 1e-7
    skip = 1

    plot_stability(opt_tol)
    plot_stability(phys_tol)

    plot_trajectories(opt_tol, skip)
    plot_errors(opt_tol, skip)

    plot_trajectories(phys_tol, skip)
    plot_errors(phys_tol, skip)

    plt.show()


if __name__ == "__main__":
    main()
