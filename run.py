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


def get_recipe(*baked_goods_pages):
    '''Get the ingredients amount in a nested list 
    and servings into a dictionary'''
    recipes = []
    servings = {}
    
    for page in baked_goods_pages:
        worksheet = SHEET.worksheet(page)
        data = worksheet.get_all_values()
        servings[page] = data[0][2]
        recipe_data = [[column[0], column[2], column[1]] for column in data]
        recipes.append((page, recipe_data))
    return recipes, servings[page]

def show_menu_get_recipe():
    '''Show the menu with the recipes and return the recipe chosen'''
    title = 'Which recipe?'
    options = {
        'croissants',
        'pastel de nata',
        'portuguese rice flour cakes',
        'brownies',
        'Go back to main menu'
    }
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
        

def update_recipe_doses():
    print('''Update the recipe doses by multiplying the ingredients amount 
    with the number of servings''')
    


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
    for recipe_name, recipe_data in recipes:
        for ingredient, amount, unit in recipe_data:
            '''Check if the ingredient is already in the goals dictionary'''
            if ingredient in goals:
                goals[ingredient][0] += float(amount)
            else:
                goals[ingredient] = [float(amount), unit]

    '''Apply a 20% increase to all ingredient amounts'''
    goals_with_increase = {
        ingredient: [amount * 1.2, unit] for ingredient, (amount, unit) in goals.items()
    }
    print(goals_with_increase)
    
    # Transpose the data
    transposed_data = list(map(list, zip(*goals_with_increase.items())))
    print(transposed_data)

    '''Update the "recipe_goals" worksheet with the new values'''
    pantry_goals_worksheet = SHEET.worksheet('pantry_goals')
    pantry_goals_worksheet.clear()
    pantry_goals_worksheet.append_row(['Ingredient', 'Amount', 'Unit'])
    for key, (amount, unit) in goals_with_increase.items():
        pantry_goals_worksheet.append_row([key, amount, unit])
    return goals_with_increase

def get_shopping_list():
    '''Get the shopping list by subtracting pantry amounts 
    from pantry_goals amounts'''
    recipes = get_recipe('pantry_goals', 'pantry')
    
    pantry_goals_data = recipes[0][1]  # Data for pantry_goals
    pantry_data = recipes[1][1]       # Data for pantry

    pantry_goals = {row[0]: [float(row[1]), row[2]] for row in pantry_goals_data}
    pantry = {row[0]: [float(row[1]), row[2]] for row in pantry_data}
    
    shopping_list = {}
    
    for ingredient, (amount_goals, unit_goals) in pantry_goals.items():
        if ingredient in pantry:
            amount_pantry, unit_pantry = pantry[ingredient]
            if amount_pantry < amount_goals:
                shopping_list[ingredient] = (amount_goals - amount_pantry, unit_goals)
    
    if not shopping_list:
        print("No items to buy. Your pantry is well-stocked!")
    else:
        print("Shopping List:")
        for ingredient, (amount, unit) in shopping_list.items():
            print(f"{ingredient}: {amount} {unit}")
    


def register_shopped_groceries():
    print('Functionality for registering shopped groceries goes here.')


def main():
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

    while True:
        user_choice = menu_entry_index + 1

        if user_choice is not None:
            if user_choice == 1:
                get_shopping_list()
            elif user_choice == 2:
                register_shopped_groceries()
            elif user_choice == 3:
                update_recipe_doses()
            elif user_choice == 4:
                print(get_recipe(show_menu_get_recipe()))
            elif user_choice == 5:
                main()
                break


if __name__ == '__main__':
    main()