from flask import Flask, render_template, request, redirect, url_for, Response, abort, jsonify, make_response
from pymongo import MongoClient
from bson import ObjectId

import config

app = Flask(__name__, template_folder='templates')
mongodb_client = MongoClient(config.DB_URI)
mongo_db = mongodb_client.blog_db
db_posts = mongo_db.posts


@app.route('/', methods=['GET'])
def index() -> str:
    return render_template('index.html')


@app.route('/posts', methods=['GET', 'POST', 'DELETE'])
def posts() -> str | Response:
    if request.method == 'POST':
        db_posts.insert_one(request.get_json())
        return make_response(jsonify({'message': 'Created', 'code': 'SUCCESS'}), 201)
    elif request.method == 'DELETE':
        db_posts.delete_many({})
        return make_response(jsonify({'message': 'Deleted', 'code': 'SUCCESS'}), 200)
    posts = db_posts.find()
    return render_template('posts.html', posts=posts)


@app.route('/posts/<path:post_id>', methods=['GET', 'PUT', 'DELETE'])
def post(post_id: str = '') -> str | Response:
    if not ObjectId.is_valid(post_id):
        abort(404)
    query: dict[str, ObjectId] = {'_id': ObjectId(post_id)}
    if request.method == 'PUT':
        db_posts.update_one(query, {'$set': request.get_json()})
        return make_response(jsonify({'message': 'Updated', 'code': 'SUCCESS'}), 200)
    elif request.method == 'DELETE':
        db_posts.delete_one(query)
        return make_response(jsonify({'message': 'Deleted', 'code': 'SUCCESS'}), 200)
    post = db_posts.find_one(query)
    return render_template('post.html', post=post)


if __name__ == '__main__':
    app.run()
