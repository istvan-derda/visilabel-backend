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
    design_ids = dao.get_100_design_ids()
    batches = {"batches": [
        {"design_id": design_id[0], "background_colors": pick_background_colors()} for design_id in design_ids
    ]}
    return jsonify(batches)


def pick_background_colors():
    return [get_random_sprd_color() for _ in range(8)]


def get_random_sprd_color():
    all_product_colors = [product_color_row[0] for product_color_row in dao.get_all_product_colors()]
    return random.choice(all_product_colors)


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
