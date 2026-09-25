from config.database import get_connection


def add_supplier(name, phone, email, address):
    connection = get_connection()

    if connection is None:
        return False

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO suppliers
                (supplier_name, phone, email, address)
                VALUES (%s, %s, %s, %s)
                RETURNING supplier_id
                """,
                (name, phone, email, address)
            )

            supplier_id = cursor.fetchone()[0]

        connection.commit()

        print(f"Supplier added successfully. ID: {supplier_id}")
        return True

    except Exception as error:
        connection.rollback()
        print(f"Error adding supplier: {error}")
        return False

    finally:
        connection.close()


def get_suppliers():
    connection = get_connection()

    if connection is None:
        return []

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    supplier_id,
                    supplier_name,
                    phone,
                    email,
                    address
                FROM suppliers
                ORDER BY supplier_id
                """
            )

            return cursor.fetchall()

    except Exception as error:
        print(f"Error fetching suppliers: {error}")
        return []

    finally:
        connection.close()