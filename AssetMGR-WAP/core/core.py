import bson.json_util as utiljs
import pymongo
import json
import flask
from flask import Flask, request, jsonify, session
import bson
import pandas as pd
import json
import flask_login 

cli = pymongo.MongoClient("mongodb://localhost:27017/")
db = cli["AssetMGR"]
tp = db["credentials"]
pwpl = tp.find()
# Remove static users dict and check credentials dynamically
def verify_password(username, password):
    user = tp.find_one({'username': username})
    if user and user.get('password') == password:
        return True
    return False

app = Flask(__name__)
app.secret_key= 'hello world'
app.run(host='0.0.0.0', port=9020)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
def get_users():
    users={}
    for doc in pwpl:
        if 'username' in doc and 'password' in doc:
            users[doc['username']]={'password':doc['password']}
    return users

users = get_users()

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email
    return user
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return flask.send_file('login.html')

    email = flask.request.form['email']
    if email in users and flask.request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return flask.redirect("/")

    return 'Bad login'

@app.route('/ratpi/view', methods=['GET', 'POST'])
@flask_login.login_required
def view():
    asn = request.args.get('asid')
    if asn is None:
        return jsonify({"error": "asid parameter is required"})
    else:
        cli = pymongo.MongoClient("mongodb://localhost:27017/")
        db = cli["AssetMGR"]
        tp = db["KCS"]
        tp.find({"_id": asn})
        return utiljs.dumps(tp.find({"_id": asn}))
    
@app.route('/ratpi/addasset', methods=['GET', 'POST'])
@flask_login.login_required
def add():
    desc = request.args.get('assetdesc')
    cat = request.args.get('category')
    mfsn = request.args.get('Manufacturer_Serial_Number')
    mf = request.args.get('Manufacturer')
    typ = request.args.get('Type')
    rcap = request.args.get('Rated_Capacity')
    act = request.args.get('Activity')
    loc = request.args.get('Location')
    if desc is None:
        return jsonify({"error": "Description parameter is required"})
    else:
        cli = pymongo.MongoClient("mongodb://localhost:27017/")
        db = cli["AssetMGR"]
        tp = db["KCS"]
        gj = tp.insert_one({"assetdesc":desc, "category": cat, "Location": loc, "Manufacturer_Serial_Number": mfsn, "Manufacturer": mf, "Type": typ, "Rated_Capacity": rcap, "Activity": act, "Tally":False})
        print(gj)
    return flask.redirect('/showpass?asid=' + str(tp.find_one({"assetdesc": desc})["_id"]))


@app.route('/add-object', methods=['GET', 'POST'])
@flask_login.login_required
def add_object():
    return flask.send_file('ao.html')

@app.route('/ratpi/style.css', methods=['GET', 'POST'])
def css():
    return flask.send_file('style.css')


        

@app.route('/', methods=['GET','POST'])
@flask_login.login_required
def home():
    return flask.send_file('home.html')

@app.route('/get_details', methods=['GET', 'POST'])
@flask_login.login_required
def gd():
    return flask.send_file('fetch.html')    


@app.route('/ratpi/fetch_one', methods=['GET', 'POST'])
@flask_login.login_required
def fetch_one():
    asn = request.args.get('asid')
    if asn is None:
        return jsonify({"error": "asid parameter is required"})
    else:
        cli = pymongo.MongoClient("mongodb://localhost:27017/")
        db = cli["AssetMGR"]
        tp = db["KCS"]
        result = tp.find_one({"_id":bson.objectid.ObjectId(asn)})
        return utiljs.dumps(result), 200
        
