#!/usr/bin/env python
import pandas as pd

aces = pd.read_csv("aces_prec.csv", header=0)
btsettl = pd.read_csv("btsettl_prec.csv", header=0)

print(aces.columns)
print(aces.head())
print(btsettl.head())
# temp,logg,feh,alpha,band,resolution,vsini,sampling,correctflag,quality,cond1,cond2,cond3

df_merged = pd.merge(aces, btsettl, on=["temp", "band", "vsini", "resolution", "sampling"], how="outer", suffixes=("_aces", "_btsettl"))

print(df_merged.head())

selected = df_merged[["temp", "band","vsini", "resolution",
                      "cond1_aces", "cond2_aces", "cond3_aces",
                      "cond1_btsettl", "cond2_btsettl", "cond3_btsettl"]]

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

print("Done")

print(sorted.to_latex())