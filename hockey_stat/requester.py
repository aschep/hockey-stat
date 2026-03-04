import logging
import typing as t

import requests
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)


def make_request(url_: str) -> t.Optional[str]:
    try:
        url = f"https://pfo.fhr.ru{url_}"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.text
    except RequestException as e:
        logger.error(f"Request failed: {e}")
