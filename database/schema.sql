CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE suppliers (
    supplier_id SERIAL PRIMARY KEY,
    supplier_name VARCHAR(150) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(150),
    address TEXT
);
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL,
    category_id INTEGER NOT NULL,
    supplier_id INTEGER,
    price NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
    stock_quantity INTEGER NOT NULL DEFAULT 0 CHECK (stock_quantity >= 0),
    reorder_level INTEGER NOT NULL DEFAULT 10 CHECK (reorder_level >= 0),

    CONSTRAINT fk_product_category
        FOREIGN KEY (category_id)



        
        REFERENCES categories(category_id),

    CONSTRAINT fk_product_supplier
        FOREIGN KEY (supplier_id)
        REFERENCES suppliers(supplier_id)
);

CREATE TABLE purchases (
    purchase_id SERIAL PRIMARY KEY,
    supplier_id INTEGER NOT NULL,
    purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount NUMERIC(12, 2) DEFAULT 0,

    CONSTRAINT fk_purchase_supplier
        FOREIGN KEY (supplier_id)
        REFERENCES suppliers(supplier_id)
);
CREATE TABLE purchase_items (
    purchase_item_id SERIAL PRIMARY KEY,
    purchase_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_cost NUMERIC(10, 2) NOT NULL CHECK (unit_cost >= 0),

    CONSTRAINT fk_purchase_item_purchase
        FOREIGN KEY (purchase_id)
        REFERENCES purchases(purchase_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_purchase_item_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);

//sales

CREATE TABLE sales (
    sale_id SERIAL PRIMARY KEY,
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount NUMERIC(12, 2) DEFAULT 0
);
CREATE TABLE sale_items (
    sale_item_id SERIAL PRIMARY KEY,
    sale_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10, 2) NOT NULL CHECK (unit_price >= 0),

    CONSTRAINT fk_sale_item_sale
        FOREIGN KEY (sale_id)
        REFERENCES sales(sale_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_sale_item_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);