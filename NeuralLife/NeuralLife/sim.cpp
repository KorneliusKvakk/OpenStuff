#include "sim.hpp"

Sim::Sim()
{
    //ToggleFullscreen();
    world = World();
    evolutionManager = EvolutionManager();
    while (Creatures.size() < MAX_CREATURES) {
        Creatures.push_back(evolutionManager.GenerateGenesisCreature());
    }
    timeStep = 0;
    exitWindowRequested = false;
}

Sim::~Sim()
{

}

void Sim::UpdateTimeStep()
{
    timeStep++;
}

bool Sim::IsInChunkRadius(Vector2 position, int chunk_x_idx, int chunk_y_idx)
{
    if (position.x >= static_cast<float>((chunk_x_idx - 1) * CHUNK_SIZE) and position.x < static_cast<float>(CHUNK_SIZE + (chunk_x_idx + 1) * CHUNK_SIZE)) {
        if (position.y >= static_cast<float>((chunk_y_idx - 1) * CHUNK_SIZE) and position.y < static_cast<float>(CHUNK_SIZE + (chunk_y_idx + 1) * CHUNK_SIZE)) {
            return { true };
        }
            
    }
        
    return { false };
}

void Sim::Update()
{
    // remove entities
    for (std::vector<Food>::iterator it = world.Foods.begin(); it != world.Foods.end();) {
        if (it->GetHealth() <= 0.f) {
            world.Foods.erase(it);
            break;
        }
        else { ++it; }
    }
    for (std::vector<Creature>::iterator it = Creatures.begin(); it != Creatures.end();) {
        if (it->GetHealth() <= 0.f) {
            Creatures.erase(it);
            break;
        }
        else { ++it; }
    }
    // update targets
    UpdateTargets();
    // update entities
    for (auto& food : world.Foods) {
        food.UpdatePosition();
        // clamp food position
        if (food.GetPosition().x < 0.f) {
            food.SetPositionX(static_cast<float>(SCREEN_WIDTH));
        }
        else if (food.GetPosition().x > static_cast<float>(SCREEN_WIDTH)) {
            food.SetPositionX(0.f);
        }
        if (food.GetPosition().y < 0.f) {
            food.SetPositionY(static_cast<float>(SCREEN_HEIGHT));
        }
        else if (food.GetPosition().y > static_cast<float>(SCREEN_HEIGHT)) {
            food.SetPositionY(0.f);
        }
    }
    for (auto& creature : Creatures) {
        creature.UpdatePosition();
        // clamp food position
        if (creature.GetPosition().x < 0.f) {
            creature.SetPositionX(static_cast<float>(SCREEN_WIDTH));
        }
        else if (creature.GetPosition().x > static_cast<float>(SCREEN_WIDTH)) {
            creature.SetPositionX(0.f);
        }
        if (creature.GetPosition().y < 0.f) {
            creature.SetPositionY(static_cast<float>(SCREEN_HEIGHT));
        }
        else if (creature.GetPosition().y > static_cast<float>(SCREEN_HEIGHT)) {
            creature.SetPositionY(0.f);
        }
        creature.UpdateSatiation();
        creature.UpdateHunger();
        creature.UpdateHealth();
        creature.UpdateOscillator();
        creature.UpdateRandomNoise();
        creature.UpdateSenses();
        creature.ExecuteActions();
        creature.ClampVelocity();
    }
    // handle collisions
    HandleCollisions();
    // add entities
    if (world.Foods.size() < MAX_FOOD) {
        world.GenerateFood();
    }
    if (Creatures.size() < MAX_FOOD) {
        Creatures.push_back(evolutionManager.GenerateGenesisCreature());
    }
    UpdateTimeStep();
}

