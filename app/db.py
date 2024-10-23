import sqlite3


def drop_create_database():
    conn = sqlite3.connect('price_tracker.db')
    cursor = conn.cursor()
    # Supprimer les tables si elles existent déjà (pour réinitialiser la base de données)
    cursor.execute('DROP TABLE IF EXISTS price_history')
    cursor.execute('DROP TABLE IF EXISTS products')
    # Table des produits
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            url TEXT NOT NULL
        )
    ''')

    # Table historique des prix
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            price REAL NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    ''')
    product = {
        "name": "Sac à dos Herschel",
        "url": "https://www.fnac.com/Sac-a-dos-Herschel-Gris-et-Noir/a18822103/w-4"
    }
    product_id = add_product(product['name'],
                         product['url'])
    add_price(product_id=product_id, price=120.0)

    conn.commit()
    conn.close()


def add_product(name, url):
    conn = sqlite3.connect('price_tracker.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO products (name, url)
        VALUES (?, ?)
    ''', (name, url))
    product_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return product_id


def add_price(product_id, price):
    conn = sqlite3.connect('price_tracker.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO price_history (product_id, price)
        VALUES (?, ?)
    ''', (product_id, price))
    conn.commit()
    conn.close()


def get_last_price(product_id):
    conn = sqlite3.connect('price_tracker.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT price FROM price_history
        WHERE product_id = ?
        ORDER BY date DESC
        LIMIT 1
    ''', (product_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


def get_price_history(product_id):
    conn = sqlite3.connect('price_tracker.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT price, date FROM price_history
        WHERE product_id = ?
        ORDER BY date ASC
    ''', (product_id,))
    history = cursor.fetchall()
    conn.close()
    return history


def load_products():
    # Connexion à la base de données SQLite
    conn = sqlite3.connect('price_tracker.db')
    cursor = conn.cursor()
    # Exécuter la requête pour récupérer tous les produits
    cursor.execute('''
        SELECT id, name, url FROM products
    ''')
    # Récupérer tous les résultats sous forme de liste
    rows = cursor.fetchall()
    # Fermer la connexion à la base de données
    conn.close()
    # Transformer les résultats en une liste de dictionnaires
    products = []
    for row in rows:
        products.append({
            'id': row[0],
            'name': row[1],
            'url': row[2]
        })
    return products
