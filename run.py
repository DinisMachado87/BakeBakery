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

def get_recipe(baked_goods_page):
    '''Get the ingredients amount for the recipe defined in the variable'''
    worksheet = SHEET.worksheet(baked_goods_page)
    data = worksheet.get_all_values()
    baked_goods = {
        column[0]: column[2] for column in data
    }
    return baked_goods

def print_recipe(baked_goods_page):
    '''Print the recipe'''
    baked_goods = get_recipe(baked_goods_page)
    for key, value in baked_goods.items():
        print(f'{key}: {value}')

def update_recipe_doses():
    print('Functionality for updating recipe doses goes here.')

def update_pantry_goals(recipes):
    '''Actualizes pantry goals adding ingredients from all recipes 
    and adding 20% to each ingredient'''
    pantry_goals_worksheet = SHEET.worksheet('pantry_goals')
    goals_data = pantry_goals_worksheet.get_all_values()
    goals = {
        column[0]: float(column[1]) for column in goals_data
    }

    for recipe_name, recipe in recipes.items():
        for ingredient, amount in recipe.items():
            '''Check if the ingredient is already in the goals dictionary'''
            if ingredient in goals:
                goals[ingredient] += amount
            else:
                goals[ingredient] = amount

    '''Apply a 20% increase to all ingredient amounts'''
    goals_with_increase = {
        ingredient: amount * 1.2 for ingredient, amount in goals.items()
    }

    # Update the "recipe_goals" worksheet with the new values
    pantry_goals_worksheet.clear()
    pantry_goals_worksheet.append_rows(
        [list(goals_with_increase.keys()), list(goals_with_increase.values())]
    )

# Get recipes
croissants_recipe = get_recipe(
    'recipe_croissants'
)
pastel_de_nata_recipe = get_recipe(
    'recipe_pastel_de_nata'
)
portuguese_rice_flour_cakes_recipe = get_recipe(
    'recipe_portuguese_rice_flour_cakes'
)
brownies_recipe = get_recipe(
    'recipe_brownies'
)

# Create a dictionary to hold all recipes
all_recipes = {
    'croissants': croissants_recipe,
    'pastel_de_nata': pastel_de_nata_recipe,
    'portuguese_rice_flour_cakes': portuguese_rice_flour_cakes_recipe,
    'brownies': brownies_recipe
}

def get_shopping_list():
    print('Functionality for getting the shopping list goes here.')

def register_shopped_groceries():
    print('Functionality for registering shopped groceries goes here.')

def show_menu():
    title = 'What would you like to do?'
    options = [
        'Get Shopping List', 
        'Register Shopped Groceries', 
        'Update Recipe Doses', 
        'Get Recipe', 
        'Exit'
    ]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    print(f"You have selected {options[menu_entry_index]}!")

def show_menu_get_recipe():
    title = 'Which recipe would you like to see?'
    options = [
        'Croissants', 
        'Pastel de Nata', 
        'Portuguese Rice Flour Cakes', 
        'Brownies'
    ]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    print(f"You have selected {options[menu_entry_index]}!")

def get_user_choice():
    try:
        choice = int(input())
        return choice
    except ValueError:
        print('Invalid input. Please enter a number.')
        return None

def main():
        '''Display the initial menu'''
    show_menu() 

    while True:
        user_choice = get_user_choice()

        if user_choice is not None:
            if user_choice == 1:
                get_shopping_list()
            elif user_choice == 2:
                register_shopped_groceries()
            elif user_choice == 3:
                update_recipe_doses()
            elif user_choice == 4:
                show_menu_get_recipe()

                recipe_choice = get_user_choice()
                if recipe_choice in range(0, 4):
                    recipe_page_names = {
                        1: 'recipe_croissants',
                        2: 'recipe_pastel_de_nata',
                        3: 'recipe_portuguese_rice_flour_cakes',
                        4: 'recipe_brownies'
                    }
                    print_recipe(recipe_page_names[recipe_choice])
                elif recipe_choice == 4:
                    show_menu()
                else:
                    print('''Invalid recipe choice. 
                    Please enter a number between 1 and 4.''')
            elif user_choice == 5:
                print('Exiting the menu. Goodbye!')
                break
            else:
                print('''Invalid choice. 
                Please enter a valid option (1-5).''')

if __name__ == '__main__':
    main()