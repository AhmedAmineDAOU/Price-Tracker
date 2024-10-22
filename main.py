from app.tracker import PriceTracker
from app.db import load_products, drop_create_database


def main():

    drop_create_database()

    # Charger tous les produits à surveiller depuis la base de données
    products = load_products()

    # Initialiser le tracker de prix
    tracker = PriceTracker()

    # Vérifier chaque produit
    for product in products:
        tracker.check_price_change(product)

    # TODO: recuperer tous les produits ayant eu un changement de prix


if __name__ == "__main__":
    main()
