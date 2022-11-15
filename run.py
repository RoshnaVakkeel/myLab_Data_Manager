import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint
import pandas as pd

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('mylab_data')

# Welcome message to the user
print('\nWelcome to MyLab Data Management Tool !!')
print('Your guide to locating and updating chemical inventory.\n')

# Connects to chem_inventory worksheet of myLab spreadsheet.
chem_inventory = SHEET.worksheet('chem_inventory')
data = chem_inventory.get_all_values()


def display_all():
    """
    Diplays all data upon selection 1.
    """
    print('Displaying all the chemicals in the list with its details \n')
    pprint(data)


def display_chem_keyword_search():
    """
    Diplays data matching Chemical Name keyword.
    Upon option 2 selection, user will be asked for keyword input.
    Upon input, all the rows containing the keyword will be shown.
    """
    print('Displaying chemicals and details based on chemical name / keyword search \n')
    df = pd.DataFrame(chem_inventory.get_all_records())

    while True:
        print("\nEnter chemical name you are looking for: ")
        i = input()

        if i.strip() != '':
            print("Oops! invalid entry. Try again..\n")
        else:
            print("Ok")
            
        if i not in df:
            df1 = df[df['Chemical Name'].str.contains(i)]
            print(df1)
            break



            
def display_destination_keyword_search():
    """'
    Diplays data matching destination keyword.
    Upon option 3 selection, user will be asked for keyword input.
    Upon input, all rows containing the keyword will be shown.
    """
    print('Displaying the chemicals and details based on destination search \n')
    df = pd.DataFrame(chem_inventory.get_all_records())

    print("Enter the destination name: ")
    i = input()

    if i not in df:
        df1 = df[df['Destination'].str.contains(i)]
        print(df1)
    else:
        print("Oops! invalid entry. Try again..") 


def display_quantity_search():
    """
    Diplays data matching quantity entered.
    Upon option 4 selection, user will be asked for keyword input.
    Upon input, all rows containing the keyword will be shown.
    """
    print('Displaying the chemicals and details based on destination search \n')
    df = pd.DataFrame(chem_inventory.get_all_records())

    print("Enter the the quantity of the chemical: ")
    i = input()

    if i not in df:
        df1 = df[df['Total Amount'].str.contains(i, case=False, na=False)]
        print(df1)
    else:
        print("Oops! Are you sure you entered the unit correctly?") 


def display_brand_search():
    """
    Diplays data matching brand name.
    Upon option 4 selection, user will be asked for keyword input.
    Upon input, all rows containing the keyword will be shown.
    """
    print('Displaying the chemicals and details based on destination search \n')
    df = pd.DataFrame(chem_inventory.get_all_records())

    print("Enter the the quantity of the chemical: ")
    i = input()

    if i not in df:
        df1 = df[df['Total Amount'].str.contains(i, case=False, na=False)]
        print(df1)     


# Set an initial value for selection other than the value for exit i.e. 8.
selection = ''

"""
Loop to run through the options and ask for user input.
When user selects an option by making an input, function will get triggered. 
"""
while(selection != '8'):
    #Providing users with options to select from.
    print('Get started by selecting from one of these options!!')
    print('1) Display all the chemicals chemical inventory with its details')
    print('2) Display the chemicals and details based on chemical name / keyword search')
    print('3) Display the chemicals and details based on destination search')
    print('4) Display the chemicals and details based on quantity search')
    print('5) Display the chemical details based on brand name')
    print('6) Update inventory list')
    print('7) Delete finished chemical details')
    print('8) Exit\n')

    # Ask for the user's selection.
    selection = (input("What do you want the Data Manager to do? "))

    # if else conditions for user selection
    
    if selection == '1':
        display_all()
    elif selection == '2':
        display_chem_keyword_search()
    elif selection == '3':
        display_destination_keyword_search()
    elif selection == '4':
        display_quantity_search()
    elif selection == '5':
        print('Displaying the chemicals and details based on brand name \n')
    elif selection == '6':
        print('Updating inventory list \n')
    elif selection == '7':
        print('Deleting the selected chemical details \n')
    elif selection == '8':
        print('You entered exit. See you later then!! \n')
    else:
        print('Appropriate number was not entered! Please select from the list provided.\n')
    break
