import datetime

def get_age(string):
    string=string.split("-")
    today=datetime.datetime.today().date()
    dbdate=datetime.date(int(string[0]), int(string[1]),int(string[2]))
    year=today-dbdate
    age= str((year//365))[:3]
    return age

def heigth(string):
    c=string.split("'")[:2]
    
    c_s=c[0]+"."+c[1]
    
    return c_s
    