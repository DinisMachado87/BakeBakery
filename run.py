import gspread
from google.oauth2.service_account import Credencials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('BakeryBake')

receipes = SHEET.worksheet('receipes')
data = receipes.get_all_values()
print(data)

pantry_targets = {
    "flour (kg)": 1,
    "eggs (unit)": 6,
    "yeast (gr)": 200,
    "butter (kg)": 0.4,
    "chocolate (gr)": 200,
    "sugar (gr)": 400,
    "salt (g)": 50
}

pantry = {
    "flour (kg)": 1,
    "eggs (unit)": 6,
    "yeast (gr)": 200,
    "butter (kg)": 0.4,
    "chocolate (gr)": 200,
    "sugar (gr)": 400,
    "salt (g)": 50
}

recipes = {
    "croissant": {
        "ingredients": {
            "flour (g)": 400,
            "milk (ml)": 200,
            "sugar (g)": 40,
            "salt (g)": 8,
            "butter (g)": 200,
            "yeast (g)": 10,
            "chocolate chips (g)": 100
        },
        "serves": 10
    },
    "pastel_de_nata": {
        "ingredients": {
            "puff pastry (sheets)": 2,
            "milk (ml)": 500,
            "egg yolks": 6,
            "sugar (g)": 150,
            "cornstarch (g)": 20,
            "vanilla extract (ml)": 5,
            "cinnamon (g)": 5
        },
        "serves": 12
    },
    "portuguese_rice_flour_cakes": {
        "ingredients": {
            "rice flour (grams)": 250,
            "sugar (grams)": 100,
            "eggs": 3,
            "milk (ml)": 250,
            "butter (grams)": 50,
            "lemon zest (teaspoon)": 1,
            "vanilla extract (teaspoon)": 1
        },
        "serves": 8
    },
    "brownies": {
        "ingredients": {
            "unsalted butter (grams)": 200,
            "granulated sugar (grams)": 200,
            "cocoa powder (grams)": 75,
            "eggs": 3,
            "vanilla extract (teaspoon)": 1,
            "all-purpose flour (grams)": 100,
            "salt (teaspoon)": 0.5,
            "chocolate chips (grams)": 100
        },
        "serves": 12
    }
}

def update_pantry_targets(pantry_targets, recipes):
    for recipe in recipes.values():
        ingredients = recipe.get("ingredients", {})
        for ingredient, amount in ingredients.items():
            if ingredient in pantry_targets:
                pantry_targets[ingredient] = round(pantry_targets[ingredient] + amount * 1.2)  # Update and round to the nearest integer
            else:
                pantry_targets[ingredient] = round(amount * 1.2)  # Add new ingredient with 20% increase and round to the nearest integer

def update_pantry_targets(pantry_targets, recipes, spreadsheet_name):
    try:
        SHEET = GSPREAD_CLIENT.open(spreadsheet_name)

        for recipe in recipes.values():
            ingredients = recipe.get("ingredients", {})
            for ingredient, amount in ingredients.items():
                if ingredient in pantry_targets:
                    pantry_targets[ingredient] = round(pantry_targets[ingredient] + amount * 1.2)  # Update and round to the nearest integer
                else:
                    pantry_targets[ingredient] = round(amount * 1.2)  # Add new ingredient with 20% increase and round to the nearest integer

        return pantry_targets
    except Exception as e:
        print(f"Error updating Google Sheets: {str(e)}")
        return None


spreadsheet_name = 'BakeryBake'
pantry_targets = update_pantry_targets(pantry_targets, recipes, spreadsheet_name)
