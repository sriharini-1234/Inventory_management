from config.database import get_connection


def inventory_report():
    connection = get_connection()

    if connection is None:
        return

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT
                    p.product_id,
                    p.product_name,
                    c.category_name,
                    COALESCE(s.supplier_name, 'N/A'),
                    p.price,
                    p.stock_quantity,
                    p.reorder_level,
                    CASE
                        WHEN p.stock_quantity <= p.reorder_level
                        THEN 'LOW STOCK'
                        ELSE 'OK'
                    END AS stock_status
                FROM products p

                JOIN categories c
                    ON p.category_id = c.category_id

                LEFT JOIN suppliers s
                    ON p.supplier_id = s.supplier_id

                ORDER BY p.product_name
                """
            )

            rows = cursor.fetchall()

            print("\n========== INVENTORY REPORT ==========\n")

            for row in rows:
                print(
                    f"ID: {row[0]} | "
                    f"Product: {row[1]} | "
                    f"Category: {row[2]} | "
                    f"Supplier: {row[3]} | "
                    f"Price: ₹{row[4]} | "
                    f"Stock: {row[5]} | "
                    f"Reorder: {row[6]} | "
                    f"Status: {row[7]}"
                )

    except Exception as error:
        print(f"Error generating inventory report: {error}")

    finally:
        connection.close()


def sales_report():
    connection = get_connection()

    if connection is None:
        return

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT
                    p.product_name,
                    SUM(si.quantity) AS total_quantity_sold,
                    SUM(
                        si.quantity * si.unit_price
                    ) AS total_revenue
                FROM sale_items si

                JOIN products p
                    ON si.product_id = p.product_id

                GROUP BY p.product_id, p.product_name

                ORDER BY total_revenue DESC
                """
            )

            rows = cursor.fetchall()

            print("\n========== SALES REPORT ==========\n")

            if not rows:
                print("No sales recorded.")
                return

            for row in rows:
                print(
                    f"Product: {row[0]} | "
                    f"Quantity Sold: {row[1]} | "
                    f"Revenue: ₹{row[2]:.2f}"
                )

    except Exception as error:
        print(f"Error generating sales report: {error}")

    finally:
        connection.close()


def supplier_report():
    connection = get_connection()

    if connection is None:
        return

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT
                    s.supplier_name,
                    COUNT(p.product_id) AS product_count,
                    COALESCE(
                        SUM(pr.total_amount),
                        0
                    ) AS total_purchase_value
                FROM suppliers s

                LEFT JOIN products p
                    ON s.supplier_id = p.supplier_id

                LEFT JOIN purchases pr
                    ON s.supplier_id = pr.supplier_id

                GROUP BY s.supplier_id, s.supplier_name

                ORDER BY total_purchase_value DESC
                """
            )

            rows = cursor.fetchall()

            print("\n========== SUPPLIER REPORT ==========\n")

            for row in rows:
                print(
                    f"Supplier: {row[0]} | "
                    f"Products: {row[1]} | "
                    f"Purchase Value: ₹{row[2]:.2f}"
                )

    except Exception as error:
        print(f"Error generating supplier report: {error}")

    finally:
        connection.close()


def low_stock_report():
    connection = get_connection()

    if connection is None:
        return

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT
                    product_id,
                    product_name,
                    stock_quantity,
                    reorder_level
                FROM products
                WHERE stock_quantity <= reorder_level
                ORDER BY stock_quantity
                """
            )

            rows = cursor.fetchall()

            print("\n========== LOW STOCK REPORT ==========\n")

            if not rows:
                print("No products are currently low on stock.")
                return

            for row in rows:
                print(
                    f"ID: {row[0]} | "
                    f"Product: {row[1]} | "
                    f"Stock: {row[2]} | "
                    f"Reorder Level: {row[3]}"
                )

    except Exception as error:
        print(f"Error generating low stock report: {error}")

    finally:
        connection.close()