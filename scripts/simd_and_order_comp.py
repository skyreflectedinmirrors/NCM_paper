import perf_plotter as pp
import plot_styles as ps
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

SIMD_color = ps.color_wheel[0]
SIMT_color = ps.color_wheel[1]
SIMT_sym = ps.marker_wheel[0][0]
SIMD_sym = ps.marker_wheel[1][0]
C_hollow = False
F_hollow = True

def marker_func(name):
    retval = []
    if 'SIMT' in name:
        retval.append(SIMT_sym)
    else:
        retval.append(SIMD_sym)
    if 'C-order' in name:
        retval.append(C_hollow)
    else:
        retval.append(F_hollow)
    if 'SIMT' in name:
        retval.append(SIMT_color)
    else:
        retval.append(SIMD_color)
    return tuple(retval)

labels = ['SIMT', 'SIMD', 'C-order', 'F-order']
handles = [mlines.Line2D([], [], color=SIMT_color, marker=SIMT_sym, linestyle='',
                          markersize=ps.marker_style['size'], label='SIMT',
                          markerfacecoloralt='none',
                          fillstyle='left'),
           mlines.Line2D([], [], color=SIMD_color, marker=SIMD_sym, linestyle='',
                          markersize=ps.marker_style['size'], label='SIMD',
                          markerfacecoloralt='none',
                          fillstyle='left'),
           mlines.Line2D([], [], linestyle='', marker=(4, 0, 45), markersize=ps.marker_style['size'],
                          label='C-order', markerfacecolor='k', markeredgecolor='k'),
           mlines.Line2D([], [], linestyle='', marker=(4, 0, 45), markersize=ps.marker_style['size'],
                          label='F-order', markerfacecolor='none', markeredgecolor='k')]
legend = (handles, labels)

pp.plotter(show=True,
    cores='1', vecwidth='8', rates='hybrid', kernel='split',
    legend_handler=legend, marker_func=marker_func)