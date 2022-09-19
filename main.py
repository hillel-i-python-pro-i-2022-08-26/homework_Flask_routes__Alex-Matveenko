import csv
import json
from pathlib import Path
from typing import Any, Generator

import requests
from faker import Faker
from flask import Flask

# Path_to_files__start
HOME_PATH = Path(__file__).parents[1]
FILES_PATH = HOME_PATH.joinpath("homework_Flask_routes__Alex-Matveenko")
text_file = Path(FILES_PATH, "file_for_route.txt")
# Path_to_files__stop

app = Flask(__name__)
fake = Faker()


# main_page__start
@app.route("/")
def main_page():
    return "<h1>This is homework</h1>"


# main_page__stop


# route_requirements__start
@app.route("/requirements/")
def file_view() -> str:
    return "".join(f"<p>{string}</p>" for string in text_file.read_text().split("\n"))


# route_requirements__stop


# route_users_generate_by_default__start
@app.route("/generate-users/")
def users() -> Generator[str, Any, None]:
    all_str = ""
    for name in range(100):
        name = fake.name()
        email = f"{str(name.split()[1]).lower()}_example@mail.com"
        all_str += f"<li>{name}: {email}</li>"
    return (f"<ol>{i}</ol>" for i in all_str.split("\n"))


# route_users_generate_by_default__stop


# route_users_generate_by_number__start
@app.route("/generate-users/<int:number>")
def numerate_users(number: int) -> Generator[str, Any, None]:
    name_and_email = ""
    for name in range(number):
        name = fake.name()
        email = f"{str(name.split()[1]).lower()}_example@mail.com"
        name_and_email += f"<li>{name}: {email}</li>"
    return (f"<ol>{string}</ol>" for string in name_and_email.split("\n"))


# route_users_generate_by_number__stop


# route_space__start
@app.route("/space")
def space() -> str:
    url = "http://api.open-notify.org/astros.json"
    response = requests.get(url)
    text = response.text
    json_file = json.loads(text)
    for key, value in json_file.items():
        return f"Количество космонавтов в данный момент: {value}"


# route_space__stop


# route_for_csv__start
@app.route("/mean")
def mean() -> str:
    sum_of_height = 0
    sum_of_weight = 0
    number_of_index = 0
    with open("people_data.csv", "r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            sum_of_height += float(list(row.values())[1])
            sum_of_weight += float(list(row.values())[2])
            number_of_index += 1
        middle_height = sum_of_height / number_of_index
        middle_weight = sum_of_weight / number_of_index
        return (
            f"<li>Средний рост: {round(middle_height, 2)}.</li>"
            f"<li>Средний вес: {round(middle_weight, 2)}.</li>"
            f"<li>Количество отмерянных и взвешенных: {number_of_index}</li>"
        )


# route_for_csv__stop


if __name__ == "__main__":
    app.run(debug=True)
