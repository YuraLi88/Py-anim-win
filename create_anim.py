import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from glob import glob
import argparse
import matplotlib as mpl
import numpy as np
mpl.rcParams['figure.dpi'] = 100

def update(frame_number, frames_data, lines, ax):
    # Get data from frames_data list
    data = frames_data[frame_number] 

    for line, column in zip(lines, data.columns[1:]):
        line.set_data(data[0], data[column])
    x_arr = np.array(data[0])
    ax.set_xlim(x_arr[0], x_arr[-1])
    return lines

def read_data(files):
    data = []
    for file in files:
        data.append(pd.read_csv(file, delim_whitespace=True, header=None))
    return data

def get_min_max_y(data):
    Y_data = np.array([data[i].iloc[:,1:].to_numpy() for i in range(len(data))])
    min_y = np.min(Y_data)*1.05
    max_y = np.max(Y_data)*1.05
    return min_y, max_y

def build_animation(files, interval, xname, yname, title, fname):
    fig, ax = plt.subplots()
    ax.set_xlabel(xname)
    ax.set_ylabel(yname)
    ax.set_title(title)
    # read data from files list
    data = read_data(files)
    # get min and max y values
    ylim_min, ylim_max = get_min_max_y(data)
    ax.set_ylim(ylim_min, ylim_max)  # Set y-axis limits

    # Initialize lines for each column in the first file
    initial_data = data[0]
    lines = []
    for idx, column in enumerate(initial_data.columns[1:]):
        print(f"Init line for column {idx}")
        line, = ax.plot([], [])
        lines.append(line)
    print("Start animation")
    anim = FuncAnimation(fig, update, frames=len(files), fargs=(data, lines, ax), interval=interval)
    print("Save animation")
    # Save the animation as a GIF
    anim.save(f'{fname}.gif', writer='imagemagick')
    print("Show animation")

    # plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Build an animation from data files.')
    parser.add_argument('path', help='Directory containing .dat files')
    parser.add_argument('-i', '--interval', type=int, default=200, help='Interval between frames (ms)')
    parser.add_argument('-x', '--xname', default='x-axis', help='Label for the x-axis')
    parser.add_argument('-y', '--yname', default='y-axis', help='Label for the y-axis')
    parser.add_argument('-t', '--title', default='', help='Title of the plot')
    parser.add_argument('-n', '--name', default='animation', help='The name of gif-file')
    # parser.add_argument('--ylim_min', type=float, default=-1.05, help='Minimum y-axis limit')
    # parser.add_argument('--ylim_max', type=float, default=1.05, help='Maximum y-axis limit')
    args = parser.parse_args()

    files = [file for file in glob(f'{args.path}/*.dat')]
    build_animation(files, args.interval, args.xname, args.yname, args.title, args.name)
