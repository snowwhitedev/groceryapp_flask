from scraping import scraping
from ProductTable import ProductTable
from fuzzywuzzy import fuzz


def scraping():
	scrap = scraping()
	scrap.do_scraping()


def matching(id):
	p = ProductTable.get_product_id(id)[0]
	similarProduct = []
	allOtherProducts = ProductTable.get_not_product_id(p[0])
	for q in allOtherProducts:
		matchRate = fuzz.ratio(p[1], q[1])
		if matchRate > 70:
			similarProduct.append(q)
		else:
			pass
	return similarProduct

#def compare_and_sort(similarProduct):
	#sortedSimilarProduct =[]
	#length = range(len(similarProduct))
	#i = 0
	#for product in similarProduct:
		#min = product
		#for j in length:
			#if min > similarProduct[j]:
				#min = similarProduct[j]
				#index = j
		#i =+ 1
		#sortedSimilarProduct.append(min)
		#del similarProduct[index]
	#return sortedSimilarProduct


#z = matching(100)
#print(z)
#print("*****************************")
#v = [5,9,1,5,2]
#print(compare_and_sort(v))



def Sort(sub_li):
		l = len(sub_li)
		for i in range(0, l):
			for j in range(0, l - i - 1):
				if (sub_li[j][2] > sub_li[j + 1][2]):
					tempo = sub_li[j]
					sub_li[j] = sub_li[j + 1]
					sub_li[j + 1] = tempo
		return sub_li

	# Driver Code

