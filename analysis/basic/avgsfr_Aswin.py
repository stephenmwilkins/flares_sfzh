import matplotlib as mpl
import matplotlib.cm as cm
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

import cmasher as cmr

cmap = cmr.neon

import flares
import flares_analysis as fa
import flare.plt as fplt

# ----------------------------------------------------------------------
# --- open data

# fl = flares.flares('/cosma7/data/dp004/dc-love2/codes/flares/data/flares.hdf5', sim_type='FLARES')
fl = flares.flares('/cosma7/data/dp004/dc-payy1/my_files/flares_pipeline/data/flares.hdf5', sim_type='FLARES')
# fl.explore()

halo = fl.halos

# ----------------------------------------------------------------------
# --- define parameters and tag
tag = fl.tags[-1]  # --- tag 0 = 10

timescales = [10,30,50,100,200]
r = 30

# ----------------------------------------------------------------------
# --- define quantities to read in [not those for the corner plot, that's done later]

quantities = []

quantities.append({'path': 'Galaxy', 'dataset': f'Mstar_{r}', 'name': 'Mstar', 'log10': True})

for t in timescales:
    quantities.append({'path': 'Galaxy/SFR', 'dataset': f'SFR_{t}', 'name': None, 'log10': True})




# --- get quantities (and weights and deltas)
D = fa.get_datasets(fl, tag, quantities)

# D['log10Mstar'] -= 10. # REMOVE LATER



for t in timescales:
    D[f'log10sSFR_{t}'] = D[f'log10SFR_{t}'] - D[f'log10Mstar'] + 9. #aperture based


limits = {}
limits['log10Mstar'] = [8.05,12]
limits['log10SFR_100'] = [-1.,3.]

labels = {}
labelss = {} # short label
labels['log10Mstar'] = r'log_{10}(M_{\star}/M_{\odot})'
labelss['log10Mstar'] = 'M_{\star}'
labels['log10SFR'] = r'log_{10}(SFR/M_{\odot}\ yr^{-1})'
labelss['log10SFR'] = 'SFR'
labels['log10sSFR'] = r'log_{10}(sSFR/Gyr^{-1})'
labelss['log10sSFR'] = 'sSFR'




# --- individual plots

x = 'log10Mstar'

for y in ['log10SFR', 'log10sSFR']:

    fig, ax = fplt.simple_sm(size=2.5)

    ax.axhline(0.0, color='k', lw=2, alpha=0.2)

    for i,t in enumerate(timescales):

        c = cmap(i/len(timescales))

        # --- weighted median Lines
        R = D[f'{y}_{t}']-D[f'{y}_100']

        print(np.min(R), np.max(R))

        ax = fa.add_median_line(ax, D[x], R, D['weight'], limits[x], c=c, label = rf'$\rm {t}\ Myr $')






    ax.legend(fontsize = 7, labelspacing = 0.1)

    ax.set_xlim(limits[x])
    ax.set_ylim([-0.5,0.5])
    # ax.set_ylim([0, 3])

    ax.set_xlabel(rf'$\rm {labels[x]}$', fontsize = 9)
    ax.set_ylabel(rf'$\rm log_{{10}}({labelss[y]}/{labelss[y]}^{{100}})$', fontsize = 9)

    fig.savefig(f'figs/avgsfr_{y}_Aswin.pdf')
