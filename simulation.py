import pygame
import config
import json

# -----------------------------------------------------------------------------
# Initialisation
# -----------------------------------------------------------------------------

def init():

    # Board contains a 1D array of all live cells to lighten the load on the CPU (also allows for infinite board size)

    gameState = {
        "board": [],
        "offset": config.INITIAL_OFFSET,
        "zoom_factor": 1,
        "pause": False,

        # Simulation variables
        "simSteps": 0,
        "simTimer": 0,
        "simSpeed": -1,
        "gameClock": pygame.time.Clock(),

        "quit": False,
    }

    loadPreset(gameState, "Gosper Glider Gun")

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


def drawCells(gameState, appState):
    screen = appState["screen"]
    board = gameState["board"]
    zoom_factor = gameState["zoom_factor"]
    offset = gameState["offset"]

    cell_size_px = int(config.UNIT * zoom_factor)
    pos_px = (int(offset[0] * cell_size_px), int(offset[1] * cell_size_px))

    for i in range(len(board)):
        pygame.draw.rect(screen, config.COLOR_CELL, (board[i][0]*cell_size_px + pos_px[0],
                         board[i][1]*cell_size_px + pos_px[1], cell_size_px, cell_size_px))

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

    if(gameState["pause"]):
        return

    # Check if game should be updated
    timeSinceStep = (pygame.time.get_ticks() - gameState["simTimer"])
    if(timeSinceStep > 1/gameState["simSpeed"] * 1000):
        gameState["simTimer"] = int(pygame.time.get_ticks())
    else:
        return
    
    board = gameState["board"]
    new_board = set()

    # Create a set to store all neighbor coordinates
    neighbor_coords = set()

    # Iterate through live cells and add neighbors
    for cell in board:
        x, y = cell
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                neighbor = (x + dx, y + dy)
                neighbor_coords.add(neighbor)
    
    # Apply Conway's Game of Life rules
    for coord in neighbor_coords:
        x, y = coord
        live_neighbors = sum((x + dx, y + dy) in board for dx in [-1, 0, 1] for dy in [-1, 0, 1] if dx != 0 or dy != 0)
        if (x, y) in board and 2 <= live_neighbors <= 3:
            new_board.add((x, y))
        elif (x, y) not in board and live_neighbors == 3:
            new_board.add((x, y))

    # Update the game board with the new generation
    gameState["board"] = list(new_board)

    # Increment the simulation step counter
    gameState["simSteps"] += 1

def loadPreset(gameState, preset):

    with open('presets.json', 'r') as f:
        data = json.load(f)

    if(preset == "Gosper Glider Gun"):
        for cell in data["Gosper Glider Gun"]["live_cells"]:
            gameState["board"].append(tuple(cell))
    elif(preset == "Penta-Decathlon"):
        for cell in data["Penta-Decathlon"]["live_cells"]:
            print("added cell")
            gameState["board"].append(tuple(cell))

