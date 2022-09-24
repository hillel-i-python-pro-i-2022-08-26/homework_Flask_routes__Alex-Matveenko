import csv
import json
from typing import Any, Generator

import requests
from flask import Flask
from webargs import fields
from webargs.flaskparser import use_args

from applications.services.database_table import create_table
from applications.services.db_connection import DBConnection
from applications.services.generate_users import name_generate
from applications.settings import file_path

app = Flask(__name__)


# main_page__start
@app.route("/")
def main_page():
    return "<h1>This is homework</h1>"


# main_page__stop


# route_requirements__start
@app.route("/requirements/")
def file_view() -> str:
    return "".join(f"<p>{i}</p>" for i in file_path.read_text().split("\n"))


# route_requirements__stop


# route_users_generate_by_number__start
@app.route("/generate-users/<int:number>")
@app.route("/generate-users/")
def numerate_users(number: int = 100) -> Generator[str, Any, None]:
    num_of_people = number
    for i in range(num_of_people):
        yield f"<p>{i + 1}. {name_generate()}</p>"


# route_users_generate_by_number__stop


# route_space__start
@app.route("/space")
def space() -> str:
    url = "http://api.open-notify.org/astros.json"
    response = requests.get(url)
    text = response.text
    json_file = json.loads(text)
    return f"Количество космонавтов в данный момент: {json_file['number']}"


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
            sum_of_height += float(list(row.values())[1]) * 2.54
            sum_of_weight += float(list(row.values())[2]) * 0.45
            number_of_index += 1
        middle_height = sum_of_height / number_of_index
        middle_weight = sum_of_weight / number_of_index
        return (
            f"<li>Средний рост: {round(middle_height, 2)} см.</li>"
            f"<li>Средний вес: {round(middle_weight, 2)} кг.</li>"
            f"<li>Количество отмерянных и взвешенных: {number_of_index}</li>"
        )


# route_for_csv__stop


# Create_user_route__start
@app.route('/create-users')
@use_args({"name": fields.Str(required=True), "phone-number": fields.Int(required=True)}, location="query")
def create_users(args):
    with DBConnection() as connection:
        with connection:
            connection.execute(
                """INSERT INTO phones(contactName, phoneValue)
                VALUES (:contacName, :phoneValue);""",
                dict(contacName=args["name"], phoneValue=args["phone-number"]),
            )
    return "Пользователь успешно создан!"


# Create_user_route__stop


# Create_database_table
create_table()

# Run_project
if __name__ == "__main__":
    app.run(debug=True)
