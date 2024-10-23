import sqlite3


def drop_create_database_dev():
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
    product1 = {
        "name": "Sac à dos Herschel",
        "url": "C:/Users/DAOU/projects/price-tracker/tests/web_pages/Sac à dos Herschel Gris et Noir - Sac à dos - Achat & prix _ fnac.html"
    }
    product1_id = add_product(product1['name'],
                              product1['url'])
    add_price(product_id=product1_id, price=120.0)

    product2 = {
        "name": "Sac-a-dos-Herschel-Weather-Resistant-Roll-Top-Noir",
        "url": "C:/Users/DAOU/projects/price-tracker/tests/web_pages/Sac à dos Herschel Vert et Marron - Sac à dos - Achat & prix _ fnac.html"
    }

    product2_id = add_product(product2['name'],
                              product2['url'])
    add_price(product_id=product2_id, price=120.0)

    product3 = {
        "name": "Sac-a-dos-Herschel-Vert-et-Marron",
        "url": "C:/Users/DAOU/projects/price-tracker/tests/web_pages/Sac à dos Herschel Weather Resistant Roll Top Noir - Sac à dos - Achat & prix _ fnac.html"
    }
    product3_id = add_product(product3['name'],
                              product3['url'])

    add_price(product_id=product3_id, price=114.99)
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
