import matplotlib.pyplot as plt
import numpy as np
import json
import os

import matplotlib as mpl

def generateGraph(points, x_label, y_label, title):
    plt.plot(points)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.savefig("graphs/" + title + ".png")
    plt.show()

def loadData(file_name):
    data = []
    with open("logs/" + file_name, 'r') as f:
        data = json.load(f)
    return data

def main(log_name):

    for file_name in os.listdir("logs"):
        data  = loadData(file_name)
        points = []
        for entry in data["data"]:
            for frame_time in entry["frame_times"]:
                points.append(frame_time)
        print(points)
        generateGraph(points, "Steps", "Frame Time (ms)",  data["log_type"] + " Performance " + file_name[:-12])

if __name__ == "__main__":
    main()