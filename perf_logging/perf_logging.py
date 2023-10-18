import datetime
import json
import perf_logging.generate_graph as graph

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
    
    graph.main(log_name)
