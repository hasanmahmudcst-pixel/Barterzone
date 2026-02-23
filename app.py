from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
import os

app = Flask(__name__)
app.secret_key = "barter_secret_key_fixed"

# MongoDB Connection
MONGO_URI = "mongodb+srv://adminberterzone:Habiba19892@cluster0.pg3xfac.mongodb.net/berterzone_db?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client['berterzone_db']
products_collection = db['products']
settings_collection = db['settings']

@app.route('/')
def index():
    try:
        products = list(products_collection.find())
        # Vercel এরর এড়াতে ডিফল্ট সেটিংস
        site_settings = settings_collection.find_one() or {
            "about": "আমাদের সম্পর্কে তথ্য এখানে আসবে।",
            "refund": "রিফান্ড পলিসি এখানে আসবে।"
        }
        return render_template('index.html', products=products, settings=site_settings)
    except Exception as e:
        return f"Database error: {str(e)}"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # অ্যাডমিন পাসওয়ার্ড ভেরিফিকেশন
        if request.form.get('password') == "Habiba19892":
            session['admin'] = True
            return redirect(url_for('admin'))
        flash("ভুল পাসওয়ার্ড!")
    return render_template('auth.html')

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        trx_id = request.form.get('trx_id')
        if not trx_id:
            flash("পেমেন্ট ট্রানজেকশন আইডি বাধ্যতামূলক!")
            return redirect(url_for('add_item'))
            
        new_product = {
            "name": request.form.get('name'),
            "price": request.form.get('price'),
            "trx_id": trx_id
        }
        products_collection.insert_one(new_product)
        flash("আইটেমটি সফলভাবে জমা দেওয়া হয়েছে!")
        return redirect(url_for('index'))
    return render_template('add_item.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('admin'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        about = request.form.get('about')
        refund = request.form.get('refund')
        # ডাটাবেসে About ও Refund আপডেট করা
        settings_collection.update_one({}, {"$set": {"about": about, "refund": refund}}, upsert=True)
        flash("তথ্য আপডেট হয়েছে!")
        return redirect(url_for('admin'))
        
    products = list(products_collection.find())
    site_settings = settings_collection.find_one() or {"about": "", "refund": ""}
    return render_template('admin.html', products=products, settings=site_settings)

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

# Vercel এর জন্য এটি গুরুত্বপূর্ণ
if __name__ == "__main__":
    app.run(debug=True)