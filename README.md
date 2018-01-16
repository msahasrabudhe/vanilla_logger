# Vanilla Logger
A very vanilla, easy logger to log information.

A logger that records information during an iterative process. 
Also includes a simple function that can plot recorded information. 

Logs information in the CSV format, so can be read by other editors. 

# Usage:

 1. To plot logged values. 
    ```python
    >>> import vanilla_logger as vl
    >>> vl.plot_log(<file>, <options>)
    ```

 2. To record values at an iteration, 

    ```python
    for iter_mark in range(num_iter):
        ...
        info = {'val1': <value of val1>, 'val2': <value of val2>, ... }
        vl.log_info(<file>, info, iter_mark)
    ```

Information from several files can be plotted at once 
using `matplotlib.pyplot.subplot()`, and setting `show=False`
in each call to `plot_log()`. Finally, 
`matplotlib.pyplot.show()` should be called. 
