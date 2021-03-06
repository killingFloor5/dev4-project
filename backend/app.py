from flask import Flask, jsonify, request_started
from flask_cors import CORS
from queries import (create_user, login, get_menu,
                     get_staff, get_gallery, staff_login, post_reservation, reservatie, my_reservations,
                     tables, get_one_table, get_one_reservation)
import sqlite3

app = Flask(__name__)
CORS(app)

db_name = './database/restaurant.db'

app.add_url_rule('/register', None, create_user, methods=["POST"])
app.add_url_rule('/menu', None, get_menu, methods=["GET"])
app.add_url_rule('/login', None, login, methods=["POST"])
app.add_url_rule('/login_medewerker', None, staff_login, methods=["POST"])
app.add_url_rule('/gallerij', None, get_gallery, methods=["GET"])
app.add_url_rule('/home', None, get_staff, methods=["GET"])
app.add_url_rule('/', None, get_staff, methods=["GET"])
# make a reservation
app.add_url_rule('/reservation', None, post_reservation, methods=["POST"])
# get the user reservations
app.add_url_rule('/myreservations', None, my_reservations, methods=["GET"])
# Get all tables
app.add_url_rule('/reservatie', None, reservatie, methods=["GET", "PATCH", "DELETE"])
app.add_url_rule('/tables', None, tables, methods=["GET", "POST", "PATCH", "DELETE"])
app.add_url_rule('/reservations/table/:id', None, get_one_reservation, methods=["GET"])
app.add_url_rule('/get_one_table', None, get_one_table, methods=["GET"])
app.add_url_rule('/get_one_reservation', None, get_one_reservation, methods=["GET"])


@app.before_request
def before_request():
    request_started.send(app)


def db_connection():
    conn = None
    try:
        conn = sqlite3.connect('./database/restaurant.db')
        print("Connected to the restaurant database")
    except sqlite3.error as e:
        print(e)
    return conn


@app.errorhandler(404)
def error(e):
    return jsonify({"message": "Not found"}), 404


@app.errorhandler(500)
def error(e):
    return jsonify({"message": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(port=5000)
    app.run(debug=True)
