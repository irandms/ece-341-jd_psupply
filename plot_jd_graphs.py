#!/bin/python3

# Author: Spencer Moss
# Graphs some collected data for our Junior Design Individual Power Supplies

import matplotlib.pyplot as plt
import numpy

from pyexcel_ods import get_data
import json

from cycler import cycler

def generate_graph(plot_title, file_name):
    data = get_data(file_name)
    data_dump = json.dumps(data)

    # Set colors to be the same for both scatter data and trendline
    plt.gca().set_prop_cycle(cycler('color', 
        ['dodgerblue', 'dodgerblue',
        'orange', 'orange', 
        'red', 'red']))
    for key, value in data.items():
        # Extract the label for this set of data
        plot_label = key
        data_arrays = value
        # Extract the Y and X axis graph labels
        x_label, y_label = data_arrays[0]
        # Remove the Y and X axis labels from our raw data
        data_arrays = data_arrays[1:]

        # Create simple arrays of x-axis data, and one for y-axis data
        currents = []
        voltages = []
        for xy_pair in data_arrays:
            current, voltage = tuple(xy_pair)
            currents.append(current)
            voltages.append(voltage)

        # Scatter plot
        plt.plot(currents, voltages, "o", label=plot_label)
        # Generate trendline from raw data
        z = numpy.polyfit(currents, voltages, 3)
        p = numpy.poly1d(z)
        # Plot trendline
        plt.plot(currents,p(currents),"--", dashes=(2, 4))

    """
    General plotting settings:
    Title, with the name passed into this function as an argument
    Enable legend, to show which datasets belong to which input value
    Set x and y labels
    Set y axis to start at 0 (usually looks better)
    Saves the figure to a .png image in the directory this is called from
    Shows the figure.
    """
    plt.title(plot_title)
    plt.legend(loc='upper left')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.gca().set_ylim(ymin=0)
    plt.savefig("{}.png".format(file_name))
    plt.show()

if __name__ == "__main__":
    generate_graph('3.3V Voltage Ripple vs. Output Current', '3v3ripple.ods')
    generate_graph('5V Voltage Ripple vs. Output Current', '5vripple.ods')
