from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def render():
    return render_template('html/food-search.html')


if __name__ == '__main__':
    app.run(Debug=True)
