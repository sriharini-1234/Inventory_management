from config.database import get_connection


def record_purchase(
    supplier_id,
    product_id,
    quantity,
    unit_cost
):
    connection = get_connection()

    if connection is None:
        return False

    try:
        with connection.cursor() as cursor:

            # Step 1: Create purchase
            cursor.execute(
                """
                INSERT INTO purchases
                (supplier_id, total_amount)
                VALUES (%s, %s)
                RETURNING purchase_id
                """,
                (
                    supplier_id,
                    quantity * unit_cost
                )
            )

            purchase_id = cursor.fetchone()[0]

            # Step 2: Add purchase item
            cursor.execute(
                """
                INSERT INTO purchase_items
                (
                    purchase_id,
                    product_id,
                    quantity,
                    unit_cost
                )
                VALUES (%s, %s, %s, %s)
                """,
                (
                    purchase_id,
                    product_id,
                    quantity,
                    unit_cost
                )
            )
            cursor.execute(
                """
                UPDATE products
                SET stock_quantity =
                    stock_quantity + %s
                WHERE product_id = %s
                """,
                (
                    quantity,
                    product_id
                )
            )
            if cursor.rowcount == 0:
                raise ValueError("Product not found.")
        connection.commit()
        print(
            f"Purchase recorded successfully. "
            f"Purchase ID: {purchase_id}"
        )
        return True
    except Exception as error:
        connection.rollback()

        print(f"Purchase failed: {error}")
        print("Transaction rolled back.")

        return False

    finally:
        connection.close()