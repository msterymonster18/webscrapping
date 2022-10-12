import requests
from bs4 import BeautifulSoup
import re
import lxml
from tqdm import tqdm

class ItoScrapper:
    def __init__(self):
        self.base_url = "https://ito.org.tr/tr/meslek-komiteleri/uye-firmalar/demir-disi-metaller"
        self.numbers = list(range(1 ,340))
        self.ito_link_list = []
        self.drug_links = []

    def get_categories(self):
            for i in range(len(self.numbers)):
             x = self.base_url + f"?page={self.numbers[i]}"
             self.ito_link_list.append(x)
            return self.ito_link_list
            #print(*self.ito_link_list, sep='\n')

    def get_source(self, url):
        r = requests.get(url)
        if r.status_code == 200:
            return BeautifulSoup(r.content, "lxml")
        return False

    def get_page_company_info(self, source):
        all_company_info = source.find("div" , attrs={"class": "table"}).find_all("tr")
        return set(all_company_info)

    def find_all_company_info(self):
        categories = self.get_categories()
        bar = tqdm(categories, unit=" category link")
        for category_link in bar:
            bar.set_description(category_link)
            category_source = self.get_source(category_link)
            self.drug_links.append(self.get_page_company_info(category_source))

        return self.drug_links

if __name__ == '__main__':
    scrapper = ItoScrapper()
    bilgiler = scrapper.find_all_company_info()
    print(len(bilgiler))
    print(bilgiler)
    #source = scrapper.get_source("https://ito.org.tr/tr/meslek-komiteleri/uye-firmalar/demir-disi-metaller?page=300")
    #print(scrapper.get_page_company_info(source))
