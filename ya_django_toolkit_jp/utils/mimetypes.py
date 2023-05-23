from typing import Any


def additional_guess_type(filename: Any):
    if not isinstance(filename, str):
        return None

    if filename.endswith('.webp'):
        return 'image/webp'

    return None
