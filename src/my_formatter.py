"""Provides a function to format the axis labels of a plot"""

from typing import Callable

import numpy as np


def gcd(a: int, b: int) -> int:
    """Compute the greatest common divisor of a and b"""
    while b:
        a, b = b, a % b
    return a


def simplify_fraction(numerator: int, denominator: int) -> tuple[int, int]:
    """Simplify a fraction"""
    common = gcd(numerator, denominator)
    return numerator // common, denominator // common


def latex_frac(numerator: int, denominator: int) -> str:
    """Return a LaTeX representation of a fraction"""
    return r"\frac{" + str(numerator) + "}{" + str(denominator) + "}"


def multiple_formatter(
    denominator: int = 12,
    multiple: float = np.pi,
    latex_multiple: str = r"\pi",
) -> Callable[[float, float], str]:
    """Produce a multiple formatter"""

    def _multiple_formatter(x: float, _: float) -> str:
        den = denominator
        num = int(np.rint(den * x / multiple))
        num, den = simplify_fraction(num, den)

        if den == 1:
            if num == 0:
                return r"$0$"
            elif num == 1:
                return rf"${latex_multiple}$"
            elif num == -1:
                return rf"$-{latex_multiple}$"
            else:
                return rf"${num}{latex_multiple}$"
        else:
            if num == 1:
                return r"$\frac{%s}{%s}$" % (latex_multiple, den)
            elif num == -1:
                return r"$\frac{-%s}{%s}$" % (latex_multiple, den)
            else:
                return r"$\frac{%s%s}{%s}$" % (num, latex_multiple, den)

    return _multiple_formatter


if __name__ == "__main__":
    print(f"{gcd(12, 8) = }")
    print(f"{gcd(8, 13) = }")
    print(f"{gcd(12, 2) = }")

    print(f"{simplify_fraction(12, 8) = }")
    print(f"{simplify_fraction(8, 13) = }")
    print(f"{simplify_fraction(12, 2) = }")
    print(f"{simplify_fraction(2, 12) = }")
