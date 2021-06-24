import os

from flask import Flask, request, jsonify

from database_connector import DAO

app = Flask(__name__)

dao = DAO(os.environ['DATABASE_URL'])


@app.route('/')
def root_endpoint():
    return "<h1>Visilable Backend</h1>"


@app.route('/design')
def get_all_designs():
    return jsonify(dao.get_design_ids())


@app.route('/submitRating', methods=['POST'])
def submit_rating():
    ratings_dto = request.json
    ratings = ratings_dto['ratings']
    for rating in ratings:
        dao.write_rating(rating.user_id, rating.design_id, rating.background_color, rating.rating)


def main():
    app.run(port=5001)


if __name__ == '__main__':
    main()
