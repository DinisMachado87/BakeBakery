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
    '''Clears the terminal screen'''
    os.system('cls' if os.name == 'nt' else 'clear')


def print_ingridients():
    '''Prints the ingredients of the recipe chosen'''
    print('''\n What recipe do you want to see?\n''')
    recipes = get_recipe(show_menu_get_recipe())
    clear_terminal()
    for recipe in recipes:
        ingredients, servings, recipe_name = recipe
        print(f'\n {recipe_name} : \n')
        for ingredient in ingredients:
            print(f'{ingredient[0]}: {ingredient[1]} {ingredient[2]}')
        print('\n')
    main_menu()


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
        main_menu()


def verify_input(user_input):
    """
    Verify if the input is a non-negative
    integer or float and not an empty string.
    """
    try:
        # Check if the input is a numeric value
        input_numeric = float(user_input)

        # Check if the input is non-negative
        if input_numeric < 0:
            raise ValueError("Please enter a non-negative number.")

        # Check if the input is an integer or float
        if input_numeric.is_integer():
            return int(input_numeric)
        else:
            return input_numeric
    except ValueError:
        return None


def get_valid_input(prompt):
    """Get user input and verify its correctness."""
    while True:
        user_input = input(prompt).strip()

        '''
        Check if the input length is greater than 0
        after stripping whitespaces
        '''
        if len(user_input) > 0:
            verified_input = verify_input(user_input)

            # Check if the input is valid
            if verified_input is not None:
                return verified_input
            else:
                print("Invalid input. Please enter a non-negative number.")
        else:
            print("Input cannot be empty. Please try again.")


def update_pantry_goals():
    '''
    Actualizes pantry goals adding ingredients from all recipes
    and adding 20% to each ingredient
    '''
    print('\n Hold on! We are updating the pantry goals...\n')
    recipes = get_recipe(
        'recipe_croissants',
        'recipe_pastel_de_nata',
        'recipe_portuguese_rice_flour_cakes',
        'recipe_brownies'
    )
    # Create a dictionary with the ingredients and amounts
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
    pantry_goals_worksheet.append_row(['Ingredient', 'Unit', 'Amount'])
    for ingredient, (amount, unit) in goals_with_increase.items():
        pantry_goals_worksheet.append_row([ingredient, unit, amount])

    print('\nYour pantry goals have been updated!')
    return goals_with_increase


def update_recipe_doses():
    '''
    Update the recipe doses by multiplying the ingredients amount
    with the number of servings
    '''
    print('''\n What recipe do you want to update?''')
    recipes = get_recipe(show_menu_get_recipe())
    clear_terminal()
    servings_input = get_valid_input(
        '''
Enter the number of servings you want to resize the recipe for :
        '''
        )

    clear_terminal()
    for recipe in recipes:
        ingredients, servings, recipe_name = recipe

        # Create a list with the updated ingredients
        updated_recipe = []

        # Multiply the amount of each ingredient by the number of servings
        for ingredient, amount, unit in ingredients:
            updated_amount = (
                float(servings_input) *
                float(amount) /
                float(servings)
            )
            updated_recipe.append([ingredient, unit, updated_amount])

        # Print the updated recipe
        print(f'{recipe_name} updated recipe:\n')
        for column in updated_recipe:
            print(f'{column[0]}: {column[1]} {column[2]}')

        print('\n Hold on! We are saving the changes to the spreadsheet...\n')

        # Update the "recipe_goals" worksheet with the new values
        worksheet_to_update = SHEET.worksheet(recipe_name)
        worksheet_to_update.clear()

        for ingredient, unit, updated_amount in updated_recipe:
            worksheet_to_update.append_row([ingredient, unit, updated_amount])


def get_shopping_list():
    '''
    Get the shopping list by subtracting pantry amounts
    from pantry_goals amounts
    '''
    # Get the pantry and pantry_goals data
    recipes = get_recipe('pantry_goals', 'pantry')
    pantry_goals_data = recipes[0][0][2:]  # Skip the header row
    pantry_data = recipes[1][0][2:]       # Skip the header row

    # Create a dictionary with the pantry_goals and pantry data
    pantry_goals = {
        row[0]: [float(row[1]), row[2]] for row in pantry_goals_data
    }
    pantry = {row[0]: [float(row[1]), row[2]] for row in pantry_data}

    # Create a dictionary with the shopping list
    shopping_list = {}

    # Subtract the pantry amounts from the pantry_goals amounts
    for ingredient_goals, (amount_goals, unit_goals) in pantry_goals.items():
        if ingredient_goals in pantry:
            amount_pantry, unit_pantry = pantry[ingredient_goals]
            if amount_pantry < amount_goals:
                shopping_list[ingredient_goals] = (
                    amount_goals - amount_pantry, unit_goals
                )

    # Check if the shopping list is empty
    if not shopping_list:
        print("Your pantry is sorted. There is nothing you need to buy!")

    return shopping_list


