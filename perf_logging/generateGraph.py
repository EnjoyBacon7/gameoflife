import matplotlib.pyplot as plt
import json
import matplotlib as mpl

def generateGraph(points, x_label, y_label, title, save_path, data, dpi=100, save=False):
    # Create a figure with two subplots: one for the graph and one for the info
    fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1], 'hspace': 0.2}, figsize=(1280 / dpi, 720 / dpi), dpi=dpi)

    # Plot the graph on the top subplot
    ax1.plot(points)
    ax1.set_xlabel(x_label)
    ax1.set_ylabel(y_label)
    ax1.set_title(title)

    # Add corresponding parameters below the graph in the bottom subplot
    info_text = (
        f"Resolution: {data['resolution']}\n"
        f"GUI: {data['gui']}\n"
        f"Log Type: {data['log_type']}\n"
        f"Log Name: {data['log_name']}\n"
        f"Speed: {data['sim_speed']}\n"
        f"Time: {round(data['test_time'])}ms"
    )
    ax2.text(0.02, 0.2, info_text, fontsize=12, transform=ax2.transAxes)
    ax2.axis('off')  # Remove axis from the info subplot
    if save:
        # Save the figure with the specified DPI
        plt.savefig(f"{save_path}/{title}.png", dpi=dpi)


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

    generateGraph(points, "Steps", "Frame Time (ns)",  log_name[:-12], "perf_logging/graphs", data, save=True)

if __name__ == "__main__":

    log_name = input("Enter log file name to graph: ")

    log_path = "logs/" + log_name
    data = loadData(log_path)
    points = []
    for entry in data["data"]:
        for frame_time in entry["frame_time"]:
            points.append(frame_time)
    generateGraph(points, "Steps", "Frame Time (ns)",  log_name[:-12], "graphs", data, save=False)
    plt.show()