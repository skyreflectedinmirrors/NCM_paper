import data_parser
import argparse
import plot_styles as ps
import matplotlib.pyplot as plt
import general_plotting as gp
import numpy as np
import itertools

run = data_parser.run
rundata = data_parser.rundata
data = data_parser.parse_data()
reacs_as_x = False
norm = None

def __compare(r, name, compare_value):
    """
    Specialty comparison function to account for differences
    in runtypes
    """
    if name == 'vecwidth' and r.vectype == 'par':
        return True
    return getattr(r, name) == compare_value

def plotter(plot_name='', show=True, plot_reacs=True, norm=True, **filters):
    #apply filters
    for f in filters:
        if filters[f] is None:
            continue
        assert any(data[x] for x in data), 'No data matching all filters'
        if f in data[data.keys()[0]][0]._asdict():
            for mech in data:
                data[mech] = [x for x in data[mech] if __compare(x, f, filters[f])]
    #compute data
    for mech in data:
        for run in data[mech]:
            rund = run.rundata
    #now plot data
    to_plot = ['runtime']
    if filters['plot_compilation']:
        to_plot.append('comptime')
    if filters['plot_overhead']:
        to_plot.append('overhead')
    #get data
    plot_data = [x for mech in data for x in data[mech]]
    #get labels
    diff_check = [x for x in run._fields if x not in ['mechdata', 'rundata']]
    diffs = [set([getattr(x, check) for x in plot_data]) for check in diff_check]
    #get # with more than 1 option
    diff_locs = [i for i in range(len(diffs)) if len(diffs[i]) > 1]
    diffs = [x for x in diffs if len(x) > 1]
    if len(diff_locs) > 2:
        raise NotImplementedError
    if not diff_locs:
        #regular plot
        for plot in to_plot:
            gp.plot(plot, *gp.process_data(plot_data, plot, reacs_as_x=plot_reacs))
    else:
        #create map dict
        loc_map = {}
        for i, diff in enumerate(diffs):
            for subdiff in diff:
                loc_map[subdiff] = diff_locs[i]

        #sort
        try:
            diffs = [sorted(diff, key=lambda x: float(x)) for diff in diffs]
        except:
            diffs = [sorted(diff) for diff in diffs]

        #first pass - process data
        x_vals = []
        y_vals = []
        z_vals = []
        labels = []

        #handle 2 diffs
        if len(diffs) == 1:
            for val in [subdiff for diff in diffs for subdiff in diff]:
                check = diff_check[loc_map[val]]
                match = [x for x in plot_data if __compare(x, check, val)]
                if match:
                    labels.append(ps.pretty_names(check).format(val))
                    x, y, z = gp.process_data(match, 'runtime', reacs_as_x=plot_reacs)
                    x_vals.append(x); y_vals.append(y); z_vals.append(z)
        else:
            iterator = [zip(x,diffs[1]) for x in itertools.permutations(diffs[0],len(diffs[1]))]
            iterator = [subiter for i in iterator for subiter in i]
            for val1, val2 in iterator:
                match = [x for x in plot_data if __compare(x, diff_check[loc_map[val1]], val1)
                    and __compare(x, diff_check[loc_map[val2]], val2)]
                if match:
                    labels.append(val1 + ' - ' + val2)
                    x, y, z = gp.process_data(match, 'runtime', reacs_as_x=plot_reacs)
                    x_vals.append(x)
                    y_vals.append(y)
                    z_vals.append(z)


        #second pass - normalize
        if norm:
            xlen = len(next(x for x in x_vals if x))
            #find the max y for each x
            for ix in range(xlen):
                y_max = np.max([y_vals[i][ix] for i in range(len(y_vals)) if y_vals[i]])
                #divide
                for i in range(len(y_vals)):
                    y_vals[i][ix] = y_max / y_vals[i][ix]
                    #uncertainty of an inverse is unchanged
                    #however, we multiply by y_max as we're doing c / y
                    z_vals[i][ix] = y_max * z_vals[i][ix]

        #and finally plot
        for i in range(len(y_vals)):
            gp.plot('', x_vals[i], y_vals[i], z_vals[i],
                labels=labels, plot_ind=i)

    xlabel = 'Speedup' if norm else r'Runtime ($\frac{\si{\milli\second}}{\text{state}}$)'
    plt.ylabel(xlabel)
    plt.xlabel(r'Number of {} in Model'.format('Species' if not plot_reacs else 'Reactions'))
    plt.legend(**ps.legend_style)
    ps.finalize()
    if plot_name:
        plt.savefig(plot_name)
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--lang',
        required=False,
        default='opencl',
        type=str)
    parser.add_argument('--vecwidth',
        required=False,
        default=None,
        type=str)
    parser.add_argument('--order',
        required=False,
        default=None,
        type=str,
        choices=['C', 'F'])
    parser.add_argument('--vectype',
        required=False,
        default=None,
        type=str,
        choices=['par', 'w', 'd'])
    parser.add_argument('--platform',
        required=False,
        default=None,
        type=str,
        choices=['intel', 'nvidia', 'amd'])
    parser.add_argument('--rates',
        required=False,
        default=None,
        type=str,
        choices=['fixed', 'hybrid', 'full'])
    parser.add_argument('--kernel',
        required=False,
        default=None,
        type=str,
        choices=['single', 'split'])
    parser.add_argument('--cores',
        required=False,
        default=None,
        type=str)
    parser.add_argument('--plot_name',
        required=False,
        default='',
        type=str)
    parser.add_argument('--mech',
        required=False,
        default=None,
        type=str,
        choices=data.keys()
        )
    parser.add_argument('--plot_compilation',
        required=False,
        default=False,
        action='store_true'
        )
    parser.add_argument('--plot_overhead',
        required=False,
        default=False,
        action='store_true'
        )
    parser.add_argument('--no_norm',
        dest='norm',
        action='store_false',
        required=False,
        default=True)
    opts = vars(parser.parse_args())
    options = { k : opts[k] for k in opts if opts[k] != None }
    plotter(**options)

