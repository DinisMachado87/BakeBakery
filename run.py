import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('BakeryBake')

def get_recipe(baked_goods_page):
    worksheet = SHEET.worksheet(baked_goods_page)
    data = worksheet.get_all_values()
    baked_goods = {column[0]: column[2] for column in data}
    return baked_goods

def print_recipe(baked_goods_page):
        baked_goods = get_recipe(baked_goods_page)
        for key, value in baked_goods.items():
            print(f"{key}: {value}")


print_recipe('recipe_croissants')

def update_pantry_goals(recipes):
    pantry_goals_worksheet = SHEET.worksheet('pantry_goals')
    goals_data = pantry_goals_worksheet.get_all_values()
    goals = {column[0]: float(column[1]) for column in goals_data}

    for recipe_name, recipe in recipes.items():
        for ingredient, amount in recipe.items():
            # Check if the ingredient is already in the goals dictionary
            if ingredient in goals:
                goals[ingredient] += amount
            else:
                goals[ingredient] = amount

    # Apply a 20% increase to all ingredient amounts
    goals_with_increase = {ingredient: amount * 1.2 for ingredient, amount in goals.items()}

    # Update the "recipe_goals" worksheet with the new values
    recipe_goals_worksheet.clear()
    recipe_goals_worksheet.append_rows([list(goals_with_increase.keys()), list(goals_with_increase.values())])

# Get recipes
croissants_recipe = get_recipe('recipe_croissants')
pastel_de_nata_recipe = get_recipe('recipe_pastel_de_nata')
portuguese_rice_flour_cakes_recipe = get_recipe('recipe_portuguese_rice_flour_cakes')
brownies_recipe = get_recipe('recipe_brownies')

# Create a dictionary to hold all recipes
all_recipes = {
    'croissants': croissants_recipe,
    'pastel_de_nata': pastel_de_nata_recipe,
    'portuguese_rice_flour_cakes': portuguese_rice_flour_cakes_recipe,
    'brownies': brownies_recipe
}

# Update recipe goals
update_pantry_goals(all_recipes)