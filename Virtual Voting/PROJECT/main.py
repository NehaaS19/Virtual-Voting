from flask import Flask,render_template,request,session,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user
from flask_mail import Mail
import json
from collections import defaultdict 

with open('config.json','r') as c:
    params = json.load(c)["params"]

# MY db connection
local_server= True
app = Flask(__name__)
app.secret_key='aneesrehmankhan'


# this is for getting unique user access
login_manager=LoginManager(app)
login_manager.login_view='login'

# SMTP MAIL SERVER SETTINGS

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail-user'],
    MAIL_PASSWORD=params['gmail-password']
)
mail = Mail(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# app.config['SQLALCHEMY_DATABASE_URL']='mysql://username:password@localhost/databas_table_name'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost:8111/mydata'
db=SQLAlchemy(app)


# here we will create db models that is tables
class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    email=db.Column(db.String(100))

class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50))
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(1000))

class Candidate(db.Model):
    email = db.Column(db.String(80), primary_key=True)
    username = db.Column(db.String(80))
    pid = db.Column(db.Integer, primary_key=True)
    
class Post(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

class Vote(db.Model):
    vid=db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80))
    

class Admin(db.Model):
    aid=db.Column(db.Integer,primary_key=True)
    adminname=db.Column(db.String(50))
    email=db.Column(db.String(50))
    password=db.Column(db.String(1000))

class Trigr(db.Model):
    tid=db.Column(db.Integer,primary_key=True)
    pid=db.Column(db.Integer)
    email=db.Column(db.String(50))
    name=db.Column(db.String(50))
    action=db.Column(db.String(50))
    timestamp=db.Column(db.String(50))


# here we will pass endpoints and run the fuction
@app.route('/')
def index():
    a=params['gmail-user']
    print(a)
    return render_template('index.html')
    

@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == "POST":
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()
        if user:
            flash("Email Already Exist","warning")
            return render_template('/signup.html')
        encpassword=generate_password_hash(password)

        new_user=db.engine.execute(f"INSERT INTO `user` (`username`,`email`,`password`) VALUES ('{username}','{email}','{encpassword}')")

        # this is method 2 to save data in db
        # newuser=User(username=username,email=email,password=encpassword)
        # db.session.add(newuser)
        # db.session.commit()
        flash("Signup Succes Please Login","success")
        return render_template('login.html')

          

    return render_template('signup.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password,password):
            login_user(user)
            flash("Login Success","primary")
            query=db.engine.execute("SELECT pid,name FROM `post`").fetchall()
            return render_template('getcandidate.html',query=query)
        else:
            flash("invalid credentials","danger")
            return render_template('login.html')    


    return render_template('login.html')



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout SuccessFul","warning")
    return redirect(url_for('login'))





@app.route('/test')
def test():
    try:
        Test.query.all()
        return 'My database is Connected'
    except:
        return 'My db is not Connected'
    

@app.route('/details1')
@login_required
def details1():
    # posts=Trigr.query.all()
    posts=db.engine.execute("SELECT * FROM `candidate`")
    return render_template('display.html',posts=posts)

@app.route('/admin',methods=['POST','GET'])
def admin():

    if request.method == "POST":
        adminname=request.form.get('adminname')
        email=request.form.get('email')
        password=request.form.get('password')
        admin=Admin.query.filter_by(email=email).first()
        if admin:
            flash("Admin Already Exist","warning")
            return render_template('/admin.html')
        encpassword=generate_password_hash(password)

        new_user2=db.engine.execute(f"INSERT INTO `admin` (`adminname`,`email`,`password`) VALUES ('{adminname}','{email}','{encpassword}')")

        # this is method 2 to save data in db
        #newuser=User(adminname=adminname,email=email,password=encpassword)
        #db.session.add(newuser)
        #db.session.commit()
        flash("Admin entry Success","success")
        return render_template('admin_login.html')

          

    return render_template('admin.html')

@app.route('/admin_login',methods=['POST','GET'])
def admin_login():
    if request.method == "POST":
        email=request.form.get('email')
        password=request.form.get('password')
        admin=Admin.query.filter_by(email=email).first()

        if admin and check_password_hash(admin.password,password):
            
            flash("Login Success","primary")
            query=db.engine.execute("SELECT pid FROM `post`").fetchall()
            return render_template('admin_interface.html',query=query)  
        else:
            flash("Invalid Credentials","danger")
            return render_template('admin_login.html')    


    return render_template('admin_login.html')

@app.route('/candidate/delete', methods=["POST"])
def deletecandidate():
    email = request.form["email"]
    #c = Candidate.query.filter_by(username=username).first()
    db.engine.execute(f"DELETE FROM `candidate` WHERE `email`='{email}'")
    
    return render_template('admin_interface.html')


@app.route('/candidate/new',methods=['POST','GET'])
def addcandidate():
    post=db.engine.execute("SELECT * FROM `post`")
    if request.method == "POST":
        username=request.form.get('username')
        email=request.form.get('email')
        pid=request.form.get('pid')
        candidate=Candidate.query.filter_by(username=username).first()
        if candidate:
            flash("Candidate Already Exist","warning")
            return render_template('/admin_interface.html')
        
        new_user3=db.engine.execute(f"INSERT INTO `candidate` (`email`,`username`,`pid`) VALUES ('{email}','{username}','{pid}')")

        
        flash("Candidate Added Successfully","success")
        return render_template('admin_interface.html')

@app.route('/candidate/search',methods=['POST','GET'])
def search():
    if request.method=="POST":
        query=request.form.get('search')
        username=Candidate.query.filter_by(username=query).first()
        if username:
            flash("Candidate is Available","info")
        else:

            flash("Candidate is Not Available","danger")
    return redirect('/')

@app.route('/getcandidate',methods=['POST','GET'])
@login_required
def getcandidate(): 
    pid=request.form.get('pid')
    query=db.engine.execute(f"SELECT pid,username FROM `candidate` WHERE pid='{pid}'").fetchall()
     
    return render_template('vote.html',query=query)


   

@app.route('/display',methods=['POST','GET'])
def display():  
    return render_template('display.html')


@app.route('/getcandi')
def getcandi():
     query=db.engine.execute("SELECT pid,name FROM `post`").fetchall()
     return render_template('getcandidate.html',query=query)


@app.route('/vote',methods=['POST','GET'])
def vote(): 
    #query=db.engine.execute(f"SELECT * FROM `candidate` WHERE pid='{pid}'")
    #print(query)
    #query=Candidate.query.filter_by(pid=pid).first()
    if request.method=="POST":
        #pid=request.form.get('pid')
        username=request.form.get('username')
        query=db.engine.execute(f"INSERT INTO `vote` (`username`) VALUES ('{username}')")
       # new=db.engine.execute(f"SELECT * FROM `user` WHERE id='{id}'")
        return redirect(url_for('display'))
            
    
    
@app.route('/pnamedisplay',methods=['POST','GET'])
def pnamedisplay(): 
    query=db.engine.execute(f"SELECT pid,name FROM `post`").fetchall()
    return render_template('pnamedisplay.html',query=query)


app.run(debug=True)    
# username=current_user.username







