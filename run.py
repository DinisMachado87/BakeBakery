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


print_recipe('recipe_croisants')