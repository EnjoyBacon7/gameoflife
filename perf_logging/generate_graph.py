import matplotlib.pyplot as plt
import json

import matplotlib as mpl

def generateGraph(points, x_label, y_label, title):
    plt.plot(points)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.savefig("perf_logging/graphs/" + title + ".png")
    plt.show()

def loadData(log_name):
    data = []
    with open("perf_logging/logs/" + log_name, 'r') as f:
        data = json.load(f)
    return data

def main(log_name):

    data  = loadData(log_name)
    points = []
    for entry in data["data"]:
        for frame_time in entry["frame_times"]:
            points.append(frame_time)
    print(points)
    generateGraph(points, "Steps", "Frame Time (ns)",  data["log_type"] + " Performance " + log_name[:-12])

if __name__ == "__main__":
    main()