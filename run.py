import os
import json
import flask
import requests

from flask_restful import Api, Resource

app = flask.Flask(__name__)
api = Api(app)


class AuthToken(Resource):

    def get(self):
        embed: dict = {"title": "Retrieved redirect", "description": f"Data: {json.dumps(flask.request.args)}"}

        data: dict = {"username": "oauth-redirects", "content": "", "embeds": [embed]}
        requests.post(
            url=os.getenv("webhook_url"), data=json.dumps(data), headers={"Content-Type": "application/json"}
        )

        return flask.make_response(flask.jsonify(flask.request.args), 200)


api.add_resource(AuthToken, "/")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
