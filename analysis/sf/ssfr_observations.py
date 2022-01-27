

# Import CMasher to register colormaps
import cmasher as cmr

import numpy as np
import matplotlib.cm as cm

import pickle

from astropy.io import ascii

from load import * # loads flares_analysis as a and defined mass/luminosity limits and tags/zeds


# ----------------------------------------------------------------------
# --- define quantities to read in [not those for the corner plot, that's done later]

quantities = []

quantities.append({'path': 'Galaxy/Mstar_aperture', 'dataset': f'30', 'name': f'Mstar_30', 'log10': True})
quantities.append({'path': f'Galaxy/SFR_aperture/30', 'dataset': f'50Myr', 'name': f'SFR_50', 'log10': True})


x = 'log10Mstar_30'
y = 'log10sSFR'

D = {}
s = {}

for tag, z in zip(tags, zeds):

    # --- get quantities (and weights and deltas)
    D[z] = a.get_datasets(tag, quantities)

    D[z]['log10sSFR'] = D[z]['log10SFR_50'] - D[z]['log10Mstar_30'] + 9

    s[z] = D[z][x]>s_limit[x]



limits = flares_utility.limits.limits
limits[x][0] = s_limit[x]

fig, axes = flares_utility.plt.linear_redshift(D, zeds, x, y, s, limits = limits, scatter = False, rows=1, add_weighted_range = True)


observations = {}
observations['Salmon+15'] = {}
observations['Salmon+15']['redshifts'] = [5.0, 6.0]
observations['Salmon+15']['c'] = 'b'
observations['Salmon+15']['s'] = 3

observations['Salmon+15'][5.0] = {}
observations['Salmon+15'][5.0]['log10M*'] = np.array([9.0,9.25,9.50,9.75,10.,10.25])
observations['Salmon+15'][5.0]['log10SFR'] = np.array([0.88,1.04,1.12,1.23,1.46,1.62])
observations['Salmon+15'][5.0]['error'] = np.array([0.42,0.38,0.41,0.43,0.31,0.37])

observations['Salmon+15'][6.0] = {}
observations['Salmon+15'][6.0]['log10M*'] = np.array([9.0,9.25,9.50,9.75,10.])
observations['Salmon+15'][6.0]['log10SFR'] = np.array([0.92,1.07,1.27,1.40,1.147])
observations['Salmon+15'][6.0]['error'] = np.array([0.19,0.21,0.35,0.26,0.07])

# --- calculate sSFRs
for z in observations['Salmon+15']['redshifts']:
    observations['Salmon+15'][z]['log10sSFR'] = observations['Salmon+15'][z]['log10SFR']-observations['Salmon+15'][z]['log10M*']+9.0 # convert to sSFR/Gyr


Tacchella21 = {}
Tacchella21['continuity'] = ascii.read('obs/table_result_eazy.cat')
Tacchella21['parametric'] = ascii.read('obs/table_result_eazy_param.cat')
Tacchella21['bursty'] = ascii.read('obs/table_result_eazy_bursty.cat')



added_tacchella = False
added_salmon = False

for tag, z, ax in zip(tags, zeds, axes):


    add_legend = False

    # Salmon+

    for obsname in ['Salmon+15']:

        for zobs in observations[obsname]['redshifts']:

            obs = observations[obsname][zobs]

            if np.fabs(zobs-z)<0.51: # if points at this redshift

                if not added_salmon:
                    label = rf'$\rm {obsname}$'
                    add_legend = True
                    added_salmon = True
                else:
                    label = None

                ax.errorbar(obs['log10M*'], obs['log10sSFR'], yerr = obs['error'], color=observations[obsname]['c'], markersize=observations[obsname]['s'], label = label, marker = 'o', linestyle='none', elinewidth = 1)


    # % Tacchella

    colors = cmr.take_cmap_colors('cmr.apple', 3, cmap_range=(0.15, 0.85), return_fmt='hex')


    for prior, c in zip(['continuity','parametric','bursty'], colors):

        s = np.fabs(Tacchella21[prior]['redshift_q50']-z)<0.51

        if len(Tacchella21[prior]['log_stellar_mass_q50'][s])>0:

            x = Tacchella21[prior]['log_stellar_mass_q50'][s]
            y = Tacchella21[prior]['log_ssfr_50_q50'][s]+9
            xerr = (x-Tacchella21[prior]['log_stellar_mass_q16'][s], Tacchella21[prior]['log_stellar_mass_q84'][s]-x)
            yerr = (y-(Tacchella21[prior]['log_ssfr_50_q16'][s]+9), (Tacchella21[prior]['log_ssfr_50_q84'][s]+9)-y)

            if not added_tacchella:
                label = rf'$\rm T22/{prior}$'
                add_legend = True
                added_tacchella = True
            else:
                label = None


            # ax.errorbar(x, y, xerr=xerr, yerr=yerr, color=c, markersize=2, label = label, marker = 'o', linestyle='none', elinewidth = 1)

            ax.scatter(x, y, color=c, s=2, label = rf'$\rm T22/{prior}$', marker = 'o')



    if add_legend:
        ax.legend(loc = 'lower left', fontsize = 7, labelspacing = 0.05, handletextpad = 0.1, handlelength = 0.75)









fig.savefig(f'figs/ssfr_observations.pdf')
fig.savefig(f'figs/ssfr_observations.png')
