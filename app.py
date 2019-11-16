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


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
