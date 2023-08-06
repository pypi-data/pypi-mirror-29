import numpy as np


def gaussian_band(wn, A, s, m):
    return A/s*np.sqrt(2*np.pi)*np.exp(-(wn-m)**2/2/s**2)
    
def lorentzian_band(wn, A, w, m):
    return A /(1 + (wn - m)**2/w**2)/(w*np.pi)


def band(wn, band_params):
    if band_params[0] == "gauss":
        return gaussian_band(wn, *band_params[1:])
    elif band_params[0] == "lorentz":
        return lorentzian_band(wn, *band_params[1:])
    else:
        raise ArgumentError('Unknown band {}'.format(band_params[0]))

def spectrum(wn, band_params, noise_level=0):
    spec = np.zeros_like(wn)
    for band_param in band_params:
        spec = spec + band(wn, band_param)
    if noise_level > 0:
        spec = spec + noise_level * np.random.randn(*spec.shape)
    return spec
