from app.tracker import PriceTracker
from app.db import load_products, drop_create_database_dev


def main():

    drop_create_database_dev()

    # Charger tous les produits à surveiller depuis la base de données
    products = load_products()

    # Initialiser le tracker de prix
    tracker = PriceTracker()
    products_with_price_change = []
    # Vérifier chaque produit
    for product in products:
        result = tracker.check_price_change(product)
        if result:
            products_with_price_change.append(result)

if __name__ == "__main__":
    main()
