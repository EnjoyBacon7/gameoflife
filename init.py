import argparse
import config
import pygame

# -----------------------------------------------------------------------------
# Initialisations
# -----------------------------------------------------------------------------

# Initialise app state (args, resolution, etc...)
def initApp():
    parser = argparse.ArgumentParser(description="Game of Life")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-lf", "--log_full", action="store_true", help="Log full data")
    group.add_argument("-lg", "--log_graphics", action="store_true", help="Log graphics data")
    group.add_argument("-ls", "--log_simulation", action="store_true", help="Log simulation data")
    parser.add_argument("-nogui", action="store_true", help="disable gui")
    parser.add_argument("-r", "--resolution", nargs=2, type=int, help="Set resolution")
    parser.add_argument("-p", "--preset", type=str, help="Load preset")
    parser.add_argument("-b", "--board_size", nargs=2, type=int, help="Set board size")
    parser.add_argument("-w", "--wrap", action="store_true", help="Enable wrapping")
    args = parser.parse_args()

    appState = {
        "resolution": None,
        "gui": None,
        "logging": None,
        "screen": None,
        "preset": None,
        "board_size": None,
        "wrap": None
    }

    if args.resolution:
        appState["resolution"] = args.resolution
    else:
        appState["resolution"] = (1080, 720)

    if args.nogui:
        appState["gui"] = False
    else:
        appState["gui"] = True

    if args.log_full:
        appState["logging"] = 1
    elif args.log_graphics:
        appState["logging"] = 2
    elif args.log_simulation:
        appState["logging"] = 3
    else:
        appState["logging"] = 0

    if args.preset:
        appState["preset"] = args.preset
    else:
        appState["preset"] = None

    if args.board_size:
        appState["board_size"] = args.board_size
    else:
        appState["board_size"] = (-1, -1)

    if args.wrap:
        appState["wrap"] = True
    else:
        appState["wrap"] = False

    pygame.init()
    if(appState["logging"] == 0):
        appState["screen"] = pygame.display.set_mode(appState["resolution"], pygame.RESIZABLE)
    else:
        appState["screen"] = pygame.display.set_mode(appState["resolution"])
    pygame.display.set_caption("Game of Life")

    return appState
