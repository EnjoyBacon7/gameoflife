import matplotlib.pyplot as plt
import json
import matplotlib as mpl

def generateGraph(points, x_label, y_label, title, save_path, data, dpi=100):
    plt.plot(points)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)

    # Add corresponding parameters below the graph
    plt.text(0.02, -0.2, "Resolution : " + str(data["resolution"]), fontsize=12, transform=plt.gca().transAxes)
    plt.text(0.02, -0.275, "GUI : " + str(data["gui"]), fontsize=12, transform=plt.gca().transAxes)
    plt.text(0.02, -0.35, "Log Type : " + str(data["log_type"]), fontsize=12, transform=plt.gca().transAxes)
    plt.text(0.02, -0.425, "Log Name : " + str(data["log_name"]), fontsize=12, transform=plt.gca().transAxes)
    plt.text(0.02, -0.5, "Speed : " + str(data["sim_speed"]), fontsize=12, transform=plt.gca().transAxes)

    plt.subplots_adjust(bottom=0.3)

    plt.savefig(save_path + "/" + title + ".png", dpi=dpi)
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
        for frame_time in entry["frame_time"]:
            points.append(frame_time)
    generateGraph(points, "Steps", "Frame Time (ns)",  data["log_type"] + " Performance " + log_name[:-12], "perf_logging/graphs", data)

if __name__ == "__main__":

    log_name = input("Enter log file name to graph: ")

    log_path = "logs/" + log_name
    data = loadData(log_path)
    points = []
    for entry in data["data"]:
        for frame_time in entry["frame_time"]:
            points.append(frame_time)
    generateGraph(points, "Steps", "Frame Time (ns)",  data["log_type"] + " Performance " + log_name[:-12], "graphs", data)