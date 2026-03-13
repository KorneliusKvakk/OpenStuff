#include "world.hpp"

World::World()
{
    GenerateChunks();
    while (Foods.size() < MAX_FOOD) {
        GenerateFood();
    }
}

World::~World()
{

}

void World::GenerateChunks()
{
    for (int x_idx = 0; x_idx < N_CHUNKS_X; x_idx++) {
        for (int y_idx = 0; y_idx < N_CHUNKS_Y; y_idx++) {
            Chunks.insert(Chunk(x_idx, y_idx));
        }
    }
}

void World::GenerateFood()
{
    Foods.push_back(Food());
}