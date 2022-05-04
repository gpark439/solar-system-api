import pytest
from app.models.planets import *
from app.routes.planets import *

def test_get_planets_returns_status_200_and_empty_array():
    # arrange


    # act

    result = get_all_planets()

    # assert

    assert result == 0


# GET /planets/1 returns a response body that matches our fixture

def test_get_planets_1_returns_status_200_and_response_body():
    # arrange
    planet_id = 1

    # act
    result = get_one_planet(planet_id)

    # assert
    assert result == {
    "description": "Smallest planet in the solar system",
    "id": 1,
    "moons": 0,
    "name": "Mercury"
}



# GET /planets/1 with no data in test database (no fixture) returns a 404



# GET /planets with valid test data (fixtures) returns a 200 with an array including appropriate test data



# POST /planets with a JSON request body returns a 201