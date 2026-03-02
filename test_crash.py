import pygame
import os
os.environ["SDL_VIDEODRIVER"] = "dummy"
from main import GameController

print("Init...")
g = GameController()
print("Preparing simulation...")
g.state = 5 # SIMULATION
g.prepare_simulation()
print("Drawing simulation...")
g.draw_simulation()
print("Success!")
