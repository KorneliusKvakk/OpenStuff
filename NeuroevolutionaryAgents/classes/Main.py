# %%
from configNeuroevolutionaryAgents import *
from Sim import *

drawEnvironment = True
simShouldEnd = False

pygame.init()

sim = Sim()

while not simShouldEnd:
    sim.Update()

    if drawEnvironment:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                simShouldEnd = True
        sim.Draw()

if drawEnvironment:
    pygame.quit()
    
# %%
