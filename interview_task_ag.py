import pandas
import sqlite3
import re
from datetime import datetime


def create_table (col,table_name):
        col=col+"_t"
        joiner=" Text,"
	joiner=joiner.join(col)
	create_text ="CREATE TABLE IF NOT EXISTS "+table_name+" ("+joiner +" date)"
        conn=sqlite3.connect("masters.db")
        cur=conn.cursor()
        cur.execute(create_text)
        conn.commit()
        conn.close()

def insert_data (col,table_name):
	x=[]
	for i in range(0,len(col)):
		print(i)
		if (i== (len(col)-1)):
			x.append(" ?")
		else:
			x.append(" ?,")
	qtext=""
	qtext=qtext.join(x)
	create_text="INSERT INTO "+table_name+" VALUES ("+qtext+" )"
	return (create_text)



 
    


df_raw=pandas.read_excel("D:\mysite\Master.xlsx",sheet_name=0)

dim=df_raw.shape
no_recs=dim[0]
no_columns=dim[1]

df_meta=pandas.DataFrame(columns=['number','Table Name','Last_updated_dt','header1','header2','header3','header4','start_index'])
count=0
for i in range(0,no_recs):
	if (re.match("Table",str(df_raw["col1"][i]))):
		x = df_raw["col1"][i].split(":")
		start_index = i
		number = count+1
		table_name = x[1]
		y = df_raw["col1"][i+1].split(":")
		updated_dt = y[1]
		header1 = str(df_raw["col1"][i+2])
		header2 = str(df_raw["col2"][i+2])
		header3 = str(df_raw["col3"][i+2])
		header4 = str(df_raw["col4"][i+2])
		df_meta=df_meta.append({"number": number, "Table Name": table_name, "Last_updated_dt" : updated_dt, "header1" :header1 ,"header2" : header2 , "header3" : header3 ,"header4" : header4 ,"start_index" : start_index }, ignore_index=True)
		count=count+1


iter=0

while iter <= (len(df_meta)-1):
	df_name="df_"+str(iter)
	print (df_name)
	df_name = pandas.DataFrame(columns=[df_meta["header1"][iter],df_meta["header2"][iter],df_meta["header3"][iter],df_meta["header4"][iter]])
	df_name
	if (iter == (len(df_meta)-1)):
		for j in range((df_meta["start_index"][iter]+3),no_recs):
			df_name = df_name.append({df_meta["header1"][iter]: df_raw["col1"][j] , df_meta["header2"][iter] : df_raw["col2"][j] , df_meta["header3"][iter] : df_raw["col3"][j] , df_meta["header4"][iter] : df_raw["col4"][j]}, ignore_index=True)
	else:
		for j in range((df_meta["start_index"][iter]+3),(df_meta["start_index"][iter+1]-3)):
			df_name = df_name.append({df_meta["header1"][iter]: df_raw["col1"][j] , df_meta["header2"][iter] : df_raw["col2"][j] , df_meta["header3"][iter] : df_raw["col3"][j] , df_meta["header4"][iter] : df_raw["col4"][j]}, ignore_index=True)
	df_name.dropna(axis=1,how='all',inplace=True)
	last_upd=df_meta["Last_updated_dt"][iter]
	df_name["last_updated_dt"]= df_name.shape[0]*[last_upd]
	df_name
	col=df_name.columns
	table_name=df_meta["Table Name"][iter]
	table_name=table_name.replace(" ","_")
	print(col,table_name)
	create_table(col,table_name)
	conn=sqlite3.connect("masters.db")
        cur=conn.cursor()
	for i in range(0,df_name.shape[0]):
                cur.execute(insert_data(col,table_name),df_name.loc[i])
        conn.commit()
        conn.close()
	iter=iter+1
          	
