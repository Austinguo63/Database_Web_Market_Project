import sqlite3 as sql
from threading import local
from jinja2 import environmentfunction
import pandas as pd
import hashlib
 
def encrypt(password):
    return hashlib.sha256(bytes(password, encoding='utf-8')).hexdigest()

connection = sql.connect('database.db')

addresses = pd.read_csv('./NittanyMarketDataset-v8/Address.csv')
addresses.to_sql('Address',con=connection,if_exists='replace',index=False)
test=pd.read_sql(sql=r'select * from Address',con=connection)
print(test.head(5))

buyers = pd.read_csv('./NittanyMarketDataset-v8/Buyers.csv')
buyers.to_sql('Buyers',con=connection,if_exists='replace',index=False)
test=pd.read_sql(sql=r'select * from Buyers',con=connection)
print(test.head(5))

categories = pd.read_csv('./NittanyMarketDataset-v8/Categories.csv')
categories.to_sql('Categories',con=connection,if_exists='replace',index=False)
test=pd.read_sql(sql=r'select * from Categories',con=connection)
print(test.head(5))

Credit_Cards = pd.read_csv('./NittanyMarketDataset-v8/Credit_Cards.csv')
Credit_Cards.to_sql('Credit_Cards',con=connection,if_exists='replace',index=False)
test=pd.read_sql(sql=r'select * from Credit_Cards',con=connection)
print(test.head(5))

Local_Vendors = pd.read_csv('./NittanyMarketDataset-v8/Local_Vendors.csv')
Local_Vendors.to_sql('Local_Vendors',con=connection,if_exists='replace',index=False)
test=pd.read_sql(sql=r'select * from Local_Vendors',con=connection)
print(test.head(5))

Orders = pd.read_csv('./NittanyMarketDataset-v8/Orders.csv')
Orders.to_sql('Orders',con=connection,if_exists='replace',index=False)
test=pd.read_sql(sql=r'select * from Orders',con=connection)
print(test.head(5))

Product_listing = pd.read_csv('./NittanyMarketDataset-v8/Product_listing.csv')
Product_listing.to_sql('Product_listing',con=connection,if_exists='replace',index=False)
test=pd.read_sql(sql=r'select * from Product_listing',con=connection)
print(test.head(5))

Ratings = pd.read_csv('./NittanyMarketDataset-v8/Ratings.csv')
Ratings.to_sql('Ratings',con=connection,if_exists='replace',index=False)
test=pd.read_sql(sql=r'select * from Ratings',con=connection)
print(test.head(5))

Reviews = pd.read_csv('./NittanyMarketDataset-v8/Reviews.csv')
Reviews.to_sql('Reviews',con=connection,if_exists='replace',index=False)
test=pd.read_sql(sql=r'select * from Reviews',con=connection)
print(test.head(5))

Sellers = pd.read_csv('./NittanyMarketDataset-v8/Sellers.csv')
Sellers.to_sql('Sellers',con=connection,if_exists='replace',index=False)
test=pd.read_sql(sql=r'select * from Sellers',con=connection)
print(test.head(5))

Users = pd.read_csv('./NittanyMarketDataset-v8/Users.csv')
Users['encrypt']=Users.apply(lambda x: encrypt(x.password),axis=1)
Users['password']=None
Users.to_sql('Users',con=connection,if_exists='replace',index=False)
test=pd.read_sql(sql=r'select * from Users',con=connection)
print(test.head(5))

Zipcode_Info = pd.read_csv('./NittanyMarketDataset-v8/Zipcode_Info.csv')
Zipcode_Info.to_sql('Zipcode_Info',con=connection,if_exists='replace',index=False)
test=pd.read_sql(sql=r'select * from Zipcode_Info',con=connection)
print(test.head(5))

cursor=connection.cursor()
cursor.execute('create view User_Profile as SELECT Users.email as email,first_name,last_name,age,gender,home_address.street_name as home_street,home_zip.city as home_city,home_zip.state_id as home_state,home_address.zipcode as home_zipcode,billing_address.street_name as billing_street,billing_zip.city as billing_city,billing_zip.state_id as billing_state,billing_address.zipcode as billing_zipcode,credit_card_num FROM Users,Buyers,Address as home_address,Address as billing_address,Credit_Cards,Zipcode_info as home_zip, Zipcode_info as billing_zip WHERE Users.email=Buyers.email and home_address.address_id=Buyers.home_address_id and billing_address.address_id=Buyers.billing_address_id and home_zip.zipcode=home_address.zipcode and billing_zip.zipcode=billing_address.zipcode and Credit_Cards.Owner_email=Users.email;')

# cursor.execute('create view Top_Categories as select A.parent_category as top_category from Categories as A where not exists (select category_name from Categories as B where A.parent_category=B.category_name)')
# cursor.execute('select * from User_Profile where email="arubertelli0@nsu.edu"')
# row=cursor.fetchall()
# print(row)

connection.commit()
