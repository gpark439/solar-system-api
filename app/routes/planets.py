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

@planets_bp.route("/<planet_id>", methods=["GET"])
def get_one_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except ValueError:
        return jsonify({"message": f"Planet id: {planet_id} is invalid. Planet id must be an integer."}), 400

    chosen_planet = Planet.query.get(planet_id)

    if chosen_planet is None:
        return jsonify({"message": f"Planet with id: {planet_id} not found."}), 404

    return jsonify({
                "id" : chosen_planet.id,
                "name" : chosen_planet.name,
                "description": chosen_planet.description,
                "moons": chosen_planet.moons
            }
)

@planets_bp.route("/<planet_id>", methods=["PUT"])
def update_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except ValueError:
        return jsonify({"message": f"Planet id: {planet_id} is invalid. Planet id must be an integer."}), 400

    request_body = request.get_json()

    if "name" not in request_body or \
        "description" not in request_body or \
        "moons" not in request_body:
        return jsonify({"msg": f"Request must include name, description, and moons."}), 400
    
    chosen_planet = Planet.query.get(planet_id)

    if chosen_planet is None:
        return jsonify({"msg": f"Could not find planet with id {planet_id}"}), 404    

    chosen_planet.name = request_body["name"]
    chosen_planet.description = request_body["description"]
    chosen_planet.moons = request_body["moons"]

    db.session.commit()

    return jsonify({"msg": f"Successfully updated planet with id {planet_id}"})

@planets_bp.route("/<planet_id>", methods=["DELETE"])
def delete_one_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except ValueError:
        return jsonify({"message": f"Planet id: {planet_id} is invalid. Planet id must be an integer."}), 400
    
    chosen_planet = Planet.query.get(planet_id)

    if chosen_planet is None:
        return jsonify({"msg": f"Could not find planet with id {planet_id}"}), 404  

    db.session.delete(chosen_planet)
    db.session.commit()

    return jsonify({"msg": f"Successfully deleted planet with id {planet_id}"})