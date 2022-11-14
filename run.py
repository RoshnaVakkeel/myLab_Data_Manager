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
SHEET = GSPREAD_CLIENT.open('mylab_data')

chem_inventory = SHEET.worksheet('chem_inventory')
data = chem_inventory.get_all_values()
#print(data)

# Welcome message to the user
print('\nWelcome to MyLab Data Management Tool !!')
print('Your guide to locating and updating chemical inventory.\n')

"""
Providing users with options to select from.
"""

# Set an initial value for selection other than the value for exit i.e. 8.

selection = ''

"""
Loop to run through the options.
"""
while(selection != '8'):

    print('1) Display all the chemicals in the list with its details')
    print('2) Display the chemical category with its details using typed in keyword')
    print('3) Display the selected chemical with its details (using full chemical name')
    print('4) Display the chemical list based on total quantity (using typed in keyword')
    print('5) Display the chemical based on its location (using typed in keyword')
    print('6) Update inventory list')
    print('7) Delete finished chemical details')
    print('8) Exit\n')

    # Ask for the user's selection.
    selection = (input("What do you want the Data Manager to do?  "))

    # if else conditions for user selection
    
    if selection == '1':
        print('Displaying all the chemicals in the list with its details \n')
    elif selection == '2':
        print('Displaying the chemical category with its details (using typed in keyword) \n')
    elif selection == '3':
        print('Displaying the selected chemical with its details (using full chemical name) \n')
    elif selection == '4':
        print('Displaying the chemical list based on total quantity (using typed in keyword) \n')
    elif selection == '5':
        print('Displaying the chemical based on its location (using typed in keyword) \n')
    elif selection == '6':
        print('Updating inventory list \n')
    elif selection == '7':
        print('Deleting the selected chemical details \n')
    elif selection == '8':
        print('Exit \n')
    else:
        print('Appropriate number was not entered! Please select from the list provided.')
    break


