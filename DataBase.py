import csv
import os

# File paths
IMPORTED_FILE = 'imported.csv'
EXPORTED_FILE = 'exported.csv'
BILL_FILE = 'bill.csv'

# Create CSV files if not exist
def create_csv_if_not_exists(filename, headers):
    if not os.path.exists(filename):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)

create_csv_if_not_exists(IMPORTED_FILE, ['ItemID', 'ItemName', 'Quantity', 'Price'])
create_csv_if_not_exists(EXPORTED_FILE, ['ItemID', 'ItemName', 'Quantity', 'Price'])
create_csv_if_not_exists(BILL_FILE, ['BuyerName', 'ItemID', 'ItemName', 'Quantity', 'Price', 'Total'])

# Owner Functions
def add_imported_item():
    item_id = input("Enter Item ID: ")
    name = input("Enter Item Name: ")
    qty = int(input("Enter Quantity: "))
    price = float(input("Enter Price: "))

    with open(IMPORTED_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([item_id, name, qty, price])
    print("Item added to imported stock.")

def export_item():
    item_id = input("Enter Item ID to export: ")
    found = False

    rows = []
    with open(IMPORTED_FILE, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['ItemID'] == item_id:
                found = True
                with open(EXPORTED_FILE, 'a', newline='') as exp_file:
                    writer = csv.writer(exp_file)
                    writer.writerow([row['ItemID'], row['ItemName'], row['Quantity'], row['Price']])
                print("Item exported for sale.")
            else:
                rows.append(row)

    with open(IMPORTED_FILE, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['ItemID', 'ItemName', 'Quantity', 'Price'])
        writer.writeheader()
        writer.writerows(rows)

    if not found:
        print("Item ID not found in imported stock.")

# Buyer Function
def buy_item():
    buyer = input("Enter your name: ")
    cart = []

    # Load exported items into a dictionary for easy lookup
    with open(EXPORTED_FILE, 'r') as file:
        reader = csv.DictReader(file)
        stock = {row['ItemID']: row for row in reader}

    # Show available stock
    print("\nAvailable Items:")
    print(f"{'ID':<6} {'Name':<15} {'Qty':<8} {'Price'}")
    for item in stock.values():
        print(f"{item['ItemID']:<6} {item['ItemName']:<15} {item['Quantity']:<8} ₹{item['Price']}")

    while True:
        entry = input("\nEnter 'ItemID Quantity' to add to cart or type 'done' to checkout: ").strip()
        if entry.lower() == 'done':
            break
        try:
            item_id, qty = entry.split()
            qty = int(qty)

            if item_id not in stock:
                print("Item ID not found.")
                continue

            available = int(stock[item_id]['Quantity'])
            if qty > available:
                print("Not enough quantity in stock.")
                continue

            cart.append({
                'ItemID': item_id,
                'ItemName': stock[item_id]['ItemName'],
                'Quantity': qty,
                'Price': float(stock[item_id]['Price']),
                'Total': qty * float(stock[item_id]['Price'])
            })

            # Deduct stock
            stock[item_id]['Quantity'] = str(available - qty)
            print(f"Added {qty} x {stock[item_id]['ItemName']} to cart.")

        except ValueError:
            print("Invalid input format. Use: ItemID Quantity")

    if not cart:
        print("Cart is empty. No purchase made.")
        return

    # Write to bill.csv
    with open(BILL_FILE, 'a', newline='') as bill_file:
        writer = csv.writer(bill_file)
        for item in cart:
            writer.writerow([buyer, item['ItemID'], item['ItemName'], item['Quantity'], item['Price'], item['Total']])

    # Update exported stock file
    with open(EXPORTED_FILE, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['ItemID', 'ItemName', 'Quantity', 'Price'])
        writer.writeheader()
        for item in stock.values():
            writer.writerow(item)

    # Show bill summary
    print(f"Bill for {buyer}:")
    grand_total = 0
    for item in cart:
        print(f"{item['Quantity']} x {item['ItemName']} @ ₹{item['Price']} = ₹{item['Total']}")
        grand_total += item['Total']
    print(f"TOTAL: ₹{grand_total}")


# Dealer View
def dealer_view():
    print("\n--- IMPORTED STOCK ---")
    with open(IMPORTED_FILE, 'r') as file:
        print(file.read())

    print("\n--- EXPORTED STOCK ---")
    with open(EXPORTED_FILE, 'r') as file:
        print(file.read())

# Main Program
def main():
    while True:
        print("\nLogin as:")
        print("1. Owner")
        print("2. Dealer")
        print("3. Buyer")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            while True:
                print("\n OWNER MENU")
                print("1. Add Imported Item")
                print("2. Export Item for Sale")
                print("3. Finish (Back to Main Menu)")
                opt = input("Choose: ")

                if opt == '1':
                    add_imported_item()
                elif opt == '2':
                    export_item()
                elif opt == '3':
                    print("⬅Returning to main menu.")
                    break
                else:
                    print("Invalid input. Try again.")

        elif choice == '2':
            dealer_view()

        elif choice == '3':
            buy_item()

        elif choice == '4':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid input. Try again.")

if __name__ == '__main__':
    main()
