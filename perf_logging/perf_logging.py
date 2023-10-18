import matplotlib.pyplot as plt
import datetime
import json
import matplotlib as mpl

def init(log_state):
    log_type = ""
    if log_state == 0:
        return
    elif log_state == 1:
        log_type = "full"
    elif log_state == 2:
        log_type = "graphics"
    elif log_state == 3:
        log_type = "simulation"

    # Create file name
    log_name = str(datetime.datetime.now()).replace(" ", "_").replace(":", "-") + ".json"
    
    log_data = {
        "log_type": log_type,
        "log_name": log_name,
        "data": []
    }

    return log_data

def dumpData(log_data):
    log_name = log_data["log_name"]
    with open("perf_logging/logs/" + log_name, "w") as f:
        json.dump(log_data, f)
    
    graph_data(log_name)

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

def graph_data(log_name):

    data  = loadData(log_name)
    points = []
    for entry in data["data"]:
        for frame_time in entry["frame_times"]:
            points.append(frame_time)
    generateGraph(points, "Steps", "Frame Time (ns)",  data["log_type"] + " Performance " + log_name[:-12])