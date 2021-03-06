
import numpy as np

import flares_utility.analyse
import flares_utility.stats
import flares_utility.limits
import flares_utility.plt
# import flares_utility.colors 
import flare.plt as fplt

# ----------------------------------------------------------------------
# --- open data and load analyser

filename = flares_utility.analyse.flares_master_file
a = flares_utility.analyse.analyse_flares(filename, default_tags = False)

# a.list_datasets()

s_limit = {'log10Mstar_30': 8.5, 'log10FUV': 28.5}

tags = ['005_z010p000','006_z009p000','007_z008p000','008_z007p000','009_z006p000','010_z005p000']
zeds = np.array([float(tag[5:].replace('p','.')) for tag in tags])

tags2 = ['000_z015p000','001_z014p000','002_z013p000','003_z012p000','004_z011p000','005_z010p000','006_z009p000','007_z008p000','008_z007p000','009_z006p000','010_z005p000']
zeds2 = np.array([float(tag[5:].replace('p','.')) for tag in tags2])


labels = flares_utility.labels.labels
limits = flares_utility.limits.limits
