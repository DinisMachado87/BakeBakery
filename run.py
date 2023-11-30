import os
import gspread
from google.oauth2.service_account import Credentials
from simple_term_menu import TerminalMenu


SCOPE = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive'
]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('BakeryBake')


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_ingridients():
    recipes = get_recipe(show_menu_get_recipe())
    clear_terminal()
    for recipe in recipes:
        ingredients, servings, recipe_name = recipe
        print(f'\n {recipe_name} : \n')
        for ingredient in ingredients:
            print(f'{ingredient[0]}: {ingredient[1]} {ingredient[2]}')
        print('\n')
    main()

def get_recipe(*baked_goods_pages):
    '''
    Get the ingredients amount in a nested list 
    and servings into a dictionary
    '''
    recipes = []
    
    for page in baked_goods_pages:
        worksheet = SHEET.worksheet(page)
        data = worksheet.get_all_values()
        servings = data[0][2]
        ingredients = [[column[0], column[2], column[1]] for column in data]
        recipe_name = page
        recipes.append([ingredients, servings, recipe_name])
    return recipes


def show_menu_get_recipe():
    '''Show the menu with the recipes and return the recipe chosen'''
    title = 'Which recipe?'
    print(title)
    options = [
        'croissants',
        'pastel de nata',
        'portuguese rice flour cakes',
        'brownies',
        'Go back to main menu'
    ]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    if menu_entry_index == 0:
        recipe = 'recipe_croissants'
        return recipe  
    elif menu_entry_index == 1:
        recipe = 'recipe_pastel_de_nata'
        return recipe
    elif menu_entry_index == 2:
        recipe = 'recipe_portuguese_rice_flour_cakes'
        return recipe
    elif menu_entry_index == 3:
        recipe = 'recipe_brownies'
        return recipe
    elif menu_entry_index == 4:
        main()

def update_pantry_goals():
    '''
    Actualizes pantry goals adding ingredients from all recipes 
    and adding 20% to each ingredient
    '''
    recipes = get_recipe(
        'recipe_croissants',
        'recipe_pastel_de_nata',
        'recipe_portuguese_rice_flour_cakes',
        'recipe_brownies'
    )

    goals = {}
    for ingredients, servings, recipe_name in recipes:
        for ingredient, amount, unit in ingredients:
            # Check if the ingredient is already in the goals dictionary
            if ingredient in goals:
                goals[ingredient][0] += float(amount)
            else:
                goals[ingredient] = [float(amount), unit]

    # Apply a 20% increase to all ingredient amounts
    goals_with_increase = {
        ingredient: [
            amount * 1.2, unit
        ] for ingredient, (amount, unit) in goals.items()
    }

    # Update the "recipe_goals" worksheet with the new values
    pantry_goals_worksheet = SHEET.worksheet('pantry_goals')
    pantry_goals_worksheet.clear()
    pantry_goals_worksheet.append_row(['Ingredient', 'Amount', 'Unit'])
    for ingredient, (amount, unit) in goals_with_increase.items():
        pantry_goals_worksheet.append_row([ingredient, amount, unit])

    return goals_with_increase


def update_recipe_doses():
    '''
    Update the recipe doses by multiplying the ingredients amount 
    with the number of servings
    '''
    recipes = get_recipe(show_menu_get_recipe())
    clear_terminal()
    servings_input = input("Enter the number of servings: ")
    clear_terminal()
    for recipe in recipes:
        ingredients, servings, recipe_name = recipe

        updated_recipe = []

        for ingredient, amount, unit in ingredients:
            updated_amount = float(servings_input) * float(amount) / float(servings)
            updated_recipe.append([ingredient, unit, updated_amount])

        print(f'{recipe_name} updated recipe:')
        for column in updated_recipe:
            print(f'{column[0]}: {column[1]} {column[2]}')

        # Update the "recipe_goals" worksheet with the new values
        worksheet_to_update = SHEET.worksheet(recipe_name)
        worksheet_to_update.clear()
    
        for ingredient, unit, updated_amount in updated_recipe:
            worksheet_to_update.append_row([ingredient, unit, updated_amount])

    try:
        servings = float(servings_input)
        print(f"You entered {servings} servings.")
    except ValueError:
        print("Invalid input. Please enter a valid number of servings.")




def register_shopped_groceries():
    print('Functionality for registering shopped groceries goes here.')


def main():
    title = 'What would you like to do?'
    print(f'\n{title}\n')
    options = [
        'Get Shopping List', 
        'Register Shopped Groceries', 
        'Update Recipe Doses', 
        'Get Recipe', 
        'Exit'
    ]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()

    while True:
        user_choice = menu_entry_index + 1

        if user_choice is not None:
            if user_choice == 1:
                clear_terminal()
                get_shopping_list()
                main()
            elif user_choice == 2:
                clear_terminal()
                register_shopped_groceries()
                main()
            elif user_choice == 3:
                clear_terminal()
                update_recipe_doses()
                main()
            elif user_choice == 4:
                clear_terminal()
                print_ingridients()
                main()
            elif user_choice == 5:
                clear_terminal()
                main()
                break


if __name__ == '__main__':
    main()
