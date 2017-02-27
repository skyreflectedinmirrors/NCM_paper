import os
import numpy as np
script_dir = os.path.dirname(os.path.abspath(__file__))
error_path = os.path.join(script_dir, 'error_checking')
mechs = [os.path.join(error_path, x) for x in os.listdir(error_path) if os.path.isdir(os.path.join(error_path, x))]

rtol = 1e-6
atol = 1e-10

err_dicts = {}
for mech in mechs:
    mech_name = os.path.basename(os.path.normpath(mech))
    #get file list
    files = [os.path.join(mech,x) for x in os.listdir(mech) if os.path.isfile(os.path.join(mech,x)) if x.endswith('.npz')]
    err_dicts[mech_name] = {}
    for file in files:
        arrs = np.load(file)
        for name in arrs:
            if 'value' in name or 'component' in name or 'store' in name:
                continue
            errs = arrs[name]
            values = arrs[name + '_value']
            errs = errs / (atol + rtol * np.abs(values))

            precs = None
            if 'rop_net' in name:
                #calculate the precision norms
                precs = arrs['rop_component'] / (atol + rtol * np.abs(values))

            if name in err_dicts[mech_name]:
                err_dicts[mech_name][name] = np.maximum(err_dicts[mech_name][name], errs)
                if 'rop_net' in name:
                    update_locs = np.where(err_dicts[mech_name][name] == errs)
                    #update the precision norms at these locations
                    err_dicts[mech_name]['rop_component'][update_locs] = precs[update_locs]
            else:
                err_dicts[mech_name][name] = errs
                if precs is not None:
                    err_dicts[mech_name]['rop_component'] = precs

def format(val):
    return '{:1.2e}'.format(val)

keyarr = ['fwd', 'rev', 'net', 'comp', 'wdot']
for mech in err_dicts:
    print(mech)
    for name in sorted(err_dicts[mech], key=lambda x:keyarr.index(next(y for y in keyarr if y in x))):
        if 'l2' in name:
            continue
        err_vals = err_dicts[mech][name][np.where(np.logical_not(
            np.isnan(err_dicts[mech][name])))]
        if 'wdot' in name:
            print('tdot', format(err_vals[0]))
            print('species', format(np.linalg.norm(err_vals[1:], ord=np.inf)))
        elif 'rop_net' in name:
            #find prevision range
            maxv = np.linalg.norm(err_vals, ord=np.inf)
            maxind = np.where(err_dicts[mech][name] == maxv)[0][0]
            print(name, format(maxv))
            print('rop_component', format(err_dicts[mech]['rop_component'][maxind]))
        elif 'component' not in name:
            print(name, format(np.linalg.norm(err_vals, ord=np.inf)))