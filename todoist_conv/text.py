from chardet import detect


def detect_encoding(path):
    with open(path, "rb") as fp:
        content = fp.read()

    return detect(content)["encoding"]
