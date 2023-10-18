import pygame
import init

import config
import simulation

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main():

    # Initialise pygame and app state
    appState = init.initApp()    

    # Display the main menu
    #menus(appState, screen)

    # Initialise the game state
    gameState = simulation.initGame()
    # Main loop
    simulation.loop(appState, gameState)

# -----------------------------------------------------------------------------
# Menus
# -----------------------------------------------------------------------------

def menus(appState, screen):

    # Initialise menu demo
    gameState = simulation.initGame()
    simulation.loadPreset(gameState, "Gosper Glider Gun")
    gameState["simSpeed"] = -1

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            # On click
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Start button
                if event.button == 1:
                    running = False
            elif event.type == pygame.VIDEORESIZE:
                appState["resolution"] = event.size
        
        # Handle demo logic
        simulation.handleGameLogic(gameState)
        # Draw
        simulation.drawGame(gameState, screen, True)
        drawMenus(appState, screen)
        pygame.display.flip()
        # Tick
        gameState["gameClock"].tick(config.FPS_MAX)


def drawMenus(appState, screen):
    drawMainMenu(appState, screen)

def drawMainMenu(appState, screen):

    menuHud_w = appState["resolution"][0] * config.MENU_BOX_SIZE[0] / 100
    menuhud_h = appState["resolution"][1] * config.MENU_BOX_SIZE[1] / 100

    menuhud = pygame.Surface((menuHud_w, menuhud_h), pygame.SRCALPHA)

    pygame.draw.rect(menuhud, config.COLOR_MENU_BG, (0, 0, menuHud_w, menuhud_h), 0, 10)
    pygame.draw.rect(menuhud, config.COLOR_MENU_BORDER, (0, 0, menuHud_w, menuhud_h), 2, 10)

    font = pygame.font.SysFont("Roboto", 30)

    text = font.render("Main Menu", True, (0, 0, 0))
    text_rect = text.get_rect(center=(config.MAIN_MENU_TXT_POS[0]/100 * menuHud_w, config.MAIN_MENU_TXT_POS[1]/100 * menuhud_h))
    menuhud.blit(text, text_rect)

    text = font.render("Start", True, (0, 0, 0))
    text_rect = text.get_rect(center=(config.MAIN_MENU_START_POS[0]/100 * menuHud_w, config.MAIN_MENU_START_POS[1]/100 * menuhud_h + 50))
    menuhud.blit(text, text_rect)

    screen.blit(menuhud, (config.MENU_BOX_POS[0] * appState["resolution"][0] / 100, config.MENU_BOX_POS[1] * appState["resolution"][1] / 100))

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    main()
