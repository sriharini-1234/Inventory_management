from config.database import get_connection


def add_category(category_name):
    connection = get_connection()

    if connection is None:
        return False

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO categories (category_name)
                VALUES (%s)
                RETURNING category_id
                """,
                (category_name,)
            )

            category_id = cursor.fetchone()[0]

        connection.commit()

        print(f"Category added successfully. ID: {category_id}")
        return True

    except Exception as error:
        connection.rollback()
        print(f"Error adding category: {error}")
        return False

    finally:
        connection.close()

def get_categories():
    connection = get_connection()

    if connection is None:
        return []

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT category_id, category_name
                FROM categories
                ORDER BY category_id
                """
            )

            return cursor.fetchall()

    except Exception as error:
        print(f"Error fetching categories: {error}")
        return []

    finally:
        connection.close()