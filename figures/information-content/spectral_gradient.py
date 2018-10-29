
# Create plots for Gradient change.
import matplotlib

# matplotlib.rcParams["text.usetex"] = False
# matplotlib.rcParams["text.latex.unicode"] = True
matplotlib.rcParams["xtick.labelsize"] = 11
matplotlib.rcParams["ytick.labelsize"] = 11
import matplotlib.pyplot as plt
plt.style.use("thesis")
import numpy as np
from eniric.utilities import load_aces_spectrum

# from eniric.Qcalculator import slope, slope_grad

def slope(wavelength, flux):
    """Original version used to calculate the slope. [Looses one value of array]."""
    delta_flux = np.diff(flux)
    delta_lambda = np.diff(wavelength)

    return delta_flux / delta_lambda

def slope_grad(wavelength, flux):
    """Slope using gradient."""
    return np.gradient(flux, wavelength)  # Yes they should be opposite order

def slope_adjusted(wavelength, flux):
    """Slope that adjust the wave and flux values to match diff."""
    derivf_over_lambda = np.diff(flux) / np.diff(wavelength)
    wav_new = (wavelength[:-1] + wavelength[1:])/2
    flux_new = (flux[:-1] + flux[1:])/2
    return derivf_over_lambda, wav_new, flux_new


# Load spectrum
wl_, flux_ = load_aces_spectrum([3900, 4.5, 0.0, 0])   # M0 star
wl_ = wl_*1000


mask = ((wl_/1000) > 2.20576) & ((wl_/1000) < 2.20586)
wl, flux = wl_[mask], flux_[mask]
flux = flux / max(flux) # Normalize maximum to 1

f_slope = slope(wl, flux)
f_grad = slope_grad(wl, flux)
f_adj, new_wl, new_flux = slope_adjusted(wl, flux)



# Another example
mask2 = ((wl_/1000) > 2.10580) & ((wl_/1000) < 2.1059)
wl2, flux2 = wl_[mask2], flux_[mask2]
flux2 = flux2/max(flux2)

f_slope2 = slope(wl2, flux2)
f_grad2 = slope_grad(wl2, flux2)
f_adj2, new_wl2, new_flux2 = slope_adjusted(wl2, flux2)


plt.figure(figsize=(7, 5))

ax1 = plt.subplot(221)
plt.plot(wl2, flux2, "o-", label="Spectrum")
plt.ylabel("Normalized Flux", fontsize=14)


ax2 = plt.subplot(223, sharex=ax1)
plt.plot(wl2[:-1], f_slope2, "s--", label="FFD")
plt.plot(new_wl2, f_adj2, "o-.", label="FFD(shifted)")
plt.plot(wl2, f_grad2, "*--", label="Numpy")
plt.ylim([-2, 3])
plt.xlabel("Wavelength (nm)", fontsize=14)
plt.ylabel("Gradient", fontsize=14)
plt.legend(fontsize=11)


ax3 = plt.subplot(222)
plt.plot(wl, flux, "o-", label="Spectrum")
plt.ticklabel_format(axis="x", style="plain",)
plt.ticklabel_format(axis="both", fontsize=20)


ax4 = plt.subplot(224, sharex=ax3)
plt.plot(wl[:-1], f_slope, "s--", label="FFD")
plt.plot(new_wl, f_adj, "o-.", label="FFD(shifted)")
plt.plot(wl, f_grad, "*--", label="Numpy")
plt.ylim([-31, 32])
plt.xlabel("Wavelength (nm)", fontsize=14)
plt.legend(fontsize=11)


ax4.ticklabel_format(useOffset=False)
ax3.tick_params(labelbottom=False)
ax2.ticklabel_format(useOffset=False)
ax1.tick_params(labelbottom=False)
plt.tight_layout(pad=0.01)
plt.savefig("spectral_gradients.pdf")
plt.show()