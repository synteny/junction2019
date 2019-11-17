import json

from flask import Flask, request
import requests

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/recipes')
def recipies():
    url = 'https://kesko.azure-api.net/v1/search/recipes'

    data = '''{
        "query": "%s"
    }''' % request.args.get("query")

    response = requests.post(url, data=data, headers={
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": "c3adbde35d0a40d58e6bc1c99751c129"
    })
    return response.content


@app.route('/searchRecipes', methods=["POST"])
def search_recipe():
    ingredients = [str(i) for i in request.json]
    print(", ".join(ingredients))

    with open("mock_response.json") as f:
        return ''.join(f.readlines())


if __name__ == '__main__':
    app.run(Debug=True)