@app.route('/ratpi/fetch_all', methods=['GET', 'POST'])
@flask_login.login_required
def fetch_all():
    cli = pymongo.MongoClient("mongodb://localhost:27017/")
    db = cli["AssetMGR"]
    tp = db["KCS"]
    results = tp.find()
    table_rows = "".join(
        f"<tr><th>{key}</th><td>{value}</td></tr>"
        for result in results for key, value in result.items()
    )
    html = f"""
    <html>
      <script src="https://cdn.jsdelivr.net/npm/qrcode@1.5.1/build/qrcode.min.js"></script>
    <body>
        <table border="1" cellpadding="5" cellspacing="0">
            {table_rows}
        </table>
    </body>
    </html>
    """
    return html, 200, {'Content-Type': 'text/html'}

@app.route('/showpass', methods=['GET', 'POST'])
def showpass():
    asn = request.args.get('asid')
    html = f"""
  <html>
  <head>
      <title>Asset ID: {asn}</title>
  </head>
  <script>
      window.onload = window.print()
      
      </script>
    <script src="https://cdn.jsdelivr.net/npm/qrcode@1.5.1/build/qrcode.min.js"></script>
  <body>
  <table style="width:100%; text-align:center; font-family:Arial, sans-serif; border-collapse:collapse; border: 1px solid black;">
      <tr>
      <td>
      <img src="https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={asn}"></iframe>
      </td>
      </tr>
      <tr>
      <td style="border: 1px solid black;">
      <h2 style="font-size:30px">Asset ID:</h2>
      <h2 style="font-size:25px">{asn}</h2>
      </td>
      </tr>
      </table>
      
  </body>
  </html>
            """
    return html, 200, {'Content-Type': 'text/html'}

@app.route('/ratpi/updateasset', methods=['POST'])
@flask_login.login_required
def update_asset():
    asid = request.form.get('asid') or request.json.get('asid')
    update_fields = {}
    allowed_fields = ["assetdesc", "category", "Location", "Manufacturer_Serial_Number", "Manufacturer", "Type", "Rated_Capacity", "Activity"]
    for field in allowed_fields:
        value = request.form.get(field) or (request.json.get(field) if request.is_json else None)
        if value is not None:
            update_fields[field] = value

    if not asid:
        return jsonify({"error": "asid parameter is required"}), 400
    if not update_fields:
        return jsonify({"error": "No fields to update"}), 400

    cli = pymongo.MongoClient("mongodb://localhost:27017/")
    db = cli["AssetMGR"]
    tp = db["KCS"]
    result = tp.update_one(
        {"_id": bson.objectid.ObjectId(asid)},
        {"$set": update_fields}
    )
    if result.matched_count == 0:
        return jsonify({"error": "Asset not found"}), 404
    return jsonify({"message": "Asset updated successfully"}), 200

@app.route('/ratpi/logout', methods=['GET', 'POST'])
def logoutd():
    html = f"""
<html>
<head>
    <title>Logout Successful</title>
    </head>
<body>
    <h1>Logout Successful</h1>
    </body>"""
    return html, 200

@app.route('/ratpi/getfilter', methods=['GET', 'POST'])
@flask_login.login_required
def get_filter():
    filter = request.args.get('filter')
    lokup = request.args.get('lookup')
    if filter is None or lokup is None:
        return jsonify({"error": "filter and lookup parameters are required"}), 400 
    cli = pymongo.MongoClient("mongodb://localhost:27017/")
    db = cli["AssetMGR"]
    tp = db["KCS"]
    results = tp.find({filter: lokup})
    #if results.count() == 0:
    #    return jsonify({"error": "No results found"}), 404
    return utiljs.dumps(list(results)), 200

@app.route('/ratpi/filterhtml', methods=['GET', 'POST'])
@flask_login.login_required
def test():
    cli = pymongo.MongoClient("mongodb://localhost:27017/")
    db = cli["AssetMGR"]
    tp = db["KCS"]
    filter = request.args.get('filter')
    lokup = request.args.get('lookup')
    if filter is None or lokup is None:
        return jsonify({"error": "filter and lookup parameters are required"}), 400
    results = tp.find({filter: lokup})
    jsonyy = utiljs.dumps(list(results))

    json_string = jsonyy

    data = json.loads(json_string)
    df = pd.DataFrame(data)
    html_table = df.to_html()
    return html_table

