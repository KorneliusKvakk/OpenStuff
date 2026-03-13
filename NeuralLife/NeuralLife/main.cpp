// hpp
#include "evolutionManager.hpp"
#include "sim.hpp"
#include "world.hpp"
#include "entity.hpp"
#include "creature.hpp"
#include "genome.hpp"
#include "neuralNetwork.hpp"
#include "neuron.hpp"
#include "config.hpp"
// cpp
#include "evolutionManager.cpp"
#include "sim.cpp"
#include "world.cpp"
#include "entity.cpp"
#include "creature.cpp"
#include "genome.cpp"
#include "neuralNetwork.cpp"
#include "neuron.cpp"

int main()
{
	InitWindow(SCREEN_WIDTH, SCREEN_HEIGHT, "Neural Life");
	//SetExitKey(KEY_NULL);

	// sim
	Sim sim;
	SetTargetFPS(FPS);
	noise.SetNoiseType(FastNoiseLite::NoiseType_OpenSimplex2);

	textureCircle = LoadTexture("assets/whiteCircle.png");

	bool exitWindow = false; // Flag to set window to exit

	// game loop
	while (exitWindow == false)
	{
		// event handling
		sim.HandleInput();
		// update state
		sim.Update();
		// draw
		sim.Draw();
		// exit game
		if (sim.exitWindowRequested) { exitWindow = true; }
	}
}