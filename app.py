import json

from flask import Flask, render_template, request
import requests
from sqlalchemy import create_engine, func, desc
from sqlalchemy.orm import sessionmaker

from orm import Recipe, RecipeIngredient

app = Flask(__name__)

engine = create_engine("sqlite:///recipes.db", echo=True)
Session = sessionmaker(bind=engine)

def query_db(ingredients):
    session = Session()

    q = session.query(Recipe.id, func.count(Recipe.id).label('cnt')).join(RecipeIngredient).filter(RecipeIngredient.type_name.in_(ingredients)).group_by(Recipe.id).order_by(desc('cnt')).all()

    for r in q:
        yield r.id

    session.close()
    # return ["3308", "10457"]


def fetch_recipe(id):
    url = 'https://kesko.azure-api.net/v1/search/recipes'

    data = '''{ "filters": { "ids": [ "%s" ] }}''' % id

    response = requests.post(url, data=data, headers={
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": "c3adbde35d0a40d58e6bc1c99751c129"
    })

    return next(iter(json.loads(response.content)['results']))


def match_recipes(ingredients):
    recipe_ids = query_db(ingredients)

    for id in recipe_ids:
        r = fetch_recipe(id)

        available_ingredients = {ing[0]['Name'] for ing in r['Ingredients'][0]['SubSectionIngredients'] if
                        'IngredientTypeName' in ing[0] and ing[0]['IngredientTypeName'] in ingredients}
        yield {
          'title': r['Name'],
          'categories': {cat['MainName'] for cat in r['Categories']} if 'Categories' in r else {},
          'available_ingredients': available_ingredients,
          'unavailable_ingredients': {ing[0]['Name'] for ing in r['Ingredients'][0]['SubSectionIngredients']}.difference(available_ingredients),
          'img': r['PictureUrls'][0]['Normal'],
          'url': "https://www.k-ruoka.fi/reseptit/" + r['UrlSlug']
        }


@app.route("/", methods=["GET", "POST"])
def render():
    recipes = match_recipes(list(request.form.values())) if request.form else None

    return render_template('foodremix.html', recipes=recipes)


if __name__ == '__main__':
    app.run(Debug=True)
