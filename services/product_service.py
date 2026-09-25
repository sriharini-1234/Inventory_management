from config.database import get_connection


def add_product(
    product_name,
    category_id,
    supplier_id,
    price,
    stock_quantity,
    reorder_level
):
    connection = get_connection()

    if connection is None:
        return False

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO products
                (
                    product_name,
                    category_id,
                    supplier_id,
                    price,
                    stock_quantity,
                    reorder_level
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING product_id
                """,
                (
                    product_name,
                    category_id,
                    supplier_id,
                    price,
                    stock_quantity,
                    reorder_level
                )
            )

            product_id = cursor.fetchone()[0]

        connection.commit()

        print(f"Product added successfully. ID: {product_id}")
        return True

    except Exception as error:
        connection.rollback()
        print(f"Error adding product: {error}")
        return False

    finally:
        connection.close()


def get_products():
    connection = get_connection()

    if connection is None:
        return []

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
                    p.reorder_level
                FROM products p

                JOIN categories c
                    ON p.category_id = c.category_id

                LEFT JOIN suppliers s
                    ON p.supplier_id = s.supplier_id

                ORDER BY p.product_id
                """
            )

            return cursor.fetchall()

    except Exception as error:
        print(f"Error fetching products: {error}")
        return []

    finally:
        connection.close()


def find_product(product_id):
    connection = get_connection()

    if connection is None:
        return None

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    product_id,
                    product_name,
                    category_id,
                    supplier_id,
                    price,
                    stock_quantity,
                    reorder_level
                FROM products
                WHERE product_id = %s
                """,
                (product_id,)
            )

            return cursor.fetchone()

    except Exception as error:
        print(f"Error finding product: {error}")
        return None

    finally:
        connection.close()


def update_product(
    product_id,
    product_name,
    category_id,
    supplier_id,
    price,
    reorder_level
):
    connection = get_connection()

    if connection is None:
        return False

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE products
                SET
                    product_name = %s,
                    category_id = %s,
                    supplier_id = %s,
                    price = %s,
                    reorder_level = %s
                WHERE product_id = %s
                """,
                (
                    product_name,
                    category_id,
                    supplier_id,
                    price,
                    reorder_level,
                    product_id
                )
            )

            if cursor.rowcount == 0:
                print("Product not found.")
                connection.rollback()
                return False

        connection.commit()

        print("Product updated successfully.")
        return True

    except Exception as error:
        connection.rollback()
        print(f"Error updating product: {error}")
        return False

    finally:
        connection.close()


def delete_product(product_id):
    connection = get_connection()

    if connection is None:
        return False

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM products
                WHERE product_id = %s
                """,
                (product_id,)
            )

            if cursor.rowcount == 0:
                print("Product not found.")
                connection.rollback()
                return False

        connection.commit()

        print("Product deleted successfully.")
        return True

    except Exception as error:
        connection.rollback()
        print(
            "Cannot delete product. "
            "It may be referenced by purchases or sales."
        )
        print(f"Details: {error}")
        return False

    finally:
        connection.close()