from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from Utils import Utils
from TrailAngel import TrailAngel
from Hiker import Hiker
from TrailAngelService import TrailAngelService
from HikerService import HikerService
from data.database import Database
from Post import Post
from PostService import PostService

utils = Utils()
app = Flask(__name__)
CORS(app)

# ===== POSTS =====

@app.post("/post")
def create_post():
    json = request.get_json()
    parsed_post = Post(**json)
    created_post = post_service.create_post(parsed_post)
    return jsonify(created_post.__dict__)

@app.route("/posts")
def get_posts():
    posts = post_service.get_posts()
    return utils.jsonify_list(posts)

@app.route("/post")
def get_post():

    post_id = None
    try:
        post_id = request.args["id"]
    except Exception:
        return jsonify("Missing id")

    post = post_service.get_post(post_id)
    return jsonify(post.__dict__)

@app.delete("/post")
def delete_post():
    post_id = None
    try:
        post_id = request.args["id"]
    except Exception:
        return ({"Message": "Missing ID"}, 400)

    post_service.delete_post(post_id)
    return ("", 204)

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


if __name__ == "__main__":
    db = Database("data/hiker_helper.db")
    trail_angel_service = TrailAngelService(db)
    hiker_service = HikerService(db)
    post_service = PostService(db)

    db.setup()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
