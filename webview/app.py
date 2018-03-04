from flask import Flask,render_template,redirect,url_for,request

import db

app = Flask(__name__)

@app.route('/')
def index():
    return "working"
    # return render_template('google_maps.html')

@app.route('/adduserinfo/<sender_id>',methods = ['GET'])
def addUserInfo(sender_id):
    print request.args
    name = request.args.get('name') if 'name' in request.args else False

    if name:
        user_data = db.get_userdata(sender_id)
        interest_data = db.get_user_interests(sender_id)
        interests=""
        for intdata in interest_data:
            interests += "!#!"+intdata[1]
        if user_data:
            kwargs = {
                    'sender_id' : sender_id,
                    'name' : request.args.get('name'),
                    'phone' : user_data[0][8],
                    'email' : user_data[0][3],
                    'status' : user_data[0][4],
                    'visibility' : user_data[0][7],
                    'interests' : interests
            }
        else:
            kwargs = {
                    'sender_id' : sender_id,
                    'name' : request.args.get('name'),
                    'phone' : '',
                    'email' : '',
                    'staus' : '',
                    'visibility' : '',
                    'interests' : ''
            }
        return render_template('adduserinfo.html',**kwargs)
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
            'visibility' : request.form['visibility'] if 'visibility' in request.form else '',
        }
        int_data = request.form['interests'] if 'interests' in request.form else ''
        interest_data = [i for i in int_data.split("!#!") if len(i)>2]
        if 'sender_id' in request.form:
            db.set_userdata(user_data,request.form['sender_id'])
            db.set_user_interests(interest_data,request.form['sender_id'])
        return redirect('/adduserinfo/'+str(request.form['sender_id'])+'?name='+str(request.form['name']))



@app.route('/submitlocation/<sender_id>',methods = ['GET'])
def submitLocation(sender_id):
    if request.method == 'GET':
        lon = request.args.get('lon') if 'lon' in request.args else False
        lat = request.args.get('lat') if 'lat' in request.args else False
        name = request.args.get('name') if 'name' in request.args else False
        if lon and lat and name:
            user_data = {
                'sender_id' : sender_id,
                'lon' : lon,
                'lat' : lat,
            }
            db.set_userdata(user_data,sender_id)
            return redirect('/adduserinfo/'+str(sender_id)+'?name='+str(name))
        else:
            return "Invalid URL"
    else:
        return "Invalid URL"

@app.route('/checkuserlocation/<sender_id>')
def checkuserlocation(sender_id):
    data = db.get_userdata(sender_id)
    if data:
        if data[0][5] and data[0][6]:
            return '1'
        else:
            return '0'
    else:
        return '0'

@app.route('/getpinnedlocations/',methods = ['GET'])
def getpinnedlocations():
    if request.method == 'GET':
        data = db.get_user_interest_data(request.args.get('interest'))
        if data:
            return render_template('google_maps.html',data=data)
        else:
            return "N/A"


if __name__ == '__main__':
    app.run(threaded=True)
