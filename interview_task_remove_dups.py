import pandas
import sqlite3
from datetime import datetime

#function to create the table to import transcations.txt

def create_table():
    conn=sqlite3.connect("transactions.db")
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS transactions (rowid integer PRIMARY KEY,transactionId text , custId integer, transaction_date date, product_sold text, units_sold integer)")
    conn.commit()
    conn.close()


#function to insert rows to the table

def insert_recs(rowid,transaction_id,cust_id,transaction_date,product_sold,units_sold):
    conn=sqlite3.connect("transactions.db")
    cur=conn.cursor()
    cur.execute("INSERT INTO transactions VALUES (?,?,?,?,?,?)",(int(rowid),transaction_id,int(cust_id),transaction_date,int(units_sold)))
    conn.commit()
    conn.close()
    view()

def view():
    conn=sqlite3.connect("transactions.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM transactions")
    rows=cur.fetchall()
    conn.close()
    return rows

def remove_duplicates():
    conn=sqlite3.connect("transactions.db")
    cur=conn.cursor()
    cur.execute("""delete from transactions where rowid not in(select max(rowid) from transactions group by transactionId,custId,transaction_date,product_sold,units_sold)""")
    conn.commit()
    conn.close()


#import transactions.txt to a data frame and define columns

df=pandas.read_csv("D:\mysite\Transaction.txt",sep="|")
df.columns=["transaction_id","cust_id","transaction_date","product_sold","units_sold"]
shp=df.shape
range_iter=shp[0]

create_table()

for i in range(0,range_iter):
    insert_recs(i,df["transaction_id"][i],int(df["cust_id"][i]),df["transaction_date"][i],df["product_sold"][i],int(df["units_sold"][i]))


view()

remove_duplicates()

view()
    

    
    


                
