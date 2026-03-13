#include "creature.hpp"

Creature::Creature(
    Genome genome,
    NeuralNetwork net,
    Vector2 position)
{
    this->genome = genome;
    this->net = net;
    this->position = position;
    // init senses and actions
    for (size_t i = 1; i <= n_Senses; i++) {
        Senses.insert({ i, 0.f });
    }
    for (size_t i = n_Senses + 1; i <= n_Senses + n_Actions; i++) {
        Actions.insert({ i, 0.f });
    }
    fitness = 0.f;
    // init variables
    velocity = { 0.f, 0.f };
    toTarget = { 0.f, 0.f };
    targetDistance_x = 0.f;
    targetDistance_y = 0.f;
    targetVelocity = { 0.f, 0.f };
    targetHealthFraction = 1.f;
    // stats
    float roll = GenerateRandomFloatUniform(0.f, 1.f);
    if (roll < 0.2f) {
        isCarnivore = true;
        isHerbivore = false;
    }
    else {
        isHerbivore = true;
        isCarnivore = false;
    }
    //isHerbivore = genome.isHerbivore;
    //isCarnivore = genome.isCarnivore;
    healthStatFraction = genome.healthShare / (genome.healthShare + genome.attackShare + genome.speedShare);
    attackStatFraction = genome.attackShare / (genome.healthShare + genome.attackShare + genome.speedShare);
    speedStatFraction = genome.speedShare / (genome.healthShare + genome.attackShare + genome.speedShare);
    size = genome.size;
    color = genome.color;
    statPoints = 200.f;
    health_0 = statPoints * healthStatFraction;
    health = health_0;
    attackPower = 0.01f * statPoints * attackStatFraction;
    maxVelocity = (1.f + 2.f * speedStatFraction) * INITIAL_SIZE / size;
    satiation = 100.f;
    metabolicRate = 0.02f * std::pow(size, 0.75f);
    // init senses
    biasValue = genome.biasValue;
    counterOscillator = genome.counterOscillator;
    oscillatorFrequency = genome.oscillatorFrequency;
    oscillatorValue = genome.oscillatorValue;
    randomNoiseSeed = genome.randomNoiseSeed;
    counterRandomNoise = genome.counterRandomNoise;
    randomNoiseFrequency = genome.randomNoiseFrequency;
    randomNoiseValue = genome.randomNoiseValue;
}

Creature::Creature()
{

}

Creature::~Creature()
{

}

void Creature::UpdateSatiation()
{
    satiation -= metabolicRate;
}

void Creature::UpdateHunger()
{
    if (satiation <= 0.f) {
        satiation = 0.f;
        health -= 0.1;
    }
    else if (satiation >= 50.f) {
        health += 0.1f;
    }
}

void Creature::UpdateHealth()
{
    if (health > health_0) {
        health = health_0;
    }
}

void Creature::SetSatiationAdjustment(float satiationAdjustment)
{
    satiation += satiationAdjustment;
}

void Creature::SetHealthAdjustment(float healthAdjustment)
{
    health += healthAdjustment;
}

void Creature::ClampVelocity()
{
    if (Vector2Length(velocity) > MAX_VELOCITY) {
        velocity = Vector2Scale(Vector2Normalize(velocity), MAX_VELOCITY);
    }
    else if (Vector2Length(velocity) > maxVelocity) {
        velocity = Vector2Scale(Vector2Normalize(velocity), maxVelocity);
    }
}

void Creature::UpdateToTarget(Vector2 newToTarget)
{
    toTarget = Vector2Subtract(position, newToTarget);
}

void Creature::UpdateTargetVelocity(Vector2 newTargetVelocity)
{
    targetVelocity = newTargetVelocity;
}

void Creature::UpdateTargetHealthFraction(float newTargetHealthFraction)
{
    targetHealthFraction = newTargetHealthFraction;
}

void Creature::UpdateOscillator()
{
    oscillatorValue = std::sin(oscillatorFrequency * static_cast<float>(counterOscillator));
    counterOscillator++;
}

void Creature::UpdateRandomNoise()
{
    randomNoiseValue = noise.GetNoise(randomNoiseFrequency * static_cast<float>(counterRandomNoise) + randomNoiseSeed, 0.f);
    counterRandomNoise++;
}

