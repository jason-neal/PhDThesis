# Plot the change of precision against different metallicities
# Subset from Theoretical metallicity distribution Notebook

import warnings

from matplotlib import rc
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
#from styler import styler

rc('font', **{'family': 'sans-serif', 'sans-serif': ['Helvetica']})
rc('text', usetex=True)
warnings.simplefilter('ignore')


plt.style.use('AandAfull')
bands = ["Z", "Y", "J", "H", "K"]

#@styler
def feh_plot(*args, **kwargs):
    df = pd.read_csv("metallicity_effect.csv")
    vsini = 1
    res = 100000
    logg = 4.5
    assert np.all(df.Resolution == res)
    assert np.all(df.logg == logg)
    assert np.all(df.vsini == vsini)

    fig, axes = plt.subplots(1, 5, figsize=(7, 4), sharey=True)
    # for res in [60000, 80000, 100000]:
    for temp, mtype in zip([2600, 2800, 3500, 3900], ["M9", "M6", "M3", "M0"]):
        for ii, band in enumerate(bands):
            this_df = df[(df.Band.str.strip() == band) &
                         (df.vsini == vsini) &
                         (df.Temp == temp) &
                         (df.Resolution == res) &
                         (df.logg == logg)
                         ]
            axes[ii].plot(this_df["[Fe/H]"], this_df.Quality,
                          ".-", label="{}".format(mtype))

    for ii, band in enumerate(bands):
        axes[ii].set_xlabel("[Fe/H]")
        if ii == 0:
            axes[ii].set_ylabel("Quality")
        axes[ii].annotate("{} Band".format(band), xy=(0.05, 0.95), xycoords="axes fraction")
        axes[-1].legend(loc=(0.36, 0.66), framealpha=0.5)
    plt.tight_layout()

    savename = kwargs.get("name", None)
    if savename is not None:
        plt.savefig(savename, dpi=500)
    plt.close()

#@styler
def logg_plot( *args, **kwargs):
    df = pd.read_csv("logg_effect.csv")
    vsini = 1
    res = 100000
    feh = 0.0
    assert np.all(df.Resolution == res)
    assert np.all(df["[Fe/H]"] == feh)
    assert np.all(df.vsini == vsini)
    fig, axes = plt.subplots(1, 5, figsize=(7, 4), sharey=True)
    for temp, mtype in zip([2600, 2800, 3500, 3900], ["M9", "M6", "M3", "M0"]):
        for ii, band in enumerate(bands):
            this_df = df[(df.Band.str.strip() == band) &
                         (df.vsini == vsini) &
                         (df.Temp == temp) &
                         (df.Resolution == res) &
                         (df["[Fe/H]"] == feh)
                         ]
            axes[ii].plot(this_df["logg"], this_df.Quality,
                          ".-", label="{}".format(mtype))

    for ii, band in enumerate(bands):
        axes[ii].set_xlabel("logg")
        if ii == 0:
            axes[ii].set_ylabel("Quality")
        axes[ii].annotate("{} Band".format(band), xy=(0.05, 0.95), xycoords="axes fraction")
        axes[-1].legend(loc=(0.36, 0.66), framealpha=0.5)
    plt.tight_layout()

    savename = kwargs.get("name", None)
    if savename is not None:
        plt.savefig(savename, dpi=500)

    plt.close()

feh_plot(name="metalicity_effect.pdf")

feh_plot(name="metalicity_effect.png")


logg_plot(name="logg_effect.pdf")

logg_plot(name="logg_effect.png")

plt.close()