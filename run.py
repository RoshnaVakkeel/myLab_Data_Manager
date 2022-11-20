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

# Connects the worksheets of myLab spreadsheet.
chem_inventory = SHEET.worksheet('chem_inventory')
assess_list = SHEET.worksheet('assess')
storage_list = SHEET.worksheet('storage')
deleted_list = SHEET.worksheet('deleted_items')
manual_entry_list = SHEET.worksheet('manual_entry')

data = chem_inventory.get_all_values()


def display_all():
    """
    Diplays all chemical and details upon option 1 selection.
    """
    print('Displaying all the chemicals with their details \n')
    pprint(data)


def display_chem_keyword_search():
    """
    Diplays data matching Chemical Name keyword.
    Upon option 2 selection, user will be asked for keyword input.
    Upon input, all the rows containing the keyword will be shown.
    """
    df = pd.DataFrame(chem_inventory.get_all_records())

    print('\nEnter the chemical name you are looking for: ')
    i = input()
    if i not in df:
        print('Displaying the chemicals with their details \n')
        print(df[df['Chemical Name'].str.contains(i, case=False)])

    i = input('\nDid the search help you?[y/n]\n')
    if i == 'n':
        i = input('\nTry more specific keyword: \n')
        if i not in df:
            print('\nDisplaying chemicals and details:\n')
            print(df[df['Chemical Name'].str.match(i, case=False)])
            print('\nGreat! You got it now!!\n')
    elif i == 'y':
        print('Awesome!')
    else:
        print('Please enter y/n!')


def display_destination_keyword_search():
    """
    Displays data matching destination keyword.
    Upon option 3 selection, user will be asked for keyword input.
    Upon input, all rows containing the keyword will be shown.
    """
    df = pd.DataFrame(chem_inventory.get_all_records())

    print("Enter the destination name: ")
    i = input()

    if i not in df:
        df1 = df[df['Destination'].str.contains(i, case=False)]
        print('Displaying the chemicals based on destination search \n')
        print(df1)
        print('There you have it!!')
        print('List doesn\'t fully appear? try to be specific')


def display_quantity_search():
    """
    Diplays data matching quantity entered.
    Upon option 4 selection, user will be asked for keyword input.
    Upon input, all rows containing the keyword will be shown.
    """
    df = pd.DataFrame(chem_inventory.get_all_records())

    print("Enter the exact quantity of the chemical: ")
    i = input()

    if i not in df:
        df1 = df[df['Total Amount'].str.fullmatch(i, case=False, na=False)]
        print('Displaying the chemicals based on based on quantity search \n')
        print(df1)


def display_brand_search():
    """
    Diplays data matching brand name.
    Upon option 5 selection, user will be asked for keyword input.
    Upon input, all rows containing the keyword will be shown.
    """
    df = pd.DataFrame(chem_inventory.get_all_records())

    print("Enter the the brand name of the chemical: ")
    i = input()

    if i not in df:
        df1 = df[df['Brand'].str.contains(i, case=False, na=False)]
        print('Displaying the chemicals based on brand name search \n')
        print(df1)


def update_assess_worksheet():
    """
    Function to update "assess" worksheet.
    Upon option 6 selection, undefined bottles will be retrieved.
    The list will be updated in "assess" worksheet.
    """
    # create dataframe to append first row into the worksheet
    df1 = pd.DataFrame({
        'Chemical Name': ['Chemical Name'],
        'Brand': ['Brand'],
        'Total Amount': ['Total Amount'],
        'Amount remaining': ['Amount remaining'],
        'Destination': ['Destination']
        })
    df1_values = df1.values.tolist()
    SHEET.values_update(
        'assess',
        {'valueInputOption': 'RAW'},
        {'values': df1_values})

    # Retrieves undefined bottles to enter in assess_list
    df = pd.DataFrame(chem_inventory.get_all_records())
    df2 = df[df['Amount remaining'] == '']
    if True:
        print('\nUpdating assess list with retrieved data..\n')

    # concatanate two dataframes together
    sum_df = [df1, df2]
    df_undefined = pd.concat(sum_df)

    # Updates assess worksheet with retrieved data
    df_undefined_values = df_undefined.values.tolist()
    SHEET.values_update(
        'assess',
        {'valueInputOption': 'RAW'},
        {'values': df_undefined_values})
    pprint(df_undefined_values)


