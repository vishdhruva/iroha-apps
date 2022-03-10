# import functions from CLI.ipynb
from tinyfunctions import add_asset_quantity, create_asset, transfer_assets, account_assets, create_account
# CLI
while (True):
    print("""Choose option: 
    1. Create asset
    2. Add asset quantity
    3. Account assets
    4. Transfer assets
    5. Create account
    6. Exit""")
    option = input()
    if option == "1":
        create_asset(input("Enter asset name: "))
    elif option == "2":
        add_asset_quantity(input("Enter asset name: "),input("Enter amount: "))
    elif option == "3":
        account_assets(input("Enter account id: "))
    elif option == "4":
        transfer_assets(input("Enter source account id: "),input("Enter destination account id: "),input("Enter asset id: "),input("Enter amount: "))
    elif option == "5":
        create_account(input("Enter account name: "))
    elif option == "6":
        break
    else:
        print("Invalid option\n")
