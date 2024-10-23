from app.db import add_price, get_last_price
from app.notifier import send_email
from app.scraper import Scraper


class PriceTracker:
    def check_price_change(self, product):
        # Initialiser le scraper avec l'URL du produit
        scraper = Scraper(product['url'])

        # Obtenir la fonction de scraping appropriée
        custom_scraper = scraper.get_scraper()

        # Récupérer le nouveau prix
        new_price = custom_scraper()

        # Comparer et traiter le changement de prix
        old_price = get_last_price(product['id'])
        if new_price != old_price:
            add_price(product['id'], new_price)
            self.notify_price_change(product, new_price, old_price)
            return {
                'scraper': scraper,
                'product': product,
                'old_price': old_price,
                'new_price': new_price
            }
        return None

    def notify_price_change(self, product, new_price, last_price):
        subject = f"Changement de prix pour {product['name']}"
        message = f"Nouveau prix : {new_price}€, Ancien prix : {last_price}€"
        #send_email('gmail', 'destinataire@example.com', subject, message)
