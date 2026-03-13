#pragma once
#include "world.hpp"
#include "creature.hpp"
#include "evolutionManager.hpp"
#include "config.hpp"

class Sim {
    private:
        World world;
        int timeStep;
    public:
        Sim();
        ~Sim();
        void UpdateTimeStep();
        bool IsInChunkRadius(Vector2 position, int chunk_x_idx, int chunk_y_idx);
        void Update();
        void HandleCollisions();
        void UpdateTargets();
        void HandleInput();
        void Draw();
        std::vector<Creature> Creatures;
        EvolutionManager evolutionManager;
        bool exitWindowRequested;
};