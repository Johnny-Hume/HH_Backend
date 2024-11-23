from flask import Flask, jsonify, request
from http import HTTPStatus

from flask_cors import CORS
import os
import traceback
from Utils import Utils
from TrailAngel import TrailAngel
from Hiker import Hiker
from TrailAngelService import TrailAngelService
from HikerService import HikerService
from data.database import Database
from RidePost import RidePost
from RidePostService import RidePostService
from GeneralPost import GeneralPost
from GeneralPostService import GeneralPostService
from PostService import PostService

utils = Utils()
app = Flask(__name__)
CORS(app)

@app.errorhandler(Exception)
def handle(e):
    print(traceback.format_exc())
    return "Internal Server Error", HTTPStatus.INTERNAL_SERVER_ERROR

# ===== GENERALPOSTS =====

@app.post("/general_post")
def create_general_post():
    json = request.get_json()
    parsed_post = GeneralPost(**json)
    created_post = general_post_service.create_general_post(parsed_post)
    return created_post.__dict__, HTTPStatus.CREATED

@app.route("/general_posts")
def get_general_posts():
    general_posts = general_post_service.get_general_posts()
    return utils.jsonify_list(general_posts)

@app.route("/general_post")
def get_general_post():
    general_post_id = __get_id(request)

    general_post = general_post_service.get_general_post(general_post_id)
    return jsonify(general_post.__dict__)

# ===== RIDE POSTS =====

@app.post("/ride_post")
def create_ride_post():
    json = request.get_json()
    parsed_ride_post = RidePost(**json)
    created_ride_post = ride_post_service.create_ride_post(parsed_ride_post)
    return created_ride_post.__dict__, HTTPStatus.CREATED

@app.route("/ride_posts")
def get_ride_posts():
    ride_posts = ride_post_service.get_ride_posts()
    return utils.jsonify_list(ride_posts)

@app.route("/ride_post")
def get_ride_post():

    ride_post_id = None
    try:
        ride_post_id = request.args["id"]
    except Exception:
        return jsonify("Missing id")

    ride_post = ride_post_service.get_ride_post(ride_post_id)
    return jsonify(ride_post.__dict__)

@app.delete("/ride_post")
def delete_ride_post():
    ride_post_id = None
    try:
        ride_post_id = request.args["id"]
    except Exception:
        return ({"Message": "Missing ID"}, 400)

    ride_post_service.delete_ride_post(ride_post_id)
    return ("", 204)

# ===== POSTS =====
@app.route("/posts")
def get_all_posts():
    posts = post_service.get_all_posts()
    return utils.jsonify_list(posts)

# ===== HIKERS =====

@app.post("/hiker")
def create_hiker():
    r_json = request.get_json()
    parsed_hiker = Hiker(**r_json)
    created_hiker = hiker_service.create_hiker(parsed_hiker)
    return jsonify(created_hiker.__dict__)


@app.route("/hikers")
def get_hikers():
    hikers = hiker_service.get_all_hikers()
    return utils.jsonify_list(hikers)


# ===== TRAIL ANGELS =====


@app.route("/trailangels")
def get_trail_angels():

    angels = trail_angel_service.get_all_trail_angels()
    return utils.jsonify_list(angels)


@app.route("/trailangel")
def get_trail_angel_by_id():

    angel_id = None
    try:
        angel_id = request.args["id"]
    except Exception:
        return jsonify("Missing id")

    angel = trail_angel_service.get_trail_angel(angel_id)
    return jsonify(angel.__dict__)


@app.post("/trailangel")
def create_trail_angel():
    json = request.get_json()
    created_angel = trail_angel_service.create_trail_angel(TrailAngel(**json))
    return jsonify(created_angel.__dict__)

def __get_id(request):
    try:
        return request.args["id"]
    except Exception:
        raise exceptions.BadRequest("Missing [id]")

if __name__ == "__main__":
    db = Database("data/hiker_helper.db")

    trail_angel_service = TrailAngelService(db)
    hiker_service = HikerService(db)

    ride_post_service = RidePostService(db)
    general_post_service = GeneralPostService(db)
    post_service = PostService(ride_post_service, general_post_service)

    db.setup()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
