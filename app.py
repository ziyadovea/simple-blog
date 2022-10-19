from flask import Flask, render_template, request, redirect, url_for, Response, abort
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
        new_post: dict[str, str | None] = {
            'title': request.form['title'],  # required
            'author': request.form['author'],  # required
            'description': request.form.get('description'),  # optional
            'content': request.form['content'],  # required
        }
        db_posts.insert_one(new_post)
        return redirect(url_for('posts'))
    elif request.method == 'DELETE':
        db_posts.delete_many({})
    posts = db_posts.find()
    return render_template('posts.html', posts=posts)


@app.route('/posts/<path:post_id>', methods=['GET', 'PUT', 'DELETE'])
def post(post_id: str = '') -> str:
    if not ObjectId.is_valid(post_id):
        abort(404)
    query: dict[str, ObjectId] = {'_id': ObjectId(post_id)}
    if request.method == 'PUT':
        db_posts.update_one(query, {'$set': request.get_json()})
    elif request.method == 'DELETE':
        db_posts.delete_one(query)
    post = db_posts.find_one(query)
    return render_template('post.html', post=post)


if __name__ == '__main__':
    app.run()