@app.route('/filter', methods=['GET', 'POST'])
@flask_login.login_required
def filter_page():
    return flask.send_file('filter.html')

@app.route('/ratpi/report', methods=['GET', 'POST'])
def report():
    cli = pymongo.MongoClient("mongodb://localhost:27017/")
    db = cli["AssetMGR"]
    tp = db["KCS"]
    results = tp.count_documents({})
    return jsonify({'total':results}), 200
@app.route('/report', methods=['GET', 'POST'])
@flask_login.login_required
def report_page():
    return flask.send_file('report.html')
@app.route('/favicon.ico', methods=['GET', 'POST'])
def favicon():
    return flask.send_file('favicon.ico')

@app.route('/fetch.js')
def fetchjs():
    return flask.send_file('fetch.js')

@app.route('/filter.js')
def filter():
    return flask.send_file('filter.js')
@app.route('/ratpi/')
def ratpiroute():
    html = f"""
<html>
<body>
<h1> This is RatPI, an API developed by RG Servers</h1
</body
</html
"""
    return html, 200

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return flask.redirect('/login')

@login_manager.unauthorized_handler
def unauthorized_handler():
    return flask.send_file('unauthorized.html')

@app.route('/new_user', methods=['GET','POST'])
@flask_login.login_required
def newusr():
    return flask.send_file('add_user.html')
    

@app.route('/tally', methods=['GET', 'POST'])
@flask_login.login_required
def tally():
    return flask.send_file('tally.html')

@app.route('/ratpi/tallyasset', methods=['GET', 'POST'])
@flask_login.login_required
def tally_asset():
    try:
        asid = request.args.get('asid')
        if not asid:
            return jsonify({"error": "asid parameter is required"}), 400
        try:
            uid = bson.objectid.ObjectId(asid)
        except Exception:
            return jsonify({"error": "Invalid asid format"}), 400

        cli = pymongo.MongoClient("mongodb://localhost:27017/")
        db = cli["AssetMGR"]
        tp = db["KCS"]
        result = tp.update_one(
            {"_id": uid},
            {"$set": {"Tally": True}}
        )
        if result.matched_count == 0:
            return jsonify({"error": "Asset not found"}), 404
        return flask.redirect('/tally')
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route('/tally.js', methods=['GET', 'POST'])
def tally_js():
    return flask.send_file('tally.js')

@app.route('/ratpi/gettally', methods=['GET', 'POST'])
@flask_login.login_required
def get_tally():
    cli = pymongo.MongoClient("mongodb://localhost:27017/")
    db = cli["AssetMGR"]
    tp = db["KCS"]
    results = tp.find({"Tally": False})
    #if results.count() == 0:
    #    return jsonify({"error": "No results found"}), 404
    return utiljs.dumps(list(results)), 200

@app.route('/tallyreport.js', methods=['GET', 'POST'])
@flask_login.login_required
def tally_report_js():
    return flask.send_file('tallyreport.js')

@app.route('/tallyreport', methods=['GET', 'POST'])
@flask_login.login_required
def tally_report():
    return flask.send_file('tallyreport.html')

@app.route('/ratpi/add_user', methods=['GET', 'POST'])
@flask_login.login_required
def add_user():
    unm = request.args.get('username')
    pwd = request.args.get('password')
    if unm is None or pwd is None:
        return jsonify({"error": "username and password parameters are required"}), 400
    cli = pymongo.MongoClient("mongodb://localhost:27017/")
    db = cli["AssetMGR"]
    tp = db["credentials"]
    existing_user = tp.find_one({"username": unm})
    if existing_user:
        return jsonify({"error": "Username already exists"}), 400
    tp.insert_one({"username": unm, "password": pwd})
    return flask.redirect('/new_user')
