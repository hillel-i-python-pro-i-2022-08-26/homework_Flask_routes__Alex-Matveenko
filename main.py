import csv
import json
from typing import Any, Generator

import requests
from flask import Flask, Response
from webargs import fields
from webargs.flaskparser import use_args

from applications.services.database_table import create_table
from applications.services.db_connection import DBConnection
from applications.services.generate_users import name_generate
from applications.settings import file_path

app = Flask(__name__)


@app.route("/")
def main_page():
    return "<h1>This is homework</h1>"


@app.route("/requirements/")
def file_view() -> str:
    return "".join(f"<p>{i}</p>" for i in file_path.read_text().split("\n"))


@app.route("/generate-users/<int:number>")
@app.route("/generate-users/")
def numerate_users(number: int = 100) -> Generator[str, Any, None]:
    num_of_people = number
    for i in range(num_of_people):
        yield f"<p>{i + 1}. {name_generate()}</p>"


@app.route("/space")
def space() -> str:
    url = "http://api.open-notify.org/astros.json"
    response = requests.get(url)
    text = response.text
    json_file = json.loads(text)
    return f"Количество космонавтов в данный момент: {json_file['number']}"


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


@app.route("/users/create-user")
@use_args(
    {"name": fields.Str(required=True), "phone-number": fields.Int(required=True)},
    location="query",
)
def create_users(args) -> str:
    with DBConnection() as connection:
        with connection:
            connection.execute(
                """INSERT INTO phones(contactName, phoneValue)
                VALUES (:contacName, :phoneValue);""",
                dict(contacName=args["name"], phoneValue=args["phone-number"]),
            )
    return "Пользователь успешно создан!"


@app.route("/users/all-users")
def view_users() -> str:
    with DBConnection() as connection:
        phones_table = connection.execute(
            """
        SELECT * FROM phones;
        """
        ).fetchall()
    return "<br>".join(
        [
            f'{user["phoneID"]}. {user["contactName"]}'
            f' контактный телефон: {user["phoneValue"]}'
            for user in phones_table
        ]
    )


@app.route("/users/user/<int:phone_id>")
def view_user(phone_id: int) -> str:
    with DBConnection() as connection:
        user = connection.execute(
            """
        SELECT * FROM phones
        WHERE (phoneID=:phone_id);""",
            {"phone_id": phone_id},
        ).fetchone()
    return (
        f"{user['phoneID']}. {user['contactName']} "
        f"контактный телефон: {user['phoneValue']}"
    )


@app.route("/users/update/<int:phone_id>")
@use_args({"name": fields.Str(), "phone-number": fields.Int()}, location="query")
def update_user(args, phone_id: int) -> Response | str:
    with DBConnection() as connection:
        with connection:
            name = args.get("name")
            value = args.get("phone-number")
            # Check if arguments exists
            if name is None and value is None:
                return Response("Укажите хотя бы один аргумент", status=406)
            # Check what argument is pass, and include to it list
            request_args = []
            if name is not None:
                request_args.append("contactName=:name")
            if value is not None:
                request_args.append("phoneValue=:value")
            # Update database with given arguments
            connection.execute(
                "UPDATE phones "
                f'SET {", ".join(request_args)} '
                "WHERE phoneID=:phone_id;",
                {
                    "phone_id": phone_id,
                    "name": name,
                    "value": value,
                },
            )
    return "Данные успешно обновлены."


@app.route("/users/delete/<int:phone_id>")
def delete_user(phone_id: int) -> str:
    with DBConnection() as connection:
        with connection:
            connection.execute(
                "DELETE FROM phones WHERE phoneID=:phone_id",
                {"phone_id": phone_id},
            )
    return "Пользователь успешно удален!"


# Create_database_table
create_table()

# Run_project
if __name__ == "__main__":
    app.run(debug=True)
