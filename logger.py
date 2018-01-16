# .................. VANILLA LOGGER ..................
# 
# A very simple logger to log several values during
#   an iterative process. Keeps logging values into
#   a CSV file. 
# A very simple use case is a training process 
#   for a machine learning algorithm. 
#
# Usage:
#
# 1. To plot logged values. 
#   >>> import vanilla_logger as vl
#   >>> vl.plot_logs(<file>, <options>)
#
# 2. To record values at an iteration, 
#
#   for iter_mark in range(num_iter):
#       ...
#       info = {'val1': <value of val1>, 'val2': <value of val2>, ... }
#       vl.log_info(<file>, info, iter_mark)
#
# Information from several files can be plotted at once 
#   using matplotlib.pyplot.subplot, and setting show=False
#   in each call to plot_log(). Finally, 
#   matplotlib.pyplot.show() should be called. 
#
#
# WARNING:  If iter_mark == 0, that is, it is the first iteration, 
#           then <file> is overwritten, and value names are placed
#           on the first line, followed by values on the second line. 
# ....................................................

# Required imports
import matplotlib.pyplot as plt
import numpy as np

# Define some linestyles. 
linestyles = ['r-', 'b-', 'y-', 'g-', 'k-', 'r-.', 'b-.', 'y-.', 'g-.', 'k-.', 'r--', 'b--', 'y--', 'g--', 'k--']
# Define some marker styles. 
markers    = ['', 'o', 'v', 's', 'x']

# ...................................................
# A function to log information at a certain iteration. 
# Inputs
#   logfile     The file which records all logs.
#   info        The information to be logged for a certain
#               iteration
#   iter_mark   The iteration. Starts at zero. 
#
def log_info(logfile, info, iter_mark):
    if iter_mark == 0:
        with open(logfile, 'w') as fptr:
        # If first iteration, write headings. 
            keys = ','.join(info.keys())
            fptr.write(keys + '\n')
            vals = ','.join([str(info[i]) for i in info.keys()])
            fptr.write(vals + '\n')
    else:
        # Write values. 
        with open(logfile, 'a') as fptr:
            vals = ','.join([str(info[i]) for i in info.keys()])
            fptr.write(vals + '\n')

    return
# ...................................................

# ...................................................
# A function to plot recorded values. 
# 
# Inputs
#   cfile       The CSV file containing values to be plotted. 
#   v_ids       IDs of values to be plotted. If None, v_names
#               is checked. 
#   v_names     The names of values to be plotted. If None, 
#               all values are plotted. 
#   smoothing   Whether plots should be smoothed using 1D
#               convolution. 
#   xlabel      Label to place on x-axis. None for no label
#   ylabel      See xlabel
#   title       See xlabel
#   show        Whether to render the plot. 
#
def plot_log(cfile, v_ids=None, v_names=None, smoothing=5,
        xlabel=None, ylabel=None, title=None, show=True):
    # Read the heading - value names. 
    with open(cfile, 'r') as f:
        heading = f.readline().strip()
        heading = heading.split(',')

    # Read the values themselves. 
    values = np.loadtxt(cfile, delimiter=',', skiprows=1)

    # Get the numbers of values and iterations. 
    n_iters = values.shape[0]
    n_vals  = values.shape[1]

    # If the IDs of values to be logged are specified, choose only those. 
    if v_ids is not None:
        values  = values[:,v_ids]
        heading = [heading[i] for i in v_ids]
    # Instad, if value names are specified, choose only those. 
    elif v_names is not None:
        v_ids   = [i for i in range(n_vals) if heading[i] in v_names]
        values  = values[:,v_ids]
        heading = [heading[i] for i in v_ids]

    # We will choose a different style for each plot. 
    n_lstyles = len(linestyles)
    n_mstyles = len(markers)

    # Handles to plots. These are used to place legends on the plot. 
    handles = []

    # If smoothing is desired, we perform it here. 
    if smoothing > 0:
        for l in range(n_vals):
            values[:,l] = conv(values[:,l], smoothing)

    # A dictionary returns all plotted values. 
    return_dict = {}

    # Plot now. 
    for l in range(n_vals):
        # Get line style based on 
        lstyle_id = l%n_lstyles
        mstyle_id = l/n_mstyles
        h, = plt.plot(values[:,l], linestyles[lstyle_id], marker=markers[mstyle_id])
        # Keep the handle. 
        handles.append(h)
        # Also keep the values just plotted. 
        return_dict[heading[l]] = values[:,l]

    # Place a legend. 
    plt.legend(handles, heading)
    # Place a grid. 
    plt.grid()
    # If xlabel, ylabel and title are desired, we place them too. 
    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)
    if title is not None:
        plt.title(title)
    
    # Whether the final plot is to be rendered. 
    if show:
        plt.show()

    # Return the plotted values in a dictionary. 
    return return_dict
# ...................................................

# ...................................................
# Define a 1D convolution operation. To be used if 
#   smoothing of graphs is desired. 
# Numpy's inbulit convolution is not good - it does
#   not handle boundary conditions properly. 
#
def conv(signal, length):
    output = np.zeros_like(signal)
    for i in range(signal.size):
        s_id = i - (length/2 if i > length/2 else 0)
        e_id = (length%2) + i + (length/2 if i + length/2 < signal.size else signal.size)
        output[i] = np.mean(signal[s_id:e_id])
    return output
# ...................................................
