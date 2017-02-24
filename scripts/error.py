import os
import numpy as np
script_dir = os.path.dirname(os.path.abspath(__file__))
error_path = os.path.join(script_dir, 'error_checking')
mechs = [os.path.join(error_path, x) for x in os.listdir(error_path) if os.path.isdir(os.path.join(error_path, x))]

err_dicts = {}
for mech in mechs:
    mech_name = os.path.basename(os.path.normpath(mech))
    #get file list
    files = [os.path.join(mech,x) for x in os.listdir(mech) if os.path.isfile(os.path.join(mech,x))]
    err_dicts[mech_name] = {}
    for file in files:
        with open(file, 'r') as f:
            lines = [x for x in f.read().split('\n') if x.strip()]
        for line in lines:
            name = line[:line.index(':')].strip()
            err_arr = np.array([float(x) for x in line[line.index(':') + 1:].split(',') if x.strip()])
            if ('rop_fwd' in name or 'rop_rev' in name) and 'linf' in name and np.any(err_arr > 1):
                print(file, np.where(err_arr > 1))
            if name in err_dicts[mech_name]:
                try:
                    assert np.allclose(err_dicts[mech_name][name], err_arr)
                    err_dicts[mech_name][name] = err_arr
                except AssertionError:
                    err_dicts[mech_name][name] = np.maximum(err_dicts[mech_name][name], err_arr)
            else:
                err_dicts[mech_name][name] = err_arr

def format(val):
    return '{:1.2e}'.format(val)
for mech in err_dicts:
    print(mech)
    for name in err_dicts[mech]:
        if 'l2' in name:
            continue
        err_vals = err_dicts[mech][name][np.where(np.logical_not(
            np.isnan(err_dicts[mech][name])))]
        if 'wdot' in name:
            print('tdot', format(err_vals[0]))
            print('species', format(np.linalg.norm(err_vals[1:], ord=np.inf)))
        elif 'rop_net ' in name:
            #find prevision range
            maxv = np.linalg.norm(err_vals, ord=np.inf)
            maxind = np.where(err_dicts[mech][name] == maxv)[0][0]
            print(name, format(maxv))
            print('precision_max', format(err_dicts[mech]['rop_net_precmax - linf'][maxind]))
            print('precision_min', format(err_dicts[mech]['rop_net_precmin - linf'][maxind]))
        elif 'prec' not in name:
            print(name, format(np.linalg.norm(err_vals, ord=np.inf)))