def register_shopped_groceries():
    '''
    create a list with the shopped groceries and update the pantry
    '''

    # Create a list with the shopped groceries through user input
    amount_shopped = []

    print('Enter the amount of each ingredient shopped:\n')

    flour = get_valid_input("flour (g): ")
    milk = get_valid_input("milk (ml): ")
    sugar = get_valid_input("sugar (g): ")
    salt = get_valid_input("salt (g): ")
    butter = get_valid_input("butter (g): ")
    yeast = get_valid_input("yeast (g): ")
    chocolate_chips = get_valid_input("chocolate chips (g): ")
    puff_pastry = get_valid_input("puff pastry (sheets): ")
    egg = get_valid_input("egg (units): ")
    cornstarch = get_valid_input("cornstarch (g): ")
    vanilla_extract = get_valid_input("vanilla extract (ml): ")
    cinnamon = get_valid_input("cinnamon (g): ")
    rice_flour = get_valid_input("rice flour (g): ")
    eggs = get_valid_input("eggs (units): ")
    lemon = get_valid_input("lemon (units): ")
    cocoa = get_valid_input("cocoa (g): ")

    amount_shopped.extend([
        ["flour", "g", flour],
        ["milk", "ml", milk],
        ["sugar", "g", sugar],
        ["salt", "g", salt],
        ["butter", "g", butter],
        ["yeast", "g", yeast],
        ["chocolate chips", "g", chocolate_chips],
        ["puff pastry", "sheets", puff_pastry],
        ["egg", "units", egg],
        ["cornstarch", "g", cornstarch],
        ["vanilla extract", "ml", vanilla_extract],
        ["cinnamon", "g", cinnamon],
        ["rice flour", "g", rice_flour],
        ["eggs", "units", eggs],
        ["lemon", "units", lemon],
        ["cocoa", "g", cocoa],
    ])

    print('\n Hold on! We are saving the changes to the pantry database...\n')

    # Get the pantry content
    pantry = get_recipe('pantry')
    pantry_content = pantry[0][0][2:]
    updated_pantry = []

    # Add the amounts from pantry and amount_shopped
    for row in pantry_content:
        ingredient, amount, unit = row
        # Find the corresponding amount_shopped value for the ingredient
        amount_shopped_value = next(
            (item[2] for item in amount_shopped if item[0] == ingredient), 0
        )
        # Add the amounts from pantry and amount_shopped
        updated_amount = float(amount) + amount_shopped_value
        updated_pantry.append([ingredient, unit, updated_amount])

    # Update the "pantry" worksheet with the new values
    pantry_worksheet = SHEET.worksheet('pantry')
    pantry_worksheet.clear()
    pantry_worksheet.append_row(['Ingredient', 'Unit', 'Amount'])
    for ingredient, unit, amount in updated_pantry:
        pantry_worksheet.append_row([ingredient, unit, amount])

    print('\nYour pantry has been updated!')


def register_cooked_recipe():
    '''
    Subtracts from the pantry
    the expended ingredients in a recipe selected
    '''

    # Get the recipe details
    recipe = get_recipe(show_menu_get_recipe())
    print(f'\n Hold on! We are updating the pantry...\n')
    ingredients_to_subtract = recipe[0][0][1:]

    updated_pantry = []

    # Get the pantry content
    pantry = get_recipe('pantry')
    pantry_content = pantry[0][0][1:]

    for pantry_row, spent_row in zip(pantry_content, ingredients_to_subtract):
        pantry_ingredient, pantry_amount, pantry_unit = pantry_row
        ingredient, amount, unit = spent_row

        # Find the corresponding pantry value for the ingredient
        pantry_value = next(
            (item[2] for item in pantry_content if item[0] == ingredient), 0
        )
        # Subtract the expended amount from the pantry
        updated_amount = float(pantry_amount) - float(amount)
        updated_pantry.append([ingredient, unit, updated_amount])

    # Update the "pantry" worksheet with the new values
    pantry_worksheet = SHEET.worksheet('pantry')
    pantry_worksheet.clear()
    pantry_worksheet.append_row(['Ingredient', 'Unit', 'Amount'])
    for ingredient, unit, amount in updated_pantry:
        pantry_worksheet.append_row([ingredient, unit, amount])

    print('\nYour pantry has been updated!')


def main_menu():
    '''Main menu function that calls the other functions'''
    title = 'What would you like to do?'
    print(f'\n{title}\n')
    options = [
        'Get Shopping List',
        'Register Shopped Groceries',
        'Update Recipe Doses',
        'Get Recipe',
        'register cooked recipe expended goods',
        'Exit'
    ]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()

    while True:
        user_choice = menu_entry_index

        if user_choice is not None:
            if user_choice == 0:
                clear_terminal()
                get_shopping_list()
                main_menu()
            elif user_choice == 1:
                clear_terminal()
                register_shopped_groceries()
                main_menu()
            elif user_choice == 2:
                clear_terminal()
                update_recipe_doses()
                update_pantry_goals()
                main_menu()
            elif user_choice == 3:
                clear_terminal()
                print_ingridients()
                main_menu()
            elif user_choice == 4:
                clear_terminal()
                register_cooked_recipe()
                main_menu()
            elif user_choice == 5:
                print('Goodbye!')
                break


def main():
    '''Runs a welcome message and the main menu function'''
    print('''
    Welcome to Bakery Bake!
    This is a tool to help you manage your bakery's pantry.
    It will be your right hand managing recipes,
    pantry goals, and shopping lists for your bakery.
    It will help you to interact with recipes,
    update pantry goals based on recipes,
    get shopping lists, register shopped groceries,
    and more.
    Just navigate the menu with the arrows, type,
    and click enter for choices!!!
    ''')
    main_menu()


if __name__ == '__main__':
    main()
