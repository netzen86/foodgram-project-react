def get_unique_recipe_ingredients(recipes):
    """
    Ингредиенты в результирующем списке не должны дублироваться;
    если в двух рецептах есть сахар (в одном рецепте 5 г, в другом — 10 г),
    то в списке должен быть один пункт: Сахар — 15 г.
    """
    result = {}

    for recipe in recipes:
        for ingredients in recipe.IngredientsRecipe.all():
            ingredient = {
                "id": ingredients.ingredients_id.id,
                "name": ingredients.ingredients_id.name,
                "unit": ingredients.ingredients_id.measurement_unit,
                "amount": ingredients.amount,
            }

            if not result.get(f"id_{ingredient['id']}"):
                result[f"id_{ingredient['id']}"] = ingredient
            else:
                result[f"id_{ingredient['id']}"]["amount"] += ingredient[
                    "amount"
                ]

    return result
