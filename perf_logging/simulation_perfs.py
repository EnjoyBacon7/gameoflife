import time
import simulation
import datetime
import json
from perf_logging import generateGraph

STEP_LIMIT = 5000

def init_log(appState):

    log_type = appState["logging"]

    log_type_str = ""
    if log_type == 0:
        return
    elif log_type == 1:
        log_type_str = "full"
    elif log_type == 2:
        log_type_str = "graphics"
    elif log_type == 3:
        log_type_str = "simulation"
    
    log_data = {
        "log_type": log_type_str,
        "log_name": "",
        "resolution": appState["resolution"],
        "gui": appState["gui"],
        "preset": appState["preset"],
        "sim_speed": 0,
        "zoom_factor": 0,
        "offset": (0, 0),
        "pause": False,
        "test_time": time.perf_counter(),
        "data": []
    }

    # Create file name
    log_time = str(datetime.datetime.now()).replace(" ", "_").replace(":", "-")
    log_name = log_type_str.capitalize() + "_Log_" + str(log_data["resolution"][1]) + "p_" + log_data["preset"] + "_" + log_time + ".json"

    log_data["log_name"] = log_name

    return log_data

def dumpData(log_data):
    log_name = log_data["log_name"]
    with open("perf_logging/logs/" + log_name, "w") as f:
        json.dump(log_data, f)

def loop(appState, gameState):

    # Logging (depending on app args)
    log_data = init_log(appState)
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
                "frame_time": [log_end - log_start],
            })
            if(appState["gui"] == False):
                print("Step: " + str(gameState["simSteps"]) + " | Frame Time (ns): " + str(log_end - log_start))
            if(gameState["simSteps"] >= STEP_LIMIT):

                log_data["sim_speed"] = gameState["simSpeed"]
                log_data["zoom_factor"] = gameState["zoom_factor"]
                log_data["offset"] = gameState["offset"]
                log_data["pause"] = gameState["pause"]
                log_data["test_time"] = (time.perf_counter() - log_data["test_time"]) * 1000

                gameState["quit"] = True

    # Dump log data to file
    dumpData(log_data)
    generateGraph.graphData(log_data["log_name"])