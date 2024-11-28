from flask import Flask, jsonify, request
from http import HTTPStatus

from flask_cors import CORS
import os
import traceback

from domain.comment import Comment
from service.comment_service import CommentService
from service.user_service import UserService
from utils import Utils
from domain.trail_angel import TrailAngel
from domain.hiker import Hiker
from service.trail_angel_service import TrailAngelService
from service.hiker_service import HikerService
from data.database import Database
from domain.ride_post import RidePost
from service.ride_post_service import RidePostService
from domain.general_post import GeneralPost
from service.general_post_service import GeneralPostService
from service.post_service import PostService
from werkzeug.exceptions import BadRequest, NotFound

utils = Utils()
app = Flask(__name__)
CORS(app)


@app.errorhandler(Exception)
def handle(e):
    print(traceback.format_exc())
    return "Internal Server Error", HTTPStatus.INTERNAL_SERVER_ERROR


@app.errorhandler(BadRequest)
def handlebr(e):
    print(traceback.format_exc())
    return {"Message": e.description}, HTTPStatus.BAD_REQUEST


@app.errorhandler(NotFound)
def handlenf(e):
    print(traceback.format_exc())
    return {"Message": e.description}, HTTPStatus.NOT_FOUND

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
    ride_post_id = __get_id(request)
    ride_post = ride_post_service.get_ride_post(ride_post_id)
    return jsonify(ride_post.__dict__)


@app.delete("/ride_post")
def delete_ride_post():
    ride_post_id = __get_id(request)
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


@app.route("/hiker")
def get_hiker():
    id = __get_id(request)
    return hiker_service.get_hiker(id).__dict__, 200

# ===== TRAIL ANGELS =====


@app.route("/trailangels")
def get_trail_angels():

    angels = trail_angel_service.get_all_trail_angels()
    return utils.jsonify_list(angels)


@app.route("/trailangel")
def get_trail_angel_by_id():
    angel_id = __get_id(request)
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

# ===== COMMENTS =====


@app.post("/comment")
def create_comment():
    json = request.get_json()
    created_comment = comment_service.create_comment(Comment(**json))
    return created_comment.__dict__, 201


@app.route("/comments")
def get_comments():
    post_id = request.args.get("post_id")
    if not post_id:
        raise BadRequest("Missing post_id in URL")
    comments = comment_service.get_comments_for_post(post_id)
    return utils.jsonify_list(comments)

# ===== USERS =====


@app.route("/user")
def get_user():
    id = __get_id(request)
    return user_service.get_user(id).__dict__, 200


@app.post("/user_names")
def get_user_names():
    ids = request.get_json().get("ids")
    if ids == None:
        raise BadRequest("Missing ids in request body")
    return user_service.get_users_names(ids)


if __name__ == "__main__":
    db = Database("data/hiker_helper.db")

    trail_angel_service = TrailAngelService(db)
    hiker_service = HikerService(db)

    ride_post_service = RidePostService(db)
    general_post_service = GeneralPostService(db)
    post_service = PostService(db, ride_post_service, general_post_service)

    comment_service = CommentService(
        db,
        hiker_service,
        trail_angel_service,
        ride_post_service,
        general_post_service,
        post_service
    )

    user_service = UserService(
        db,
        trail_angel_service,
        hiker_service
    )

    db.setup()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
