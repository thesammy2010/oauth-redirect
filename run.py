import datetime
import json
import os
import uuid
from typing import Any, Dict, List

import flask
from flask_restful import Api, Resource

from discord import post_to_discord
from mongo import send_to_mongo

app = flask.Flask(__name__)
api = Api(app)


class AuthToken(Resource):
    def get(self) -> flask.Response:

        request_id: str = str(uuid.uuid4())
        request_time: datetime.datetime = datetime.datetime.now()
        request_headers: Dict[str, Any] = dict(flask.request.headers)
        request_args: Dict[str, Any] = dict(flask.request.args)
        errors_array: List[str] = []
        try:
            request_form: Dict[str, Any] = dict(flask.request.get_json() if flask.request.is_json else {})
        except json.decoder.JSONDecodeError as e:
            request_form = {}
            errors_array.append("Failed to decode JSON")
            errors_array.append(str(e))
        sent_to_discord: bool = False
        sent_to_mongo: bool = False
        status_code: int = 500
        data: Dict[str, Any] or None = None if not (request_args or request_form) else {**request_args, **request_form}
        status_text: str = ""

        # only send to discord if there's data, ignore generic hits
        if data:
            try:
                sent_to_discord = post_to_discord(
                    request_id=request_id,
                    request_time=request_time.isoformat(),
                    request_args=request_args,
                    request_data=request_form,
                )
            except Exception as e:
                errors_array.append(f"[Discord] Internal error! {e}")

        try:
            sent_to_mongo = send_to_mongo(
                request_id=request_id,
                request_time=request_time,
                request_headers=request_headers,
                request_data=request_form,
                request_args=request_args,
                sent_to_discord=sent_to_discord,
            )
        except Exception as e:
            errors_array.append(f"[MongoDb] Internal error! {e}")

        if sent_to_mongo and sent_to_discord:
            status_code = 200
            status_text = "Success"
        elif not data:
            status_code = 400
            status_text = "No data provided. Send as JSON or as a url variable"
        elif sent_to_mongo and not sent_to_discord:
            status_code = 501
            status_text = "Failed to post data to Discord"
        elif not sent_to_mongo and sent_to_discord:
            status_code = 502
            status_text = "Failed to record data to MongoDb"
        elif not (sent_to_mongo and sent_to_discord):
            status_code = 503
            status_text = "Failed to make requests to Discord and MongoDb"
        else:
            status_code = 500
            status_text = "Unknown internal error"

        response: Dict[str, Any] = {
            "request_id": request_id,
            "status_code": status_code,
            "result": status_text,
            "errors": errors_array,
            "data": data,
        }

        # JSON return
        if request_headers.get("Accept") == "application/json":
            return flask.make_response(flask.jsonify(response), status_code)
        else:
            # HTML return
            html: str = (
                "<html><body><h1>Response</h1><pre><code>\n"
                + json.dumps(response, indent=4)
                + "\n</code></pre></body></html>"
            )
            return flask.make_response(html, status_code)

    def post(self) -> flask.Response:
        return self.get()

    def put(self) -> flask.Response:
        return self.get()


api.add_resource(AuthToken, "/")


if __name__ == "__main__":
    if os.getenv("FLASK_ENV") == "production":
        import waitress

        waitress.serve(app, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
    else:
        app.run(
            debug=True, host="127.0.0.1", port=int(os.getenv("PORT", 8080)),
        )
