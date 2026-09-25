from services.category_service import (
    add_category,
    get_categories
)

from services.supplier_service import (
    add_supplier,
    get_suppliers
)

from services.product_service import (
    add_product,
    get_products,
    find_product,
    update_product,
    delete_product
)

from services.purchase_service import (
    record_purchase
)

from services.sales_servies import (
    record_sale
)

from services.report_service import (
    inventory_report,
    sales_report,
    supplier_report,
    low_stock_report
)

from utils.validators import (
    get_positive_integer,
    get_non_negative_integer,
    get_positive_float
)


def display_header():
    print("\n" + "=" * 55)
    print("          INVENTORY MANAGEMENT SYSTEM")
    print("=" * 55)


def display_menu():
    print("\n1. Add Category")
    print("2. Add Supplier")
    print("3. Add Product")
    print("4. View Products")
    print("5. Update Product")
    print("6. Delete Product")
    print("7. Record Purchase")
    print("8. Record Sale")
    print("9. View Low Stock")
    print("10. Sales Report")
    print("11. Inventory Report")
    print("12. Supplier Report")
    print("13. Exit")


def add_category_menu():
    print("\n========== ADD CATEGORY ==========")

    name = input("Category name: ").strip()

    if not name:
        print("Category name cannot be empty.")
        return

    add_category(name)


def add_supplier_menu():
    print("\n========== ADD SUPPLIER ==========")

    name = input("Supplier name: ").strip()
    phone = input("Phone: ").strip()
    email = input("Email: ").strip()
    address = input("Address: ").strip()

    if not name:
        print("Supplier name cannot be empty.")
        return

    add_supplier(
        name,
        phone,
        email,
        address
    )


def add_product_menu():
    print("\n========== ADD PRODUCT ==========")

    categories = get_categories()

    if not categories:
        print("Please add a category first.")
        return

    print("\nAvailable Categories:")

    for category in categories:
        print(
            f"{category[0]}. {category[1]}"
        )

    category_id = get_positive_integer(
        "Category ID: "
    )

    suppliers = get_suppliers()

    if suppliers:
        print("\nAvailable Suppliers:")

        for supplier in suppliers:
            print(
                f"{supplier[0]}. {supplier[1]}"
            )

    supplier_id = get_positive_integer(
        "Supplier ID: "
    )

    product_name = input(
        "Product name: "
    ).strip()

    price = get_positive_float(
        "Price: "
    )

    stock = get_non_negative_integer(
        "Initial stock: "
    )

    reorder_level = get_non_negative_integer(
        "Reorder level: "
    )

    add_product(
        product_name,
        category_id,
        supplier_id,
        price,
        stock,
        reorder_level
    )


def view_products_menu():
    print("\n========== PRODUCTS ==========")

    products = get_products()

    if not products:
        print("No products found.")
        return

    for product in products:
        print("-" * 60)

        print(f"ID          : {product[0]}")
        print(f"Product     : {product[1]}")
        print(f"Category    : {product[2]}")
        print(f"Supplier    : {product[3]}")
        print(f"Price       : ₹{product[4]}")
        print(f"Stock       : {product[5]}")
        print(f"Reorder     : {product[6]}")


def update_product_menu():
    print("\n========== UPDATE PRODUCT ==========")

    product_id = get_positive_integer(
        "Product ID: "
    )

    product = find_product(product_id)

    if product is None:
        print("Product not found.")
        return

    print("\nCurrent Product:")

    print(f"Name: {product[1]}")
    print(f"Price: ₹{product[4]}")
    print(f"Reorder Level: {product[6]}")

    name = input(
        f"Product name [{product[1]}]: "
    ).strip()

    price_input = input(
        f"Price [{product[4]}]: "
    ).strip()

    reorder_input = input(
        f"Reorder level [{product[6]}]: "
    ).strip()

    if not name:
        name = product[1]

    if price_input:
        try:
            price = float(price_input)

            if price <= 0:
                print("Price must be greater than 0.")
                return

        except ValueError:
            print("Invalid price.")
            return
    else:
        price = product[4]

    if reorder_input:
        try:
            reorder_level = int(reorder_input)

            if reorder_level < 0:
                print("Invalid reorder level.")
                return

        except ValueError:
            print("Invalid reorder level.")
            return
    else:
        reorder_level = product[6]

    update_product(
        product_id,
        name,
        product[2],
        product[3],
        price,
        reorder_level
    )


def delete_product_menu():
    print("\n========== DELETE PRODUCT ==========")

    product_id = get_positive_integer(
        "Product ID: "
    )

    product = find_product(product_id)

    if product is None:
        print("Product not found.")
        return

    print(f"\nProduct: {product[1]}")

    confirmation = input(
        "Delete this product? (y/n): "
    ).strip().lower()

    if confirmation == "y":
        delete_product(product_id)
    else:
        print("Delete cancelled.")


def purchase_menu():
    print("\n========== RECORD PURCHASE ==========")

    suppliers = get_suppliers()

    if not suppliers:
        print("Please add a supplier first.")
        return

    print("\nSuppliers:")

    for supplier in suppliers:
        print(
            f"{supplier[0]}. {supplier[1]}"
        )

    supplier_id = get_positive_integer(
        "Supplier ID: "
    )

    product_id = get_positive_integer(
        "Product ID: "
    )

    quantity = get_positive_integer(
        "Quantity purchased: "
    )

    unit_cost = get_positive_float(
        "Unit cost: "
    )

    record_purchase(
        supplier_id,
        product_id,
        quantity,
        unit_cost
    )


def sale_menu():
    print("\n========== RECORD SALE ==========")

    product_id = get_positive_integer(
        "Product ID: "
    )

    quantity = get_positive_integer(
        "Quantity sold: "
    )

    record_sale(
        product_id,
        quantity
    )


def main():
    while True:

        display_header()
        display_menu()

        choice = input(
            "\nEnter your choice: "
        ).strip()

        if choice == "1":
            add_category_menu()

        elif choice == "2":
            add_supplier_menu()

        elif choice == "3":
            add_product_menu()

        elif choice == "4":
            view_products_menu()

        elif choice == "5":
            update_product_menu()

        elif choice == "6":
            delete_product_menu()

        elif choice == "7":
            purchase_menu()

        elif choice == "8":
            sale_menu()

        elif choice == "9":
            low_stock_report()

        elif choice == "10":
            sales_report()

        elif choice == "11":
            inventory_report()

        elif choice == "12":
            supplier_report()

        elif choice == "13":
            print(
                "\nThank you for using "
                "Inventory Management System!"
            )
            break

        else:
            print(
                "\nInvalid choice. "
                "Please enter 1-13."
            )


if __name__ == "__main__":
    main()