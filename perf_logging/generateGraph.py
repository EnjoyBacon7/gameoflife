import matplotlib.pyplot as plt
import datetime
import json
import matplotlib as mpl


def generateGraph(points, x_label, y_label, title, save_path):
    plt.plot(points)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.savefig(save_path + "/" + title + ".png")
    plt.show()

def loadData(log_path):
    data = []
    with open(log_path, 'r') as f:
        data = json.load(f)
    return data

def graphData(log_name):

    log_path = "perf_logging/logs/" + log_name
    data  = loadData(log_path)
    points = []
    for entry in data["data"]:
        for frame_time in entry["frame_times"]:
            points.append(frame_time)
    generateGraph(points, "Steps", "Frame Time (ns)",  data["log_type"] + " Performance " + log_name[:-12], "perf_logging/graphs")

if __name__ == "__main__":

    log_name = input("Enter log file name to graph: ")

    log_path = "logs/" + log_name
    data = loadData(log_path)
    points = []
    for entry in data["data"]:
        for frame_time in entry["frame_times"]:
            points.append(frame_time)
    generateGraph(points, "Steps", "Frame Time (ns)",  data["log_type"] + " Performance " + log_name[:-12], "graphs")