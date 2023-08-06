from .utils import spectrum


import numpy as np




    
def polynomial_baseline():
    band_params = [('gauss', 1, 1, 1485), 
               ('gauss', 2.5, 2.5, 1515),
               ('gauss', 5, 5, 1540),
               ('gauss', 10, 10, 1590)]
    wn = np.arange(1460,1650,.5)
    full_spec = spectrum(wn, band_params)
    baseline = 5 + (wn-1400)*0.01 - (wn-1500)**2*10E-4
    spectrum_baseline = full_spec + baseline
    return {'wn':wn,
            'spectrum':full_spec,
            'baseline':baseline,
            'spectrum_baseline':spectrum_baseline}


def SG_smoothing():
    band_params = [('gauss', 1, 1, 1485), 
                   ('gauss', 2.5, 2.5, 1515),
                   ('gauss', 5, 5, 1540),
                   ('gauss', 10, 10, 1590)]
    wn = np.arange(1460,1621)
    noiseless = spectrum(wn, band_params)
    noisy = noiseless + .1 * np.random.randn(*noiseless.shape)
    return {"wn":wn, "noiseless":noiseless,"noisy":noisy}
