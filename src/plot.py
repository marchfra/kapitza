import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from my_formatter import multiple_formatter


def check_stability(a: float, sigma: float) -> bool:
    return a**2 > 2 * sigma


plt.style.use(["grid", "science", "notebook", "mylegend"])

df = pd.read_csv("data/stability.csv")

TOL = 1e-2

df["stability"] = df["endpoint"].apply(lambda x: x < TOL)
df["stability"] = df["stability"].astype(bool)
df["is_stable"] = check_stability(df["a"], df["sigma"])

stable_index = df["stability"]
stable = df[stable_index]
unstable = df[~stable_index]

fig, ax = plt.subplots(1, 1)
MARKER = "s"
SKIP = 1
# ax.scatter(
#     df["a"][::SKIP],
#     df["sigma"][::SKIP],
#     color=check_stability(df["a"][::SKIP], df["sigma"][::SKIP]).map(
#         {True: "green", False: "red"}
#     ),
#     marker="o",
# )
ax.scatter(
    stable["a"][::SKIP],
    stable["sigma"][::SKIP],
    color="green",
    label="Stable",
    marker=MARKER,
)
ax.scatter(
    unstable["a"][::SKIP],
    unstable["sigma"][::SKIP],
    color="red",
    label="Unstable",
    marker=MARKER,
)

# stable_index = df["is_stable"]
# stable = df[stable_index]
# unstable = df[~stable_index]
# MARKER = "."
# ax.scatter(
#     stable["a"][::SKIP],
#     stable["sigma"][::SKIP],
#     color="green",
#     label="Stable",
#     marker=MARKER,
# )
# ax.scatter(
#     unstable["a"][::SKIP],
#     unstable["sigma"][::SKIP],
#     color="red",
#     label="Unstable",
#     marker=MARKER,
# )

a_max = np.sqrt(2 * df["sigma"].max())
a = np.linspace(df["a"].min(), a_max)
ax.plot(a, 0.5 * a**2)

ax.set_title("Stability of the Kapitza pendulum")
ax.set_xlabel(r"$a$")
ax.set_ylabel(r"$\sigma$")

ax.legend()

fig.tight_layout()

df = pd.read_csv("data/trajectory.csv")

fig, ax = plt.subplots(1, 1)
for a in df["a"].unique()[:: SKIP**2]:
    for sigma in df["sigma"].unique()[:: SKIP**2]:
        data = df[df["a"] == a]
        trajectory = data[data["sigma"] == sigma]
        ax.plot(
            trajectory["t"], trajectory["theta"], label=f"a = {a:.2g}, σ = {sigma:.2g}"
        )

ax.set_title("Trajectory of the Kapitza pendulum")
ax.set_xlabel(r"$t$")
ax.set_ylabel(r"$\theta(t)$")

ax.yaxis.set_major_locator(plt.MultipleLocator(np.pi / 6))
ax.yaxis.set_major_formatter(plt.FuncFormatter(multiple_formatter(6)))

fig.tight_layout()
plt.show()
