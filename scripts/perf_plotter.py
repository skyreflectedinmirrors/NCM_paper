import data_parser
import argparse
import plot_styles as ps
import matplotlib.pyplot as plt
import general_plotting as gp

run = data_parser.run
rundata = data_parser.rundata
data = data_parser.parse_data()
reacs_as_x = False
norm = None

def plotter(plot_name='plot.pdf', **filters):
    #apply filters
    for f in filters:
        if filters[f] is None:
            continue
        assert any(data[x] for x in data), 'No data matching all filters'
        if f in data[data.keys()[0]][0]._asdict():
            for mech in data:
                data[mech] = [x for x in data[mech] if getattr(x, f) == filters[f]]
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
    assert len(diff_locs) <= 1, "Don't know how to create graphs for more than one diff"
    if not diff_locs:
        #regular plot
        gp.plot(plot_data, to_plot, norm=['runtime'])
    else:
        loc = diff_locs[0]
        diffs = sorted(diffs[loc])
        labels = [diff_check[loc] + ' ' + x for x in diffs]
        for i, val in enumerate(diffs):
            match = [x for x in plot_data if getattr(x, diff_check[loc]) == val]
            gp.plot(match,
                to_plot, norm=['runtime'], labels=labels, plot_ind=i)
    plt.ylabel(r'Runtime ($\frac{\si{\milli\second}}{\text{state}}$)')
    plt.xlabel(r'Number of Species in Model')
    plt.legend(**ps.legend_style)
    ps.finalize()
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
        default='plot.pdf',
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
    opts = vars(parser.parse_args())
    options = { k : opts[k] for k in opts if opts[k] != None }
    plotter(**options)

