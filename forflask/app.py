from flask import Flask, request, Response
from flask_restx import Resource, Api, fields
from flask import abort, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)

ns_movies = api.namespace('ns_movies', description='Movies APIs')

movie_data = api.model(
    'Movie Data',
    {
      "name": fields.String(description="movie name", required=True),
      "price": fields.Integer(description="movie price", required=True),
      "descript": fields.String(description="descript", required=True),
    }
)

movie_info = {}
number_of_movies = 0

@ns_movies.route('/movies')
class movies(Resource):
  def get(self):
    return {
        'number_of_movies': number_of_movies,
        'movie_info': movie_info
    }

@ns_movies.route('/movies/<string:name>')
class movies_name(Resource):
  # 영화 정보 조회
  def get(self, name):
    if not name in movie_info.keys():
      abort(404, description=f"Movie {name} doesn't exist")
    data = movie_info[name]

    return {
        'number_of_movies': len(data.keys()),
        'data': data
    }

  # 새로운 영화 생성
  @api.expect(movie_data) # body
  def post(self, name):
    if name in movie_info.keys():
      abort(404, description=f"Movie {name} already exists")

    params = request.get_json() # get body json
    movie_info[name] = params
    global number_of_movies
    number_of_movies += 1
  
    return Response(status=200)

  # 영화 정보 삭제
  def delete(self, name):
    if not name in movie_info.keys():
      abort(404, description=f"Movie {name} doesn't exists")
      
    del movie_info[name]
    number_of_movies -= 1
    return Response(status=200)

  # 영화 이름 변경
  @api.expect(movie_data)
  def put(self, name):
    global movie_info

    if not name in movie_info.keys():
      abort(404, description=f"Movie {name} doesn't exists")
    
    params = request.get_json()
    movie_info[name] = params
    
    return Response(status=200)
   
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=65432)
