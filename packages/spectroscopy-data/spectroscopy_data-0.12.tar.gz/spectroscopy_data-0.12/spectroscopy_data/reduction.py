from .utils import spectrum
import numpy as np

def integration():

    k1 = 1 # rate constant A -> B
    k2 = 0.3 # rate constant B -> C
    cA0 = 1 # initial concentration A


    t = np.linspace(0,10)
    wn = np.arange(1000,1800)

    cA = cA0 * np.exp(-k1*t)
    cB = cA0 * k1/(k2-k1) * (np.exp(-k1*t) - np.exp(-k2*t))
    cC = cA0 * (1 + (k1*np.exp(-k2*t) - k2 * np.exp(-k2*t))/(k2-k1))


    bandsA = [('gauss', 1, 10, 1150), 
              ('gauss', .5, 17, 1400), 
              ('gauss', .5, 20, 1700), 
              ('gauss', 1, 5, 1600)]
    bandsB = [('gauss', .3, 10, 1055), 
              ('gauss', .5, 20, 1500), 
              ('gauss', 1, 5, 1600)]
    bandsC = [('gauss', 1, 10, 1200), 
              ('gauss', .5, 20, 1300), 
              ('gauss', 1, 150, 1400),
              ('gauss', 1, 5, 1700)]

    specA = spectrum(wn, bandsA)
    specB = spectrum(wn, bandsB)
    specC = spectrum(wn, bandsC)

    dataset = np.vstack((cA, cB, cC)).T.dot(np.vstack((specA, specB, specC)))
    dataset_noisy = dataset + 1E-2 * np.random.randn(*dataset.shape)


    return dict(wn=wn,
                dataset=dataset,
                dataset_noisy=dataset_noisy,
                specA=specA,
                specB=specB,
                specC=specC
                )
