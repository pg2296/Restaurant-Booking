from booking_app import db
from models import *
from datetime import datetime


availablity_slot='{"1200":1,"1230":0,"1300":1,"1330":1,"1400":1,"1430":1,"1500":1,"1900":1,"1930":1,"2000":1,"2030":1,"2100":1,"2130":1,"2200":1}'

db.create_all()
rest_1=Restaurant("Big Restaurant","+917404383563","big@bigres.com","Neeladri Nagar")
rest_2=Restaurant("Big Restaurant","+917404383563","big@bigres.com","Electronics City")
menu_1 =Menu("Roti",12,1)
menu_2 =Menu("Roti",12,2)
menu_11=Menu("Naan",24,1)
table_type_1=Table_type("T2",100,1)
table_type_11=Table_type("T4",200,1)
table_type_12=Table_type("T6",250,1)
table_type_2=Table_type("T2",150,2)
table_type_21=Table_type("T4",200,2)
table_type_22=Table_type("T6",300,2)
table_1=Tables(1,"T2")
table_11=Tables(1,"T2")
table_12=Tables(1,"T4")
table_13=Tables(1,"T6")
table_2=Tables(2,"T2")
table_21=Tables(2,"T2")
table_22=Tables(2,"T4")
db.session.add_all([rest_1,rest_2,menu_1,menu_2,menu_11,table_type_1,table_type_11,table_type_12,table_type_2,table_type_21,table_type_22,table_1,table_11,table_12,table_13,table_22,table_21,table_2])
db.session.commit()
dates=datetime(2019,10,3)
availablity_1=Availablity(3,dates,availablity_slot)
db.session.add(availablity_1)
db.session.commit()
