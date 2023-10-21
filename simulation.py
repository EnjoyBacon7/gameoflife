import pygame
import config
import json

# -----------------------------------------------------------------------------
# Initialisation
# -----------------------------------------------------------------------------

def init(appState):

    # Board contains a 1D array of all live cells to lighten the load on the CPU (also allows for infinite board size)

    gameState = {
        "board": loadPreset(appState["preset"]),
        "offset": config.INITIAL_OFFSET,
        "zoom_factor": 1,
        "pause": False,
        "board_size": appState["board_size"],
        "wrap": appState["wrap"],

        # Simulation variables
        "simSteps": 0,
        "simTimer": 0,
        "simSpeed": -1,
        "gameClock": pygame.time.Clock(),

        "quit": False,
    }

    return gameState

# -----------------------------------------------------------------------------
# Game Loop
# -----------------------------------------------------------------------------

def loop(appState, gameState):

    while gameState["quit"] == False:

        # Start with inputs (and events)
        handleEvents(appState, gameState)
        # Then handle game logic
        handleGameLogic(gameState)
        # Then draw
        drawGame(appState, gameState)
        # Tick
        gameState["gameClock"].tick(config.FPS_MAX)

# ---------- Handle Inputs and Events ----------
def handleEvents(appState, gameState):

    if appState["gui"] == False:
        return

    # One press events
    for event in pygame.event.get():
        # Quit (cmd+q, alt+f4, X button, etc.)
        if event.type == pygame.QUIT:
            pygame.quit()

        if(appState["logging"] != 0):
            continue

        # Resize window
        elif event.type == pygame.VIDEORESIZE:
            appState["resolution"] = event.size
        elif event.type == pygame.KEYDOWN:
            # Quit [ESC]
            if event.key == pygame.K_ESCAPE:
                gameState["quit"] = True
            # Reset the board [R]
            elif(event.key == pygame.K_r):
                gameState["board"] = []
            # Pause simulation [SPACE]
            elif(event.key == pygame.K_SPACE):
                gameState["pause"] = not gameState["pause"]

    if(appState["logging"] != 0):
        return

    # Hold events
    keys = pygame.key.get_pressed()
    # Increase zoom level [O]
    if(keys[pygame.K_o]):
        gameState["zoom_factor"] += 0.01
    # Decrease zoom level [P]
    if(keys[pygame.K_p]):
        gameState["zoom_factor"] -= 0.01
    # Move up [ARR_UP]
    if(keys[pygame.K_UP]):
        gameState["offset"] = (gameState["offset"][0],
                               gameState["offset"][1] - 0.1)
    # Move down [ARR_DOWN]
    if(keys[pygame.K_DOWN]):
        gameState["offset"] = (gameState["offset"][0],
                               gameState["offset"][1] + 0.1)
    # Move left [ARR_LEFT]
    if(keys[pygame.K_LEFT]):
        gameState["offset"] = (gameState["offset"][0] -
                               0.1, gameState["offset"][1])
    # Move right [ARR_RIGHT]
    if(keys[pygame.K_RIGHT]):
        gameState["offset"] = (gameState["offset"][0] +
                               0.1, gameState["offset"][1])
    # Increase simulation speed [B]
    if(keys[pygame.K_b]):
        gameState["simSpeed"] += 0.1
    # Decrease simulation speed [N]
    if(keys[pygame.K_n]):
        gameState["simSpeed"] -= 0.1
    # Add Cell [LMB]
    if(pygame.mouse.get_pressed()[0]):
        pos = pygame.mouse.get_pos()
        cell_size_px = int(config.UNIT * gameState["zoom_factor"])
        pos = (int((pos[0] - gameState["offset"][0] * cell_size_px) / cell_size_px),
               int((pos[1] - gameState["offset"][1] * cell_size_px) / cell_size_px))
        gameState["board"].append(pos)



# ---------- Draw the game ----------
def drawGame(appState, gameState):

    if(not appState["gui"]):
        return

    appState["screen"]

    appState["screen"].fill(config.COLOR_BACKGROUND)
    drawCells(gameState, appState)
    drawGrid(gameState, appState)
    drawHUD(gameState, appState)
    
    pygame.display.flip()


