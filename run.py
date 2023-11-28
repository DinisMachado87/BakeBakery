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
    title = 'Which recipe?'
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

def get_recipe(*baked_goods_pages):
    '''Get the ingredients amount for the recipe defined in the variable'''
    recipes = {}
    servings = {}
    for page in baked_goods_pages:
        worksheet = SHEET.worksheet(page)
        data = worksheet.get_all_values()
        servings[page] = data[0][0]
        recipes[page] = {column[0]: column[2] for column in data}
    return recipes


def print_recipe(baked_goods_page):
    '''Print the recipe'''
    baked_goods = get_recipe(baked_goods_page)
    for key, value in baked_goods.items():
        print(f'{key}: {value}')

def update_recipe_doses():
    show_menu_get_recipe()
    user_choice = get_user_choice()
    if user_choice in range(0, 5):    
        if user_choice == 1:
            recipe = 'recipe_croissants'
        elif user_choice == 2:
            recipe = 'recipe_pastel_de_nata'
        elif user_choice == 3:
            recipe = 'recipe_portuguese_rice_flour_cakes'
        elif user_choice == 4:
            recipe = 'recipe_brownies'
    
    servings_input = input("Enter the number of servings: ")

    recipe_to_update = get_recipe(recipe)
    updated_recipe = {}
    for ingridient, amount in recipe_to_update.items():
        updated_recipe[ingridient] = servings_input * amount / servings
    print(updated_recipe)

    try:        
        servings = int(servings_input)
        print(f"You entered {servings} servings.")
    except ValueError:
        print("Invalid input. Please enter a valid number of servings.")



def update_pantry_goals():
    '''Actualizes pantry goals adding ingredients from all recipes 
    and adding 20% to each ingredient'''
    recipes = get_recipe(
        'recipe_croissants',
        'recipe_pastel_de_nata',
        'recipe_portuguese_rice_flour_cakes',
        'recipe_brownies'
    )
    
    goals = {}
    for recipe_name, recipe in recipes.items():
        for ingredient, amount in recipe.items():
            '''Check if the ingredient is already in the goals dictionary'''
            if ingredient in goals:
                goals[ingredient] += float(amount)
            else:
                goals[ingredient] = float(amount)

    '''Apply a 20% increase to all ingredient amounts'''
    goals_with_increase = {
        ingredient: float(amount) * 1.2 for ingredient, amount in goals.items()
    }
    
    # Transpose the data
    transposed_data = list(map(list, zip(*goals_with_increase.items())))
    print(transposed_data)

    '''Update the "recipe_goals" worksheet with the new values'''
    pantry_goals_worksheet = SHEET.worksheet('pantry_goals')
    pantry_goals_worksheet.clear()
    for column in goals_with_increase:
            pantry_goals_worksheet.append_rows([column])
    return goals_with_increase

def get_shopping_list():
    print('Functionality for getting the shopping list goes here.')

def register_shopped_groceries():
    print('Functionality for registering shopped groceries goes here.')

if __name__ == '__main__':
    update_pantry_goals()
    main()