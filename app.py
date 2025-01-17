from flask import Flask, jsonify, request
from http import HTTPStatus

from flask_cors import CORS
import os
import traceback

from domain.comment import Comment
from utils import Utils
from domain.user import User
from data.database import Database
from domain.post import Post
from service.post_service import PostService
from service.comment_service import CommentService
from service.user_service import UserService
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

# ===== POSTS =====


@app.post("/post")
def create_post():
    json = request.get_json()
    parsed_post = Post.from_json(json)
    created_post = post_service.create_post(parsed_post)
    return created_post.__dict__, HTTPStatus.CREATED


@app.route("/posts")
def get_posts():
    posts = post_service.get_posts()
    return utils.jsonify_list(posts)


@app.route("/post")
def get_post():
    post_id = __get_id(request)

    post = post_service.get_post(post_id)
    return jsonify(post.__dict__)


# ===== USERS =====


@app.post("/user")
def create_user():
    r_json = request.get_json()
    parsed = User(**r_json)
    created_user = user_service.create_user(parsed)
    return jsonify(created_user.__dict__)


@app.route("/users")
def get_users():
    users = user_service.get_all_users()
    return utils.jsonify_list(users)


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

def __get_id(request):
    try:
        return request.args["id"]
    except Exception:
        raise BadRequest("Missing [id]")

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


db = Database("data/hiker_helper.db")
db.setup()

user_service = UserService(db)

post_service = PostService(db)

comment_service = CommentService(
    db,
    user_service,
    post_service
)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
