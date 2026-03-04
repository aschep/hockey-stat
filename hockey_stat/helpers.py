def get_id_from_url(url: str, sep: str = "-") -> str:
    return url.rsplit(sep, 1)[1][:-1]