def drawGrid(gameState, appState):

    screen = appState["screen"]
    resolution = appState["resolution"]
    zoom_factor = gameState["zoom_factor"]
    pos = gameState["offset"]

    cell_size_px = int(config.UNIT * zoom_factor)
    grid_offset_px = ((int(pos[0] * cell_size_px) % cell_size_px),
                      (int(pos[1] * cell_size_px)) % cell_size_px)

    for i in range(int(resolution[0] / cell_size_px)):
        pygame.draw.line(screen, config.COLOR_GRID, (i * cell_size_px + grid_offset_px[0], 0), (i * cell_size_px + grid_offset_px[0], resolution[1]))
    for i in range(int(resolution[1] / cell_size_px)):
        pygame.draw.line(screen, config.COLOR_GRID, (0, i * cell_size_px + grid_offset_px[1]), (resolution[0], i * cell_size_px + grid_offset_px[1]))

    # If there is a board size limit, draw a border
    if(gameState["board_size"][0] != -1):
        pygame.draw.line(screen, config.COLOR_GRID, ((gameState["board_size"][0] + pos[0]) * cell_size_px, 0), ((gameState["board_size"][0] + pos[0]) * cell_size_px, resolution[1]), 3)
        pygame.draw.line(screen, config.COLOR_GRID, (pos[0] * cell_size_px, 0), (pos[0] * cell_size_px, resolution[1]), 3)
    if(gameState["board_size"][1] != -1):
        pygame.draw.line(screen, config.COLOR_GRID, (0, (gameState["board_size"][1] + pos[1]) * cell_size_px), (resolution[0], (gameState["board_size"][1] + pos[1]) * cell_size_px), 3)
        pygame.draw.line(screen, config.COLOR_GRID, (0, pos[1] * cell_size_px), (resolution[0], pos[1] * cell_size_px), 3)

def drawCells(gameState, appState):
    screen = appState["screen"]
    board = gameState["board"]
    zoom_factor = gameState["zoom_factor"]
    offset = gameState["offset"]

    cell_size_px = int(config.UNIT * zoom_factor)
    pos_px = (int(offset[0] * cell_size_px), int(offset[1] * cell_size_px))

    for cell in board:
        pygame.draw.rect(screen, config.COLOR_CELL, (cell[0] * cell_size_px + pos_px[0], cell[1] * cell_size_px + pos_px[1], cell_size_px, cell_size_px))

def drawHUD(gameState, appState):
    resolution = appState["resolution"]
    screen = appState["screen"]
    font = pygame.font.SysFont("Roboto", 30)
    zoom_factor = gameState["zoom_factor"]
    offset = gameState["offset"]
    simSpeed = gameState["simSpeed"]
    pause = gameState["pause"]

    infobox_w = config.INFO_BOX_SIZE[0] * resolution[0] / 100
    infobox_h = config.INFO_BOX_SIZE[1] * resolution[1] / 100

    hud = pygame.Surface((infobox_w, infobox_h), pygame.SRCALPHA)

    pygame.draw.rect(hud, config.COLOR_INFO_BG, (0, 0, infobox_w, infobox_h), 0, 10)
    pygame.draw.rect(hud, config.COLOR_INFO_BORDER, (0, 0, infobox_w, infobox_h), 2, 10)

    hud.blit(font.render("Zoom: " + str(round(zoom_factor, 2)), True, (0, 0, 0)), (10, 10))
    hud.blit(font.render("Offset: " + str(round(offset[0], 2)) + ", " + str(round(offset[1], 2)), True, (0, 0, 0)), (10, 40))
    hud.blit(font.render("Sim Speed: " + str(round(simSpeed, 2)), True, (0, 0, 0)), (10, 70))
    hud.blit(font.render("Pause: " + str(pause), True, (0, 0, 0)), (10, 100))
    hud.blit(font.render("Steps: " + str(gameState["simSteps"]), True, (0, 0, 0)), (10, 130))

    screen.blit(hud, (config.INFO_BOX_POS[0] * resolution[0] / 100, config.INFO_BOX_POS[1] * resolution[1] / 100))


# ---------- Game Logic ----------

def handleGameLogic(gameState):
    if gameState["pause"]:
        return

    current_time = pygame.time.get_ticks()
    sim_timer = gameState["simTimer"]
    sim_speed = gameState["simSpeed"]

    time_since_step = current_time - sim_timer
    time_threshold = 1000 / sim_speed

    if time_since_step < time_threshold:
        return

    sim_timer = current_time
    gameState["simTimer"] = sim_timer

    board = gameState["board"]
    new_board = set()
    board_size = gameState["board_size"]

    live_neighbors_count = {}  # Use a dictionary to track live neighbor counts

    for x, y in board:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                neighbor = (x + dx, y + dy)
                live_neighbors_count[neighbor] = live_neighbors_count.get(neighbor, 0) + 1

    for cell in live_neighbors_count:
        x, y = cell
        count = live_neighbors_count.get(cell, 0)

        if (x, y) in board and 2 <= count <= 3:
            new_board.add((x, y))
        elif (x, y) not in board and count == 3:
            new_board.add((x, y))

    gameState["board"] = new_board

    if board_size != (-1, -1):
        x_max, y_max = board_size
        gameState["board"] = {(x, y) for (x, y) in new_board if 0 <= x < x_max and 0 <= y < y_max}

    gameState["simSteps"] += 1

    if gameState["simSteps"] % 100 == 0:
        print("Number of cells: " + str(len(new_board)))




def loadPreset(preset):

    if(preset == None):
        return []
    
    board = []

    with open('presets.json', 'r') as f:
        data = json.load(f)

    for cell in data[preset]["live_cells"]:
        board.append(tuple(cell))

    return board

