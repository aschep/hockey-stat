def read_file(filename: str) -> str:
    with open(filename, "r") as fp:
        return fp.read()
