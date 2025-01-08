import requests
from bs4 import BeautifulSoup

class WebScraper:
    def scrape(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        headlines = [h.text.strip() for h in soup.find_all("h2", class_="headline")]
        return headlines