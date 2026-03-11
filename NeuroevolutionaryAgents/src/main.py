# %%
from configNeuroevolutionaryAgents import *
from sim import *

drawEnvironment = True

simShouldEnd = False

pygame.init()

sim = Sim()
sim.Initialize()

while not simShouldEnd:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            simShouldEnd = True

    sim.Update()

    if drawEnvironment:
        sim.Draw()

if drawEnvironment:
    pygame.quit()

# %%