void Sim::HandleCollisions()
{
    for (auto& chunk : world.Chunks) {
        int idx_creatureAggressor = 0;
        for (auto& creatureAggressor : Creatures) {
            if (IsInChunkRadius(creatureAggressor.GetPosition(), chunk.x_idx, chunk.y_idx)) {
                if (creatureAggressor.IsHerbivore()) {
                    for (auto& food : world.Foods) {
                        if (IsInChunkRadius(food.GetPosition(), chunk.x_idx, chunk.y_idx)) {
                            if (CheckCollisionCircles(creatureAggressor.GetPosition(), creatureAggressor.GetSize() / 2.f, food.GetPosition(), food.GetSize() / 2.f)) {
                                creatureAggressor.SetSatiationAdjustment(+1.f * creatureAggressor.GetAttackPower());
                                food.SetHealthAdjustment(-1.f * creatureAggressor.GetAttackPower());
                                creatureAggressor.SetFitnessAdjustment(+1.f);
                            }
                        }
                    }
                }
                else if (creatureAggressor.IsCarnivore()) {
                    int idx_creatureTarget = 0;
                    for (auto& creatureTarget : Creatures) {
                        if (idx_creatureAggressor == idx_creatureTarget) {
                            idx_creatureTarget++;
                            continue;
                        }
                        if (IsInChunkRadius(creatureTarget.GetPosition(), chunk.x_idx, chunk.y_idx)) {
                            if (CheckCollisionCircles(creatureAggressor.GetPosition(), creatureAggressor.GetSize() / 2.f, creatureTarget.GetPosition(), creatureTarget.GetSize() / 2.f)) {
                                if (creatureTarget.IsHerbivore()) {
                                    creatureAggressor.SetSatiationAdjustment(+1.f * creatureAggressor.GetAttackPower());
                                    creatureTarget.SetHealthAdjustment(-1.f * creatureAggressor.GetAttackPower());
                                    creatureAggressor.SetHealthAdjustment(-0.2f * creatureTarget.GetAttackPower());
                                    creatureAggressor.SetFitnessAdjustment(+1.f);
                                    creatureTarget.SetFitnessAdjustment(-1.f);
                                }
                            }
                        }
                        idx_creatureTarget++;
                    }

                }
            }
            idx_creatureAggressor++;
        }
    }
}

void Sim::UpdateTargets()
{
    for (auto& chunk : world.Chunks) {
        int idx_creatureAggressor = 0;
        for (auto& creatureAggressor : Creatures) {
            if (IsInChunkRadius(creatureAggressor.GetPosition(), chunk.x_idx, chunk.y_idx)) {
                if (creatureAggressor.IsHerbivore()) {
                    float distanceToClosestFood = 2000.f;
                    float newDistanceToClosestFood = distanceToClosestFood;
                    int idx_food = 0;
                    int idx_closestFood = 0;
                    for (auto& food : world.Foods) {
                        if (IsInChunkRadius(food.GetPosition(), chunk.x_idx, chunk.y_idx)) {
                            newDistanceToClosestFood = Vector2Length(Vector2Subtract(food.GetPosition(), creatureAggressor.GetPosition()));
                            if (newDistanceToClosestFood < distanceToClosestFood) {
                                distanceToClosestFood = newDistanceToClosestFood;
                                idx_closestFood = idx_food;
                            }
                        }
                        idx_food++;
                    }
                    creatureAggressor.UpdateToTarget(world.Foods.at(idx_closestFood).GetPosition());
                    creatureAggressor.UpdateTargetVelocity(world.Foods.at(idx_closestFood).GetVelocity());
                    creatureAggressor.UpdateTargetHealthFraction(world.Foods.at(idx_closestFood).GetHealthFraction());
                }
                else if (creatureAggressor.IsCarnivore()) {
                    float distanceToClosestCreatureTarget = 2000.f;
                    float newDistanceToClosestCreatureTarget = distanceToClosestCreatureTarget;
                    int idx_creatureTarget = 0;
                    int idx_closestCreatureTarget = 0;
                    for (auto& creatureTarget : Creatures) {
                        if (idx_creatureAggressor == idx_creatureTarget) {
                            idx_creatureTarget++;
                            continue;
                        }
                        if (IsInChunkRadius(creatureTarget.GetPosition(), chunk.x_idx, chunk.y_idx)) {
                            if (creatureTarget.IsHerbivore()) {
                                newDistanceToClosestCreatureTarget = Vector2Length(Vector2Subtract(creatureTarget.GetPosition(), creatureAggressor.GetPosition()));
                                if (newDistanceToClosestCreatureTarget < distanceToClosestCreatureTarget) {
                                    distanceToClosestCreatureTarget = newDistanceToClosestCreatureTarget;
                                    idx_closestCreatureTarget = idx_creatureTarget;
                                }
                            }
                        }
                        idx_creatureTarget++;
                    }
                    creatureAggressor.UpdateToTarget(Creatures.at(idx_closestCreatureTarget).GetPosition());
                    creatureAggressor.UpdateTargetVelocity(Creatures.at(idx_closestCreatureTarget).GetVelocity());
                    creatureAggressor.UpdateTargetHealthFraction(Creatures.at(idx_closestCreatureTarget).GetHealthFraction());
                }
            }
            idx_creatureAggressor++;
        }
    }
}

void Sim::HandleInput()
{
    if (IsKeyPressed(KEY_ESCAPE))
    {
        exitWindowRequested = true;
    }
}

void Sim::Draw()
{
    BeginDrawing();
    ClearBackground(COLOR_BACKGROUND);
    for (auto& food : world.Foods) {
        food.Draw();
    }
    for (auto& creature : Creatures) {
        creature.Draw();
    }
    DrawFPS(20, 20);
    EndDrawing();
}