import sqlite3
from pprint import pprint

#Connect to Database
conn = sqlite3.connect('CadetPay.db')
c = conn.cursor()

#ALL Cadetpay Data for individual cadet Query Statement
#c.execute("SELECT * FROM CadetPay WHERE EmpID=?", ('0208153',))

#Textbook Audit Query Statememts
#c.execute("SELECT * FROM Cadetpay WHERE EmpID=? AND Rotc_Code=?", ('0216871','ROTC45',)) #Lists all Textbook Payments
#c.execute("SELECT sum(Amount) FROM Cadetpay WHERE EmpID=? AND Rotc_Code=?", ('0216871','ROTC45',)) #Totals All Textbook Payments

#POC Audit Query Statements
#c.execute("SELECT * FROM Cadetpay WHERE EmpID=? AND Rotc_Code=?", ('0216871','ROTC11',)) #Lists all POC Payments
#c.execute("SELECT sum(Amount) FROM Cadetpay WHERE EmpID=? AND Rotc_Code=?", ('0216871','ROTC11',)) Total POC Pay

#GMC Audit Query Statements
#c.execute("SELECT * FROM Cadetpay WHERE EmpID=? AND Rotc_Code=?", ('0216871','ROTC12',)) #Lists all GMC Payments
#c.execute("SELECT sum(Amount) FROM Cadetpay WHERE EmpID=? AND Rotc_Code=?", ('0216871','ROTC12',)) #Total GMC Pay

#POC & GMC Audit Summary Query Statements
#c.execute("SELECT * FROM Cadetpay WHERE EmpID=? AND Rotc_Code=? OR EmpID=? AND Rotc_Code=?", ('0216871','ROTC12','0216871','ROTC11',)) #Lists all GMC and POC payments
#c.execute("SELECT sum(Amount) FROM Cadetpay WHERE EmpID=? AND Rotc_Code=? OR EmpID=? AND Rotc_Code=?", ('0216871','ROTC12','0216871','ROTC11',)) #Totals all GMC and POC payments
pprint(c.fetchall())
conn.commit()
conn.close()

