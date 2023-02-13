import sqlite3 as sql
import os
# if os.file("database.db"):
os.remove("database.db")    
connection = sql.connect('database.db')

connection.execute('create table Address('
                   'address_id STRING UNIQUE,'
                   'zipcode INTEGER,'
                   'street_num INTEGER,'
                   'street_name STRING);')

connection.execute('create table Buyers('
                   'email STRING UNIQUE,'
                   'first_name STRING,'
                   'last_name STRING,'
                   'gender STRING,'
                   'age INTEGER,'
                   'home_address_id STRING,'
                   'billing_address_id STRING);')

connection.execute('create table Categories('
                   'parent_category STRING,'
                   'category_name STRING UNIQUE);')

connection.execute('create table Credit_Cards('
                   'credit_card_num STRING UNIQUE,'
                   'card_code INTEGER,'
                   'expire_month INTEGER,'
                   'expire_year INTEGER,'
                   'card_type STRING,'
                   'Owner_email STRING);')

connection.execute('create table Local_Vendors('
                   'Email STRING UNIQUE,'
                   'Business_Name STRING,'
                   'Business_Address_ID STRING,'
                   'Customer_Service_Number STRING);')

connection.execute('create table Orders('
                   'Transaction_ID INTEGER UNIQUE,'
                   'Seller_Email STRING,'
                   'Listing_ID INTEGER,'
                   'Buyer_Email STRING,'
                   'Date DATE,'
                   'Quantity INTEGER,'
                   'Payment INTEGER);')

connection.execute('create table Product_Listings('
                   'Seller_Email STRING,'
                   'Listing_ID INTEGER,'
                   'Category STRING,'
                   'Title STRING,'
                   'Product_Name STRING,'
                   'Product_Description STRING,'
                   'Price STRING,'
                   'Quantity INTEGER);')

connection.execute('create table Sellers('
                   'email STRING UNIQUE,'
                   'routing_number STRING,'
                   'account_number INTEGER,'
                   'balance REAL);')

connection.execute('create table Ratings('
                   'Buyer_Email STRING,'
                   'Seller_Email STRING,'
                   'Date DATE,'
                   'Rating INTEGER,'
                   'Rating_Desc STRING,'
                   'UNIQUE(Buyer_Email, Seller_Email, Date));')
                   

connection.execute('create table Reviews('
                   'Buyer_Email STRING,'
                   'Seller_Email STRING,'
                   'Listing_ID INTEGER,'
                   'Review_Desc STRING,'
                   'UNIQUE(Buyer_Email, Seller_Email, Listing_ID));')

connection.execute('create table Users('
                   'email STRING UNIQUE,'
                   'password STRING);')

connection.execute('create table Zipcode_Info('
                   'zipcode INTEGER,'
                   'city STRING,'
                   'state_id STRING,'
                   'population INTEGER,'
                   'density REAL,'
                   'county_name STRING,'
                   'timezone STRING);')

connection.execute('create table Product_Periods('
                    'email STRING,'
                   'Listing_ID INTEGER,'
                   'Add_Time STRING,'
                   'Remove_Time STRING);')

connection.commit()
