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
    parser.add_argument("-r", "--resolution", nargs=2, type=int, help="set resolution")
    args = parser.parse_args()


    appState = {
        "resolution": None,
        "gui": None,
        "logging": None,
        "screen": None
    }

    if args.resolution:
        appState["resolution"] = args.resolution
    else:
        appState["resolution"] = config.RESOLUTION

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

    appState["screen"] = initPygame(args.resolution)

    return appState

# Initialise pygame
def initPygame(resolution):
    pygame.init()
    screen = pygame.display.set_mode(resolution, pygame.RESIZABLE)
    pygame.display.set_caption("Game of Life")
    return screen