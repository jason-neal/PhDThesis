#!/usr/bin/env python
import pandas as pd

nirps = pd.read_csv("nirps_etc_logg_4.5_ref_J_snr_100_oct2018.csv", header=0)

selected = nirps[["temp", "band", "vsini", "resolution",
                      "cond1", "cond2", "cond3"]]

# Sorting
rorder = ["75k","100k"]
rorderdict = dict(zip(rorder,range(len(rorder))))
border = ["Z","Y","J","H","K"]
borderdict = dict(zip(border,range(len(border))))

sorted = selected.assign(rorder=selected.resolution.map(rorderdict))\
                   .assign(border=selected.band.map(borderdict))\
                   .sort_values(by=["temp", "border","vsini","rorder"], ascending=[False, True, True, True])\
                   .drop("rorder",1).drop("border",1)

print(sorted.to_latex(index=False, header=False))
