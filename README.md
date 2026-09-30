# Inventory Management System

A command-line application for managing products, suppliers, purchases, and sales. It stores its information in PostgreSQL and updates product stock when purchases and sales are recorded.

## What You Can Do

- Create product categories and supplier records.
- Add, view, update, and delete products.
- Record purchases, which increase product stock.
- Record sales, which decrease stock. A sale is rejected when there is not enough stock.
- View low-stock alerts, inventory details, sales totals by product, and supplier reports.

## Requirements

- Python 3 installed
- PostgreSQL installed and running
- `pip` available from your terminal

## Set Up

Run these steps from the project folder.

### 1. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Python packages

```bash
python -m pip install -r requirements.txt
```

This installs Psycopg, the PostgreSQL driver, and `python-dotenv`, which reads the database settings from a local `.env` file.

### 3. Create a PostgreSQL database

Create an empty database named `inventory_db`. For example, if PostgreSQL command-line tools are installed:

```bash
createdb -U postgres inventory_db
```

You can also create the database with a PostgreSQL GUI such as pgAdmin. Use the database username and password you chose during PostgreSQL setup in the next step.

### 4. Configure the database connection

Create a file named `.env` in the project folder. Add your local PostgreSQL connection details:

```dotenv
DB_HOST=localhost
DB_PORT=5432
DB_NAME=inventory_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password
```

Replace `your_postgres_password` with the password for your PostgreSQL user. Keep this file private; do not commit real passwords to source control.

### 5. Create the database tables

Run the supplied SQL schema against the new database:

```bash
psql -U postgres -d inventory_db -f database/schema.sql
```

If your PostgreSQL username is not `postgres`, replace it with your username. The schema creates the tables used by the application; it does not add sample data.

## Run the Application

With the virtual environment activated and PostgreSQL running, start the program from the project folder:

```bash
python main.py
```

The application displays a numbered menu. Enter a menu number and follow the prompts. Choose **13** to exit.

## A Good First Run

1. Choose **1** to add a category, such as `Beverages`.
2. Choose **2** to add a supplier.
3. Choose **3** to add a product. Enter the category and supplier IDs shown by the application, along with the price, starting stock, and reorder level.
4. Choose **4** to check the product and its current stock.
5. Choose **7** to record a purchase and add stock, or **8** to record a sale and reduce stock.
6. Choose **9** through **12** to view stock alerts and reports.

## Menu Reference

| Option | Action |
| --- | --- |
| 1 | Add a category |
| 2 | Add a supplier |
| 3 | Add a product |
| 4 | View products |
| 5 | Update a product's name, price, or reorder level |
| 6 | Delete a product |
| 7 | Record a purchase and increase stock |
| 8 | Record a sale and decrease stock |
| 9 | List products at or below their reorder level |
| 10 | Show quantities sold and revenue by product |
| 11 | Show product, category, supplier, and stock details |
| 12 | Show supplier product counts and purchase values |
| 13 | Exit |

## Project Layout

```text
inventory-management-system/
|-- main.py
|-- config/
|   |-- __init__.py
|   `-- database.py
|-- database/
|   |-- __init__.py
|   `-- schema.sql
|-- models/
|   `-- __init__.py
|-- pictures/
|   |-- add_product.png
|   |-- Screenshot (36).png
|   |-- Screenshot (37).png
|   |-- Screenshot (38).png
|   |-- Screenshot (39).png
|   `-- Screenshot (40).png
|-- services/
|   |-- __init__.py
|   |-- category_service.py
|   |-- product_service.py
|   |-- purchase_service.py
|   |-- report_service.py
|   |-- sales_servies.py
|   `-- supplier_service.py
|-- utils/
|   |-- __init__.py
|   `-- validators.py
|-- requirements.txt
`-- README.md
```

### What Each Part Does

#Application

- `main.py` displays the menu, gathers user input, and calls the relevant service. It keeps terminal prompts separate from database work.

#Database

- `config/database.py` reads connection settings from `.env` and provides PostgreSQL connections for the services.
- `database/schema.sql` defines the tables, relationships, and data rules. Keeping the schema in SQL makes it easier to create and inspect the database independently of the Python code.

#Services

Each service groups database operations for one area of the application. This keeps `main.py` focused on the menu and makes related operations easier to find.

- `services/category_service.py` adds categories and retrieves the category list.
- `services/supplier_service.py` adds suppliers and retrieves supplier details.
- `services/product_service.py` adds, lists, finds, updates, and deletes products.
- `services/purchase_service.py` records purchases and increases product stock.
- `services/sales_servies.py` records sales, checks available stock, and decreases stock.
- `services/report_service.py` creates inventory, low-stock, sales, and supplier reports.

#Shared Utilities and Supporting Files

- `utils/validators.py` checks numeric input and asks again when a value is invalid, avoiding repeated validation code in the menu.
- `__init__.py` files mark `config/`, `database/`, `services/`, `utils/`, and `models/` as Python packages so their modules can be imported.
- `models/` currently contains only `__init__.py`; the application does not yet define model classes.
- `pictures/` contains `add_product.png` and five screenshots. The command-line application does not currently load these images.
- `requirements.txt` lists the Python packages to install.
- `README.md` documents setup, usage, and the project structure for new users and contributors.

### Why the Code Is Organized This Way

The project separates the user interface, database connection, database operations, and input validation. This makes each part easier to find and change: for example, changing a menu prompt belongs in `main.py`, while changing how products are saved belongs in `services/product_service.py`.

A typical action moves through the project like this:

1. `main.py` asks the user for a choice and collects the required values.
2. A function in `utils/validators.py` checks numeric input where needed.
3. `main.py` calls the matching function in `services/`.
4. The service obtains a connection through `config/database.py` and runs SQL against PostgreSQL.
5. `database/schema.sql` defines the tables and relationships those queries use.

The database stores categories, suppliers, and products separately and connects them with IDs. Purchases and sales each have a transaction table and an item table, so the system can store both the overall transaction and which product and quantity it contains.

## Troubleshooting

- **Database connection error:** Make sure PostgreSQL is running and the values in `.env` match your local database, username, password, host, and port.
- **Database or relation does not exist:** Confirm that `inventory_db` was created and that `database/schema.sql` was run against it.
- **`psql` is not recognized:** Add PostgreSQL's command-line tools to your PATH, or run the schema using pgAdmin's query tool.
- **Python cannot find a package:** Activate the virtual environment and run `python -m pip install -r requirements.txt` again.

## Technologies

Python, PostgreSQL, Psycopg 3, SQL, and `python-dotenv`.