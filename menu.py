from simple_term_menu import TerminalMenu
from run import get_shopping_list, register_shopped_groceries, update_recipe_doses, print_recipe


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

def main_menu():
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