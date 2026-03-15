import logging
import typing as t

import requests
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)


BASE_URL = "https://pfo.fhr.ru"


def make_request(url_: str, params=None) -> t.Optional[str]:
    try:
        url = f"{BASE_URL}{url_}"
        logger.debug("make request: %s", url)
        resp = requests.get(url, params, timeout=10)
        resp.raise_for_status()
        return resp.text
    except RequestException as e:
        logger.error(f"Request failed: {e}")
