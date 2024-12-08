import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from my_formatter import multiple_formatter

plt.style.use(["grid", "science", "notebook", "mylegend"])

SAVE_FIGURES = False


def check_stability(a: float, sigma: float) -> bool:
    """Check if the Kapitza pendulum is stable according to the Multiscale Method."""
    return a**2 > 2 * sigma


def preprocess_stability(tol: float = 1e-2) -> pd.DataFrame:
    """Preprocess the stability data."""

    df = pd.read_csv("data/stability.csv")

    df["stability"] = df["endpoint"].apply(lambda x: x < tol)
    df["stability"] = df["stability"].astype(bool)
    df["is_stable"] = check_stability(df["a"], df["sigma"])

    return df


def plot_stability(skip: int = 1) -> None:
    """Plots the stability of the Kapitza pendulum on the a-sigma plane."""

    df = preprocess_stability()[::skip]

    stable_index = df["stability"]
    stable = df[stable_index]
    unstable = df[~stable_index]

    fig, ax = plt.subplots(1, 1)
    marker = "s"
    # ax.scatter(
    #     df["a"],
    #     df["sigma"],
    #     color=df["is_stable"].map({True: "green", False: "red"}),
    #     marker="o",
    # )
    ax.scatter(
        stable["a"], stable["sigma"], color="green", label="Stable", marker=marker
    )
    ax.scatter(
        unstable["a"], unstable["sigma"], color="red", label="Unstable", marker=marker
    )

    # Plot multiscale method separation line
    a_max = np.sqrt(2 * df["sigma"].max())
    a = np.linspace(df["a"].min(), a_max)
    ax.plot(a, 0.5 * a**2)

    ax.set_title("Stability of the Kapitza pendulum")
    ax.set_xlabel(r"$a$")
    ax.set_ylabel(r"$\sigma$")

    ax.legend()

    fig.tight_layout()

    if SAVE_FIGURES:
        fig.savefig("figures/stability.pdf", dpi=200)


def plot_trajectories(skip: int = 2) -> None:
    """Plots the trajectories of the Kapitza pendulum for various values of a-sigma."""

    df = pd.read_csv("data/trajectory.csv")

    fig, ax = plt.subplots(1, 1)
    for a in df["a"].unique()[::skip]:
        for sigma in df["sigma"].unique()[::skip]:
            filt = (df["a"] == a) & (df["sigma"] == sigma)
            trajectory = df[filt]
            ax.plot(
                trajectory["t"],
                trajectory["theta"],
                label=r"$a$ = " + f"{a:.2g}, " + r"$\sigma$ = " + f"{sigma:.2g}",
            )

    ax.set_title("Trajectory of the Kapitza pendulum")
    ax.set_xlabel(r"$t$")
    ax.set_ylabel(r"$\theta(t)$")

    ax.legend(ncol=3)

    ax.yaxis.set_major_locator(plt.MultipleLocator(np.pi / 6))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(multiple_formatter(6)))

    fig.tight_layout()

    if SAVE_FIGURES:
        fig.savefig("figures/trajectory.pdf", dpi=200)


def main() -> None:
    """Main function."""

    plot_stability()

    plot_trajectories(20)

    plt.show()


if __name__ == "__main__":
    main()
