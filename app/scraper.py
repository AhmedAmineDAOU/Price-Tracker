from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class Scraper:
    def __init__(self, url):
        self.url = url

    def get_scraper(self):
        # Retourne la fonction de scraping en fonction du site web
        if "amazon" in self.url:
            return self.scrape_amazon
        elif "fnac" in self.url:
            return self.scrape_fnac
        else:
            raise ValueError(f"Pas de scraper disponible pour l'URL : {self.url}")

    def scrape_amazon(self):
        # Logique de scraping pour Amazon
        print(f"Scraping Amazon pour {self.url}")
        # Code de scraping spécifique pour Amazon
        return 100.99  # Exemple de prix retourné

    def scrape_fnac(self):
        # Configurer Selenium pour lancer Chrome en mode headless
        options = Options()
        #options.add_argument("--headless")  # Lancer Chrome sans interface graphique
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        # Puisque ChromeDriver est ajouté au PATH système, pas besoin de spécifier le chemin
        driver = webdriver.Chrome(options=options)
        driver.get(self.url)
        # Logique de scraping pour Fnac
        print(f"Scraping Fnac pour {self.url}")
        # Code de scraping spécifique pour Fnac
        # Récupérer le prix du produit en cherchant l'élément par classe
        try:
            price_element = driver.find_element(By.CLASS_NAME, "f-faPriceBox__price")
            price = price_element.text.strip()
            print(f"Le prix du produit est : {price}")
        except Exception as e:
            print(f"Erreur lors de la récupération du prix : {e}")
        # Fermer le navigateur
        driver.quit()
        return price
