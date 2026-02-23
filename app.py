from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
import os

app = Flask(__name__)
app.secret_key = "barterzone_2026_key"

# MongoDB Connection - আইপি এক্সেস এখন ওপেন আছে
MONGO_URI = "mongodb+srv://adminberterzone:Habiba19892@cluster0.pg3xfac.mongodb.net/berterzone_db?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client['berterzone_db']
products_collection = db['products']
settings_collection = db['settings']

# --- INDEX BACKEND (হোমপেজে ডাটা পাঠানোর লজিক) ---
@app.route('/')
def index():
    try:
        # ডাটাবেস থেকে সব প্রোডাক্ট লিস্ট আকারে আনা হচ্ছে
        all_products = list(products_collection.find())
        
        # ডাটাবেস থেকে About এবং Refund Policy সেটিংস আনা হচ্ছে
        # যদি ডাটাবেসে কিছু না থাকে, তবে একটি ডিফল্ট মেসেজ সেট করা হয়েছে
        site_info = settings_collection.find_one()
        if not site_info:
            site_info = {
                "about": "আমাদের সম্পর্কে তথ্য যোগ করতে অ্যাডমিন প্যানেলে লগইন করুন।",
                "refund": "রিফান্ড পলিসি এখনো সেট করা হয়নি।"
            }
        
        # ব্যাকএন্ড থেকে ফ্রন্টএন্ডে (index.html) ডাটা পাঠানো হচ্ছে
        return render_template('index.html', products=all_products, settings=site_info)
    except Exception as e:
        return f"Database error: index.html - {str(e)}"

# --- AUTH BACKEND (অ্যাডমিন লগইন) ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == "Habiba19892":
            session['admin'] = True
            return redirect(url_for('admin'))
        flash("ভুল পাসওয়ার্ড!")
    return render_template('auth.html')

# --- ADD ITEM BACKEND ($1 পেমেন্ট শর্ত সহ) ---
@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        trx_id = request.form.get('trx_id')
        if not trx_id:
            flash("ট্রানজেকশন আইডি ছাড়া পণ্য যোগ করা সম্ভব নয়!")
            return redirect(url_for('add_item'))
            
        new_item = {
            "name": request.form.get('name'),
            "price": request.form.get('price'),
            "trx_id": trx_id
        }
        products_collection.insert_one(new_item)
        flash("পণ্যটি সফলভাবে সাবমিট হয়েছে!")
        return redirect(url_for('index'))
    return render_template('add_item.html')

# --- ADMIN BACKEND (About/Refund আপডেট লজিক) ---
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('admin'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # অ্যাডমিন থেকে নতুন About ও Refund লেখা ডাটাবেসে সেভ করা হচ্ছে
        settings_collection.update_one(
            {}, 
            {"$set": {
                "about": request.form.get('about'),
                "refund": request.form.get('refund')
            }}, 
            upsert=True
        )
        flash("সাইট আপডেট সফল হয়েছে!")
        return redirect(url_for('admin'))
        
    products = list(products_collection.find())
    site_info = settings_collection.find_one() or {"about": "", "refund": ""}
    return render_template('admin.html', products=products, settings=site_info)

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)