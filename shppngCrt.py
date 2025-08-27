import argparse
from cart.cart import ShoppingCart
from database.logger import DBLogger
from uis.themes import ThemeState
import tkinter as tk
from gui.gui import GUI
import json
from dotenv import load_dotenv
import os

load_dotenv()

TUNGCART_DB = {
    "dbname": os.getenv("DB_NAME", ":) Your DB Name Here :)"),
    "user": os.getenv("DB_USER", ":) Your DB User Name Here :)"),
    "password": os.getenv("DB_PASSWORD", ":) Your Password Here :)"),
    "host": os.getenv("DB_HOST", ":) Your DC Host Here :)"),
    "port": int(os.getenv("DB_PORT", 5432))  #5432 (default, but you can write your db port)
}

#--------------------------- OPTIONAL (CLI-SECTON) ---------------------------#
def run_cli():
    db = DBLogger(TUNGCART_DB)
    cart = ShoppingCart(db_logger=db)
    while True:
        print("\n=*=*=*=*=*= Tungshoop SHOPPING CART MENU =*=*=*=*=*=")
        print("1. View Products")
        print("2. Add Product to Cart")
        print("3. View Cart")
        print("4. Update Quantity in Cart")
        print("5. Remove Item from Cart")
        print("6. Clear Cart")
        print("7. Checkout")
        print("8. Exit")
        choice = input("Please, Enter your choice here: ")
        if choice == "1":
            print("💨'View Products' Selected. Let's check the Products!")
            cart.display_products()
        elif choice == "2":
            print("💨'Add Product to Cart' Selected. Please, enter your Product ID!")
            prdctID = input("Enter Product ID: ")
            try:
                qntty = int(input("Enter Quantity: "))
                cart.add_item(prdctID, qntty)
            except ValueError:
                print("❌ Ooopsss.. Please, enter a valid number!")
        elif choice == "3":
            print("💨'View Cart' Selected. View the Cart!")
            cart.display_cart()
        elif choice == "4":
            print("💨'Update Quantity in Cart' Selected. That'll increase your Quantity!")
            prdctID = input("Enter Product ID: ")
            try:
                qntty = int(input("Enter New Quantity: "))
                cart.update_quantity(prdctID, qntty)
            except ValueError:
                print("❌ Ooopsss.. Please, enter a valid number!")
        elif choice == "5":
            print("💨'Remove Item from Cart' Selected. Remove the already selected item(s) from the Cart!")
            prdctID = input("Enter Product ID to remove: ")
            cart.remove_item(prdctID)
        elif choice == "6":
            print("💨'Clear Cart' Selected. Bye Bye to All Carts!")
            cart.clear_cart()
        elif choice == "7":
            print("💨'Checkout' Selected. Checkout the Cart!")
            cart.display_cart()
            print("💳 Checkout complete. Thank you for shopping with us!")
            cart.clear_cart()
        elif choice == "8":
            print("💨'Exit' Selected. See you later, right?!")
            print("👋 Exiting... Have a great day! Come again!")
            break
        else:
            print("⚠️ Invalid choice, please try again..!")


#--------------------------- OPTIONAL (CLI-SECTON) ---------------------------#

def run_gui():
    db = DBLogger(TUNGCART_DB)
    cart = ShoppingCart(db_logger=db)
    theme = ThemeState()
    root = tk.Tk()
    GUI(root, cart, theme)
    root.mainloop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tungshoop – Shopping Cart")
    parser.add_argument("--cli", action="store_true", help="Run in CLI mode instead of GUI")
    args = parser.parse_args()

    if args.cli:
        run_cli()
    else:
        run_gui()
