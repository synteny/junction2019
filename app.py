from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def render():
    recipes = [
        {'title': 'Item 1', 'categories': ['cat 1', 'cat 2'], 'ingredients': ['item 1', 'item 2'],
         'img': 'https://k-file-storage-qa.imgix.net/f/k-ruoka/recipe/6832?w=1000&h=1000&fit=clip'},
        {'title': 'Item 2', 'categories': ['cat 1', 'cat 2'], 'ingredients': ['item 1', 'item 2'],
         'img': 'https://k-file-storage-qa.imgix.net/f/k-ruoka/recipe/6832?w=1000&h=1000&fit=clip'}
    ]

    return render_template('foodremix.html', recipes=recipes if request.form else None)


if __name__ == '__main__':
    app.run(Debug=True)
