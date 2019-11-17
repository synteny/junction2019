import json

import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from orm import Base, RecipeIngredient, Recipe


def init_db():
    engine = create_engine("sqlite:///recipes.db", echo=True)

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    return engine


def fetch_recipes():
    url = 'https://kesko.azure-api.net/v1/search/recipes'

    data = '''{
        "query": "*"
    }'''

    response = requests.post(url, data=data, headers={
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": "c3adbde35d0a40d58e6bc1c99751c129"
    })

    return response.content


def save_recipe(r, session):
    id = r["Id"]
    ingredients = r["Ingredients"][0]["SubSectionIngredients"]

    recipe = Recipe(id=id)
    session.add(recipe)

    for ingr in ingredients:
        name = ingr[0]["Name"]
        ingrType = ingr[0]["IngredientType"] if "IngredientType" in ingr[0] else None
        ingrTypeName = ingr[0]["IngredientTypeName"] if "IngredientTypeName" in ingr[0] else None
        ean = ingr[0]["Ean"] if "Ean" in ingr[0] else None

        ingredient = RecipeIngredient(name=name, type=ingrType, type_name=ingrTypeName, ean=ean, recipe_id=id)
        ingredient.belongs_in_recipe.append(recipe)
        session.add(ingredient)


def parse_recipes(session):
    parsed = json.loads(fetch_recipes())
    for r in parsed["results"]:
        save_recipe(r, session)


def main():
    engine = init_db()

    Session = sessionmaker(bind=engine)
    session = Session()

    parse_recipes(session)

    session.commit()


if __name__ == '__main__':
    main()