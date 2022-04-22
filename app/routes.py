from flask import Blueprint, jsonify

# Define a Planet class with the attributes id, name, description, and moons
class Planet:
    def __init__(self, id, name, description, moons):
        self.id = id
        self.name = name
        self.description = description
        self.moons = moons

# Create a list of Planet instances
planets = [
    Planet(1, "Mercury", "Smallest planet in the solar system", 0),
    Planet(2, "Venus", "Hottest planet in the solar system", 0),
    Planet(3, "Earth", "Planet we live on!", 1),
    Planet(4, "Mars", "The most visited planet", 2),
    Planet(5, "Jupiter", "Largest planet in the solar system", 79),
    Planet(6, "Saturn", "Most moons of all the planets", 82),
    Planet(7, "Uranus", "Only visited once", 27),
    Planet(8, "Neptune", "Most distant planet from the Sun", 14)
]

planets_bp = Blueprint("planets", __name__)

@planets_bp.route("/planets", methods=["GET"])
def get_all_planets():
    response_body = []
    for planet in planets:
        response_body.append(
            {
                "id" : planet.id,
                "name" : planet.name,
                "description": planet.description,
                "moons": planet.moons
            })
    return jsonify(response_body)