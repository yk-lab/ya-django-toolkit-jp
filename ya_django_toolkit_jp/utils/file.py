from pathlib import Path
from typing import NamedTuple
from urllib.parse import quote


class FileInfo(NamedTuple):
    filename: str
    mimetype: tuple[str | None, str | None]
    suffix: str | None
    content_disposition: str


def generate_content_disposition(filename: str, mode: str = 'attachment'):
    f_name = Path(filename).name
    try:
        f_name.encode('ascii')
        file_expr = 'filename="{}"'.format(
            f_name.replace('\\', '\\\\').replace('"', r"\"")
        )
    except UnicodeEncodeError:
        file_expr = "filename*=utf-8''{}".format(quote(f_name))
    return f'{mode}; {file_expr}'
