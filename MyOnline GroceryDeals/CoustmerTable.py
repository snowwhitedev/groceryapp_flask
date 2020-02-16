import mysql.connector
mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	passwd="rof11223344",#don't forget to change it
	database="GroceryDeals"

)

class CoustmerTable:

 def get_coustmer_id(email):
    mycursor = mydb.cursor()
    sqlFormula = "SELECT * FROM coustmer WHERE email = %s"
    productEmail= (email, )
    mycursor.execute(sqlFormula ,productEmail)
    result = mycursor.fetchall()
    mycursor.close()
    return result