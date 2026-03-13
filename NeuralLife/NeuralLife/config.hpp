#pragma once
#include "raylib.h"
#include "FastNoiseLite.hpp"

#include <unordered_set>
#include <algorithm>
#include <array>
#include <vector>
#include <map>
#include <string>
#include <cmath>
#include <random>
#include <thread>

// CODE FOMATTING
// map with enum key / struct data combination to contain static objects such as abilities
// vectors to contain dynamic objects such as projectiles
// size is diameter unless specified
// temperatures in kelvin
// velocity is typically world vector velocity, speed is typically movement speed of set paths / animations such as melee attacks
// velocityies in units per second
// one unit is one pixel in 3840x2160
// game scale factor is set to 1.f at 3840x2160
// time dependant variables scaled with frame time

/////////////// DEFINITIONS

#define main WinMain

std::thread thread_1;
std::thread thread_2;

FastNoiseLite noise;

Texture2D textureCircle;

/////////////// CONSTANTS

// sim
const int FPS = 6000;
const int SCREEN_WIDTH = 1000; //2560; // 1920; // 1728; // 3840
const int SCREEN_HEIGHT = 1000; // 1440; // 1080; // 972; // 2160

// world
const int CHUNK_SIZE = 200;
const int N_CHUNKS_X = SCREEN_WIDTH / CHUNK_SIZE;
const int N_CHUNKS_Y = SCREEN_HEIGHT / CHUNK_SIZE;
const int N_CHUNKS = N_CHUNKS_X * N_CHUNKS_Y;

// creatures
const int MAX_CREATURES = 500;
const int MAX_FOOD = 200;

const float INITIAL_SIZE = 12.f;
const float MAX_VELOCITY = 4.f;
const float MAX_FOOD_VELOCITY = 2.f;

const size_t maxNodeGenes = 40;
const float minConnectionWeight = -1.f;
const float maxConnectionWeight = 1.f;
//float mutationRate;
//float addNodeRate;
//float addConnectionRate;
const float mutationProbability = 0.8f;
const float perturbingProbability = 0.9f;
const float perturbingSigma = 0.1f;
const float perturbingRadius = 0.2f;
const float inheritDisabledGeneProbability = 0.75f;
const float c1 = 1.0f; // weight of excess and disjoint genes
const float c2 = 0.4f; // weight of average connection weight difference

// math
const float pi = 3.1415927f; // 3.141592653589793238462643383
const float phi = 1.6180340f; // 1.618033988749894848204586834
const float e = 2.7182818f; // 2.718281828459045235360287471
const float sqrt2 = 1.4142136f; // 1.414213562373095048801688724
const float sqrt3 = 1.7320508f; // 1.732050807568877293527446341
const float sqrt3_over2 = 0.8660254f; // 0.866025403784438646763723170
const float deg_to_rad = pi / 180.f;
const float rad_to_deg = 180.f / pi;

const enum NetworkNodeType {
	INPUT,
	HIDDEN,
	OUTPUT,
};

Color COLOR_BACKGROUND = { 255, 255, 204, 255 };
Color COLOR_FOOD = { 51, 204, 51, 255 };
Color COLOR_HERBIVORE = { 153, 102, 51, 255 };
Color COLOR_CARNIVORE = { 255, 51, 0, 255 };

// random number generator
std::random_device rd;
std::mt19937 rng(rd());

// generates a random integer between min_val (inclusive) and max_val (inclusive)
int GenerateRandomInt(int min_val, int max_val) {
	std::uniform_int_distribution<int> uni(min_val, max_val);
	return uni(rng);
}
// generates a random float between min_val (inclusive) and max_val (inclusive)
float GenerateRandomFloatUniform(float min_val, float max_val) {
	std::uniform_real_distribution<float> unif(min_val, max_val);
	return unif(rng);
}
// generates a random float according to a normal distribution with a mean value and a standard deviation (sigma)
float GenerateRandomFloatGaussian(float mean, float sigma) {
	std::normal_distribution<float> distribution(mean, sigma);
	return distribution(rng);
}
// round float to nearest integer that is a multiple of input multiple
int RoundToClosestMultiple(float input, int multiple) {
	return static_cast<int>(std::round(input / multiple) * multiple);
}
// clamp float between min and max float
float ClampFloat(float variable, float min_value, float max_value) {
	float output = variable;
	if (variable < min_value) {
		output = min_value;
	}
	else if (variable > max_value) {
		output = max_value;
	}
	return output;
}