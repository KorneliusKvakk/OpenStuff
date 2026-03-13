#pragma once
#include "config.hpp"

const class Entity {
    protected:
	    Vector2 position;
	    Vector2 velocity;
	    float size;
	    Color color;
    public:
	    Entity(Vector2 initialPosition);
		Entity();
	    ~Entity();
	    virtual void UpdatePosition();
		void SetPositionX(float newPositionX);
		void SetPositionY(float newPositionY);
	    Vector2 GetPosition();
	    Vector2 GetVelocity();
	    float GetSize();
	    Color GetColor();
};