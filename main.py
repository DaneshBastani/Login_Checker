# Flask Project to Save User information and password
from flask import Flask,render_template
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from sqlalchemy import create_engine,MetaData,Table,Column,String,Integer

engine = create_engine('sqlite:///my_users.db')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
meta = MetaData()
#Create Form
class User(FlaskForm):
    name=StringField('Enter Your User Name')
    password= PasswordField('Enter Your Password')
    Login = SubmitField('Login')
    Register = SubmitField('Register')

#Create Table
users = Table(
    'users',
    meta,
    Column('id',Integer,primary_key=True),
    Column('Name',String),
    Column('Password',Integer)

)

#Connection to database
meta.create_all(engine)
conn = engine.connect()

#Home Route
@app.route('/')
def home():
    form = User()
    return render_template('index.html',form=form)


#Login Route
@app.route('/Login',methods=['GET','POST'])
def login():
    form =User()
    return render_template('Login.html',form=form)


#Register Route
@app.route('/Register',methods=['GET','POST'])
def register():
    form = User()
    return render_template('Register.html',form=form)

#Logged in Route
@app.route('/success' ,methods=['GET','POST'])
def success():
    form = User()
    new_user = form.name.data
    new_pass = form.password.data
    select_statement =users.select()
    result=conn.execute(select_statement)
    conn.commit()
    for row in result.fetchall():
      if new_user==row[1] and new_pass==str(row[2]):
        return render_template('success.html')
    return 'Wrong Username/Password'

#Registration Successfully
@app.route('/Registered',methods=['GET','POST'])
def registered():
    form = User()
    user_name=form.name.data
    password = form.password.data
    insert_statement=users.insert().values(Name=user_name,Password=password)
    conn.execute(insert_statement)
    conn.commit()
    return render_template('Registered.html',form=form)


if __name__=='__main__':
    app.run(debug=True)