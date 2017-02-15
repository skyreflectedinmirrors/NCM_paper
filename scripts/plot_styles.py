#a single consolidated place to import
#such that all figures have identical styling (when possible)

import matplotlib as mpl
import matplotlib.pyplot as plt
import os.path

#setup latex
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rc('text.latex',
    preamble=r'\usepackage{amsmath},\usepackage{siunitx}')
plt.rc('font', family='serif')

legend_style = {'loc':0,
    'fontsize':16,
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
marker_wheel = [('o', True), ('>', True), ('s', True)]
marker_dict = {x : marker_wheel[i] for i, x in enumerate(default_keys)}

def pretty_names(pname):
    pname_dict = {'runtime' : 'Runtime',
        'comptime' : 'Compilation time',
        'overhead' : 'Kernel Construction Overhead',
        'vecwidth' : 'Vector Width = {}',
        'w' : 'Shallow SIMD',
        'par' : 'SIMT'
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
