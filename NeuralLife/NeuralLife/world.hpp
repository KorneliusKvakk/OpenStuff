#pragma once
#include "entity.hpp"
#include "config.hpp"

// chunk for calculating interactions
const struct Chunk {
	int x_idx; // x lowerrightcorner?
	int y_idx; // y lowerrightcorner?
	Chunk(int x_idx, int y_idx) {
		this->x_idx = x_idx;
		this->y_idx = y_idx;
	}
};
// define the equality comparison operator for asteroidchunk struct
bool operator==(const Chunk& lhs, const Chunk& rhs) {
	return lhs.x_idx == rhs.x_idx && lhs.y_idx == rhs.y_idx;
}
// hash function for asteroidMap hash table
namespace std {
	template <> struct hash<Chunk> {
		size_t operator()(const Chunk& s) const {
			hash<int> int_hash;
			size_t sx = int_hash(s.x_idx);
			size_t sy = int_hash(s.y_idx);
			return sx ^ (sy + 0x9e3779b9 + (sx << 6) + (sx >> 2));
		}
	};
};

const struct Food : public Entity {
	float health_0 = 50.f;
	float health = health_0;
	Food() {
		this->position = { GenerateRandomFloatUniform(0.f, static_cast<float>(SCREEN_WIDTH)), GenerateRandomFloatUniform(0.f, static_cast<float>(SCREEN_HEIGHT)) };
		this->velocity = { GenerateRandomFloatUniform(-MAX_FOOD_VELOCITY, MAX_FOOD_VELOCITY), GenerateRandomFloatUniform(-MAX_FOOD_VELOCITY, MAX_FOOD_VELOCITY) };
		this->size = 8.f;
		this->color = COLOR_FOOD;
	}
	void SetHealthAdjustment(float healthAdjustment) {
		health += healthAdjustment;
	}
	float GetHealth() {
		return { health };
	}
	float GetHealthFraction() {
		return { health / health_0 };
	}
	void Draw() {
		//DrawTextureV(textureCircle, { position.x - size / 2.f, position.y - size / 2.f }, COLOR_FOOD);
		//DrawTextureEx(textureCircle, { position.x - size / 2.f, position.y - size / 2.f }, 0.f, size, COLOR_FOOD);
		DrawTexturePro(
			textureCircle,
			{ 0.0f, 0.0f, static_cast<float>(textureCircle.width), static_cast<float>(textureCircle.height) },
			{ position.x, position.y, size, size },
			{ size / 2.f, size / 2.f },
			0.f,
			COLOR_FOOD
		);
	}
};

const class World {
	private:
	public:
		World();
		~World();
		std::unordered_set<Chunk> Chunks;
		std::vector<Food> Foods;
		void GenerateChunks();
		void GenerateFood();
};