def update_storage_worksheet():
    """
    Function to update "storage" worksheet.
    Upon option 7 selection, full bottles will be retrieved.
    The list will be updated in "storage" worksheet.
    """
    # create dataframe to append first row into the worksheet
    df1 = pd.DataFrame({
        'Chemical Name': ['Chemical Name'],
        'Brand': ['Brand'],
        'Total Amount': ['Total Amount'],
        'Amount remaining': ['Amount remaining'],
        'Destination': ['Destination']
        })
    df1_values = df1.values.tolist()
    SHEET.values_update(
        'assess',
        {'valueInputOption': 'RAW'},
        {'values': df1_values}
        )

    # Retrieves full bottles to enter in storage_list
    df = pd.DataFrame(chem_inventory.get_all_records())
    df_same = df[df[['Total Amount', 'Amount remaining']].nunique(axis=1) == 1]

    # concatanate two dataframes together
    sum_df_same = [df1, df_same]
    pprint(sum_df_same)
    df_same_sum = pd.concat(sum_df_same)

    # Updates storage worksheet with retrieved data
    df_same_sum_values = df_same_sum.values.tolist()
    SHEET.values_update(
        'storage',
        {'valueInputOption': 'RAW'},
        {'values': df_same_sum_values})
    print('\nUpdating storage worksheet..\n')


def update_del_items_worksheet():
    """
    Function to update "deleted_items" worksheet.
    Upon option 8 selection, empty bottles will be retrieved.
    The list will be updated in "deleted_items" worksheet.
    """
    # create dataframe to append first row into the worksheet
    df1 = pd.DataFrame({
        'Chemical Name': ['Chemical Name'],
        'Brand': ['Brand'],
        'Total Amount': ['Total Amount'],
        'Amount remaining': ['Amount remaining'],
        'Destination': ['Destination']
        })

    df1_values = df1.values.tolist()
    SHEET.values_update(
        'deleted_items',
        {'valueInputOption': 'RAW'},
        {'values': df1_values}
        )

    # Retrieves undefined bottles to enter in assess_list
    df = pd.DataFrame(chem_inventory.get_all_records())
    df2 = df[(df['Amount remaining'] == '0 g')]
    df3 = df[(df['Amount remaining'] == '0 ml')]

    # concatanate two dataframes together
    sum_df = [df1, df2, df3]
    pprint(sum_df)
    df_deleted = pd.concat(sum_df)

    # Updates deleted_items worksheet with retrieved data
    df_deleted_values = df_deleted.values.tolist()
    SHEET.values_update(
        'deleted_items',
        {'valueInputOption': 'RAW'},
        {'values': df_deleted_values}
        )
    print('\nUpdating deleted_items worksheet..\n')


def update_manual_entry_worksheet():
    """
    Function to update "manual_entry" worksheet.
    Upon option 9 selection, user will be asked for input.
    User input will be appended to "manual_entry" worksheet.
    """
    # Manual input of data
    while True:
        print('Do you want to add data? Type in the values:')
        print('Chem name, Brand, Total Amt., Amt. left, Destination')
        data_manual = input('Enter your data here: \n')

        processed_data = data_manual.split(",")
        print(processed_data)

        if validate_data(processed_data):
            print('Data is valid!')
            print("Updating manual_entry worksheet...\n")
            manual_entry_worksheet = SHEET.worksheet('manual_entry')
            manual_entry_worksheet.append_row(processed_data)
            print("manual_entry worksheet updated successfully.\n")
            break

    return processed_data


def validate_data(values):
    """
    Raises ValueError if entries aren't exactly 5 values.
    """
    try:
        [value for value in values]
        if len(values) != 5:
            raise ValueError(
                f"Exactly 5 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid input: {e}, please try again.\n")
        return False

    return True


def main():
    # Set an initial value for selection other than the value for exit i.e. 10.
    selection = ''
    """
    Loop to run through the options and ask for user input.
    When user selects an option, these functions will get triggered.
    """
    while (selection != '10'):
        # Providing users with options to select from.
        print('\nSelect a number matching your option!!\n')
        print('1) Display all the chemical detail from chemical inventory')
        print('2) Display the chemical details based on keyword search')
        print('3) Display the chemical details based on destination search')
        print('4) Display the chemical details based on quantity search')
        print('5) Display the chemical details based on brand name')
        print('6) Update assess list with undefined amounts')
        print('7) Update storage list with unused bottles')
        print('8) Update deleted list with empty bottles')
        print('9) Update manual entry sheet with manual input')
        print('10) Exit\n')

        # Ask for the user's selection.
        selection = (input("What do you want the Data Manager to do? \n"))

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
            display_brand_search()
        elif selection == '6':
            update_assess_worksheet()
        elif selection == '7':
            update_storage_worksheet()
        elif selection == '8':
            update_del_items_worksheet()
        elif selection == '9':
            update_manual_entry_worksheet()
        elif selection == '10':
            print('You entered exit. See you later then!! \n')
        else:
            print('Please select from the list provided!\n')


# Welcome message to the user
print('\n         Welcome to MyLab Data Management Tool!!        ')
print(' - Your guide to locating and updating chemical inventory  -\n')
main()
