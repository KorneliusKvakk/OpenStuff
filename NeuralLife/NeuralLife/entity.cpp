#include "entity.hpp"

Entity::Entity(Vector2 initialPosition)
{
    position = initialPosition;
    velocity = { 0.f, 0.f };
    size = 0.f;
    color = { 0, 0, 0, 0 };
}

Entity::Entity()
{
    position = { 0.f, 0.f };
    velocity = { 0.f, 0.f };
    size = 0.f;
    color = { 0, 0, 0, 0 };
}

Entity::~Entity()
{

}

void Entity::UpdatePosition()
{
    // update entity position
    position = Vector2Add(position, velocity);
}

void Entity::SetPositionX(float newPositionX)
{
    position.x = newPositionX;
}

void Entity::SetPositionY(float newPositionY)
{
    position.y = newPositionY;
}

Vector2 Entity::GetPosition()
{
    return { position };
}

Vector2 Entity::GetVelocity()
{
    return { velocity };
}

float Entity::GetSize()
{
    return { size };
}

Color Entity::GetColor()
{
    return { color };
}