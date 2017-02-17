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

xval, yval, zval, label = pp.plotter('../SIMD_SIMT_Order_comparison.pdf', show=False,
    cores='1', vecwidth='8', rates='hybrid', kernel='split',
    legend_handler=legend, marker_func=marker_func, return_vals=True,
    norm=False, ylog=True)

#print stats
C_order = [i for i,l in enumerate(label) if 'C-order' in l]
F_order = [i for i in range(len(label)) if i not in C_order]

C_SIMT = next(i for i in C_order if 'SIMT' in label[i])
C_SIMD = next(i for i in C_order if i != C_SIMT)
F_SIMT = next(i for i in F_order if 'SIMT' in label[i])
F_SIMD = next(i for i in F_order if i != F_SIMT)

print 'SIMT vs SIMD'
for i in range(len(yval[0])):
    print i, 'C', yval[C_SIMT][i] / yval[C_SIMD][i]
    print i, 'F', yval[F_SIMT][i] / yval[F_SIMD][i]

print 'C vs F'
for i in range(len(yval[0])):
    print i, 'SIMT', yval[F_SIMT][i] / yval[C_SIMT][i]
    print i, 'SIMD', yval[F_SIMD][i] / yval[C_SIMD][i]