from config.database import get_connection


def record_sale(product_id, quantity):
    connection = get_connection()

    if connection is None:
        return False

    try:
        with connection.cursor() as cursor:

            # Find product and current stock
            cursor.execute(
                """
                SELECT price, stock_quantity
                FROM products
                WHERE product_id = %s
                FOR UPDATE
                """,
                (product_id,)
            )

            product = cursor.fetchone()

            if product is None:
                raise ValueError("Product not found.")

            price, stock_quantity = product

            if stock_quantity < quantity:
                raise ValueError(
                    f"Insufficient stock. "
                    f"Available: {stock_quantity}"
                )

            total_amount = price * quantity

            # Create sale
            cursor.execute(
                """
                INSERT INTO sales(total_amount)
                VALUES (%s)
                RETURNING sale_id
                """,
                (total_amount,)
            )

            sale_id = cursor.fetchone()[0]

            # Create sale item
            cursor.execute(
                """
                INSERT INTO sale_items
                (
                    sale_id,
                    product_id,
                    quantity,
                    unit_price
                )
                VALUES (%s, %s, %s, %s)
                """,
                (
                    sale_id,
                    product_id,
                    quantity,
                    price
                )
            )

            # Reduce stock
            cursor.execute(
                """
                UPDATE products
                SET stock_quantity =
                    stock_quantity - %s
                WHERE product_id = %s
                """,
                (
                    quantity,
                    product_id
                )
            )

        connection.commit()

        print(
            f"Sale recorded successfully. "
            f"Sale ID: {sale_id}"
        )

        print(f"Total amount: ₹{total_amount:.2f}")

        return True

    except Exception as error:

        connection.rollback()

        print(f"Sale failed: {error}")
        print("Transaction rolled back.")

        return False

    finally:
        connection.close()