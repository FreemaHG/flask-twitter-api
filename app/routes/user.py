from flask_restful import Api, Resource

from app import create_app

app = create_app()
api = Api(app)


class Hello(Resource):
    def get(self):
        return {'data': 'Hello, World!'}, 200


api.add_resource(Hello, '/hello', endpoint='hello')


if __name__ == '__main__':
    app.run(debug=True)
