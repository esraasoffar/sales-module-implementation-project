from customer import Customer
from product import Product
from sale_order import SaleOrder


def list_products(products):
    print("\nAvailable Products:")
    for i, p in enumerate(products, start=1):
        print(f"{i}. {p.name} - ${p.price} - Stock: {p.quantity}")


def list_customers(customers):
    print("\nSelect Customer:")
    for i, c in enumerate(customers, start=1):
        print(f"{i}. {c.name}")


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

        elif choice == "2":
            # Remove product
            if not sale_order.lines:
                print("No products in order to remove.")
                continue

            print("\nCurrent Order Lines:")
            for i, line in enumerate(sale_order.lines, start=1):
                print(f"{i}. {line.product.name} - Qty: {line.quantity}")

            try:
                remove_idx = int(input("Enter line number to remove: ")) - 1
                removed_line = sale_order.lines.pop(remove_idx)
                print(f"Removed {removed_line.product.name} from order.\n")
            except:
                print("Invalid input.")

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
            # Finish as draft
            sale_order.state = "draft"
            print("\nOrder saved as DRAFT.")
            if sale_order.lines:
                print("Order Summary:")
                for line in sale_order.lines:
                    print(f"- {line.product.name}: {line.quantity} pcs (Subtotal: {line.subtotal})")
                print(f"Order Total = {sale_order.compute_total()}")
            break  # Return to main menu

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

    orders = []  # Keep all orders

    while True:
        print("\n=== Sales System ===")
        print("1. Create Sale Order")
        print("2. Resume Draft Order")
        print("3. View All Orders")
        print("4. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            order = create_sale_order(customers, products)
            if order:
                orders.append(order)

        elif choice == "2":
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

        elif choice == "3":
            if not orders:
                print("No orders yet.")
                continue
            print("\nAll Orders:")
            for i, order in enumerate(orders, start=1):
                print(f"{i}. {order.customer.name} - {order.state} - Total: {order.compute_total()}")

        elif choice == "4":
            print("Goodbye.")
            break

        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    main()
