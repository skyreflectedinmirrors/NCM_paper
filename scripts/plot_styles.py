#a single consolidated place to import
#such that all figures have identical styling (when possible)

import matplotlib as mpl
import matplotlib.pyplot as plt
import os.path

#setup latex
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rc('text.latex',
    preamble=r'\usepackage{amsmath},\usepackage{siunitx},\usepackage[version=3]{mhchem}')
plt.rc('font', family='serif')

legend_style = {'loc':0,
    'fontsize':18,
    'numpoints':1,
    'shadow':True,
    'fancybox':True
}

tick_font_size = 20

marker_style = {
    'size' : 15
}

clear_marker_style = {
    'size' : 17
}

default_keys = ['runtime', 'comptime', 'overhead']
marker_wheel = [('o', True), ('>', True), ('s', True),
    ('D', True)]
marker_dict = {x : marker_wheel[i] for i, x in enumerate(default_keys)}

class dummy_formatter(object):
    def __init__(self, choicedict):
        self.choices = choicedict.keys()
        self.values = [choicedict[x] for x in self.choices]

    def __hash__(self):
        return hash(repr(self))

    def format(self, val):
        return next(self.values[i] for i, x in enumerate(self.choices)
            if x == val)

legend_key = {'H2':r'H$_2$/CO',
              'CH4':r'GRI-Mech 3.0',
              'C2H4':r'USC-Mech II',
              'IC5H11OH':r'IC$_5$H$_{11}$OH'
              }

def pretty_names(pname, short=False):
    pname_dict = {'runtime' : 'Runtime',
        'comptime' : 'Compilation time',
        'overhead' : 'Kernel Construction Overhead',
        'vecwidth' : 'Vector Width = {}',
        'vectype' : dummy_formatter({'w' : 'Shallow SIMD',
            'par' : 'SIMT',
            'd' : 'Deep SIMD'}),
        'order' : dummy_formatter({'C' : 'C-order',
            'F' : 'F-order'}),
        'kernel' : dummy_formatter({'single' : 'Single Rate Kernel',
            'split' : 'Split Rate Kernels'}),
        'rates' : dummy_formatter({'fixed' : 'Fixed Rate Specialization',
            'hybrid' : 'Hybrid Rate Specialization',
            'full' : 'Full Rate Specialization'}),
        'mechdata.mech' : dummy_formatter(legend_key)
    }
    if pname in pname_dict:
        return pname_dict[pname]
    return pname

#color schemes
color_wheel = ['r', 'b', 'g', 'k']
color_dict = {x : color_wheel[i] for i, x in enumerate(default_keys)}


def finalize(tight=True):
    ax = plt.gca()
    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
     ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(tick_font_size)

    if tight:
        plt.tight_layout()
