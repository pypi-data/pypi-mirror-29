'''
Heteromotility input/output functions
'''

from __future__ import print_function
import csv
import glob
import pickle
import numpy as np

def import_tracksXY(tracksX_path, tracksY_path, verbose=False):
    '''
    Imports cell tracks from (N, T) CSVs of X and Y coordinates.

    Parameters
    ----------
    tracksX_path : string.
        location of N x T CSV of sequential X locations
    tracksY_path : string.
        location of N x T CSV of sequential Y locations
    verbose : bool
        print notices if empty CSVs are imported.

    Returns
    -------
    tracksX, tracksY : ndarray.
        N x T arrays of X and Y locations respectively
    '''
    # Check if files are empty

    with open(tracksX_path) as f:
        contents = len(f.read())

    if contents == 0:
        if verbose:
            print('tracksX and tracksY are empty.')
        return False, False
    tracksX = np.loadtxt(tracksX_path, delimiter=',')
    tracksY = np.loadtxt(tracksY_path, delimiter=',')

    return tracksX, tracksY

def write_motility_stats(output_dir, output_name, gf, rwf, merged_list):
    '''
    Aggregates and exports statistics from `heteromotility` measurement modules
    to an N x M feature matrix.

    Parameters
    ----------
    output_dir : string.
        path to output directory.
    output_name : string.
        name of the output file.
    gf : hmstats.GeneralFeatures object.
    rwf : hmstats.RWFeatures object.
    merged_list : list.
        list of merged feature values from `hmtools.make_merged_list`.
    '''
    output_file_path = str(output_dir + output_name)

    motility_header = ['Well/XY', 'cell_id', 'total_distance', 'net_distance', 'linearity', 'spearmanrsq','progressivity',
    'max_speed', 'min_speed', 'avg_speed', 'MSD_slope', 'hurst_RS', 'nongauss', 'disp_var', 'disp_skew', 'rw_linearity', 'rw_netdist', 'rw_kurtosis01',
    'rw_kurtosis02', 'rw_kurtosis03', 'rw_kurtosis04', 'rw_kurtosis05', 'rw_kurtosis06', 'rw_kurtosis07',
    'rw_kurtosis08', 'rw_kurtosis09', 'rw_kurtosis10', 'avg_moving_speed01', 'avg_moving_speed02',
    'avg_moving_speed03', 'avg_moving_speed04', 'avg_moving_speed05', 'avg_moving_speed06',
    'avg_moving_speed07', 'avg_moving_speed08', 'avg_moving_speed09', 'avg_moving_speed10',
    'time_moving01', 'time_moving02', 'time_moving03', 'time_moving04', 'time_moving05',
    'time_moving06', 'time_moving07', 'time_moving08', 'time_moving09', 'time_moving10']

    theta_stats_list = []
    for i in gf.tau_range:
        for j in gf.interval_range:
            theta_stats_list.append( 'mean_theta_' + str(i) + '_' + str(j) )
            theta_stats_list.append( 'min_theta_' + str(i) + '_' + str(j) )
            theta_stats_list.append( 'max_theta_' + str(i) + '_' + str(j) )

    turn_stats_list = []
    for i in gf.tau_range:
        for j in gf.interval_range:
            turn_stats_list.append( 'p_rturn_' + str(i) + '_' + str(j) )

    autocorr_stats_list = []
    for i in range(1, rwf.autocorr_max_tau):
        autocorr_stats_list.append('autocorr_' + str(i))

    motility_header = motility_header + autocorr_stats_list
    motility_header = motility_header + turn_stats_list
    motility_header = motility_header + theta_stats_list

    with open(output_file_path, 'w') as out_file:
        selectric = csv.writer(out_file, delimiter = ',', quoting=csv.QUOTE_NONE, quotechar='')
        selectric.writerow( motility_header )
        i = 0
        while i < len(merged_list):
            selectric.writerow( merged_list[i] )
            i += 1

    print('Wrote ', output_dir, output_name)

def import_centroids(input_dir):
    '''Legacy function. Imports centroids from CSV files.'''
    centroid_arrays = []
    for matlab_export in glob.glob( input_dir ):
        in_file = open(matlab_export, "rU")
        with in_file as f:
            reader = csv.reader(f, delimiter=',')
            try:
                x, y = zip(*reader)
            except ValueError:
                x, y = (10000000,),(10000000,)

        i = 0
        array = []
        while i < len(x):
            array.append( ( float(x[i]), float(y[i]) ) )
            i += 1
        centroid_arrays.append(array)
    return centroid_arrays

motility_header = [
    'Well/XY', 'cell_id', 'total_distance', 'net_distance', 'linearity', 'spearmanrsq','progressivity',
    'max_speed', 'min_speed', 'avg_speed', 'MSD_slope', 'hurst_RS', 'nongauss',
    'disp_var', 'disp_skew', 'rw_linearity', 'rw_netdist',
    'rw_kurtosis01', 'rw_kurtosis02', 'rw_kurtosis03', 'rw_kurtosis04', 'rw_kurtosis05', 'rw_kurtosis06', 'rw_kurtosis07',
    'rw_kurtosis08', 'rw_kurtosis09', 'rw_kurtosis10', 'avg_moving_speed01', 'avg_moving_speed02',
    'avg_moving_speed03', 'avg_moving_speed04', 'avg_moving_speed05', 'avg_moving_speed06',
    'avg_moving_speed07', 'avg_moving_speed08', 'avg_moving_speed09', 'avg_moving_speed10',
    'time_moving01', 'time_moving02', 'time_moving03', 'time_moving04', 'time_moving05',
    'time_moving06', 'time_moving07', 'time_moving08', 'time_moving09', 'time_moving10']
