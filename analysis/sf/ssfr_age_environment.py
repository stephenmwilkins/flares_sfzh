
import pickle

import numpy as np
import matplotlib.cm as cm


from load import * # loads flares_analysis as a and defined mass/luminosity limits and tags/zeds


# ----------------------------------------------------------------------
# --- define quantities to read in [not those for the corner plot, that's done later]

quantities = []

# quantities.append({'path': 'Galaxy', 'dataset': 'Mstar_30', 'name': None, 'log10': True})
quantities.append({'path': 'Galaxy/Mstar_aperture', 'dataset': f'30', 'name': 'Mstar_30', 'log10': True})
quantities.append({'path': f'Galaxy/SFR_aperture/30', 'dataset': f'50Myr', 'name': f'SFR_50', 'log10': True})


Dp = pickle.load(open('moments_and_percentiles.p','rb'))

x = 'log10Mstar_30'

D = {}
s = {}


for tag, z in zip(tags, zeds):

    # --- get quantities (and weights and deltas)
    D[z] = a.get_datasets(tag, quantities)

    D[z]['log10sSFR'] = D[z]['log10SFR_50'] - D[z]['log10Mstar_30'] + 9

    D[z]['age'] = Dp[z]['P0.5']#*1E3 # Myr
    D[z]['log10age'] = np.log10(D[z]['age'])

    # print(np.median(D[z]['log10age']))
    # print(np.median(D[z]['log10Mstar_30']))

    s[z] = D[z][x]>s_limit[x]

    # print(len(D[z][x][s[z]]))

    D[z]['ldelta'] = np.log10(1+D[z]['delta'])



for y in ['log10age','log10sSFR']:

    limits = flares_utility.limits.limits
    limits[x][0] = s_limit[x]

    fig = flares_utility.plt.linear_redshift_density(D, zeds, 'log10Mstar_30', y, s, limits = limits, rows=1)

    fig.savefig(f'figs/{y}_environment.pdf')
    fig.savefig(f'figs/{y}_environment.png')
