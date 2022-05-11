from flask import Blueprint, jsonify, make_response, request, abort
from app import db
from app.models.planets import Planet

planets_bp = Blueprint("planets", __name__, url_prefix = "/planets")

# Create planet
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

# Get all planets
@planets_bp.route("", methods=["GET"])
def get_all_planets():
    response_body = []
    params = request.args
    if "name" in params and "moons" in params:
        planets = Planet.query.filter_by(name=params["name"], moons=params["moons"])
    elif "name" in params:
        planets = Planet.query.filter_by(name=params["name"])
    elif "moons" in params:
        planets = Planet.query.filter_by(moons=params["moons"])
    else:
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

# Helper function to validate input for get_one_planet
def get_planet_or_abort(planet_id):
    try:
        planet_id = int(planet_id)
    except:
        abort(make_response(jsonify({'msg': f"Invalid driver id: '{planet_id}'. ID must be an integer"}), 400))

    planet = Planet.query.get(planet_id)

    if planet is None:
        abort(make_response(jsonify({"message": f"Planet with id: {planet_id} not found."}), 404))

    return planet


@planets_bp.route("/<planet_id>", methods=["GET"])
def get_one_planet(planet_id):
    planet = get_planet_or_abort(planet_id)

    return jsonify({
                "id" : planet.id,
                "name" : planet.name,
                "description": planet.description,
                "moons": planet.moons
            }
), 200

# Update one planet
@planets_bp.route("/<planet_id>", methods=["PUT"])
def update_planet(planet_id):

    request_body = request.get_json()

    if "name" not in request_body or \
        "description" not in request_body or \
        "moons" not in request_body:
        return jsonify({"msg": f"Request must include name, description, and moons."}), 400
    
    chosen_planet = get_planet_or_abort(planet_id)

    chosen_planet.name = request_body["name"]
    chosen_planet.description = request_body["description"]
    chosen_planet.moons = request_body["moons"]

    db.session.commit()

    return jsonify({"msg": f"Successfully updated planet with id {planet_id}"})

# Delete one planet
@planets_bp.route("/<planet_id>", methods=["DELETE"])
def delete_one_planet(planet_id):
    chosen_planet = get_planet_or_abort(planet_id)

    db.session.delete(chosen_planet)
    db.session.commit()

    return jsonify({"msg": f"Successfully deleted planet with id {planet_id}"})