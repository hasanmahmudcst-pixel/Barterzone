from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
import os

app = Flask(__name__)
app.secret_key = "barterzone_final_key"

# MongoDB Connection
MONGO_URI = "mongodb+srv://adminberterzone:Habiba19892@cluster0.pg3xfac.mongodb.net/berterzone_db?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client['berterzone_db']
products_collection = db['products']
settings_collection = db['settings']

@app.route('/')
def index():
    try:
        # ডাটাবেস থেকে সব প্রোডাক্ট আনা [ব্যাকএন্ড কানেকশন]
        all_products = list(products_collection.find())
        
        # সাইট সেটিংস (About/Refund) আনা
        site_info = settings_collection.find_one() or {
            "about": "আমাদের সম্পর্কে তথ্য যোগ করতে অ্যাডমিন প্যানেলে যান।",
            "refund": "রিফান্ড পলিসি এখনো সেট করা হয়নি।"
        }
        return render_template('index.html', products=all_products, settings=site_info)
    except Exception as e:
        # এরর হলে এই মেসেজটি দেখাবে
        return f"Database error: index.html - {str(e)}"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == "Habiba19892":
            session['admin'] = True
            return redirect(url_for('admin'))
        flash("ভুল পাসওয়ার্ড!")
    return render_template('auth.html')

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        trx_id = request.form.get('trx_id')
        if trx_id:
            products_collection.insert_one({
                "name": request.form.get('name'),
                "price": request.form.get('price'),
                "trx_id": trx_id
            })
            flash("পণ্যটি জমা হয়েছে!")
            return redirect(url_for('index'))
    return render_template('add_item.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('admin'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # অ্যাডমিন থেকে সাইট আপডেট করার ব্যাকএন্ড
        settings_collection.update_one({}, {"$set": {
            "about": request.form.get('about'),
            "refund": request.form.get('refund')
        }}, upsert=True)
        flash("আপডেট সফল!")
        return redirect(url_for('admin'))
        
    products = list(products_collection.find())
    site_info = settings_collection.find_one() or {"about": "", "refund": ""}
    return render_template('admin.html', products=products, settings=site_info)

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))