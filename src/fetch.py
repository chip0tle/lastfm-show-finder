from typing import Any
from requests.models import Response
from requests.exceptions import HTTPError, Timeout, ConnectionError
import requests


def get_as_json(api_key: str | None, url: str) -> dict | Any:
    """
    Request data from API, return json object
    """
    try:
        r: Response = requests.get(url)
        r.raise_for_status()
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response body: {r.text}")
    except ConnectionError as conn_err:
        print(f"Connection error: {conn_err}")
        print(f"Response body: {r.text}")
    except Timeout:
        print("Request timed out.")
    except Exception as e:
        print(f"Unexpected error: {e}")
    else:
        return r.json()
