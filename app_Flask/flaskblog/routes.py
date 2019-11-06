from flask import render_template, url_for, flash, redirect ,request
from flaskblog import app , db ,bcrypt
from flaskblog.forms import FeaturesForm,RegistrationForm, LoginForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
import requests, json



url = 'http://127.0.0.1:12347/predict_pr'

url1 = 'http://127.0.0.1:12347/predict_rf'
url2 = 'http://127.0.0.1:12347/predict'


@app.route("/")

@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        #flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)
   

@app.route("/featureForm", methods=['GET', 'POST'])
def featureForm():
    form = FeaturesForm(prefix="form")
    result =0
    if  "form-submit1" in request.form:
        print("features")
        if form.submit1.data and form.validate_on_submit() :
            data = { "list" : [[form.rho.data, form.nu.data, form.F.data, form.K.data,form.T.data,form.alpha.data,form.beta.data]] }
            j_data = json.dumps(data)
            headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
            # We send thanks to post an HTTP Post request to the according url, after transforming the data to a json data with dunp 
            r = requests.post(url, data=j_data, headers=headers)
            result = r.json()[0]
            flash(f' Volatility : {result}', 'success')

    elif  "form-submit2" in request.form:
        print("features")
        if form.submit2.data and form.validate_on_submit() :
            data = { "list" : [[form.rho.data, form.nu.data, form.F.data, form.K.data,form.T.data,form.alpha.data,form.beta.data]] }
            j_data = json.dumps(data)
            headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
            # We send thanks to post an HTTP Post request to the according url, after transforming the data to a json data with dunp 
            r = requests.post(url1, data=j_data, headers=headers)
            result = r.json()[0]
            flash(f'Volatility : {result}', 'success')

    elif "form-submit3" in request.form:
        print("features")
        if form.submit3.data and form.validate_on_submit() :
            data = { "list" : [[form.rho.data, form.nu.data, form.F.data, form.K.data,form.T.data,form.alpha.data,form.beta.data]] }
            j_data = json.dumps(data)
            headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
            # We send thanks to post an HTTP Post request to the according url, after transforming the data to a json data with dunp 
            r = requests.post(url2, data=j_data, headers=headers)
            print(r.json())
            result = r.json()
            flash(f'Volatility : {result}', 'success')

    return render_template('featureForm.html',form = form, result=result,)            
