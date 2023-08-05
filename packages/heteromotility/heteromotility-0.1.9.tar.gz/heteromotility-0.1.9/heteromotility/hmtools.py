'''
Tools for manipulating data structures.
TODO : refactor and replace with standard `pandas` implementations.
'''
from __future__ import print_function, division
import numpy as np

def dict2array(d):
    '''
    Merges a dict of lists into a list of lists with the same order.

    Parameters
    ----------
    d : dict.

    Returns
    -------
    output : list.
        list of lists.
    order : list.
        keys from dict in order of listing.
    '''
    output = []
    order = []
    for u in d:
        output.append(list(d[u]))
        order.append(u)
    return output, order

def dictofdict2array(top_dict):
    '''
    Converts a dictionary of dictionaries with scalar values and converts
    to a list of lists.

    Parameters
    ----------
    top_dict : dict
        i.e. { a: {x1 : a1, x2 : a2, x3 : a3},
               b: {x1 : b1, x2 : b2, x3 : b3} }
    Returns
    -------
    output : list
        i.e. [ [a1, b1, c1], [a2, b2, c2] ]
    order : list
        keys of top_dict, ordered as listed.
    '''
    output = []
    order = []
    N = len( top_dict[ list(top_dict)[0] ] ) # number of cells
    i = 0
    while i < N:
        row = []
        for key1 in top_dict:
            key2 = list(top_dict[key1])[i]
            #print(key2)
            order.append(key2)

            row.append( top_dict[key1][key2] )
        output.append(row)
        i += 1
    return output, dedupe(order)

def tripledict2array(top_dict):
    '''
    Converts a teriary leveled dictionary to a list of lists.

    Parameters
    ----------
    top_dict : dict
        i.e. { a: {x1 : {y1 : [z1,]}, x2 : {y2: [z2,]} },
               b: {x1 : {y1 : [z1,]}, x2 : {y2: [z2, z3, z4]} } }

    Returns
    -------
    output : list
        i.e. [[z1, z2], [z1, z2, z3, z4]]
    order : list.
        keys of the tertiary dictionaries, ordered as listed.
    '''
    output = []
    order1 = []
    order2 = []
    order3 = []
    j = 0
    while j < len( top_dict[ list(top_dict)[0] ][ list(top_dict[ list(top_dict)[0] ])[0] ] ):
        row = []
        for key1 in top_dict:
            order1.append(key1)
            for key2 in top_dict[key1]:
                order2.append(key2)
                order3.append(list(top_dict[key1][key2])[j])
                if type(top_dict[key1][key2][ list(top_dict[key1][key2])[j] ]) == list:
                    for item in top_dict[key1][key2][ list(top_dict[key1][key2])[j] ]:
                        row.append(item)
                else:
                    row.append( top_dict[key1][key2][ list(top_dict[key1][key2])[j] ] )
        output.append(row)
        j += 1
    return output, dedupe(order3)

def cell_ids2tracks(cell_ids):
    '''
    Converts a `cell_ids` dict to `tracksX` and `tracksY` (N,T) coordinate arrays.

    Parameters
    ----------
    cell_ids : dict
        cell paths, keyed by an `id`, valued are a list of tuple (x,y) coordinates.

    Returns
    -------
    tracksX, tracksY : ndarray.
        N x T arrays of X and Y locations respectively
    '''
    N = len(cell_ids)
    T = len(cell_ids[list(cell_ids)[0]])
    tracksX = np.zeros([N,T])
    tracksY = np.zeros([N,T])

    n_count = 0
    for c in cell_ids:
        cell = cell_ids[c]
        for t in range(T):
            tracksX[n_count, t] = cell[t][0]
            tracksY[n_count, t] = cell[t][1]
        n_count = n_count + 1

    return tracksX, tracksY


def dedupe(seq, idfun=None):
    '''
    Deduplicates lists.
    '''
    # order preserving
    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        # in old Python versions:
        # if seen.has_key(marker)
        # but in new ones:
        if marker in seen: continue
        seen[marker] = 1
        result.append(item)
    return result

import itertools
def merge_flat_lists(lists):
    '''
    Merges a tertiary list of lists into a seconday list of lists.

    Parameters
    ----------
    lists : list.
        tertiary list of lists [ [[a0,a1,a2], [b0,b1,b2]] ]

    Returns
    -------
    merged_list : list.
        secondary list of lists [[a0,a1,a2,b0,b1,b2]]
    '''
    merged_list = []
    n_rows = len(lists[0])
    i = 0
    while i < n_rows:
        tmp_list = []
        for l in lists:
            tmp_list.append(l[i])

        tmp_merged = list( itertools.chain( *tmp_list ) )
        merged_list.append(tmp_merged)
        i += 1

    # merged_list = [ [all vals for one cell], [...], ... ]
    return merged_list

