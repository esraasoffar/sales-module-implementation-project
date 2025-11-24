from customer import Customer
from product import Product
from sale_order import SaleOrder
from invoice import Invoice
from customer import Customer


def list_products(products):
    print("\nAvailable Products:")
    for i, p in enumerate(products, start=1):
        print(f"{i}. {p.name} - ${p.price} - Stock: {p.quantity}")


def list_customers(customers):
    print("\nSelect Customer:")
    for i, c in enumerate(customers, start=1):
        print(f"{i}. {c.name}")
def cancel_order(orders):
    """Cancel a confirmed order and restore stock."""
    confirmed_orders = [o for o in orders if o.state == "confirmed"]
    if not confirmed_orders:
        print("No confirmed orders to cancel.")
        return

    print("\nConfirmed Orders:")
    for i, order in enumerate(confirmed_orders, start=1):
        print(f"{i}. {order.customer.name} - Total: {order.compute_total()}")

    try:
        idx = int(input("Select order to cancel: ")) - 1
        order_to_cancel = confirmed_orders[idx]
    except:
        print("Invalid selection.")
        return

    confirm = input(f"Are you sure you want to cancel the order for {order_to_cancel.customer.name}? (yes/no): ").strip().lower()
    if confirm == "yes":
        for line in order_to_cancel.lines:
            line.product.increase_stock(line.quantity)
        order_to_cancel.state = "canceled"
        print("Order canceled. Stock has been restored.")
    else:
        print("Order not canceled.")

def create_sale_order(customers, products, existing_order=None):
    # Resume draft or create new
    if existing_order:
        sale_order = existing_order
        print(f"\nResuming Draft Order for {sale_order.customer.name}\n")
    else:
        list_customers(customers)
        try:
            cust_idx = int(input("Enter customer number: ")) - 1
            customer = customers[cust_idx]
        except:
            print("Invalid selection.")
            return None

        sale_order = SaleOrder(customer)
        print(f"\nSale Order Created for {customer.name}\n")

    while True:
        print("\n--- Order Menu ---")
        print("1. Add product")
        print("2. Remove product")
        print("3. View current order")
        print("4. Finish order (save as draft)")
        print("5. Confirm order")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            # Add product
            list_products(products)
            try:
                prod_idx = int(input("Enter product number to add: ")) - 1
                product = products[prod_idx]
            except:
                print("Invalid product number.")
                continue

            try:
                qty = int(input("Enter quantity: "))
                if qty <= 0:
                    print("Quantity must be positive.")
                    continue
            except:
                print("Invalid quantity.")
                continue

            if qty > product.quantity:
                print(f"Error: Not enough stock for {product.name}. "
                      f"Available: {product.quantity}, Requested: {qty}")
                continue

            try:
                sale_order.add_line(product, qty)
                print(f"Added {qty} x {product.name} to order.\n")
            except Exception as e:
                print("Error:", e)

        elif choice == "3":
            # View current order
            if not sale_order.lines:
                print("No products in order.")
                continue
            print("\nCurrent Sale Order Lines:")
            for line in sale_order.lines:
                print(f"- {line.product.name}: {line.quantity} pcs (Subtotal: {line.subtotal})")
            print(f"Order Total = {sale_order.compute_total()}")



        elif choice == "4":

            # Finish order (draft)

            sale_order.state = "draft"

            print("\nOrder saved as DRAFT.")

            return sale_order

        elif choice == "5":
            # Confirm order
            if not sale_order.lines:
                print("Cannot confirm empty order.")
                continue
            try:
                sale_order.confirm()
                print("Order confirmed successfully!")
            except Exception as e:
                print("Error:", e)
            break  # Return to main menu


        else:
            print("Invalid option, try again.")

    return sale_order


def main():
    # Sample customers
    customers = [
        Customer("Alice", "alice@email.com"),
        Customer("Bob", "bob@email.com")
    ]

    # Sample products
    products = [
        Product("Laptop", 25000, 10),
        Product("Mouse", 250, 50),
        Product("Keyboard", 500, 30)
    ]


    # Sample Invoices for testing show invoices
    invoice_alice = Invoice(name="INV001", customer=customers[0], sale_order=None)
    invoice_alice.add_line(products[0], 1)
    invoice_alice.post()
    customers[0].add_invoice(invoice_alice)

    invoice_bob = Invoice(name="INV002", customer=customers[1], sale_order=None)
    invoice_bob.add_line(products[1], 5)
    customers[1].add_invoice(invoice_bob)


    orders = []  # Keep all orders

    while True:
        print("\n=== Sales System ===")
        print("1. Create Sale Order")
        print("2. Add New Customer")   # New option
        print("3. Resume Draft Order")
        print("4. View All Orders")
        print("5. Show Customer Invoices")
        print("6. Cancel Confirmed Order")
        print("7. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            order = create_sale_order(customers, products)
            if order:
                orders.append(order)
        elif choice == "2":
            # Add a new customer
            name = input("Enter customer name: ").strip()
            email = input("Enter customer email: ").strip()
            if name and email:
                new_customer = Customer(name, email)
                customers.append(new_customer)
                print(f"Customer '{name}' added successfully.")
            else:
                print("Invalid input. Customer not added.")
        elif choice == "3":
            draft_orders = [o for o in orders if o.state == "draft"]
            if not draft_orders:
                print("No draft orders available.")
                continue

            print("\nDraft Orders:")
            for i, o in enumerate(draft_orders, start=1):
                print(f"{i}. {o.customer.name} - Total: {o.compute_total()}")

            try:
                idx = int(input("Select draft order to resume: ")) - 1
                order = draft_orders[idx]
            except:
                print("Invalid selection.")
                continue

            updated_order = create_sale_order(customers, products, existing_order=order)
            orders[orders.index(order)] = updated_order  # Update the order in list

        elif choice == "4":
            if not orders:
                print("No orders yet.")
                continue
            print("\nAll Orders:")
            for i, order in enumerate(orders, start=1):
                cust_name = order.customer.name if order else "Unknown"
                state = order.state if order else "Unknown"
                total = order.compute_total() if order else 0
                print(f"{i}. {cust_name} - {state} - Total: {total}")


        elif choice == "5":
            list_customers(customers)
            try:
                cust_idx = int(input("Enter customer number to view invoices: ")) - 1
                customer = customers[cust_idx]
            except (ValueError, IndexError):
                print("Invalid selection.")
                continue

            print(f"\n--- Invoices for {customer.name} ---")
            customer.show_invoices()
            print("---------------------------------")
            # -----------------------------------------------
        elif choice == "6":
            cancel_order(orders)
        elif choice == "7":
            print("Goodbye.")
            break

        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    main()
