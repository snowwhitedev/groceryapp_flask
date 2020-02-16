from bs4 import BeautifulSoup
import requests, re
from ProductTable import ProductTable

class scraping:

	def __init__(self):
		pass

	def scraping_in_carrefour(self, soup, link):
		listProduct = soup.find_all("div", attrs={"class": "plp-list__item"})
		shopName = "كارفور"
		for product in listProduct:

			# get product name
			productName = product.find("p", attrs={"class": "comp-productcard__name"}).text
			name = re.sub("(\s|-)?\s\d+.*", "", productName).replace(".", "").strip()

			# get product price
			productPrice = product.find("p", attrs={"class": "comp-productcard__price"}).find("strong").text
			price = productPrice.replace("SAR", "").strip()

			# get product size if exist
			try:
				productSize = product.find("p", attrs={"class": "comp-productcard__note"}).text
				size = re.sub("الحجم:", "", productSize)

			except AttributeError as e:
				size = None

			productImge = product.find("figure", attrs={"class": "comp-productcard__fig"}).find("img").get("src")

			product = ProductTable(name, price, size, shopName, productImge)
			ProductTable.insert_product(product)

	#---------------------------------------------------------------------------------

	def scraping_in_hyperPanda(self, soup, link):
		listProduct = soup.find_all("div", attrs={"class": "product-block clearfix"})
		shopName = "هايبر بنده"
		for product in listProduct:
			productName = product.find("h3", attrs={"class": "product-name name"}).text

			name = re.sub("((\s)?\((.)*\)|(\d\d+.*)*)", "", productName).strip()
			sizeCheck = re.findall(r'((?<=\().*?(?=\)))', productName)

			if sizeCheck:
				size = sizeCheck[0].strip()
			else:
				size = re.sub(name, "", productName).strip()

			try:
				productPrice = product.find("span", attrs={"class": "regular-price"}).text
			except AttributeError as e:
				productPrice = product.find("p", attrs={"class": "special-price"}).find("span",attrs={"class": "price"}).text
			price = productPrice.replace("SAR", "").strip()

			productImge = product.find("div", attrs={"class": "product-img img"}).find("img").get("src")

			product = ProductTable(name, price, size, shopName, productImge)
			ProductTable.insert_product(product)

	#---------------------------------------------------------------------------------

	def do_scraping(self):
		with open("web_links.txt","r") as file:
			for link in file.read().splitlines():

				if link == 'c':
					webStructure = link

				elif link == 'd':
					webStructure = link

				else:
					source = requests.get(link).text
					soup = BeautifulSoup(source, 'html5lib')

					if webStructure == 'c':
						self.scraping_in_carrefour(soup, link)
					elif webStructure == 'd':
						self.scraping_in_hyperPanda(soup, link)

		file.close()

