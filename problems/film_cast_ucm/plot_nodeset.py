from __future__ import print_function
import argparse
import exodus
import sys
import operator
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot values over a nodeset intersection')
    parser.add_argument('nodeset', metavar='NS', type=int,
                        help='The nodeset to plot')

    parser.add_argument('variable', metavar='VAR', type=str, 
                    help='The variable to plot')

    parser.add_argument('exofile', metavar='EXOFILE', type=str,
                            help='The exodus file to use')


    args = parser.parse_args()

    try:
        e = exodus.exodus(args.exofile)
    except Exception:
        print("Could not open exodus file", file=sys.stderr)
        sys.exit(-1)

    nodeset = args.nodeset
    nodesets = e.get_node_set_ids()
    if nodeset not in nodesets:
        print("Nodeset not found in ", args.exofile, file=sys.stderr)
        print("Available nodesets are:", file=sys.stderr)
        print(nodesets)
        sys.exit(-1)


    var = args.variable
    nodal_vars = e.get_node_variable_names()
    if var not in nodal_vars:
        print("Variable not found in ", args.exofile, file=sys.stderr)
        print("Available variables are:", file=sys.stderr)
        print(nodal_vars)
        sys.exit(-1)


    nodes = [node-1 for node in e.get_node_set_nodes(nodeset)]
    x,y,z = e.get_coords()
    # only checking first timestep at the moment
    values = e.get_node_variable_values(var, 1)
    dmx = e.get_node_variable_values("DMX", 1)
    dmy = e.get_node_variable_values("DMY", 1)
    dmz = e.get_node_variable_values("DMZ", 1)

    nodeset_values = [float(values[node]) for node in nodes]
    nodeset_x = [x[node] + dmx[node] for node in nodes]
    nodeset_y = [y[node] + dmy[node] for node in nodes]
    nodeset_z = [z[node] + dmz[node] for node in nodes]

    plot_dim = sorted(zip(nodeset_x, nodeset_y, nodeset_z, nodeset_values), key = operator.itemgetter(0,1))
    plot_x = np.array([x for x, y, z, v in plot_dim])
    plot_y = np.array([y for x, y, z, v in plot_dim])
    plot_z = np.array([z for x, y, z, v in plot_dim])
    plot_v = np.array([v for x, y, z, v in plot_dim])

    distx = np.max(plot_x) - np.min(plot_x)
    distz = np.max(plot_z) - np.min(plot_z)

    print("dist(x) = ", distx)
    print("dist(z) = ", distz)

    # print("x\ty\tvalue")
    # for x,z, v in plot_dim:
        # print(x, "\t", y, "\t", v)

    # plot over largest distance

    paper = pd.read_csv("250.csv")

    if distx >= distz:
        plt.plot(10*(np.max(plot_x) - plot_x), 10*plot_z)
        plt.plot(paper['x'], paper['y'])
        #plt.ylabel(var)
        plt.ylabel('z coord')
        plt.xlabel('x coord')
    else:
        plt.plot(plot_z, plot_x)
        plt.ylabel(var)
        plt.xlabel('y coord')
    plt.show()
        
