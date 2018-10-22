from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.TEXT, unique=True)
    text = db.Column(db.TEXT)
    image = db.Column(db.TEXT)
    detail_text = db.Column(db.TEXT)


    def __init__(self, title, text, image, detail_text):
        self.image = image
        self.text = text
        self.detail_text = detail_text
        self.title = title


class Tips(db.Model):
    __tablename__ = 'tips'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.TEXT, unique=True)
    text = db.Column(db.TEXT)
    image = db.Column(db.TEXT)

    def __init__(self, title, text, image):
        self.text = text
        self.title = title
        self.image = image


class Videos(db.Model):
    __tablename__ = 'videos'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.TEXT, unique=True)
    text = db.Column(db.TEXT)
    videoId = db.Column(db.TEXT)

    def __init__(self, title, text, videoid):
        self.title = title
        self.text = text
        self.videoId = videoid


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        #fields = ('id','title', 'text')
        fields = ('id', 'title', 'text', 'image')


class NewsDetailSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'title', 'text', 'image','detail_text')


class VideosSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'title', 'text', 'videoId')


new_detail_schema = NewsDetailSchema()
news_detail_schema = NewsDetailSchema(many=True)


user_schema = UserSchema()
users_schema = UserSchema(many=True)


video_schema = VideosSchema()
videos_schema = VideosSchema(many=True)


# endpoint to create new user
@app.route("/news", methods=["POST"])
def add_news():
    __tablename__ = 'news'
    title = request.json['title']
    text = request.json['text']
    image = request.json['image']
    detail_text = request.json['detail_text']

    new_news = News(title, text, image, detail_text)

    db.session.add(new_news)
    db.session.commit()

    return user_schema.jsonify(new_news)


@app.route("/tips", methods=["POST"])
def add_tips():
    __tablename__ = 'tips'
    title = request.json['title']
    text = request.json['text']
    image = request.json['image']

    new_tip = Tips(title, text, image)

    db.session.add(new_tip)
    db.session.commit()

    return user_schema.jsonify(new_tip)


# endpoint to show all users
@app.route("/tips", methods=["GET"])
def get_tips():
    all_users = Tips.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result.data)


@app.route("/news", methods=["GET"])
def get_news():
    all_users = News.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result.data)


@app.route("/videos", methods=["GET"])
def get_videos():
    all_users = Videos.query.all()
    result = videos_schema.dump(all_users)
    return jsonify(result.data)


@app.route("/", methods=["GET"])
def get():
    return "Hello world"


# endpoint to get user detail by id
@app.route("/news/<id>", methods=["GET"])
def news_detail(id):
    news_d = News.query.get(id)
    return new_detail_schema.jsonify(news_d)


# endpoint to update user
# @app.route("/user/<id>", methods=["PUT"])
# def user_update(id):
#     user = User.query.get(id)
#     username = request.json['username']
#     email = request.json['email']
#
#     user.email = email
#     user.username = username
#
#     db.session.commit()
#     return user_schema.jsonify(user)


# endpoint to delete user
@app.route("/tips/<id>", methods=["DELETE"])
def tip_delete(id):
    tip = Tips.query.get(id)
    db.session.delete(tip)
    db.session.commit()

    return user_schema.jsonify(tip)


if __name__ == '__main__':
    #app.run(debug=True)
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
