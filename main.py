from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# A Model to store Videos
class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    # method to allow valid return value (string representation) on 'print()'
    def __repr__(self):
        return f"Video(name = {name}, views = {views}, likes = {likes})"

# determines if a request meets any of the requirements to either be allowed or denied to "create video"
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True) # requirement 1
video_put_args.add_argument("views", type=int, help="Views of the video", required=True) # requirement 2
video_put_args.add_argument("likes", type=int, help="Likes on the video", required=True) # requirement 3

# determines if a request meets any of the requirements to either be allowed or denied to "update video"
video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video is required") # requirement 1
video_update_args.add_argument("views", type=int, help="Views of the video") # requirement 2
video_update_args.add_argument("likes", type=int, help="Likes on the video") # requirement 3

# define the fields from the VideoModel Class
resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}

# Create Resource
class Video(Resource):
    # returns an object of an instance from 'VideoModel Class'
    @marshal_with(resource_fields) # serializes return object using fields
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Could not find video with that id")
        return result
    # create new video
    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="Video id taken...")
        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video) # adds object into current database session
        db.session.commit() # finalize add method
        return video, 201 # video successfully created
    # update video
    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video doesn't exist, cannot update")
        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']
        db.session.commit()
        return result
    # delete video
    def delete(self, video_id):
        del videos[video_id]
        return '', 204 # video successfully deleted

# Register Resource (Class, "API Endpoint/<parameter>")
api.add_resource(Video, "/video/<int:video_id>")

if __name__=="__main__":
    app.run(debug=True)