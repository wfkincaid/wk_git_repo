from pylab import *
from pyspecdata import *

# HERE we get dictionaries of nddata
data = find_file("BSA_Ras_Coomassie_220809", exp_type="UV_Vis/LG_Bradford_UV-Vis")
print("the experiments present in this file are:", data.keys())
wv = "$\\lambda$"
# HERE make a dictionary with keys equal to labels (using concentration,
# and with values equal to the actual nddata objects for the spectra
first_run = {
    "Water": data["Water"],
    "0 μg/mL": data["HEPES_294_6_1"],
    "62.5 μg/mL": data["BSA_62_5_1"],
    "125 μg/mL": data["BSA_125_1"],
    "250 μg/mL": data["BSA_250_1"],
    "500 μg/mL": data["BSA_500_1"],
    "750 μg/mL": data["BSA_750_1"],
    "1000 μg/mL": data["BSA_1000_1"], 
    "118_6_6 μg/mL" : data["L118_6_6_1"],
    "118_3_6 μg/mL" : data["L118_3_6_1"],
    "159_6_6 μg/mL" : data["L159_6_6_1"],
    "159_3_6 μg/mL" : data["L159_3_6_1"],
    "67_6_6 μg/mL" : data["M67_6_6_1"],
    "67_3_6 μg/mL" : data["M67_3_6_1"],
    "51_6_6 μg/mL" : data["S51_6_6_1"],
    "51_3_6 μg/mL" : data["S51_3_6_1"],
    
}
second_run = {
    "Water": data["Water"],
    "0 μg/mL": data["HEPES_dil_294_6_1"],
    "62.5 μg/mL": data["BSA_dil_62_5_1"],
    "125 μg/mL": data["BSA_dil_125_1"],
    "250 μg/mL": data["BSA_dil_250_1"],
    "500 μg/mL": data["BSA_dil_500_1"],
    "750 μg/mL": data["BSA_dil_750_1"],
    "1000 μg/mL": data["BSA_dil_1000_1"],
    "118_6_6 μg/mL" : data["L118_dil_6_6_1"],
    "118_3_6 μg/mL" : data["L118_dil_3_6_1"],
    "159_6_6 μg/mL" : data["L159_dil_6_6_1"],
    "159_3_6 μg/mL" : data["L159_dil_3_6_1"],
    "67_6_6 μg/mL" : data["M67_dil_6_6_1"],
    "67_3_6 μg/mL" : data["M67_dil_3_6_1"],
    "51_6_6 μg/mL" : data["S51_dil_6_6_1"],
    "51_3_6 μg/mL" : data["S51_dil_3_6_1"],
   }
# HERE make sure you have a list of the run dictionaries you just defined
# -- only what's listed here will be used!
list_of_runs = [first_run, second_run]
 #HERE add a dilution factor -- we'll multiply in the final plot
dilution_factor = [1, 2]
# HERE give labels of equal length
labels_of_runs = ["first", "second"]
finalcurve = [{} for j in range(len(list_of_runs))]  # two dicts, one for each
A312 = [{} for j in range(len(list_of_runs))]  # two dicts, one for each

# {{{ here I'm using fancier features of raw matplotlib (no figlist) to get a
#     nice layout
gs = GridSpec(len(finalcurve), 5)  # raw matplotlib -- flexible plotting
fig = plt.figure()
ax_rawcoom = []
ax_coom = []
ax_left = []
for k in range(len(finalcurve)):
    ax_rawcoom.append(fig.add_subplot(gs[k, 1:3]))
    ax_coom.append(fig.add_subplot(gs[k, 3:5]))
    ax_left.append(fig.add_subplot(gs[k, 0]))
prop_cycle = plt.rcParams["axes.prop_cycle"]
prop_cycle = prop_cycle * plt.cycler(alpha=[0.5])
thecycler = prop_cycle()
print(plt.rcParams["ytick.major.size"])
plt.rcParams["ytick.major.size"] = 3
print(plt.rcParams["ytick.major.size"])
plt.rcParams["font.size"] = 8
plt.rcParams["legend.fontsize"] = 8
# }}}
whichunits = "μg/mL"
for j, thisset in enumerate(list_of_runs):
    for k, v in thisset.items():
        kw = next(thecycler)
        thisd = v[wv:(241, None)]
        if k not in ["Water"]:
            A312[j][k] = v[wv:(312, 316)].C.mean(wv).item()
        plot(thisd[wv:(357, None)], ax=ax_rawcoom[j], label=k, **kw)
        if k not in [f"0 {whichunits}", "Water"]:
            coom_diff = thisd[wv:(357, None)] - thisset[f"0 {whichunits}"][wv:(357, None)]
            finalcurve[j][k] = coom_diff[wv:(577, 595)].C.mean(wv).item()
            plot(coom_diff/finalcurve[j][k], ax=ax_coom[j], **kw)
        plot(thisd[wv:(None, 350)], ax=ax_left[j], **kw)
        if j == 0:  # only label the top plots
            ax_rawcoom[j].set_title("Coomasie Region")
            ax_coom[j].set_title("Norm'd. Diff. Spec.")
            ax_left[j].set_title("A280 Region")
        ax_rawcoom[j].legend()
fig.tight_layout()
# {{{
figure()
for j in range(len(finalcurve)):
    # {{{ actual coomasie
    thisdil = dilution_factor[j]
    x, y = zip(*finalcurve[j].items())
    x = [float(j.replace(f" {whichunits}", "")) for j in x]
    y = list(y)
    plot(x, array(y)*dilution_factor[j], "o", alpha=0.5, label=f"{labels_of_runs[j]} Coomasie")
    # }}}
    # {{{ A280 standin
    x, y = zip(*A312[j].items())
    x = [float(j.replace(f" {whichunits}", "")) for j in x]
    y = list(y)
    plot(x, array(y)*dilution_factor[j], "x", alpha=0.5, label=f"{labels_of_runs[j]} A312")
    # }}}
plt.legend(**dict(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.0))
plt.tight_layout()
title("final calibration curve")
# }}}
show()