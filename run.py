import os
import json
import flask
import requests

from flask_restful import Api, Resource

app = flask.Flask(__name__)
api = Api(app)


class AuthToken(Resource):

    def get(self):
        embed = {"title": "Received redirect", "description": json.dumps(flask.request.args)}
        data = {"username": "OAuth Redirect Response", "content": flask.request.args.get("appid"), "embeds": [embed]}
        r = requests.post(
            url=os.getenv("webhook_url"), data=json.dumps(data, indent=4), headers={"Content-Type": "application/json"}
        )

        if r.status_code == 200:
            return flask.make_response(flask.jsonify({"Result": "Success! Result has been sent to Discord"}), 200)
        else:
            return flask.make_response(flask.jsonify(
                    {"Result": "Failure! Result has failed to be sent to Discord. Check the logs"}
                ), 400
            )


api.add_resource(AuthToken, "/")


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
