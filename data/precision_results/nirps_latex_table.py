#!/usr/bin/env python

import pandas as pd

nirps = pd.read_csv("nirps_prec_ref_J_75000.csv", header=0)


selected = nirps[["temp", "band", "vsini", "resolution",
                      "cond1", "cond2", "cond3"]]

# Sorting
rorder = ["60k","80k","100k"]
rorderdict = dict(zip(rorder,range(len(rorder))))
border = ["Z","Y","J","H","K"]
borderdict = dict(zip(border,range(len(border))))

sorted = selected.assign(rorder=selected.resolution.map(rorderdict))\
                   .assign(border=selected.band.map(borderdict))\
                   .sort_values(by=["temp", "border","vsini","rorder"], ascending=[False, True, True, True])\
                   .drop("rorder",1).drop("border",1)

sorted.to_csv("combined_aces_btsettl_precsion.csv", index=False)


print(sorted.to_latex())
