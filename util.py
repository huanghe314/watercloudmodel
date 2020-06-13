import pathlib


def is_csv(filename: str) -> bool:
    if pathlib.Path(filename).suffix == '.csv':
        return True
    return False
