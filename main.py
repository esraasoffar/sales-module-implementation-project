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


def create_sale_order(customers, products):
    # Select customer
    list_customers(customers)
    try:
        cust_idx = int(input("Enter customer number: ")) - 1
        customer = customers[cust_idx]
    except:
        print("Invalid selection.")
        return None

    sale_order = SaleOrder(customer)
    print(f"\nSale Order Created for {customer.name}\n")

    # Add products
    while True:
        list_products(products)
        product_input = input("\nEnter product number to add (or 'done' to finish): ")

        if product_input.lower() == "done":
            break

        # Select product
        try:
            prod_idx = int(product_input) - 1
            if prod_idx not in range(len(products)):
                print("Invalid product number, try again.")
                continue
            product = products[prod_idx]
        except:
            print("Invalid product input, try again.")
            continue

        # Select quantity
        try:
            qty = int(input("Enter quantity: "))
            if qty <= 0:
                print("Quantity must be positive.")
                continue
        except:
            print("Invalid quantity. Enter a number.")
            continue

        # Validate stock
        if qty > product.quantity:
            print(f"Error: Not enough stock for {product.name}. "
                  f"Available: {product.quantity}, Requested: {qty}")
            continue

        # Add line
        try:
            sale_order.add_line(product, qty)
            print(f"Added {qty} x {product.name} to order.\n")
        except Exception as e:
            print("Error:", e)

    # Show order summary
    if not sale_order.lines:
        print("No products added. Order discarded.")
        return None

    print("\nSale Order Lines:")
    for line in sale_order.lines:
        print(f"- {line.product.name}: {line.quantity} pcs (Subtotal: {line.subtotal})")

    print(f"\nOrder Total = {sale_order.compute_total()}")

    # Confirm order
    confirm = input("\nConfirm order? (yes/no): ").strip().lower()
    if confirm == "yes":
        try:
            sale_order.confirm()
            print("Order confirmed successfully!")
        except Exception as e:
            print("Error:", e)
    else:
        print("Order saved as DRAFT.")

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

    while True:
        print("\n=== Sales System ===")
        print("1. Create Sale Order")
        print("2. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            create_sale_order(customers, products)
        elif choice == "2":
            print("Goodbye.")
            break
        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    main()