void Creature::UpdateSenses()
{
    // normalising and clamping target distance in x and y calculation, can get math error if too far away and applying logistics function
    if (toTarget.x > -1000.f and toTarget.x < 1000.f) {
        targetDistance_x = 2.f / (1.f + std::exp(-2.f * (toTarget.x / 500.f))) - 1; // sigmoiding distance
    }
    else {
        targetDistance_x = 1.f;
    }
    if (toTarget.y > -1000.f and toTarget.y < 1000.f) {
        targetDistance_y = 2.f / (1.f + std::exp(-2.f * (toTarget.y / 500.f))) - 1; // sigmoiding distance
    }
    else {
        targetDistance_y = 1.f;
    }

    // update senses (this should happen after all alien variables are updated)
    Senses[SenseType(TARGET_HEALTH)] = targetHealthFraction;
    Senses[SenseType(TAGET_DISTANCE_X)] = targetDistance_x;
    Senses[SenseType(TAGET_DISTANCE_Y)] = targetDistance_y;
    Senses[SenseType(TARGET_VELOCITY_X)] = targetVelocity.x / MAX_VELOCITY;
    Senses[SenseType(TARGET_VELOCITY_Y)] = targetVelocity.y / MAX_VELOCITY;
    Senses[SenseType(SELF_HEALTH)] = health / health_0;
    Senses[SenseType(SELF_VELOCITY_X)] = velocity.x / MAX_VELOCITY;
    Senses[SenseType(SELF_VELOCITY_Y)] = velocity.y / MAX_VELOCITY;
    Senses[SenseType(BIAS)] = biasValue;
    Senses[SenseType(OSCILLATOR)] = oscillatorValue;
    Senses[SenseType(RANDOM_NOISE)] = randomNoiseValue;
}

void Creature::ExecuteActions()
{
    // calculate actions (this should happen after all senses are updated)
    Actions = net.Calculate(Senses);
    // find highest move action signal
    size_t idx_highestMoveAction = ActionType(MOVE_NORTH);
    float highestMoveAction = -1.f;
    for (auto& action : Actions) {
        // assuming move actions are in the sequential order: north, south, east, west
        if (action.first < ActionType(MOVE_NORTH) or action.first > ActionType(MOVE_WEST)) {
            continue;
        }
        if (action.second > highestMoveAction) {
            idx_highestMoveAction = action.first;
            highestMoveAction = action.second;
        }
    }
    // apply thrust in highest move action direction
    Vector2 powerVector = { 0.f, 0.f };
    if (idx_highestMoveAction == ActionType(MOVE_NORTH)) {
        powerVector = Vector2{ Actions[ActionType(ACTIVITY)] * 0.f, Actions[ActionType(ACTIVITY)] * -0.05f };
    }
    else if (idx_highestMoveAction == ActionType(MOVE_SOUTH)) {
        powerVector = Vector2{ Actions[ActionType(ACTIVITY)] * 0.f, Actions[ActionType(ACTIVITY)] * 0.05f };
    }
    else if (idx_highestMoveAction == ActionType(MOVE_EAST)) {
        powerVector = Vector2{ Actions[ActionType(ACTIVITY)] * 0.05f, Actions[ActionType(ACTIVITY)] * 0.f };
    }
    else if (idx_highestMoveAction == ActionType(MOVE_WEST)) {
        powerVector = Vector2{ Actions[ActionType(ACTIVITY)] * -0.05f, Actions[ActionType(ACTIVITY)] * 0.f };
    }
    velocity = Vector2Add(velocity, powerVector);
}

void Creature::Draw()
{
    //DrawTextureV(textureCircle, { position.x - size / 2.f, position.y - size / 2.f }, COLOR_HERBIVORE);
    //DrawTextureEx(textureCircle, { position.x - size / 2.f, position.y - size / 2.f }, 0.f, size, COLOR_HERBIVORE);

    if (isHerbivore) {
        DrawTexturePro(
            textureCircle,
            { 0.0f, 0.0f, static_cast<float>(textureCircle.width), static_cast<float>(textureCircle.height) },
            { position.x, position.y, size, size },
            { size / 2.f, size / 2.f },
            0.f,
            COLOR_HERBIVORE
        );
    }
    else if (isCarnivore) {
        DrawTexturePro(
            textureCircle,
            { 0.0f, 0.0f, static_cast<float>(textureCircle.width), static_cast<float>(textureCircle.height) },
            { position.x, position.y, size, size },
            { size / 2.f, size / 2.f },
            0.f,
            COLOR_CARNIVORE
        );
    }
}

void Creature::SetFitnessAdjustment(float fitnessAdjustment)
{
    fitness += fitnessAdjustment;
}

float Creature::GetFitness()
{
    return { fitness };
}

float Creature::GetHealth()
{
    return { health };
}

float Creature::GetHealthFraction()
{
    return { health / health_0 };
}

bool Creature::IsHerbivore()
{
    return { isHerbivore };
}

bool Creature::IsCarnivore()
{
    return { isCarnivore };
}

float Creature::GetAttackPower()
{
    return { attackPower };
}