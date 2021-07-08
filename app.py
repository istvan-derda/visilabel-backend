import os

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
    return [product_color_row[0] for product_color_row in dao.get_all_product_colors()][:8]


@app.route('/submitRating', methods=['POST'])
def submit_rating():
    print(request.is_json)
    ratings_dto = request.get_json()
    ratings = ratings_dto["ratings"]
    for rating in ratings:
        dao.write_rating(rating["user_id"], rating["design_id"], rating["background_color"], rating["rating"])
    return "done"


@app.route('/labelsCount', methods=['GET'])
def get_labels_count():
    count = dao.get_rated_count()[0][0]
    labels_count_dto = {'count': count}
    return jsonify(labels_count_dto)


@app.route('/labelsPerUserCount', methods=['POST'])
def get_all_count_per_user():
    user_id_dto = request.get_json()
    user_id = user_id_dto['userId']
    count = dao.get_rated_count_for_user(user_id)[0][0]
    labels_count_dto= {'count': count}
    return jsonify(labels_count_dto)


def main():
    app.run()


if __name__ == '__main__':
    main()
