import datetime

def get_age(string):
    string=string.split("-")
    today=datetime.datetime.today().date()
    dbdate=datetime.date(int(string[0]), int(string[1]),int(string[2]))
    year=today-dbdate
    age= str((year//365))[:3]
    return age

def height(string):
    c=string.split("'")[:2]
    c_s=c[0]+"."+c[1]
    return c_s
    
    
    
from collections import ChainMap
from datetime import date,time
import uuid



def calculate_age(born):
	today = date.today()
	DOB = born.split('/')
	born_date = DOB[1]
	born_month = DOB[0]
	born_year  = DOB[2]
	age = today.year - int(born_year) - ((today.month, today.day) < (int(born_month), int(born_date)))
	return age

def height_replaced(height):
	
	ht = height.replace("’",".")
	print(ht)
	return float(ht)

def min_height_replaced(height):
	
	
	ht = height.replace("’",".")

	return float(ht)

def max_height_replaced(height):
	ht = height.replace("’",".")
	return float(ht)

def height_range(min_height,max_height):
	return_height = []
	height_list = [4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 4.10, 4.11, 5.0, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8,
					5.9, 5.10, 5.11, 6.0, 6.1, 6.2]
	for i in height_list:
		if min_height < i < max_height:
			return_height.append(i)
	return return_height