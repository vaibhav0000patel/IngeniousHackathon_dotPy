import psycopg2
import os

conn = psycopg2.connect(host="ec2-54-243-31-34.compute-1.amazonaws.com",database="d507blsk8btjjs", user="toofgkcpxslwfw", password="40f362e11a521a5690649d37197dcc2701c1bf245f77900585c0d8caf108f5da")

cols = ["sender_id","name","phone","email","status","lon","lat"]

from bs4 import BeautifulStoneSoup
import cgi

def HTMLEntitiesToUnicode(text):
    """Converts HTML entities to unicode.  For example '&amp;' becomes '&'."""
    text = unicode(BeautifulStoneSoup(text, convertEntities=BeautifulStoneSoup.ALL_ENTITIES))
    return text

def unicodeToHTMLEntities(text):
    """Converts unicode to HTML entities.  For example '&' becomes '&amp;'."""
    text = cgi.escape(text).encode('ascii', 'xmlcharrefreplace')
    return text

def set_userdata(data,sender_id):
    cur = conn.cursor()
    cur.execute("Select * from user_data where sender_id='"+str(sender_id)+"'")
    userdata = cur.fetchall()
    if userdata:
        query_data = ""
        for key in data:
            query_data += key+"='"+str(data[key]).replace("'","`")+"',"
        cur.execute("UPDATE user_data SET "+query_data[:-1]+" WHERE sender_id='"+str(sender_id)+"';")
    else:
        query_data = "("
        for key in cols:
            query_data += "'"+(str(data[key]).replace("'","`") if key in data else '')+"',"
        query_data = query_data[:-1]+")"
        cur.execute("INSERT into user_data (sender_id,name,phone,email,status,lon,lat) VALUES "+query_data+";")
    conn.commit()
    cur.close()
    return data


def set_user_interests(data,sender_id):
    cur = conn.cursor()
    cur.execute("delete from user_interests where sender_id='"+str(sender_id)+"'")
    for interest in data:
        if interest!="" or interest!=None:
            cur.execute("INSERT into user_interests (sender_id,interest) VALUES ('"+str(sender_id)+"','"+str(interest)+"');")
    conn.commit()
    cur.close()
    return data

def get_userdata(sender_id):
    cur = conn.cursor()
    cur.execute("Select * from user_data where sender_id='"+str(sender_id)+"'")
    data = cur.fetchall()
    cur.close()
    return data

def get_user_interests(sender_id):
    cur = conn.cursor()
    cur.execute("Select * from user_interests where sender_id='"+str(sender_id)+"'")
    data = cur.fetchall()
    cur.close()
    return data

def get_user_interest_data(interest):
    interest = interest.lower()
    cur = conn.cursor()
    cur.execute("Select DISTINCT ud.* from user_data ud,user_interests ui where ud.sender_id=ui.sender_id and (LOWER(ui.interest)='"+interest+"' or LOWER(ud.status) like '%"+interest+"%') and ud.lon!='' and ud.lat!='' and ud.visibility != 'off' ;")
    data = cur.fetchall()
    cur.close()
    return data

def get_all_interests():
    cur = conn.cursor()
    cur.execute("Select DISTINCT interest from user_interests;")
    data = cur.fetchall()
    cur.close()
    return data
