from sqlalchemy import Integer, Column, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Recipe(Base):
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True, index=True)

    has_ingredient = relationship("RecipeIngredient", back_populates="belongs_in_recipe", uselist=True)


class RecipeIngredient(Base):
    __tablename__ = 'recipe_ingredients'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=True)
    type = Column(Integer, nullable=True)
    type_name = Column(Text, nullable=True)
    ean = Column(Text, nullable=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id'))

    belongs_in_recipe = relationship("Recipe", back_populates="has_ingredient", uselist=True)







class Ingredient(Base):
    __tablename__ = 'ingredients'

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    alt_spelling_id = Column(Integer, ForeignKey('ingredient_alt_spellings.id'))
    ean_code_id = Column(Integer, ForeignKey('ingredient_ean_codes.id'))


class IngredientAltSpelling(Base):
    __tablename__ = 'ingredient_alt_spellings'

    id = Column(Integer, primary_key=True)
    spelling = Column(Text)


class IngredientEanCode(Base):
    __tablename__ = 'ingredient_ean_codes'

    id = Column(Integer, primary_key=True)
    ean = Column(Text)


