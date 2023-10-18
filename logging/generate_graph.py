import matplotlib.pyplot as plt
import numpy as np
import json

import matplotlib as mpl

def generateGraph(data_set, x_label, y_label, title):
    for points in data_set:
        plt.plot(points)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()

def loadData():
    data = []
    with open('log.json', 'r') as f:
        data = json.load(f)
    return data

def main():
    data = loadData()
    data_set = []
    for entry in data["log"]:
        points = []
        for frame_time in entry["frame_times"]:
            points.append(frame_time)
        data_set.append(points)
    generateGraph(data_set, "Steps", "Frame Time (ms)",  "Performance Drop with Gosper Glider Gun")

if __name__ == "__main__":
    main()