def single_outputs_list(cell_ids, gf, rwf, msdf, output_dir, suffix=None):
    '''
    Creates a list of lists list[N][M] of cell statistics for CSV export.

    Parameters
    ----------
    cell_ids : dict
        cell paths, keyed by an `id`, valued are a list of tuple (x,y) coordinates.

    gf : hmstats.GeneralFeatures object
    rwf : hmstats.RWFeatures object
    msdf : hmstats.MSDFeatures object
    output_dir : string
        path to output directory.
    suffix : string
        suffix appended to output filenames.

    Returns
    -------
    output_list : list
        list of lists, output_list[N][M], where `N` is cells and `M` is features.
    '''
    # Creates a list of lists for writing out statistics
    # Ea. internal list is a single cell's stats
    output_list = []
    if suffix:
        output_dir = output_dir + str(suffix)
    for cell in cell_ids:
        output_list.append([ output_dir, cell, gf.total_distance[cell], gf.net_distance[cell],
                            gf.linearity[cell], gf.spearmanrsq[cell], gf.progressivity[cell], gf.max_speed[cell],
                            gf.min_speed[cell], gf.avg_speed[cell], msdf.alphas[cell], rwf.hurst_RS[cell], rwf.nongaussalpha[cell],
                            rwf.disp_var[cell], rwf.disp_skew[cell], rwf.diff_linearity[cell], rwf.diff_net_dist[cell] ])

    return output_list


def fix_order(correct_order, new_order, sorting):
    '''
    Fixes the order of a list in `sorting` with `new_order` to
    match the index order layed out in `correct_order`.

    Parameters
    ----------
    correct_order : list.
        contains keys in the correct order, guides sorting of the list `sorting`
    new_order : list.
        contains same set of keys in correct_order, but in a different order.
    sorting : list.
        list to be sorted based on the order in `correct_order`.
    '''
    # if order is correct, return input seq
    if correct_order == new_order:
        return sorting, new_order

    new_idx_order = [] # idx's of `correct_order[i]` loc in `new_order`
    for i in correct_order:
        new_idx_order += [new_order.index(i)]

    reordered_vals = []
    reordered_keys = []
    for i in range(len(new_idx_order)):
        reordered_vals += [sorting[new_idx_order[i]]]
        reordered_keys += [new_order[new_idx_order[i]]]

    assert correct_order == reordered_keys, 'keys not correctly ordered in `fix_order()`'
    return reordered_vals, reordered_keys


def make_merged_list(ind_outputs, gf, rwf):
    '''Merge output lists for all features

    Parameters
    ----------
    ind_outputs : list
        ind_outputs[N][M], where `N` is cells and `M` is features.
    gf : hmstats.GeneralFeatures object
    rwf : hmstats.RWFeatures object

    Returns
    -------
    merged_list : list
        merged_list[N][M], where `N` is cells and `M` is features.

    Notes
    -----
    Utilized `fix_order` and assertion checks to ensure that dictionary ordering
    is not perturbed during concatenation, which can occur in Python2 where
    dict primitive behavior is not robust to ordering in the manner of Python3.
    This is not official support for Python2, merely an attempt to prevent
    silent failure and generation of erroneous output.
    '''

    ind_order = []
    for i in ind_outputs:
        ind_order.append(i[1])

    autocorr_array, autocorr_order = dict2array(rwf.autocorr)
    autocorr_array, autocorr_order = fix_order(ind_order, autocorr_order, autocorr_array)
    assert ind_order == autocorr_order, 'individual and autocorr not in same order'

    diff_kurtosis_array, diff_kurtosis_order = dictofdict2array(rwf.diff_kurtosis)
    diff_kurtosis_array, diff_kurtosis_order = fix_order(ind_order, diff_kurtosis_order, diff_kurtosis_array)
    assert ind_order == diff_kurtosis_order, 'individual and diff_kurtosis not in same order'

    avg_moving_speed_array, avg_moving_speed_order = dictofdict2array( gf.avg_moving_speed )
    avg_moving_speed_array, avg_moving_speed_order = fix_order(ind_order, avg_moving_speed_order, avg_moving_speed_array)
    assert ind_order == avg_moving_speed_order, 'individual and avg_moving_speed not in same order'

    time_moving_array, time_moving_order = dictofdict2array( gf.time_moving )
    time_moving_array, time_moving_order = fix_order(ind_order, time_moving_order, time_moving_array)
    assert ind_order == time_moving_order, 'individual and time_moving not in same order'

    turn_list, turn_list_order = tripledict2array(gf.turn_stats)
    turn_list, turn_list_order = fix_order(ind_order, turn_list_order, turn_list)
    assert ind_order == turn_list_order, 'individual and turn_list not in same order'

    theta_list, theta_list_order = tripledict2array(gf.theta_stats)
    theta_list, theta_list_order = fix_order(ind_order, theta_list_order, theta_list)
    assert ind_order == theta_list_order, 'individual and theta_list not in same order'

    merged_list = merge_flat_lists([ind_outputs, diff_kurtosis_array, avg_moving_speed_array, time_moving_array, autocorr_array, turn_list, theta_list])
    return merged_list
