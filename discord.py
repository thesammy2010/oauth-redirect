import json
import logging
import os
from typing import Any, Dict, List

import requests


def post_to_discord(
    request_id: str, request_time: str, request_args: Dict[str, Any], request_data: Dict[str, Any]
) -> bool:

    content: str = (
        "--------------------------------"
        "--------------------------------\n"
        f"Request Time: {request_time}\n"
        f"Data: \n{json.dumps({**request_args, **request_data})}\n"
        "--------------------------------"
        "--------------------------------"
    )
    data: Dict[str, List[Dict[str, str]]] = {
        "username": "OAuth Redirect Service",
        "avatar_url": "https://static.thenounproject.com/png/1007187-200.png",
        "embeds": [{"title": f"Request ID: {request_id}", "description": content}],
    }

    r: requests.models.Response = requests.post(
        url=os.getenv("webhook_url"), json=data, headers={"Content-Type": "application/json"}
    )

    r.raise_for_status()
    logging.debug("Response sent to Discord successfully")

    return True
