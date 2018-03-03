from flask import Flask,render_template,redirect,url_for,request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('google_maps.html')

@app.route('/adduserinfo/<sender_id>',methods = ['GET'])
def addUserInfo(sender_id):
    print request.args
    name = request.args.get('name') if 'name' in request.args else False

    if name:
        user_data = get_userdata(sender_id)
        interest_data = get_user_interests(sender_id)
        interests=""
        for intdata in interest_data:
            interests += "!#!"+intdata[1]
        if user_data:
            kwargs = {
                    'sender_id' : sender_id,
                    'name' : name,
                    'phone' : user_data[0][8],
                    'email' : user_data[0][3],
                    'staus' : user_data[0][4],
                    'lon' : user_data[0][5],
                    'lat' : user_data[0][6],
                    'visibility' : user_data[0][7],
                    'interests' : interests
            }
        else:
            kwargs = {
                    'sender_id' : sender_id,
                    'name' : '',
                    'phone' : '',
                    'email' : '',
                    'staus' : '',
                    'lon' : '',
                    'lat' : '',
                    'visibility' : '',
                    'interests' : ''
            }
        return render_template('add_user_data.html',**kwargs)
    else:
        return "Invalid URL"



@app.route('/submituserinfo/',methods = ['POST'])
def submitUserInfo():
    if request.method == 'POST':
        user_data = {
            'sender_id' : request.form['sender_id'] if 'sender_id' in request.form else '',
            'name' : request.form['name'] if 'name' in request.form else '',
            'phone' : request.form['phone'] if 'phone' in request.form else '',
            'email' : request.form['email'] if 'email' in request.form else '',
            'status' : request.form['status'] if 'status' in request.form else '',
            'lon' : request.form['lon'] if 'lon' in request.form else '',
            'lat' : request.form['lat'] if 'lat' in request.form else '',
        }
        interest_data = request.form['interests'].split("!#!") if 'interests' in request.form else ''
        if 'sender_id' in request.form:
            set_userdata(user_data,request.form['sender_id'])
            set_user_interests(interest_data,request.form['sender_id'])
        return redirect(url_for('index'))

def set_userdata(data,sender_id):
    conn = psycopg2.connect(host="localhost",database="fbsa", user="root", password="123")
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
            query_data += "'"+(str(data[key]) if key in data else None)+"',"
        query_data = query_data[:-1]+")"
        cur.execute("INSERT into user_data (sender_id,name,phone,email,status,lon,lat) VALUES "+query_data+";")
    conn.commit()
    cur.close()
    return data

def set_user_interests(data,sender_id):
    conn = psycopg2.connect(host="localhost",database="fbsa", user="root", password="123")
    cur = conn.cursor()
    cur.execute("delete from user_interests where sender_id='"+str(sender_id)+"'")
    for interest in data:
        if interest!="" or interest!=None:
            cur.execute("INSERT into user_interests (sender_id,interest) VALUES ('"+str(sender_id)+"','"+str(interest)+"');")
    conn.commit()
    cur.close()
    return data

def get_userdata(sender_id):
    conn = psycopg2.connect(host="localhost",database="fbsa", user="root", password="123")
    cur = conn.cursor()
    cur.execute("Select * from user_data where sender_id='"+str(sender_id)+"'")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def get_user_interests(sender_id):
    conn = psycopg2.connect(host="localhost",database="fbsa", user="root", password="123")
    cur = conn.cursor()
    cur.execute("Select * from user_interests where sender_id='"+str(sender_id)+"'")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def get_user_interest_data(interest):
    conn = psycopg2.connect(host="localhost",database="fbsa", user="root", password="123")
    cur = conn.cursor()
    cur.execute("Select * from user_data ud,user_interests ui where ud.sender_id=ui.sender_id and ui.interest='"+interest+"';")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data



if __name__ == '__main__':
    app.run()
