import time
import simulation
import datetime
import json
from perf_logging import generateGraph

def init_log(log_type):
    log_type_str = ""
    if log_type == 0:
        return
    elif log_type == 1:
        log_type_str = "full"
    elif log_type == 2:
        log_type_str = "graphics"
    elif log_type == 3:
        log_type_str = "simulation"

    # Create file name
    log_name = str(datetime.datetime.now()).replace(" ", "_").replace(":", "-") + ".json"
    
    log_data = {
        "log_type": log_type_str,
        "log_name": log_name,
        "data": []
    }

    return log_data

def dumpData(log_data):
    log_name = log_data["log_name"]
    with open("perf_logging/logs/" + log_name, "w") as f:
        json.dump(log_data, f)

def loop(appState, gameState):

    # Logging (depending on app args)
    log_data = init_log(appState["logging"])
    log_start = 0
    log_end = 0

    while gameState["quit"] == False:

        # Logging check (to save redundant checks)
        if appState["logging"] == 1:
            log_start = time.perf_counter_ns()
            # Start with inputs (and events)
            simulation.handleEvents(appState, gameState)
            # Then handle game logic
            simulation.handleGameLogic(gameState)
            # Then draw
            simulation.drawGame(appState, gameState)
            log_end = time.perf_counter_ns()
        
        elif appState["logging"] == 2:
            # Start with inputs (and events)
            simulation.handleEvents(appState, gameState)
            # Then handle game logic
            simulation.handleGameLogic(gameState)
            log_start = time.perf_counter_ns()
            # Then draw
            simulation.drawGame(appState, gameState)
            log_end = time.perf_counter_ns()
        
        elif appState["logging"] == 3:
            # Start with inputs (and events)
            simulation.handleEvents(appState, gameState)
            log_start = time.perf_counter_ns()
            # Then handle game logic
            simulation.handleGameLogic(gameState)
            log_end = time.perf_counter_ns()
            # Then draw
            simulation.drawGame(appState, gameState)

        # add entry to log
        if(appState["logging"] != 0):
            log_data["data"].append({
                "frame_times": [log_end - log_start],
                "sim_steps": gameState["simSteps"],
                "sim_speed": gameState["simSpeed"],
                "zoom_factor": gameState["zoom_factor"],
                "offset": gameState["offset"],
                "pause": gameState["pause"],
                "resolution": appState["resolution"],
            })
            if(appState["gui"] == False):
                print("Step: " + str(gameState["simSteps"]) + " | Frame Time (ns): " + str(log_end - log_start))
            if(gameState["simSteps"] >= 1000):
                gameState["quit"] = True

    # Dump log data to file
    dumpData(log_data)
    generateGraph.graphData(log_data["log_name"])