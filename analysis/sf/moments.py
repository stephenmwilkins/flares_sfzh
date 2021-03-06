
import numpy as np
import matplotlib.cm as cm

import scipy.stats as stats

import pickle


from load import * # loads flares_analysis as a and defined mass/luminosity limits and tags/zeds


# ----------------------------------------------------------------------
# --- define quantities to read in [not those for the corner plot, that's done later]

quantities = []
quantities.append({'path': 'Galaxy/Mstar_aperture', 'dataset': f'30', 'name': 'Mstar_30', 'log10': True})

properties = ['log10lambda', 'nvariance','skew','nkurtosis']
x = 'log10Mstar_30'


D = pickle.load(open('moments_and_percentiles.p','rb'))

s = {}
for z in zeds:
    D[z]['lambda'] = 1/(D[z]['moment1'])
    D[z]['log10lambda'] = np.log10(D[z]['lambda'])
    # D[z]['nvariance'] = D[z]['moment2']*D[z]['lambda']**2
    D[z]['nvariance'] = D[z]['moment1']/np.sqrt(D[z]['moment2'])

    D[z]['skew'] = D[z]['moment3']
    D[z]['nkurtosis'] = D[z]['moment4']-3
    s[z] = D[z][f'{x}_s']




limits = flares_utility.limits.limits

limits['nvariance'] = [0.51, 1.99]
limits['nkurtosis'] = [-1., 9.99]


labels['nvariance'] = 'mean/\sqrt{var}'


limits[x][0] = s_limit[x]

# fig, axes = flares_utility.plt.linear_redshift_mcol(D, zeds, x, properties, s, limits = limits, scatter = False, add_weighted_range = True, zevo_cmap = flares_utility.colors.redshift_cmap)
fig, axes = flares_utility.plt.linear_redshift_mcol(D, zeds, x, properties, s, limits = limits, scatter = False, add_weighted_range = True)


# normalised variance, should be 1 for exp
for ax in axes[1,:]:
    ax.axhline(1.0, lw=1, c='k',alpha=0.2)
    v = np.sqrt(2)/(np.sqrt(np.pi)*np.sqrt(1-2/np.pi)) # half-normal
    print(v)
    ax.axhline(v, lw=1, c='k', ls='--',alpha=0.2)

# skew, should be 2 for exp, 1 for half normal
for ax in axes[2,:]:
    ax.axhline(2.0, lw=1, c='k',alpha=0.2)
    ax.axhline(1.0, lw=1, c='k', ls='--', alpha=0.2)


# kurtosis, should be 6 for exp
for ax in axes[3,:]:
    ax.axhline(6.0, lw=1, c='k',alpha=0.2)
    ax.axhline(0.87, lw=1, c='k', ls='--', alpha=0.2)

fig.savefig(f'figs/moments.pdf')
fig.savefig(f'figs/moments.png')
# fig.savefig(f'figs/combined_redshift_{x}.png')
