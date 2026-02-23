from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps
from pymongo import MongoClient
import os

app = Flask(__name__)
app.secret_key = "barterzone_secret_key"

# --- MongoDB কানেকশন (নিচে আপনার নিজের লিঙ্কটি বসাতে হবে) ---
# বর্তমানে এটি একটি ডামি লিঙ্ক হিসেবে দেওয়া আছে। 
MONGO_URI = "mongodb+srv://adminberterzone:Habiba19892@cluster0.pg3xfac.mongodb.net/?appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client['barterzone_db'] # ডাটাবেস নাম
items_collection = db['items'] # পণ্যের কালেকশন
settings_collection = db['settings'] # সেটিংস কালেকশন

# অ্যাডমিন তথ্য
ADMIN_USERNAME = "adminberterzone"
ADMIN_PASSWORD = "Habiba19892"

# শুরুতে সেটিংস ডাটাবেসে না থাকলে ডিফল্ট তৈরি করা
if settings_collection.count_documents({}) == 0:
    settings_collection.insert_one({
        'about': 'আমাদের সম্পর্কে তথ্য এখানে লিখুন।',
        'refund': 'রিফান্ড পলিসি এখানে লিখুন।'
    })

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    site_settings = settings_collection.find_one({}, {'_id': 0})
    return render_template('index.html', settings=site_settings)

@app.route('/auth')
def auth():
    return render_template('auth.html')

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        item = {
            'name': request.form.get('item_name'),
            'email': request.form.get('user_email'),
            'trxid': request.form.get('trx_id')
        }
        # ডাটাবেসে পণ্য সেভ করা হচ্ছে
        items_collection.insert_one(item)
        return redirect(url_for('home'))
    return render_template('add_item.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] == ADMIN_USERNAME and request.form['password'] == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('admin_panel'))
        else:
            error = 'ভুল ইউজারনেম অথবা পাসওয়ার্ড!'
    return render_template('admin_login.html', error=error)

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_panel():
    if request.method == 'POST':
        # ডাটাবেসে সেটিংস আপডেট করা হচ্ছে
        settings_collection.update_one({}, {"$set": {
            'about': request.form.get('about_text'),
            'refund': request.form.get('refund_text')
        }})
        return redirect(url_for('admin_panel'))
    
    # ডাটাবেস থেকে সব পণ্য এবং সেটিংস আনা হচ্ছে
    all_items = list(items_collection.find({}, {'_id': 0}))
    site_settings = settings_collection.find_one({}, {'_id': 0})
    return render_template('admin.html', items=all_items, settings=site_settings)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

app = app
if __name__ == '__main__':
    app.run(debug=True)