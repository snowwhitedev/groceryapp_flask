import mysql.connector
mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	passwd="rof11223344",#don't forget to change it
	database="GroceryDeals"

)

class ProductTable:

	def __init__(self, name, price, size, place_type, image):
		self.name = name
		self.price = price
		self.size = size
		self.place_type = place_type
		self.image = image


	def insert_product(self):
		mycursor = mydb.cursor()
		sqlFormula = "INSERT INTO Prouduct (name, price, size, place_type, image) VALUES (%s, %s, %s, %s, %s)"
		productInfo = (self.name, self.price, self.size, self.place_type, self.image)
		mycursor.execute(sqlFormula, productInfo)
		mydb.commit()
		mycursor.close()

	def get_all_product():
		mycursor = mydb.cursor()
		sqlFormula = "SELECT * FROM Prouduct"
		mycursor.execute(sqlFormula)
		result = mycursor.fetchall()
		mycursor.close()
		return result


	def delete_all_product():
		mycursor = mydb.cursor()
		sqlFormula = "DELETE FROM Prouduct"
		mycursor.execute(sqlFormula)
		mydb.commit()
		mycursor.close()

	def get_not_product_id(id):
		mycursor = mydb.cursor()
		sqlFormula = "SELECT * FROM Prouduct WHERE idp <> %s"
		productId = (id, )
		mycursor.execute(sqlFormula,productId)
		result = mycursor.fetchall()
		mycursor.close()
		return result

	def get_product_id(id):
		mycursor = mydb.cursor()
		sqlFormula = "SELECT * FROM Prouduct WHERE idp = %s"
		productId = (id, )
		mycursor.execute(sqlFormula,productId)
		result = mycursor.fetchall()
		mycursor.close()
		return result
