import os
import random

from flask import Flask, request, jsonify
from flask_cors import CORS

from database_connector import DAO

app = Flask(__name__)
CORS(app)

dao = DAO(os.environ['DATABASE_URL'])


@app.route('/')
def root_endpoint():
    return "<h1>Visilable Backend</h1>"


@app.route('/toRate')
def get_all_to_rate():
    design_ids = dao.get_all_design_ids()
    random.shuffle(design_ids)
    batches = {"batches": [
        {"design_id": design_id[0], "background_colors": pick_background_colors()} for design_id in design_ids
    ]}
    return jsonify(batches)


def pick_background_colors():
    return [generate_random_hexstring() for _ in range(8)]


def generate_random_hexstring():
    r = lambda: random.randint(0, 255)
    return '#%02X%02X%02X' % (r(), r(), r())


@app.route('/submitRating', methods=['POST'])
def submit_rating():
    print(request.is_json)
    ratings_dto = request.get_json()
    ratings = ratings_dto["ratings"]
    for rating in ratings:
        dao.write_rating(rating["user_id"], rating["design_id"], rating["background_color"], rating["rating"])
    return "done"


def main():
    app.run(port=5001)


if __name__ == '__main__':
    main()
