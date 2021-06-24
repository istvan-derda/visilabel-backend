from flask import Flask

from design_source import get_design

app = Flask(__name__)
app.debug = True


@app.route('/')
def root_endpoint():
    return "<h1>Visilable Backend</h1>"


@app.route('/design')
def get_designs_endpoint():
    return get_design()


def main():
    app.run(port=5001)


if __name__ == '__main__':
    main()
