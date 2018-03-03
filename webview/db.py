import psycopg2
conn = psycopg2.connect(host="localhost",database="fbsa", user="root", password="123")

cols = ["sender_id","name","phone","email","status","lon","lat"]

def set_userdata(data,sender_id):
    #conn = psycopg2.connect(host="localhost",database="fbsa", user="root", password="123")
    cur = conn.cursor()
    cur.execute("Select * from user_data where sender_id='"+str(sender_id)+"'")
    userdata = cur.fetchall()
    if userdata:
        query_data = ""
        for key in data:
            query_data += key+"='"+str(data[key])+"',"
        cur.execute("UPDATE user_data SET "+query_data[:-1]+" WHERE sender_id='"+str(sender_id)+"';")
    else:
        query_data = "("
        for key in cols:
            query_data += "'"+(str(data[key]) if key in data else '')+"',"
        query_data = query_data[:-1]+")"
        cur.execute("INSERT into user_data (sender_id,name,phone,email,status,lon,lat) VALUES "+query_data+";")
    conn.commit()
    cur.close()
    return data


def set_user_interests(data,sender_id):
    #conn = psycopg2.connect(host="localhost",database="fbsa", user="root", password="123")
    cur = conn.cursor()
    cur.execute("delete from user_interests where sender_id='"+str(sender_id)+"'")
    for interest in data:
        if interest!="" or interest!=None:
            cur.execute("INSERT into user_interests (sender_id,interest) VALUES ('"+str(sender_id)+"','"+str(interest)+"');")
    conn.commit()
    cur.close()
    return data

def get_userdata(sender_id):
    #conn = psycopg2.connect(host="localhost",database="fbsa", user="root", password="123")
    cur = conn.cursor()
    cur.execute("Select * from user_data where sender_id='"+str(sender_id)+"'")
    data = cur.fetchall()
    cur.close()
    #conn.close()
    return data

def get_user_interests(sender_id):
    #conn = psycopg2.connect(host="localhost",database="fbsa", user="root", password="123")
    cur = conn.cursor()
    cur.execute("Select * from user_interests where sender_id='"+str(sender_id)+"'")
    data = cur.fetchall()
    cur.close()
    #conn.close()
    return data

def get_user_interest_data(interest):

    cur = conn.cursor()
    cur.execute("Select DISTINCT ud.* from user_data ud,user_interests ui where ud.sender_id=ui.sender_id and (ui.interest='"+interest+"' or ud.status like '%"+interest+"%') and ud.lon!='' and ud.lat!='' and ud.visibility != 'off' ;")
    data = cur.fetchall()
    cur.close()
    #conn.close()

    return data
