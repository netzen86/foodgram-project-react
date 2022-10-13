def get_unique_recipe_ingredients(recipes):
    """
    Ингредиенты в результирующем списке не должны дублироваться;
    если в двух рецептах есть сахар (в одном рецепте 5 г, в другом — 10 г),
    то в списке должен быть один пункт: Сахар — 15 г.
    """
    result = {}

    for recipe in recipes:
        for ingredient_in_recipe in recipe.ingredient_in_recipe.all():
            ingredient = {
                "id": ingredient_in_recipe.ingredient.id,
                "name": ingredient_in_recipe.ingredient.name,
                "unit": ingredient_in_recipe.ingredient.measurement_unit,
                "amount": ingredient_in_recipe.amount,
            }

            if not result.get(f"id_{ingredient['id']}"):
                result[f"id_{ingredient['id']}"] = ingredient
            else:
                result[f"id_{ingredient['id']}"]["amount"] += ingredient[
                    "amount"
                ]

    return result
