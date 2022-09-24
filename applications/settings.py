import pathlib
from typing import Final

# Root path
ROOT_PATH: Final[pathlib.Path] = pathlib.Path(__file__).parents[1]
# Path to txt file
file_path: Final[pathlib.Path] = pathlib.Path("file_for_route.txt")
# Path to DB
db_path: Final[pathlib.Path] = ROOT_PATH.joinpath("data_base", "db.sqlite")
