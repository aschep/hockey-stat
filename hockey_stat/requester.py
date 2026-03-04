import logging
import typing as t
from http import client

logger = logging.getLogger(__name__)


def make_request(request: str) -> t.Optional[str]:
    conn = client.HTTPSConnection(host="pfo.fhr.ru")

    logger.debug("make request: %s", request)

    conn.request("GET", request)
    response = conn.getresponse()
    conn.close()

    logger.debug("response status: %r, %r", response.status, response.reason)

    if response.status == client.OK:
        return response.read().decode(encoding="ascii")
