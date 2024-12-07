"""Provides a function to format the axis labels of a plot"""

from typing import Callable

import numpy as np

# def multiple_formatter(
#     denominator: int = 12,
#     number: float = np.pi,
#     latex: str = r"\pi",
# ) -> Callable:
#     """Produce a multiple formatter"""

#     def gcd(a: int, b: int) -> int:
#         """Compute the greatest common divisor of a and b"""
#         while b:
#             a, b = b, a % b
#         return a

#     def _multiple_formatter(x, pos) -> str:
#         den = denominator
#         num = int(np.rint(den * x / number))
#         com = gcd(num, den)
#         num, den = int(num / com), int(den / com)
#         if den == 1:
#             if num == 0:
#                 return r"$0$"
#             if num == 1:
#                 return rf"${latex}$"
#             if num == -1:
#                 return rf"$-{latex}$"
#             return rf"${num}{latex}$"
#         else:
#             if num == 1:
#                 return r"$\frac{%s}{%s}$" % (latex, den)
#             if num == -1:
#                 return r"$\frac{-%s}{%s}$" % (latex, den)
#             return r"$\frac{%s%s}{%s}$" % (num, latex, den)

#     return _multiple_formatter


def multiple_formatter(denominator=12, number=np.pi, latex=r"\pi"):
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    def _multiple_formatter(x, pos):
        den = denominator
        num = int(np.rint(den * x / number))
        com = gcd(num, den)
        num, den = int(num / com), int(den / com)
        if den == 1:
            if num == 0:
                return r"$0$"
            if num == 1:
                return r"$%s$" % latex
            elif num == -1:
                return r"$-%s$" % latex
            else:
                return r"$%s%s$" % (num, latex)
        else:
            if num == 1:
                return r"$\frac{%s}{%s}$" % (latex, den)
            elif num == -1:
                return r"$\frac{-%s}{%s}$" % (latex, den)
            else:
                return r"$\frac{%s%s}{%s}$" % (num, latex, den)

    return _multiple_formatter
