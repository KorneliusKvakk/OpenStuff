#pragma once
#include "neuralNetwork.hpp"
#include "entity.hpp"
#include "config.hpp"

const enum SenseType {
	BIAS = 1, // constant bias input, constant float between -1 and 1
	OSCILLATOR = 2, // oscillator value (-1, 1)
	RANDOM_NOISE = 3, // random noise value according to simplexnoise (-1, 1)
	TARGET_HEALTH = 4, // fraction target health value (0, 1)
	TAGET_DISTANCE_X = 5, // distance to target x (-1, 1)
	TAGET_DISTANCE_Y = 6, // distance to target y (-1, 1)
	TARGET_VELOCITY_X = 7, // target velocity x (-1, 1)
	TARGET_VELOCITY_Y = 8, // target velocity y (-1, 1)
	SELF_HEALTH = 9, // fraction self health value (0, 1)
	SELF_VELOCITY_X = 10, // self velocity x (-1, 1)
	SELF_VELOCITY_Y = 11, // self velocity y (-1, 1)
};
size_t n_Senses = 11;

const enum ActionType {
	MOVE_NORTH = 12, // move in positive y direction (0, 1)
	MOVE_SOUTH = 13, // move in negative y direction (0, 1)
	MOVE_EAST = 14, // move in positive x direction (0, 1)
	MOVE_WEST = 15, // move in negative x direction (0, 1)
	ACTIVITY = 16, // activity level (0, 1)
};
size_t n_Actions = 5;

const class Creature : public Entity {
	private:
		Genome genome;
		NeuralNetwork net;
		std::map<size_t, float> Senses;
		std::map<size_t, float> Actions;
		float fitness;
		// target
		Vector2 toTarget;
		float targetDistance_x;
		float targetDistance_y;
		Vector2 targetVelocity;
		float targetHealthFraction;
		// stats from genome
		float statPoints;
		bool isHerbivore;
		bool isCarnivore;
		float healthStatFraction;
		float attackStatFraction;
		float speedStatFraction;
		float attackPower;
		float satiation;
		float metabolicRate;
		float health_0;
		float health;
		float maxVelocity;
		// senses
		float biasValue;
		float counterOscillator;
		float oscillatorFrequency;
		float oscillatorValue;
		float randomNoiseSeed;
		float counterRandomNoise;
		float randomNoiseFrequency;
		float randomNoiseValue;
	public:
		Creature(
			Genome genome,
			NeuralNetwork net,
			Vector2 position);
		Creature();
		~Creature();
		void UpdateSatiation();
		void UpdateHunger();
		void UpdateHealth();
		void SetSatiationAdjustment(float satiationAdjustment);
		void SetHealthAdjustment(float healthAdjustment);
		void ClampVelocity();
		void UpdateToTarget(Vector2 newToTarget);
		void UpdateTargetVelocity(Vector2 newTargetVelocity);
		void UpdateTargetHealthFraction(float newTargetHealthFraction);
		void UpdateOscillator();
		void UpdateRandomNoise();
		void UpdateSenses();
		void ExecuteActions();
		void Draw();
		void SetFitnessAdjustment(float fitnessAdjustment);
		float GetFitness();
		float GetHealth();
		float GetHealthFraction();
		bool IsHerbivore();
		bool IsCarnivore();
		float GetAttackPower();
};