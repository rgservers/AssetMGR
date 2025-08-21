import flask
import pymongo
import flask_login


app = flask.Flask(__name__)
app.secret_key = 'super secret string'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['AssetMGR']
credentials_collection = db['credentials']
# Use usernames instead of emails throughout the app
@app.route('/', methods=['GET','POST'])
def home():
    if flask.request.method == 'GET':
            return flask.send_file('first_creation.html')

    username = flask.request.form['un']
    pwd = flask.request.form['pwd']
    credentials_collection.insert_one({'username':username,'password':pwd})
    return flask.send_file('first_creation.html')
               
@app.route('/style.css')
def css():
    return flask.send_file('style.css')

@app.route('/favicon.ico')
def icon():
    return flask.send_file('favicon.ico')
