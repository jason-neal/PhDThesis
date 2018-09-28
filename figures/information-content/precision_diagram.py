#!/usr/bin/env python
import numpy as np
import matplotlib
from matplotlib import rcParams
rcParams["font.family"] = "DejaVu Serif"
import matplotlib.pyplot as plt
from matplotlib.patches import ArrowStyle


if __name__ == "__main__":

    x = np.arange(0, 1.1, 0.01)
    sigma = 0.2
    mean = .7
    mean2 = mean + 0.08
    plt.figure(figsize=(8,4))
    ax = plt.subplot(111)
    g1 = lambda x: 1 - 0.5 / np.sqrt(2 * np.pi * sigma ** 2) * np.exp(
        -(x - mean) ** 2 / 2 / sigma ** 2
    )
    g2 = lambda x: 1 - 0.5 / np.sqrt(2 * np.pi * sigma ** 2) * np.exp(
        -(x - mean2) ** 2 / 2 / sigma ** 2
    )
    # y2 = np.cos(x + np.pi/12)

    ax.plot(x, g2(x), "-.", label=r"$A(\lambda)$")
    ax.plot(x, g1(x), label=r"$A_{0}(\lambda)$")

    x3 = 0.42
    x2 = 0.498
    x1 = 0.505  # d lambda
    y11 = g1(x1)
    y12 = g1(x2)
    y21 = g2(x1)
    y22 = g2(x2)
    # y4 = g2(x2)

    # d lambda
    plt.annotate("d$\lambda$", xy=(x2 - .01, -0.07), xycoords="data")
    ax.vlines(x=x1, ymin=0, ymax=y21, color="orange")
    ax.vlines(x=x2, ymin=0, ymax=y21, color="orange")

    # Horizontal lines
    ax.hlines(y=y11, xmin=0, xmax=x1, color="k", alpha=0.6)
    plt.annotate(r"$A_{0}$", xy=(0.01, y11 - 0.07), xycoords="data")
    ax.hlines(y=y21, xmin=0, xmax=x1, color="k", alpha=0.6)
    plt.annotate(r"$A$", xy=(0.01, y21 - 0.07), xycoords="data")

    # Spectral range
    s1 = 0.1
    As1 = g1(s1)
    s2 = 1.0
    As2 = g1(s2)
    # plt.hlines(y=-0.1, xmin=s1, xmax=s2, color="black", linestyles="dashed", alpha=0.6)
    plt.vlines(x=s2, ymin=-0.1, ymax=As2, color="black", linestyles="dashed", alpha=0.6)
    plt.vlines(x=s1, ymin=-0.1, ymax=As1, color="black", linestyles="dashed", alpha=0.6)
    plt.annotate(
        r"$\Lambda$", xy=((s2 + s1) / 2, -0.17), xycoords="data"
    )  # Add end ticks
    plt.annotate(
        "",
        xy=(s1, -0.1),
        xytext=(s2, -0.1),
        arrowprops=dict(
            arrowstyle="<->", color="k", linestyle="dashed", alpha=.6, lw=1.1
        ),
    )

    # \delta lambda
    plt.annotate(
        r"$\delta \lambda$", xy=((x1 + x3 - 0.025) / 2, 0.85), xycoords="data"
    )
    plt.vlines(x=x1, ymin=y21, ymax=0.9, color="grey", linestyles="dashed")
    plt.vlines(x=x3, ymin=y21, ymax=0.9, color="grey", linestyles="dashed")
    plt.annotate(
        "", xy=(x1, 0.86), xytext=(x1 + 0.07, 0.86), arrowprops=dict(arrowstyle="->")
    )
    plt.annotate(
        "", xy=(x3, 0.86), xytext=(x3 - 0.07, 0.86), arrowprops=dict(arrowstyle="->")
    )

    # Hide Ticks
    ax.axes.get_xaxis().set_ticks([])
    ax.axes.get_yaxis().set_ticks([])

    plt.legend(loc="best")
    plt.ylabel(r"$A(\lambda)$")
    plt.xlabel(r"$\lambda$")

    # Hide the right and top spines
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)

    plt.ylim([-0.2, 1.1])
    plt.tight_layout()
    plt.savefig("precision_plot.pdf")
    plt.savefig("precision_plot.png", dpi=400)
#    plt.show()
