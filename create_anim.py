import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from glob import glob
import argparse
import matplotlib as mpl
import numpy as np
mpl.rcParams['figure.dpi'] = 100

def update(frame_number, files, lines, ax):
    # print(file)
    file = files[frame_number]
    data = pd.read_csv(file, delim_whitespace=True, header=None)

    for line, column in zip(lines, data.columns[1:]):
        line.set_data(data[0], data[column])
    x_arr = np.array(data[0])
    ax.set_xlim(x_arr[0], x_arr[-1])
    # ax.relim()
    # ax.autoscale_view()
    return lines

def build_animation(files, interval, xname, yname, title, fname, ylim_min, ylim_max):
    fig, ax = plt.subplots()
    ax.set_xlabel(xname)
    ax.set_ylabel(yname)
    ax.set_title(title)
    ax.set_ylim(ylim_min, ylim_max)  # Set y-axis limits

    lines = []

    # Initialize lines for each column in the first file
    initial_data = pd.read_csv(files[0], delim_whitespace=True, header=None)
    for column in initial_data.columns[1:]:
        line, = ax.plot([], [])
        lines.append(line)
    # plt.show()
    anim = FuncAnimation(fig, update, frames=len(files), fargs=(files, lines, ax), interval=interval)

    # Save the animation as a GIF
    anim.save(f'{fname}.gif', writer='imagemagick')

    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Build an animation from data files.')
    parser.add_argument('path', help='Directory containing .dat files')
    parser.add_argument('-i', '--interval', type=int, default=200, help='Interval between frames (ms)')
    parser.add_argument('-x', '--xname', default='x-axis', help='Label for the x-axis')
    parser.add_argument('-y', '--yname', default='y-axis', help='Label for the y-axis')
    parser.add_argument('-t', '--title', default='', help='Title of the plot')
    parser.add_argument('-n', '--name', default='animation', help='The name of gif-file')
    parser.add_argument('--ylim_min', type=float, default=-1.05, help='Minimum y-axis limit')
    parser.add_argument('--ylim_max', type=float, default=1.05, help='Maximum y-axis limit')
    args = parser.parse_args()

    files = [file for file in glob(f'{args.path}/*.dat')]
    build_animation(files, args.interval, args.xname, args.yname, args.title, args.name, args.ylim_min, args.ylim_max)
