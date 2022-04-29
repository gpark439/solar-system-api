from flask import Blueprint, jsonify, make_response, request
from app import db
from app.models.planets import Planet

planets_bp = Blueprint("planets", __name__, url_prefix = "/planets")

@planets_bp.route("", methods=["POST"])
def create_planet():
    request_body = request.get_json()

    new_planet = Planet(
        name = request_body["name"],
        description = request_body["description"],
        moons = request_body["moons"]
    )
    
    db.session.add(new_planet)
    db.session.commit()

    return make_response(f"Planet {new_planet.name} with id {new_planet.id} successfully created", 201)

@planets_bp.route("", methods=["GET"])
def get_all_planets():
    response_body = []
    planets = Planet.query.all()
    for planet in planets:
        response_body.append(
            {
                "id" : planet.id,
                "name" : planet.name,
                "description": planet.description,
                "moons": planet.moons
            })
    return jsonify(response_body)

# @planets_bp.route("/<planet_id>", methods=["GET"])
# def get_one_planet(planet_id):
#     try:
#         planet_id = int(planet_id)
#     except ValueError:
#         return jsonify({"message": f"Planet id: {planet_id} is invalid. Planet id must be an integer."}), 400

#     chosen_planet = None
#     for planet in planets:
#         if planet.id == planet_id:
#             chosen_planet = {
#                 "id" : planet.id,
#                 "name" : planet.name,
#                 "description": planet.description,
#                 "moons": planet.moons
#             }

#     if chosen_planet is None:
#         return jsonify({"message": f"Planet with id: {planet_id} not found."}), 404

#     return jsonify(chosen_planet)
